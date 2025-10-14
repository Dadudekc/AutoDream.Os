"""
Recovery Handlers
=================

Handles failures and recovery coordination for overnight operations.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: recovery.py (RecoverySystem class split)
License: MIT
"""

import time
from typing import Any


class RecoveryHandlers:
    """Handles different types of failures."""

    def __init__(self, logger, messaging, state):
        """Initialize handlers."""
        self.logger = logger
        self.messaging = messaging
        self.state = state

    async def handle_cycle_failure(self, cycle_number: int, error_message: str) -> None:
        """Handle failure of an entire cycle."""
        try:
            self.logger.error(f"Cycle {cycle_number} failure: {error_message}")

            failure_record = {
                "type": "cycle_failure",
                "cycle_number": cycle_number,
                "error_message": error_message,
                "timestamp": time.time(),
                "recovery_attempted": False,
            }
            self.state.failure_history.append(failure_record)

            if self.state.auto_recovery:
                await self.messaging.send_cycle_recovery_message(cycle_number, error_message)
                failure_record["recovery_attempted"] = True
                self.state.last_recovery_time = time.time()

        except Exception as e:
            self.logger.error(f"Failed to handle cycle failure: {e}")

    async def handle_task_failure(self, task_id: str, agent_id: str, error_message: str) -> None:
        """Handle failure of an individual task."""
        try:
            self.logger.error(f"Task failure: {task_id} by {agent_id} - {error_message}")

            failure_record = {
                "type": "task_failure",
                "task_id": task_id,
                "agent_id": agent_id,
                "error_message": error_message,
                "timestamp": time.time(),
                "recovery_attempted": False,
            }
            self.state.failure_history.append(failure_record)

            if agent_id in self.state.recovery_attempts:
                self.state.recovery_attempts[agent_id] += 1

            if self.state.auto_recovery:
                await self.messaging.send_task_recovery_message(task_id, agent_id, error_message)
                failure_record["recovery_attempted"] = True

            if self.state.agent_rescue and agent_id in self.state.recovery_attempts:
                if self.state.recovery_attempts[agent_id] >= self.state.max_retries:
                    await self.rescue_agent(agent_id)

        except Exception as e:
            self.logger.error(f"Failed to handle task failure: {e}")

    async def handle_stalled_agents(self, stalled_agents: list[str]) -> None:
        """Handle stalled agents."""
        try:
            self.logger.warning(f"Handling {len(stalled_agents)} stalled agents")
            for agent_id in stalled_agents:
                await self.rescue_agent(agent_id)
        except Exception as e:
            self.logger.error(f"Failed to handle stalled agents: {e}")

    async def handle_health_issues(self, health_status: dict[str, Any]) -> None:
        """Handle system health issues."""
        try:
            issues = health_status.get("issues", [])
            if not issues:
                return

            self.logger.warning(f"Handling {len(issues)} health issues")
            for issue in issues:
                await self._handle_health_issue(issue)
        except Exception as e:
            self.logger.error(f"Failed to handle health issues: {e}")

    async def rescue_agent(self, agent_id: str) -> None:
        """Rescue a stalled or failing agent."""
        try:
            self.state.recovery_attempts[agent_id] = 0
            await self.messaging.send_agent_rescue_message(agent_id)
            self.state.failure_history.append(
                {"type": "agent_rescue", "agent_id": agent_id, "timestamp": time.time()}
            )
            self.logger.info(f"Agent rescue completed for {agent_id}")
        except Exception as e:
            self.logger.error(f"Agent rescue failed for {agent_id}: {e}")

    async def _handle_health_issue(self, issue: str) -> None:
        """Handle a specific health issue."""
        try:
            self.logger.info(f"Handling health issue: {issue}")
            issue_id = f"health_{int(time.time())}"
            await self.messaging.send_health_alert(issue, issue_id)

            health_record = {
                "type": "health_issue",
                "issue_id": issue_id,
                "issue_description": issue,
                "timestamp": time.time(),
                "agents_notified": True,
            }
            self.state.failure_history.append(health_record)
        except Exception as e:
            self.logger.error(f"Failed to handle health issue: {e}")
