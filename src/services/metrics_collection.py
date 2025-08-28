"""Core metric collector implementations."""
from __future__ import annotations

import asyncio
import time
from typing import Callable, Dict, List

import psutil

from src.core.performance.metrics.collector import (
    MetricsCollector,
    MetricData,
    MetricType,
)
from .metrics_collector_config import CollectorConfig


class BaseCollector(MetricsCollector):
    """Common logic shared by all collectors."""

    def __init__(self, config: CollectorConfig | None = None):
        config = config or CollectorConfig()
        super().__init__(config.collection_interval)
        self.config = config

    def _metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        unit: str = "",
        description: str = "",
        tags: Dict[str, str] | None = None,
    ) -> MetricData:
        """Helper to build a MetricData instance."""
        full_tags = dict(self.config.tags)
        if tags:
            full_tags.update(tags)
        return MetricData(
            metric_name=name,
            metric_type=metric_type,
            value=value,
            timestamp=time.time(),
            tags=full_tags,
            unit=unit,
            description=description,
        )


class SystemMetricsCollector(BaseCollector):
    """Collect system-level metrics using `psutil`.

    Requirements:
        - ``psutil`` must be available in the environment.

    Metrics collected (with units):
        - ``cpu_usage_percent`` (percent)
        - ``memory_usage_percent`` (percent)
        - ``disk_usage_percent`` (percent)
    """

    async def collect_metrics(self) -> List[MetricData]:
        """Gather CPU, memory and disk statistics.

        Returns:
            List[MetricData]: Collected metric values with units.
        """
        if not self.enabled:
            return []

        metrics: List[MetricData] = []

        # CPU usage
        metrics.append(
            self._metric(
                "cpu_usage_percent",
                psutil.cpu_percent(interval=None),
                unit="percent",
                description="CPU usage percentage",
            )
        )

        # Memory usage
        memory = psutil.virtual_memory()
        metrics.append(
            self._metric(
                "memory_usage_percent",
                memory.percent,
                unit="percent",
                description="Memory usage percentage",
            )
        )

        # Disk usage
        disk = psutil.disk_usage("/")
        metrics.append(
            self._metric(
                "disk_usage_percent",
                disk.percent,
                unit="percent",
                description="Disk usage percentage",
            )
        )

        return metrics


class ApplicationMetricsCollector(BaseCollector):
    """Collect basic runtime information about the current process.

    Metrics collected (with units):
        - ``app_uptime_seconds`` (seconds)
        - ``event_loop_tasks`` (count)
    """

    def __init__(self, config: CollectorConfig | None = None):
        super().__init__(config)
        self.start_time = time.time()

    async def collect_metrics(self) -> List[MetricData]:
        if not self.enabled:
            return []
        uptime = time.time() - self.start_time
        tasks = len(asyncio.all_tasks())
        return [
            self._metric(
                "app_uptime_seconds",
                uptime,
                unit="seconds",
                description="Application uptime",
            ),
            self._metric(
                "event_loop_tasks",
                tasks,
                unit="count",
                description="Active asyncio tasks",
            ),
        ]


class NetworkMetricsCollector(BaseCollector):
    """Collect network I/O statistics.

    Requirements:
        - ``psutil`` must be installed.

    Metrics collected (with units):
        - ``network_bytes_sent`` (bytes)
        - ``network_bytes_recv`` (bytes)
    """

    async def collect_metrics(self) -> List[MetricData]:
        if not self.enabled:
            return []
        net = psutil.net_io_counters()
        return [
            self._metric("network_bytes_sent", net.bytes_sent, unit="bytes"),
            self._metric("network_bytes_recv", net.bytes_recv, unit="bytes"),
        ]


class CustomMetricsCollector(BaseCollector):
    """Collect metrics defined at runtime via callables.

    Each callable should return a numeric value. Units are determined by the
    caller and are not enforced.
    """

    def __init__(self, config: CollectorConfig | None = None):
        super().__init__(config)
        self._custom: Dict[str, Callable[[], float]] = {}

    def add_custom_metric(self, name: str, func: Callable[[], float]):
        """Register a custom metric producer."""
        self._custom[name] = func

    async def collect_metrics(self) -> List[MetricData]:
        if not self.enabled:
            return []
        return [self._metric(name, func()) for name, func in self._custom.items()]


__all__ = [
    "BaseCollector",
    "SystemMetricsCollector",
    "ApplicationMetricsCollector",
    "NetworkMetricsCollector",
    "CustomMetricsCollector",
]
