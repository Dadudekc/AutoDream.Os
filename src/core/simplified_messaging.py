"""
Simplified Messaging System - Radical Simplification
===================================================

Simple, direct messaging without complex templates or overhead.
Focus on communication, not formatting.

Author: Agent-4 (Captain)
License: MIT
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class SimplifiedMessaging:
    """Simplified messaging system - no templates, no overhead."""

    def __init__(self) -> None:
        """Initialize simplified messaging system."""
        logger.info("Simplified messaging system initialized")

    def format_task_completion(
        self, agent_id: str, task_name: str, files_created: list[str], status: str = "COMPLETED"
    ) -> str:
        """Format simple task completion message."""
        files_list = ", ".join(files_created) if files_created else "None"
        return f"{agent_id}: {task_name.upper()} COMPLETED\nFiles: {files_list}\nStatus: {status}"

    def format_blocker(self, agent_id: str, task_name: str, issue: str, need: str) -> str:
        """Format simple blocker message."""
        return f"{agent_id}: BLOCKED on {task_name.upper()}\nIssue: {issue}\nNeed: {need}"

    def format_coordination(self, agent_id: str, message: str) -> str:
        """Format simple coordination message."""
        return f"{agent_id}: {message}"

    def format_status_update(self, agent_id: str, task_name: str, progress: str) -> str:
        """Format simple status update."""
        return f"{agent_id}: {task_name.upper()} - {progress}"

    def validate_message(self, message: str) -> dict[str, any]:
        """Simple message validation."""
        return {
            "valid": len(message.strip()) > 0,
            "length": len(message),
            "has_agent_id": ":" in message,
        }

    def get_message_stats(self) -> dict[str, int]:
        """Get simple message statistics."""
        return {"templates_available": 4, "complexity_score": 0, "overhead_reduction": 100}


def create_simple_message(agent_id: str, message_type: str, **kwargs) -> str:
    """Create simple message without templates."""
    messaging = SimplifiedMessaging()
    if message_type == "completion":
        return messaging.format_task_completion(
            agent_id,
            kwargs.get("task_name", "TASK"),
            kwargs.get("files_created", []),
            kwargs.get("status", "COMPLETED"),
        )
    elif message_type == "blocker":
        return messaging.format_blocker(
            agent_id,
            kwargs.get("task_name", "TASK"),
            kwargs.get("issue", "Unknown issue"),
            kwargs.get("need", "Assistance needed"),
        )
    elif message_type == "coordination":
        return messaging.format_coordination(agent_id, kwargs.get("message", ""))
    elif message_type == "status":
        return messaging.format_status_update(
            agent_id, kwargs.get("task_name", "TASK"), kwargs.get("progress", "In progress")
        )
    else:
        return messaging.format_coordination(agent_id, kwargs.get("message", ""))


if __name__ == "__main__":
    completion_msg = create_simple_message(
        "Agent-2",
        "completion",
        task_name="autonomous_workflow_docs",
        files_created=["docs/SIMPLIFIED_AGENT_CYCLE.md", "src/core/simplified_messaging.py"],
        status="COMPLETED",
    )
    logger.info("Task Completion:")
    logger.info(completion_msg)
    logger.info("")
    blocker_msg = create_simple_message(
        "Agent-3",
        "blocker",
        task_name="infrastructure_optimization",
        issue="Database connection timeout",
        need="Database admin access",
    )
    logger.info("Blocker:")
    logger.info(blocker_msg)
    logger.info("")
    coord_msg = create_simple_message(
        "Agent-1", "coordination", message="Ready for Phase 1 integration testing"
    )
    logger.info("Coordination:")
    logger.info(coord_msg)
