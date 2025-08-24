"""Tests for the metric collection pipeline."""

from __future__ import annotations

import time

from src.core.health.metrics import (
    HealthMetricsCollector,
    InMemoryMetricSink,
    Metric,
    MetricSource,
    MetricSourceType,
)


class ConstantSource(MetricSource):
    """Return a constant metric value each time it is collected."""

    def __init__(self, value: float) -> None:
        self.value = value
        self.interval = 0.0

    def collect(self):
        now = time.time()
        return [Metric("const", "example", self.value, now)]


def test_pipeline_collects_aggregates_and_persists():
    source = ConstantSource(10.0)
    sink = InMemoryMetricSink()
    collector = HealthMetricsCollector({MetricSourceType.SYSTEM: source}, [sink])

    collector.collect_metrics_on_demand(MetricSourceType.SYSTEM)
    assert sink.persisted[0]["example"] == 10.0

    # Change source value and collect again to verify aggregation
    source.value = 20.0
    collector.collect_metrics_on_demand(MetricSourceType.SYSTEM)
    # The average of 10 and 20 is 15
    assert sink.persisted[-1]["example"] == 15.0

