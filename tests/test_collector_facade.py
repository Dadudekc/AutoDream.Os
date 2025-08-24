import asyncio

import pytest

from src.core.health.metrics import CollectorFacade, SystemMetricsAdapter


@pytest.mark.asyncio
async def test_collector_facade_collects_metrics():
    adapter = SystemMetricsAdapter(interval=0.05)
    facade = CollectorFacade({"system": adapter})
    await facade.start()
    await asyncio.sleep(0.15)
    await facade.shutdown()
    summary = facade.get_summary()
    assert "cpu_percent" in summary
    assert "memory_percent" in summary


@pytest.mark.asyncio
async def test_shutdown_is_thread_safe():
    adapter = SystemMetricsAdapter(interval=0.05)
    facade = CollectorFacade({"system": adapter})
    await facade.start()
    await asyncio.sleep(0.1)
    await facade.shutdown()
    # second shutdown should not raise
    await facade.shutdown()
