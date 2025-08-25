"""Orchestrator coordinating metric collectors."""
from __future__ import annotations
from typing import Iterable, List
from .metrics_collector_config import CollectorConfig
from .metrics_collector_core import BaseCollector, SystemMetricsCollector, ApplicationMetricsCollector, NetworkMetricsCollector, CustomMetricsCollector
from .metrics_collector_processor import MetricsProcessor
from .metrics_collector_storage import MetricsStorage
from .performance_monitor import MetricData, MetricType
class MetricsCollectorOrchestrator:
    """Coordinate collectors, processor, and storage."""
    def __init__(self, collectors: Iterable[BaseCollector] | None=None, config: CollectorConfig | None=None) -> None:
        self.config = config or CollectorConfig()
        self.collectors: List[BaseCollector] = list(collectors) if collectors else [
            SystemMetricsCollector(self.config), ApplicationMetricsCollector(self.config), NetworkMetricsCollector(self.config)]
        self.processor, self.storage = MetricsProcessor(), MetricsStorage()

    async def collect(self) -> List[MetricData]:
        metrics: List[MetricData] = []
        for c in self.collectors:
            metrics.extend(await c.collect_metrics())
        metrics = self.processor.normalize(metrics); self.storage.store(metrics)
        return metrics

    def get_metrics(self, name: str) -> List[MetricData]:
        return self.storage.get(name)

__all__ = ["SystemMetricsCollector", "ApplicationMetricsCollector", "NetworkMetricsCollector", "CustomMetricsCollector", "MetricsCollectorOrchestrator", "MetricData", "MetricType"]
