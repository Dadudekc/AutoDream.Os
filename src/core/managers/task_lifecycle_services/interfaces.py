"""Common interfaces for task lifecycle services."""
from queue import PriorityQueue
from typing import Dict, Protocol

from ..task_models import Task


class PersistenceInterface(Protocol):
    """Interface for task state persistence."""

    def persist(self, tasks: Dict[str, Task], queue: PriorityQueue) -> None:
        """Persist task state."""
        ...


class HealthCheckInterface(Protocol):
    """Interface for health checking."""

    def is_healthy(self) -> bool:
        """Return True if the component is healthy."""
        ...
