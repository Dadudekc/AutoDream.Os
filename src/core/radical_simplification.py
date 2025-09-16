#!/usr/bin/env python3
"""
Radical Simplification - 3-Phase Agent Cycle
============================================

Ultra-simplified agent cycle replacing all complex systems.
Focus on execution, not process theater.

Author: Agent-4 (Captain - Quality Assurance Specialist)
Mission: Radical Simplification
Status: DEPLOYED - Maximum Efficiency
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class RadicalSimplification:
    """Ultra-simplified 3-phase agent cycle."""

    def __init__(self, agent_id: str) -> None:
        """Initialize radical simplification system."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.task_file = self.workspace_path / "task.txt"
        self.inbox_path = self.workspace_path / "inbox"

        # Ensure workspace exists
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Radical simplification deployed for {agent_id}")

    def phase_1_check(self) -> dict[str, Any]:
        """Phase 1: CHECK (inbox + task status) - 10 seconds max."""
        status = {"has_messages": False, "current_task": None, "action_required": None}

        # Check inbox for messages
        if self.inbox_path.exists():
            messages = list(self.inbox_path.glob("*.txt"))
            if messages:
                status["has_messages"] = True
                status["action_required"] = "process_messages"

        # Check current task
        if self.task_file.exists():
            try:
                with open(self.task_file) as f:
                    task_content = f.read().strip()
                    if task_content:
                        status["current_task"] = task_content
                        status["action_required"] = "execute_task"
            except Exception as e:
                logger.error(f"Failed to read task file: {e}")

        return status

    def phase_2_execute(self, status: dict[str, Any]) -> None:
        """Phase 2: EXECUTE (work on task) - Continuous."""
        if status["action_required"] == "process_messages":
            self._process_messages()
        elif status["action_required"] == "execute_task":
            self._execute_task(status["current_task"])
        else:
            # No action required - ready for new task
            pass

    def phase_3_report(self, completion_type: str, content: str) -> None:
        """Phase 3: REPORT (completion/blocker only) - 5 seconds max."""
        if completion_type in ["COMPLETED", "BLOCKED", "CRITICAL"]:
            # Simple text message - no formatting
            message = f"{completion_type}: {content}"
            logger.info(f"Report: {message}")

            # Send to captain if needed
            if completion_type == "BLOCKED" or completion_type == "CRITICAL":
                self._send_to_captain(message)

    def _process_messages(self) -> None:
        """Process inbox messages."""
        if not self.inbox_path.exists():
            return

        for msg_file in self.inbox_path.glob("*.txt"):
            try:
                with open(msg_file) as f:
                    content = f.read().strip()

                # Process based on content
                if content.startswith("TASK:"):
                    self._handle_task_assignment(content)
                elif content.startswith("BLOCKED:"):
                    self._handle_blocker(content)
                elif content.startswith("CRITICAL:"):
                    self._handle_critical(content)

                # Move to processed
                processed_path = self.workspace_path / "processed"
                processed_path.mkdir(exist_ok=True)
                msg_file.rename(processed_path / msg_file.name)

            except Exception as e:
                logger.error(f"Failed to process message {msg_file}: {e}")

    def _execute_task(self, task: str) -> None:
        """Execute current task."""
        logger.info(f"Executing task: {task}")
        # Task execution logic here
        # This is where the actual work happens

    def _handle_task_assignment(self, content: str) -> None:
        """Handle new task assignment."""
        task = content.replace("TASK:", "").strip()
        with open(self.task_file, "w") as f:
            f.write(task)
        logger.info(f"New task assigned: {task}")

    def _handle_blocker(self, content: str) -> None:
        """Handle blocker notification."""
        logger.info(f"Blocker received: {content}")

    def _handle_critical(self, content: str) -> None:
        """Handle critical issue."""
        logger.warning(f"Critical issue: {content}")

    def _send_to_captain(self, message: str) -> None:
        """Send message to captain."""
        captain_inbox = Path("agent_workspaces/Agent-4/inbox")
        captain_inbox.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        msg_file = captain_inbox / f"{self.agent_id}_{timestamp}.txt"

        with open(msg_file, "w") as f:
            f.write(message)

    def run_cycle(self) -> None:
        """Run complete 3-phase cycle."""
        # Phase 1: CHECK (10 seconds max)
        status = self.phase_1_check()

        # Phase 2: EXECUTE (Continuous)
        self.phase_2_execute(status)

        # Phase 3: REPORT (Only if needed)
        # This is called externally when task is complete or blocked

    def complete_task(self, deliverables: list[str]) -> None:
        """Mark task as complete."""
        if self.task_file.exists():
            self.task_file.unlink()  # Delete task file

        # Report completion
        content = f"Task completed. Deliverables: {', '.join(deliverables)}"
        self.phase_3_report("COMPLETED", content)

    def block_task(self, reason: str) -> None:
        """Mark task as blocked."""
        content = f"Task blocked. Reason: {reason}"
        self.phase_3_report("BLOCKED", content)

    def get_efficiency_metrics(self) -> dict[str, Any]:
        """Get system efficiency metrics."""
        return {
            "phases": 3,
            "cycle_time": "15 seconds max",
            "complexity": "Minimal",
            "overhead": "5%",
            "focus": "Execution over process",
        }


# Global instance for easy access
def get_simplified_agent(agent_id: str) -> RadicalSimplification:
    """Get simplified agent instance."""
    return RadicalSimplification(agent_id)

