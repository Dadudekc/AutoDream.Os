"""Simple in-memory message queue client."""
from __future__ import annotations

from queue import Queue
from typing import Optional


class MessageQueueClient:
    """A minimal message queue wrapper for demonstration and testing."""

    def __init__(self) -> None:
        self._queue: Queue[str] = Queue()

    def send(self, message: str) -> None:
        """Enqueue ``message``."""
        self._queue.put(message)

    def receive(self) -> Optional[str]:
        """Dequeue a message if available, otherwise return ``None``."""
        if self._queue.empty():
            return None
        return self._queue.get()
