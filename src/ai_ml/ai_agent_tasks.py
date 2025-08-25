"""Task definitions and management for AI agents.

This module provides lightweight structures for describing tasks and a
simple queue for storing pending work.  It intentionally avoids any
external dependencies to keep it flexible for different execution
contexts.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Deque, Optional
from collections import deque


@dataclass(slots=True)
class AIAgentTask:
    """Represents a unit of work for an AI agent.

    Attributes:
        task_id: Unique identifier for the task.
        description: Human readable description of the work to be done.
        payload: Optional data associated with the task.  The payload is
            left intentionally untyped so callers can provide any
            structure needed by their agents.
    """

    task_id: str
    description: str
    payload: Optional[dict] = None


class TaskQueue:
    """FIFO queue for :class:`AIAgentTask` instances."""

    def __init__(self) -> None:
        self._tasks: Deque[AIAgentTask] = deque()

    def add_task(self, task: AIAgentTask) -> None:
        """Add a task to the queue."""
        self._tasks.append(task)

    def get_next_task(self) -> Optional[AIAgentTask]:
        """Retrieve the next task if available."""
        return self._tasks.popleft() if self._tasks else None

    def has_tasks(self) -> bool:
        """Return ``True`` when the queue contains pending work."""
        return bool(self._tasks)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._tasks)
