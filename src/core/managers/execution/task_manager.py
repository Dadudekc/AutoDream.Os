"""
Task Manager - Phase-2 V2 Compliance Refactoring
================================================

Handles task-specific execution operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from .base_execution_manager import BaseExecutionManager, TaskStatus
from ..contracts import ManagerContext, ManagerResult


class TaskManager(BaseExecutionManager):
    """Manages task execution operations."""

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute task operation."""
        try:
            if operation == "create_task":
                return self._create_task(context, payload)
            elif operation == "execute_task":
                return self.execute_task(context, payload.get("task_id"), payload.get("task_data", {}))
            elif operation == "cancel_task":
                return self._cancel_task(context, payload)
            elif operation == "list_tasks":
                return self._list_tasks(context, payload)
            elif operation == "get_task_status":
                return self._get_task_status(context, payload)
            else:
                return super().execute(context, operation, payload)
        except Exception as e:
            context.logger(f"Error executing task operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _get_task_status(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get specific task status."""
        try:
            task_id = payload.get("task_id")
            if not task_id or task_id not in self.tasks:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Task ID is required and must exist",
                )

            task = self.tasks[task_id]
            
            # Add execution information if available
            execution_info = {}
            for exec_id, execution in self.executions.items():
                if execution.get("task_id") == task_id:
                    execution_info = {
                        "execution_id": exec_id,
                        "execution_status": execution.get("status"),
                        "duration": self._get_execution_duration(execution),
                    }
                    break

            return ManagerResult(
                success=True,
                data={
                    "task": task,
                    "execution_info": execution_info,
                },
                metrics={"task_found": 1},
            )

        except Exception as e:
            context.logger(f"Error getting task status: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def get_status(self) -> Dict[str, Any]:
        """Get task manager status."""
        base_status = super().get_status()
        base_status.update({
            "task_queue_length": len(self.task_queue),
            "active_threads": len([t for t in self.execution_threads.values() if t.is_alive()]),
            "task_types": list(set(t.get("type", "unknown") for t in self.tasks.values())),
        })
        return base_status
