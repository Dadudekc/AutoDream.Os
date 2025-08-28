"""Orchestrator coordinating metric collectors."""
from __future__ import annotations
from typing import Iterable, List, Dict

from .metrics_collector_config import CollectorConfig
from .metrics_collection import (
    BaseCollector,
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    NetworkMetricsCollector,
    CustomMetricsCollector,
)
from .metrics_computation import MetricsProcessor
from .metrics_collector_storage import MetricsStorage
from .metrics_reporting import MetricsReporter
from src.core.performance.metrics.collector import MetricData, MetricType


class MetricsCollectorOrchestrator:
    """Coordinate collection, computation, and reporting."""

    def __init__(
        self,
        collectors: Iterable[BaseCollector] | None = None,
        config: CollectorConfig | None = None,
    ) -> None:
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
        self.reporter = MetricsReporter(self.storage)

    async def collect(self) -> List[MetricData]:
        """Collect metrics from all collectors and store them."""
        metrics: List[MetricData] = []
        for collector in self.collectors:
            metrics.extend(await collector.collect_metrics())
        normalized = self.processor.normalize(metrics)
        self.storage.store(normalized)
        return normalized

    def get_metrics(self, name: str) -> List[MetricData]:
        """Retrieve stored metrics by name."""
        return self.storage.get(name)

    def generate_report(self) -> Dict[str, Dict[str, float]]:
        """Generate a threshold-based report of collected metrics."""
        return self.reporter.generate_report()


__all__ = [
    "SystemMetricsCollector",
    "ApplicationMetricsCollector",
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
    "MetricsCollectorOrchestrator",
    "MetricData",
    "MetricType",
]
