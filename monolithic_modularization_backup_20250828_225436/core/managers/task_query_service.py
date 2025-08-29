"""Service providing task and workflow query helpers."""
from typing import Dict, List, Optional, Any

from .task_models import Task, TaskResult, TaskStatus


class TaskQueryService:
    """Query helper methods for TaskManager."""

    def __init__(self, manager) -> None:
        self._manager = manager

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        return self._manager.tasks.get(task_id, {}).get("status")

    def get_task_info(self, task_id: str) -> Optional[Task]:
        return self._manager.tasks.get(task_id)

    def get_running_tasks(self) -> List[str]:
        return list(self._manager.running_tasks.keys())

    def get_pending_tasks(self) -> List[Task]:
        with self._manager.task_lock:
            return [
                task
                for task in self._manager.tasks.values()
                if task.status == TaskStatus.PENDING
            ]

    def get_completed_tasks(self, limit: int = 100) -> List[TaskResult]:
        results = list(self._manager.completed_tasks.values())
        return sorted(results, key=lambda x: x.execution_time, reverse=True)[:limit]

    def get_task_statistics(self) -> Dict[str, Any]:
        total_tasks = len(self._manager.tasks)
        pending_tasks = len(
            [t for t in self._manager.tasks.values() if t.status == TaskStatus.PENDING]
        )
        running_tasks = len(self._manager.running_tasks)
        completed_tasks = len(
            [t for t in self._manager.tasks.values() if t.status == TaskStatus.COMPLETED]
        )
        failed_tasks = len(
            [t for t in self._manager.tasks.values() if t.status == TaskStatus.FAILED]
        )
        return {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "running_tasks": running_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (completed_tasks / total_tasks * 100)
            if total_tasks > 0
            else 0,
            "active_workflows": len(
                [
                    w
                    for w in self._manager.workflows.values()
                    if w.status == TaskStatus.RUNNING
                ]
            ),
        }
