"""Orchestrator exposing metric collectors and coordinating their use."""
from __future__ import annotations

from typing import Iterable, List

from .metrics_collector_config import CollectorConfig
from .metrics_collector_core import (
    BaseCollector,
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    NetworkMetricsCollector,
    CustomMetricsCollector,
)
from .metrics_collector_processor import MetricsProcessor
from .metrics_collector_storage import MetricsStorage
from .performance_monitor import MetricData, MetricType


class MetricsCollectorOrchestrator:
    """Coordinate multiple collectors and handle processing/storage."""

    def __init__(
        self,
        collectors: Iterable[BaseCollector] | None = None,
        config: CollectorConfig | None = None,
    ):
        self.config = config or CollectorConfig()
        self.collectors: List[BaseCollector] = (
            list(collectors)
            if collectors
            else [
                SystemMetricsCollector(self.config),
                ApplicationMetricsCollector(self.config),
                NetworkMetricsCollector(self.config),
            ]
        )
        self.processor = MetricsProcessor()
        self.storage = MetricsStorage()

    async def collect(self) -> List[MetricData]:
        """Collect metrics from all registered collectors."""
        metrics: List[MetricData] = []
        for collector in self.collectors:
            metrics.extend(await collector.collect_metrics())
        metrics = self.processor.normalize(metrics)
        self.storage.store(metrics)
        return metrics

    def get_metrics(self, name: str) -> List[MetricData]:
        """Retrieve metrics by name from storage."""
        return self.storage.get(name)


__all__ = [
    "SystemMetricsCollector",
    "ApplicationMetricsCollector",
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
    "MetricsCollectorOrchestrator",
    "MetricData",
    "MetricType",
]
