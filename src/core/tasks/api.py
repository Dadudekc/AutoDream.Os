#!/usr/bin/env python3
"""
Task Service API - Agent Cellphone V2
=====================================

Provides a simple interface composing scheduling, resource management, and
task tracking services.
"""

from typing import Any, Dict, Optional

from .scheduler import TaskScheduler
from .resource_manager import ResourceManager
from .tracker import TaskTracker
from .logger import get_task_logger


class TaskService:
    """Coordinates task services into a unified API."""

    def __init__(self, workspace_manager) -> None:
        self.logger = get_task_logger("TaskService")
        self.scheduler = TaskScheduler(workspace_manager)
        self.resources = ResourceManager()
        self.tracker = TaskTracker()

    # ------------------------------------------------------------------
    # Task lifecycle
    # ------------------------------------------------------------------
    def create_task(
        self, title: str, description: str, assigned_to: str, created_by: str, **kwargs
    ) -> Optional[str]:
        """Create and begin tracking a task."""
        task_id = self.scheduler.create_task(
            title=title,
            description=description,
            assigned_to=assigned_to,
            created_by=created_by,
            **kwargs,
        )
        if task_id:
            self.tracker.start_tracking(task_id)
        return task_id

    def update_status(self, task_id: str, status: str) -> bool:
        """Update task status and record it in the tracker."""
        task = self.scheduler.get_task(task_id)
        if not task:
            return False
        task.status = status
        self.tracker.update_status(task_id, status)
        return True

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------
    def allocate_resources(self, task_id: str, resources: Dict[str, Any]) -> None:
        """Allocate resources to a task and log the event."""
        self.resources.allocate(task_id, resources)
        self.tracker.update_status(task_id, "resources_allocated")

    def release_resources(self, task_id: str) -> None:
        """Release resources for a task."""
        self.resources.release(task_id)
        self.tracker.update_status(task_id, "resources_released")

    # ------------------------------------------------------------------
    # Information retrieval
    # ------------------------------------------------------------------
    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        """Return combined information about a task."""
        task = self.scheduler.get_task(task_id)
        allocation = self.resources.get_allocation(task_id)
        history = self.tracker.get_history(task_id)
        return {
            "task": task.__dict__ if task else None,
            "allocation": allocation.resources if allocation else None,
            "history": history,
        }


__all__ = ["TaskService"]
