"""
Execution Operations - Execution Manager Operations
===================================================
Task CRUD operations extracted for V2 compliance <200 lines.

Author: Agent-5 (extracted from base_execution_manager.py)
License: MIT
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from ..contracts import ManagerContext, ManagerResult


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionOperations:
    """Handles execution CRUD operations."""

    def __init__(self, tasks: dict, task_queue: list):
        """Initialize execution operations."""
        self.tasks = tasks
        self.task_queue = task_queue

    def create_task(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a new task."""
        try:
            task_id = str(uuid.uuid4())
            task = {
                "task_id": task_id,
                "type": payload.get("type", "general"),
                "status": TaskStatus.PENDING,
                "created_at": datetime.now().isoformat(),
                "data": payload.get("data", {}),
            }
            self.tasks[task_id] = task
            self.task_queue.append(task_id)
            return ManagerResult(
                success=True,
                data={"task_id": task_id},
                message=f"Task created: {task_id}",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to create task: {e}", errors=[str(e)]
            )

    def cancel_task(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Cancel a task."""
        try:
            task_id = payload.get("task_id")
            if not task_id or task_id not in self.tasks:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Task not found: {task_id}",
                    errors=[f"Task not found: {task_id}"],
                )
            task = self.tasks[task_id]
            if task["status"] == TaskStatus.RUNNING:
                task["status"] = TaskStatus.CANCELLED
                task["cancelled_at"] = datetime.now().isoformat()
                if task_id in self.task_queue:
                    self.task_queue.remove(task_id)
                return ManagerResult(
                    success=True,
                    data={"task_id": task_id},
                    message=f"Task cancelled: {task_id}",
                    errors=[],
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Task not running: {task_id}",
                    errors=[f"Task status: {task['status']}"],
                )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to cancel task: {e}", errors=[str(e)]
            )

    def list_tasks(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """List all tasks."""
        try:
            return ManagerResult(
                success=True,
                data={"tasks": list(self.tasks.keys()), "count": len(self.tasks)},
                message=f"Found {len(self.tasks)} tasks",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False, data={}, message=f"Failed to list tasks: {e}", errors=[str(e)]
            )
