"""Task assignment module for coordinator."""
from __future__ import annotations
from typing import Dict, List, Any


class TaskAssigner:
    """Assigns tasks to agents and tracks their queues."""

    def __init__(self) -> None:
        self._tasks: Dict[str, List[Any]] = {}

    def assign_task(self, agent_id: str, task: Any) -> None:
        self._tasks.setdefault(agent_id, []).append(task)

    def get_tasks(self, agent_id: str) -> List[Any]:
        return list(self._tasks.get(agent_id, []))
