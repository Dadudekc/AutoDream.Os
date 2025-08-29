"""Service responsible for monitoring task statuses."""
from collections import Counter
from typing import Dict

from ..task_models import Task
from .interfaces import HealthCheckInterface


class TaskMonitoringService:
    """Service responsible for monitoring task statuses."""

    def __init__(self, health: HealthCheckInterface) -> None:
        self._health = health

    def _monitor(self, tasks: Dict[str, Task]) -> Dict[str, int]:
        counts = Counter(task.status.value for task in tasks.values())
        return dict(counts)

    def check_health(self) -> bool:
        return self._health.is_healthy()
