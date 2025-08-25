"""High level orchestrator for the queue system.

This lightweight wrapper wires together the core queue storage, the
background processor and priority helpers.  The previous implementation
mixed all responsibilities in a single file; it has been split into
focused modules to improve maintainability.
"""

from __future__ import annotations

from typing import Any, Callable

from .queue_manager_core import QueueManagerCore
from .queue_processor import QueueProcessor
from .queue_priority import MessagePriority


class QueueManager:
    """Coordinate queue storage and background processing."""

    def __init__(
        self,
        handler: Callable[[Any], None],
        maxsize: int = 0,
        poll_interval: float = 0.1,
    ) -> None:
        self.core = QueueManagerCore(maxsize=maxsize)
        self.processor = QueueProcessor(self.core, handler, poll_interval)

    # ------------------------------------------------------------------
    # Queue operations
    # ------------------------------------------------------------------
    def enqueue(self, message: Any, priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        return self.core.enqueue(message, priority)

    def start(self) -> None:
        self.processor.start()

    def stop(self) -> None:
        self.processor.stop()

    def status(self) -> dict:
        return self.core.get_status()
