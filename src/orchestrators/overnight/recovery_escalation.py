"""
Recovery Escalation
===================

Manages escalation logic for overnight recovery system.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: recovery.py (RecoverySystem class split)
License: MIT
"""

import time
from typing import Any


class RecoveryEscalation:
    """Manages failure escalation."""

    def __init__(self, logger, messaging, state):
        """Initialize escalation manager."""
        self.logger = logger
        self.messaging = messaging
        self.state = state

    async def check_escalation_threshold(self) -> None:
        """Check if escalation threshold has been reached."""
        try:
            current_time = time.time()
            recent_failures = [
                f for f in self.state.failure_history if current_time - f["timestamp"] < 3600
            ]

            if len(recent_failures) >= self.state.escalation_threshold:
                await self._escalate_issues(recent_failures)

        except Exception as e:
            self.logger.error(f"Failed to check escalation threshold: {e}")

    async def _escalate_issues(self, recent_failures: list[dict[str, Any]]) -> None:
        """Escalate issues when threshold is reached."""
        try:
            self.logger.error(f"Escalating {len(recent_failures)} recent failures")
            escalation_id = f"escalation_{int(time.time())}"
            failure_summary = self.summarize_failures(recent_failures)

            await self.messaging.send_escalation_alert(
                escalation_id, len(recent_failures), failure_summary
            )

            self.state.escalated_issues.add(escalation_id)
            escalation_record = {
                "type": "escalation",
                "escalation_id": escalation_id,
                "failure_count": len(recent_failures),
                "failure_summary": failure_summary,
                "timestamp": time.time(),
                "agents_notified": True,
            }
            self.state.failure_history.append(escalation_record)
        except Exception as e:
            self.logger.error(f"Failed to escalate issues: {e}")

    @staticmethod
    def summarize_failures(failures: list[dict[str, Any]]) -> str:
        """Create a summary of recent failures."""
        failure_types = {}
        for failure in failures:
            failure_type = failure.get("type", "unknown")
            failure_types[failure_type] = failure_types.get(failure_type, 0) + 1

        summary_parts = []
        for failure_type, count in failure_types.items():
            summary_parts.append(f"{failure_type}: {count}")

        return ", ".join(summary_parts)
