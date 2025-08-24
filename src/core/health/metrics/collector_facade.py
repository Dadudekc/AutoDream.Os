from __future__ import annotations

"""Facade for coordinating metric collection components."""

from typing import Dict
import asyncio

from .adapters import MetricSourceAdapter
from .aggregation import MetricAggregator
from .scheduler import AsyncScheduler


class CollectorFacade:
    """High level interface used by the rest of the system.

    The facade wires together metric adapters, the aggregator and the async
    scheduler.  It exposes ``start``/``shutdown`` methods and a simple
    ``get_summary`` API used in tests.
    """

    def __init__(self, adapters: Dict[str, MetricSourceAdapter]):
        self.adapters = adapters
        self.aggregator = MetricAggregator()
        self.scheduler = AsyncScheduler()
        self._started = False
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        async with self._lock:
            if self._started:
                return
            self._started = True
            for adapter in self.adapters.values():
                await self.scheduler.schedule(lambda a=adapter: self._run_adapter(a), adapter.interval)

    async def _run_adapter(self, adapter: MetricSourceAdapter) -> None:
        metrics = adapter.collect()
        self.aggregator.add(metrics)

    async def shutdown(self) -> None:
        async with self._lock:
            if not self._started:
                return
            self._started = False
        await self.scheduler.shutdown()

    def get_summary(self):
        return self.aggregator.summary()
