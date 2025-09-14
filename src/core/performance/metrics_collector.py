"""Metrics collection system for performance monitoring."""

import logging
import time
from collections import deque
from datetime import datetime
from typing import Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from .dashboard_types import DashboardMetric, MetricType

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects system and application metrics for dashboard display."""

    def __init__(self, history_size: int = 1000):
        """Initialize metrics collector."""
        self.history_size = history_size
        self.metrics_history: dict[str, deque] = {}
        self.last_collection_time = datetime.now()

    def collect_system_metrics(self) -> list[DashboardMetric]:
        """Collect system-level performance metrics."""
        metrics = []
        current_time = datetime.now()

        if PSUTIL_AVAILABLE:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(DashboardMetric(
                name="cpu_usage",
                value=cpu_percent,
                unit="%",
                metric_type=MetricType.GAUGE,
                timestamp=current_time,
                category="system",
                threshold_warning=70.0,
                threshold_critical=90.0
            ))

            # Memory metrics
            memory = psutil.virtual_memory()
            metrics.append(DashboardMetric(
                name="memory_usage",
                value=memory.percent,
                unit="%",
                metric_type=MetricType.GAUGE,
                timestamp=current_time,
                category="system",
                threshold_warning=80.0,
                threshold_critical=95.0
            ))

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics.append(DashboardMetric(
                name="disk_usage",
                value=disk_percent,
                unit="%",
                metric_type=MetricType.GAUGE,
                timestamp=current_time,
                category="system",
                threshold_warning=85.0,
                threshold_critical=95.0
            ))

            # Network metrics
            network = psutil.net_io_counters()
            metrics.append(DashboardMetric(
                name="network_bytes_sent",
                value=network.bytes_sent,
                unit="bytes",
                metric_type=MetricType.COUNTER,
                timestamp=current_time,
                category="network"
            ))

            metrics.append(DashboardMetric(
                name="network_bytes_recv",
                value=network.bytes_recv,
                unit="bytes",
                metric_type=MetricType.COUNTER,
                timestamp=current_time,
                category="network"
            ))

        else:
            logger.warning("psutil not available - system metrics collection disabled")

        return metrics

    def collect_application_metrics(self) -> list[DashboardMetric]:
        """Collect application-specific metrics."""
        metrics = []
        current_time = datetime.now()

        # Application-specific metrics would go here
        # For now, we'll add some placeholder metrics

        metrics.append(DashboardMetric(
            name="active_connections",
            value=0,  # This would be collected from your application
            unit="count",
            metric_type=MetricType.GAUGE,
            timestamp=current_time,
            category="application"
        ))

        metrics.append(DashboardMetric(
            name="requests_per_second",
            value=0,  # This would be collected from your application
            unit="req/s",
            metric_type=MetricType.GAUGE,
            timestamp=current_time,
            category="application"
        ))

        return metrics

    def collect_consolidation_metrics(self) -> list[DashboardMetric]:
        """Collect consolidation-specific metrics."""
        metrics = []
        current_time = datetime.now()

        # Consolidation metrics would be collected from your consolidation system
        metrics.append(DashboardMetric(
            name="consolidation_progress",
            value=0,  # Percentage of consolidation completed
            unit="%",
            metric_type=MetricType.GAUGE,
            timestamp=current_time,
            category="consolidation"
        ))

        metrics.append(DashboardMetric(
            name="files_processed",
            value=0,  # Number of files processed
            unit="count",
            metric_type=MetricType.COUNTER,
            timestamp=current_time,
            category="consolidation"
        ))

        return metrics

    def store_metric(self, metric: DashboardMetric) -> None:
        """Store a metric in the history buffer."""
        if metric.name not in self.metrics_history:
            self.metrics_history[metric.name] = deque(maxlen=self.history_size)
        
        self.metrics_history[metric.name].append(metric)

    def get_metric_history(self, metric_name: str) -> list[DashboardMetric]:
        """Get historical data for a specific metric."""
        return list(self.metrics_history.get(metric_name, []))

    def get_all_metrics(self) -> list[DashboardMetric]:
        """Get all current metrics."""
        all_metrics = []
        all_metrics.extend(self.collect_system_metrics())
        all_metrics.extend(self.collect_application_metrics())
        all_metrics.extend(self.collect_consolidation_metrics())
        
        # Store all metrics in history
        for metric in all_metrics:
            self.store_metric(metric)
        
        self.last_collection_time = datetime.now()
        return all_metrics