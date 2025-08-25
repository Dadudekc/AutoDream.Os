from __future__ import annotations

import threading
from queue import Empty
from typing import Any, Callable, Optional


class QueueProcessor:
    """Background worker that processes messages from a queue."""

    def __init__(
        self,
        core,
        handler: Callable[[Any], None],
        poll_interval: float = 0.1,
    ) -> None:
        self.core = core
        self.handler = handler
        self.poll_interval = poll_interval
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                item = self.core.dequeue(block=True, timeout=self.poll_interval)
            except Empty:
                continue
            try:
                self.handler(item)
            except Exception:
                # Handler errors shouldn't crash the processor
                continue

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()
