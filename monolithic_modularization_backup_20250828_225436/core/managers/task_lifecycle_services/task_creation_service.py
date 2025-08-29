"""Service responsible for creating tasks."""
from queue import PriorityQueue
from typing import Dict

from ..task_models import Task
from .interfaces import PersistenceInterface, HealthCheckInterface


class TaskCreationService:
    """Service responsible for creating tasks."""

    def __init__(self, persistence: PersistenceInterface, health: HealthCheckInterface) -> None:
        self._persistence = persistence
        self._health = health

    def _create(self, tasks: Dict[str, Task], queue: PriorityQueue, task: Task) -> str:
        tasks[task.id] = task
        queue.put((task.priority.value, task.id))
        self._persistence.persist(tasks, queue)
        return task.id

    def check_health(self) -> bool:
        return self._health.is_healthy()
