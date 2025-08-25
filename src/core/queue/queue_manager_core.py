from __future__ import annotations

from dataclasses import dataclass, field
from queue import PriorityQueue, Empty
from typing import Any

from .queue_priority import MessagePriority, priority_value


@dataclass(order=True)
class _PrioritizedItem:
    priority: int
    message: Any = field(compare=False)


class QueueManagerCore:
    """Thread-safe priority queue storage."""

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: PriorityQueue[_PrioritizedItem] = PriorityQueue(maxsize=maxsize)

    def enqueue(self, message: Any, priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        try:
            item = _PrioritizedItem(-priority_value(priority), message)
            self._queue.put(item)
            return True
        except Exception:
            return False

    def dequeue(self, block: bool = False, timeout: float | None = None) -> Any:
        item = self._queue.get(block=block, timeout=timeout)
        return item.message

    def size(self) -> int:
        return self._queue.qsize()

    def is_empty(self) -> bool:
        return self._queue.empty()

    def clear(self) -> None:
        while not self.is_empty():
            try:
                self._queue.get_nowait()
            except Empty:
                break

    def get_status(self) -> dict[str, Any]:
        return {"queue_size": self.size(), "is_empty": self.is_empty()}
