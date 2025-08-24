from __future__ import annotations

"""Asynchronous scheduling helpers."""

from typing import Awaitable, Callable, List
import asyncio


class AsyncScheduler:
    """Schedule coroutines at fixed intervals."""

    def __init__(self) -> None:
        self._tasks: List[asyncio.Task] = []
        self._lock = asyncio.Lock()
        self._running = False

    async def schedule(self, coro_factory: Callable[[], Awaitable[None]], interval: float) -> None:
        """Schedule ``coro_factory`` to run repeatedly every ``interval`` seconds."""

        async def _runner() -> None:
            try:
                while self._running:
                    await coro_factory()
                    await asyncio.sleep(interval)
            except asyncio.CancelledError:
                pass

        async with self._lock:
            if not self._running:
                self._running = True
            task = asyncio.create_task(_runner())
            self._tasks.append(task)

    async def shutdown(self) -> None:
        """Cancel all scheduled tasks in a thread safe way."""
        async with self._lock:
            tasks = list(self._tasks)
            self._tasks.clear()
            self._running = False
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
