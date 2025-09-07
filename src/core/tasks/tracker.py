#!/usr/bin/env python3
"""
Task Tracker - Agent Cellphone V2
=================================

Maintains history of task states and progress.
Single responsibility: Track task status changes over time.
"""

from datetime import datetime
from typing import Dict, List

from .logger import get_task_logger


class TaskTracker:
    """Tracks task status history."""

    def __init__(self) -> None:
        self.logger = get_task_logger("TaskTracker")
        self._history: Dict[str, List[Dict[str, str]]] = {}

    def start_tracking(self, task_id: str) -> None:
        """Begin tracking a task."""
        self._history.setdefault(task_id, [])
        self.logger.debug(f"Started tracking task {task_id}")

    def update_status(self, task_id: str, status: str) -> None:
        """Record a status change for a task."""
        entry = {"status": status, "timestamp": datetime.now().isoformat()}
        self._history.setdefault(task_id, []).append(entry)
        self.logger.debug(f"Task {task_id} status updated to {status}")

    def get_history(self, task_id: str) -> List[Dict[str, str]]:
        """Get status history for a task."""
        return self._history.get(task_id, [])


__all__ = ["TaskTracker"]
