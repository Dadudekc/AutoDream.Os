"""Orchestrator coordinating metric collectors."""
from __future__ import annotations

from typing import Iterable, List

from .metrics_collector_config import CollectorConfig
from .metrics_gathering import (
    ApplicationMetricsCollector,
    BaseCollector,
    CustomMetricsCollector,
    NetworkMetricsCollector,
    SystemMetricsCollector,
)
from .metrics_aggregation import MetricsAggregator
from .metrics_definitions import MetricData, MetricType


class MetricsCollectorOrchestrator:
    """Coordinate collectors and aggregation."""

    def __init__(
        self,
        collectors: Iterable[BaseCollector] | None = None,
        config: CollectorConfig | None = None,
    ) -> None:
        self.config = config or CollectorConfig()
        self.collectors: List[BaseCollector] = list(collectors) if collectors else [
            SystemMetricsCollector(self.config),
            ApplicationMetricsCollector(self.config),
            NetworkMetricsCollector(self.config),
        ]
        self.aggregator = MetricsAggregator()

    async def collect(self) -> List[MetricData]:
        """Collect metrics from all configured collectors."""

        metrics: List[MetricData] = []
        for collector in self.collectors:
            metrics.extend(await collector.collect_metrics())
        metrics = self.aggregator.normalize(metrics)
        self.aggregator.store(metrics)
        return metrics

    def get_metrics(self, name: str) -> List[MetricData]:
        """Retrieve collected metrics by name."""

        return self.aggregator.get(name)


__all__ = [
    "SystemMetricsCollector",
    "ApplicationMetricsCollector",
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
    "MetricsCollectorOrchestrator",
    "MetricData",
    "MetricType",
]
