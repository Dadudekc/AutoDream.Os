"""
Recovery Messaging - V2 Compliant
==================================

Message sending and notification helpers for recovery system.
Extracted from recovery.py for V2 compliance.

V2 Compliance: Focused module for recovery-related messaging.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-1's work)
License: MIT
"""

import asyncio
import logging
import time

# V2 Integration imports
try:
    from ...core.messaging_pyautogui import send_message_to_agent
except ImportError:
    logging.warning("V2 messaging import failed, using mock")

    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True


class RecoveryMessaging:
    """Handles all messaging/notification for recovery system."""

    def __init__(self, logger: logging.Logger):
        """Initialize recovery messaging."""
        self.logger = logger

    async def send_cycle_recovery_message(self, cycle_number: int, error_message: str) -> None:
        """Send recovery message for cycle failure to all agents."""
        try:
            self.logger.info(f"Sending cycle {cycle_number} recovery message")

            recovery_message = f"""
[RECOVERY] Cycle {cycle_number} Recovery
Error: {error_message}
Action: Continue with next cycle, report any issues.
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(recovery_message)
            self.logger.info("Cycle recovery messages sent")

        except Exception as e:
            self.logger.error(f"Failed to send cycle recovery messages: {e}")

    async def send_task_recovery_message(
        self, task_id: str, agent_id: str, error_message: str
    ) -> None:
        """Send recovery message for task failure to specific agent."""
        try:
            self.logger.info(f"Sending task recovery message to {agent_id}")

            recovery_message = f"""
[RECOVERY] Task {task_id} Recovery
Error: {error_message}
Action: Retry task or report if impossible.
Timestamp: {time.time()}
"""

            await asyncio.get_event_loop().run_in_executor(
                None, send_message_to_agent, agent_id, recovery_message
            )

            self.logger.info(f"Task recovery message sent to {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to send task recovery message: {e}")

    async def send_agent_rescue_message(self, agent_id: str) -> None:
        """Send rescue message to stalled agent."""
        try:
            self.logger.info(f"Sending rescue message to {agent_id}")

            rescue_message = f"[RESCUE] {agent_id} - Reset and resume operations. Report status."

            await asyncio.get_event_loop().run_in_executor(
                None, send_message_to_agent, agent_id, rescue_message
            )

            self.logger.info(f"Rescue message sent to {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to send rescue message to {agent_id}: {e}")

    async def send_health_alert(self, issue: str, issue_id: str) -> None:
        """Send health alert to all agents."""
        try:
            self.logger.info(f"Sending health alert: {issue}")

            health_message = f"""
[HEALTH ALERT] System Issue Detected
Issue: {issue}
Action: Monitor and report status.
Issue ID: {issue_id}
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(health_message)
            self.logger.info("Health alerts sent")

        except Exception as e:
            self.logger.error(f"Failed to send health alerts: {e}")

    async def send_escalation_alert(
        self, escalation_id: str, failure_count: int, failure_summary: str
    ) -> None:
        """Send escalation alert to all agents."""
        try:
            self.logger.info(f"Sending escalation alert: {escalation_id}")

            escalation_message = f"""
[ESCALATION] Critical System Issues
Escalation ID: {escalation_id}
Recent Failures: {failure_count}
Summary: {failure_summary}
Action: Manual intervention required.
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(escalation_message)
            self.logger.info("Escalation alerts sent")

        except Exception as e:
            self.logger.error(f"Failed to send escalation alerts: {e}")

    async def _broadcast_to_all_agents(self, message: str) -> None:
        """Broadcast message to all 8 agents."""
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None, send_message_to_agent, agent_id, message
                )
            except Exception as e:
                self.logger.error(f"Failed to send message to {agent_id}: {e}")
