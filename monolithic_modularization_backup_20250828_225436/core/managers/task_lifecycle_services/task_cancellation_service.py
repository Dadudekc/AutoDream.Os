"""Service responsible for cancelling tasks."""
from datetime import datetime
from queue import PriorityQueue
from typing import Dict

from ..task_models import Task, TaskStatus
from .interfaces import PersistenceInterface, HealthCheckInterface


class TaskCancellationService:
    """Service responsible for cancelling tasks."""

    def __init__(self, persistence: PersistenceInterface, health: HealthCheckInterface) -> None:
        self._persistence = persistence
        self._health = health

    def _cancel(self, task_id: str, tasks: Dict[str, Task], queue: PriorityQueue) -> bool:
        task = tasks.get(task_id)
        if not task or task.status != TaskStatus.PENDING:
            return False
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now().isoformat()
        self._persistence.persist(tasks, queue)
        return True

    def check_health(self) -> bool:
        return self._health.is_healthy()
