from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ..mailbox.mailbox_manager import MailboxManager
from ..tasks.task_manager import TaskManager
from ..blockers.blocker_resolver import BlockerResolver
from ..operations.autonomous_operations import AutonomousOperations
from ...agent_devlog_automation import auto_create_devlog
from ...consolidated_messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass
class CycleResult:
    agent_id: str
    cycle_id: str
    started_at: str
    ended_at: Optional[str] = None
    actions_taken: list[str] = None
    tasks_processed: int = 0
    messages_processed: int = 0
    devlogs_created: int = 0
    status: str = "ok"
    error: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["actions_taken"] = self.actions_taken or []
        return d


class AgentAutonomousWorkflow:
    """Autonomous workflow manager for agents with quality gates, backoff, and SOP-compliant messaging."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.workspace_dir = Path(f"agent_workspaces/{agent_id}").resolve()
        self.inbox_dir = self.workspace_dir / "inbox"
        self.processed_dir = self.workspace_dir / "processed"
        self.working_tasks_file = self.workspace_dir / "working_tasks.json"
        self.future_tasks_file = self.workspace_dir / "future_tasks.json"
        self.status_file = self.workspace_dir / "status.json"

        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)

        # Initialize messaging service (optional for now)
        try:
            self.messaging_service = ConsolidatedMessagingService()
        except Exception as e:
            logger.warning(f"{self.agent_id}: Messaging service unavailable: {e}")
            self.messaging_service = None
        self.mailbox_manager = MailboxManager(agent_id, self.workspace_dir)
        self.task_manager = TaskManager(agent_id, self.workspace_dir)
        self.blocker_resolver = BlockerResolver(agent_id, self.workspace_dir)
        self.autonomous_operations = AutonomousOperations(agent_id, self.workspace_dir)

        # Loop control
        self._stop = asyncio.Event()
        self._fail_count = 0  # for escalation
        logger.info(f"Initialized autonomous workflow for {agent_id}")

    # ---------- Core cycle ----------

    async def run_autonomous_cycle(self) -> Dict[str, Any]:
        """Run one complete autonomous agent cycle (SOP: mailbox → tasks → blockers → ops → devlog → CYCLE_DONE)."""
        cycle_id = self._new_cycle_id()
        result = CycleResult(
            agent_id=self.agent_id,
            cycle_id=cycle_id,
            started_at=self._now(),
            actions_taken=[]
        )

        try:
            # 0) (OPTIONAL) Quality gates preflight (soft in manual mode)
            gates_ok, gates_detail = await self._soft_quality_precheck()
            if not gates_ok:
                result.actions_taken.append(f"Soft gates: {gates_detail}")

            # 1) MAILBOX
            msgs = await self.mailbox_manager.check_mailbox()
            result.messages_processed = msgs
            result.actions_taken.append(f"Mailbox processed: {msgs}")

            # 2) TASK STATUS
            status = await self.task_manager.evaluate_task_status()
            result.actions_taken.append(f"Task status: {status}")

            # 3) CLAIM if idle
            if status == "no_current_task":
                claimed = await self.task_manager.claim_task()
                if claimed:
                    result.tasks_processed += 1
                    result.actions_taken.append(f"Claimed task: {claimed.get('title','Unknown')}")
                else:
                    result.actions_taken.append("No tasks available to claim")

            # 4) BLOCKERS
            resolved = await self.blocker_resolver.resolve_blockers()
            if resolved:
                result.actions_taken.append(f"Resolved blockers: {resolved}")

            # 5) WORK
            if status == "task_in_progress":
                progress = await self.task_manager.continue_current_task()
                result.actions_taken.append(f"Progress: {progress}")
            elif status == "no_current_task":
                ops = await self.autonomous_operations.run_autonomous_operations()
                ok = ops.get("operations_successful", 0)
                result.actions_taken.append(f"Autonomous ops success: {ok}")

            # 6) DEVLOG (required)
            result.devlogs_created = 1
            try:
                await auto_create_devlog(
                    self.agent_id,
                    "Autonomous cycle completed",
                    "completed",
                    {"cycle": result.as_dict()}
                )
            except Exception as e:
                logger.warning(f"{self.agent_id}: Devlog creation failed: {e}")
                result.devlogs_created = 0

            # 7) CYCLE_DONE → inbox (SOP)
            next_intent = "Continue autonomous operation"
            await self._enqueue_message(
                mtype="CYCLE_DONE",
                body={
                    "agent": self.agent_id,
                    "cycle_id": cycle_id,
                    "actions": result.actions_taken,
                    "next_intent": next_intent,
                },
                priority="NORMAL",
            )

            # success path bookkeeping
            self._fail_count = 0

        except Exception as e:
            result.status = "failed"
            result.error = str(e)
            logger.exception(f"{self.agent_id}: Error in autonomous cycle")
            try:
                await auto_create_devlog(
                    self.agent_id, "Autonomous cycle error", "failed", {"error": str(e), "cycle_id": cycle_id}
                )
            except Exception as devlog_error:
                logger.warning(f"{self.agent_id}: Error devlog creation failed: {devlog_error}")
            self._fail_count += 1
            await self._maybe_escalate()

        finally:
            result.ended_at = self._now()

        return result.as_dict()

    # ---------- Continuous loop ----------

    async def run_continuous_cycles(self, base_interval_seconds: int = 300) -> None:
        """
        Continuous cycles with exponential backoff on failures and graceful stop.
        - Base cadence defaults to 5 minutes.
        - Backoff doubles on consecutive failures, capped.
        """
        logger.info(f"{self.agent_id}: Starting continuous cycles (base interval={base_interval_seconds}s)")
        backoff = 1
        try:
            while not self._stop.is_set():
                started = time.monotonic()
                cycle = await self.run_autonomous_cycle()
                logger.info(
                    f"{self.agent_id}: Cycle {cycle['cycle_id']} status={cycle['status']} "
                    f"msgs={cycle['messages_processed']} tasks={cycle['tasks_processed']}"
                )

                # adjust backoff
                if cycle["status"] == "ok":
                    backoff = 1
                else:
                    backoff = min(backoff * 2, 8)  # cap 8x

                # sleep with jitter, but allow immediate stop
                elapsed = time.monotonic() - started
                sleep_for = max(base_interval_seconds * backoff - elapsed, 3)
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self._jitter(sleep_for))
                except asyncio.TimeoutError:
                    pass

            logger.info(f"{self.agent_id}: Continuous cycles stopped.")
        except Exception:
            logger.exception(f"{self.agent_id}: Unhandled error in continuous loop")

    async def stop(self):
        """Signal the loop to stop after the current cycle."""
        self._stop.set()

    # ---------- Status ----------

    async def get_workflow_status(self) -> Dict[str, Any]:
        """Current workflow status snapshot."""
        try:
            status = {
                "agent_id": self.agent_id,
                "workspace_exists": self.workspace_dir.exists(),
                "inbox_exists": self.inbox_dir.exists(),
                "processed_exists": self.processed_dir.exists(),
                "working_tasks_exists": self.working_tasks_file.exists(),
                "future_tasks_exists": self.future_tasks_file.exists(),
                "status_file_exists": self.status_file.exists(),
                "timestamp": self._now(),
                "fail_count": self._fail_count,
            }
            status["current_task_status"] = await self.task_manager.evaluate_task_status()
            inbox_files = list(self.inbox_dir.glob("*.json")) if self.inbox_dir.exists() else []
            status["pending_messages"] = len(inbox_files)
            return status
        except Exception as e:
            logger.error(f"{self.agent_id}: Error getting workflow status: {e}")
            return {"agent_id": self.agent_id, "error": str(e), "timestamp": self._now()}

    # ---------- Messaging (SOP-compliant, atomic) ----------

    async def _enqueue_message(self, mtype: str, body: Dict[str, Any], priority: str = "NORMAL") -> None:
        """
        Enqueue a message to the agent's own inbox (SSOT queue file), atomically.
        Schema has id/version/type/timestamp to guard against drift.
        """
        try:
            mid = str(uuid.uuid4())
            ts = self._now()
            payload = {
                "id": mid,
                "version": 1,
                "type": mtype,
                "from": self.agent_id,
                "to": self.agent_id,
                "timestamp": ts,
                "priority": priority,
                "body": body,
            }
            fname = f"{ts.replace(':','').replace('.','')}_{mtype.lower()}_{mid[:8]}.json"
            target = self.inbox_dir / fname
            self._atomic_write_json(target, payload)
            logger.info(f"{self.agent_id}: Enqueued {mtype} → {target.name}")
        except Exception as e:
            logger.error(f"{self.agent_id}: Failed to enqueue {mtype}: {e}")

    async def _send_blocker_message(self, blocker_id: str, reason: str, need: str) -> None:
        """Send BLOCKER per Operating Order v1.0."""
        await self._enqueue_message(
            mtype="BLOCKER",
            body={"blocker_id": blocker_id, "reason": reason, "need": need},
            priority="HIGH",
        )

    # ---------- Helpers ----------

    async def _soft_quality_precheck(self) -> tuple[bool, str]:
        """
        Hook to your quality gates (V2/tests/SSOT). Keep soft here;
        hard gates should live in onboarding or pre-merge flows.
        """
        # TODO integrate real checks
        return True, "Gates OK (soft)"

    async def _maybe_escalate(self):
        """
        SLA/Escalation policy:
        - 2 consecutive failures → Inbox warning
        - 4 consecutive failures → Discord #ops (via ConsolidatedMessagingService)
        """
        if self._fail_count == 2:
            await self._enqueue_message(
                mtype="ESCALATION",
                body={"severity": "warning", "reason": "two consecutive cycle failures"},
                priority="HIGH",
            )
        elif self._fail_count >= 4:
            try:
                if self.messaging_service:
                    # Replace with your real broadcast (channel/routing keys)
                    await self.messaging_service.broadcast(
                        message=f"⚠ {self.agent_id}: four consecutive failures. Human review required.",
                        priority="URGENT",
                    )
                else:
                    # Fallback to inbox escalation
                    await self._enqueue_message(
                        mtype="CRITICAL_ESCALATION",
                        body={"severity": "critical", "reason": "four consecutive cycle failures"},
                        priority="URGENT",
                    )
            except Exception:
                logger.exception("Failed to alert #ops via ConsolidatedMessagingService")

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).strftime(ISO)

    @staticmethod
    def _new_cycle_id() -> str:
        return f"c-{uuid.uuid4().hex[:12]}"

    @staticmethod
    def _jitter(seconds: float) -> float:
        # +/- up to 10% jitter to avoid thundering herd
        import random
        delta = seconds * 0.1
        return max(1.0, seconds + random.uniform(-delta, delta))

    @staticmethod
    def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        os.replace(tmp, path)