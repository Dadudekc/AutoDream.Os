#!/usr/bin/env python3
"""
Core Autonomous Workflow
=========================

Core autonomous workflow implementation.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.cross_platform_paths import ensure_dir
from ..blockers.blocker_resolver import BlockerResolver
from ..mailbox.mailbox_manager import MailboxManager
from ..operations.autonomous_operations import AutonomousOperations
from ..tasks.task_manager import TaskManager

try:
    from ...consolidated_messaging_service import ConsolidatedMessagingService

    MESSAGING_AVAILABLE = True
except ImportError:
    MESSAGING_AVAILABLE = False
    ConsolidatedMessagingService = None

logger = logging.getLogger(__name__)


class AgentAutonomousWorkflow:
    """Autonomous workflow manager for agents."""

    def __init__(self, agent_id: str):
        """Initialize autonomous workflow."""
        self.agent_id = agent_id
        self.workspace_dir = Path(f"agent_workspaces/{agent_id}")
        self.inbox_dir = self.workspace_dir / "inbox"
        self.processed_dir = self.workspace_dir / "processed"
        self.working_tasks_file = self.workspace_dir / "working_tasks.json"
        self.future_tasks_file = self.workspace_dir / "future_tasks.json"
        self.status_file = self.workspace_dir / "status.json"

        # Ensure directories exist
        ensure_dir(self.workspace_dir)
        ensure_dir(self.inbox_dir)
        ensure_dir(self.processed_dir)

        # Initialize messaging service
        if MESSAGING_AVAILABLE:
            self.messaging_service = ConsolidatedMessagingService()
        else:
            self.messaging_service = None

        # Initialize components
        self.mailbox_manager = MailboxManager(agent_id, self.workspace_dir)
        self.task_manager = TaskManager(agent_id, self.workspace_dir)
        self.blocker_resolver = BlockerResolver(agent_id, self.workspace_dir)
        self.autonomous_operations = AutonomousOperations(agent_id, self.workspace_dir)

        logger.info(f"Initialized autonomous workflow for {agent_id}")

    async def run_autonomous_cycle(self) -> dict[str, Any]:
        """Run one complete autonomous agent cycle."""
        cycle_start = datetime.now()
        cycle_results = {
            "agent_id": self.agent_id,
            "cycle_start": cycle_start.isoformat(),
            "actions_taken": [],
            "tasks_processed": 0,
            "messages_processed": 0,
            "devlogs_created": 0,
        }

        try:
            # 1. MAILBOX CHECK (Priority: HIGH)
            logger.info(f"{self.agent_id}: Starting mailbox check...")
            messages_processed = await self.mailbox_manager.check_mailbox()
            cycle_results["messages_processed"] = messages_processed
            cycle_results["actions_taken"].append(f"Processed {messages_processed} messages")

            # 2. TASK STATUS EVALUATION (Priority: HIGH)
            logger.info(f"{self.agent_id}: Evaluating task status...")
            task_status = await self.task_manager.evaluate_task_status()
            cycle_results["actions_taken"].append(f"Task status: {task_status}")

            # 3. TASK CLAIMING (Priority: MEDIUM)
            if task_status == "no_current_task":
                logger.info(f"{self.agent_id}: Claiming new task...")
                claimed_task = await self.task_manager.claim_task()
                if claimed_task:
                    cycle_results["tasks_processed"] += 1
                    cycle_results["actions_taken"].append(
                        f"Claimed task: {claimed_task.get('title', 'Unknown')}"
                    )

            # 4. BLOCKER RESOLUTION (Priority: MEDIUM)
            logger.info(f"{self.agent_id}: Checking for blockers...")
            blockers_resolved = await self.blocker_resolver.resolve_blockers()
            if blockers_resolved:
                cycle_results["actions_taken"].append(f"Resolved {blockers_resolved} blockers")

            # 5. AUTONOMOUS OPERATION (Priority: LOW)
            if task_status == "task_in_progress":
                logger.info(f"{self.agent_id}: Continuing current task...")
                task_progress = await self.task_manager.continue_current_task()
                cycle_results["actions_taken"].append(f"Task progress: {task_progress}")
            elif task_status == "no_current_task":
                logger.info(f"{self.agent_id}: Running autonomous operations...")
                operations_results = await self.autonomous_operations.run_autonomous_operations()
                cycle_results["actions_taken"].append(
                    f"Autonomous operations: {operations_results['operations_successful']} successful"
                )

            # Create cycle devlog
            cycle_results["devlogs_created"] = 1
            # Note: Devlog creation handled by devlog system separately
            logger.info(f"{self.agent_id}: Autonomous cycle completed successfully")

        except Exception as e:
            logger.error(f"{self.agent_id}: Error in autonomous cycle: {e}")
            cycle_results["error"] = str(e)
            # Note: Error logging handled by logging system
            logger.error(f"{self.agent_id}: Autonomous cycle failed: {str(e)}")

        cycle_results["cycle_end"] = datetime.now().isoformat()
        return cycle_results

    async def run_continuous_cycles(self, interval_seconds: int = 300) -> None:
        """Run continuous autonomous cycles."""
        logger.info(
            f"{self.agent_id}: Starting continuous autonomous cycles (interval: {interval_seconds}s)"
        )

        try:
            while True:
                cycle_results = await self.run_autonomous_cycle()
                logger.info(
                    f"{self.agent_id}: Cycle completed - {cycle_results['messages_processed']} messages, {cycle_results['tasks_processed']} tasks"
                )

                # Wait for next cycle
                await asyncio.sleep(interval_seconds)

            # SECURITY: Key placeholder - replace with environment variable
            logger.info(f"{self.agent_id}: Continuous cycles stopped by user")
        except Exception as e:
            logger.error(f"{self.agent_id}: Error in continuous cycles: {e}")

    async def get_workflow_status(self) -> dict[str, Any]:
        """Get current workflow status."""
        try:
            status = {
                "agent_id": self.agent_id,
                "workspace_exists": self.workspace_dir.exists(),
                "inbox_exists": self.inbox_dir.exists(),
                "processed_exists": self.processed_dir.exists(),
                "working_tasks_exists": self.working_tasks_file.exists(),
                "future_tasks_exists": self.future_tasks_file.exists(),
                "status_file_exists": self.status_file.exists(),
                "timestamp": datetime.now().isoformat(),
            }

            # Get task status
            task_status = await self.task_manager.evaluate_task_status()
            status["current_task_status"] = task_status

            # Get mailbox status
            inbox_files = list(self.inbox_dir.glob("*.json")) if self.inbox_dir.exists() else []
            status["pending_messages"] = len(inbox_files)

            return status

        except Exception as e:
            logger.error(f"{self.agent_id}: Error getting workflow status: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
