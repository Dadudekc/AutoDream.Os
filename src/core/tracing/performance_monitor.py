# V3-004: Distributed Tracing Implementation - Performance Monitor
# Agent-1: Architecture Foundation Specialist
#
# Performance monitoring system for V2_SWARM distributed tracing

import threading
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import psutil

from .jaeger_tracer import trace_manager


class MetricType(Enum):
    """Metric type enumeration."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class Metric:
    """Performance metric structure."""

    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    tags: dict[str, str]
    unit: str = ""


@dataclass
class PerformanceStats:
    """Performance statistics structure."""

    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_connections: int
    timestamp: datetime


class PerformanceMonitor:
    """Performance monitoring for distributed tracing."""

    def __init__(self, collection_interval: int = 30):
        self.collection_interval = collection_interval
        self.metrics: deque = deque(maxlen=10000)
        self.custom_metrics: dict[str, list[float]] = defaultdict(list)
        self.performance_stats: deque = deque(maxlen=1000)
        self.tracer = trace_manager.get_tracer()
        self.logger = logging.getLogger(__name__)
        self._monitoring = False
        self._monitor_thread = None
        self._lock = threading.Lock()

    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True, daemon=True, daemon=True, daemon=True
        )
        self._monitor_thread.start()

        self.logger.info("Performance monitoring started")

    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)

        self.logger.info("Performance monitoring stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._monitoring:
            try:
                self._collect_system_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.collection_interval)

    def _collect_system_metrics(self) -> None:
        """Collect system performance metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_available_mb = memory.available / (1024 * 1024)

            # Disk metrics
            disk = psutil.disk_usage("/")
            disk_usage_percent = (disk.used / disk.total) * 100

            # Network metrics
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv

            # Connection metrics
            connections = len(psutil.net_connections())

            # Create performance stats
            stats = PerformanceStats(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_usage_percent,
                network_bytes_sent=network_bytes_sent,
                network_bytes_recv=network_bytes_recv,
                active_connections=connections,
                timestamp=datetime.utcnow(),
            )

            with self._lock:
                self.performance_stats.append(stats)

            # Record metrics in trace
            with self.tracer.trace_span("performance_metrics") as span:
                self.tracer.add_span_tags(
                    {
                        "system.cpu_percent": cpu_percent,
                        "system.memory_percent": memory_percent,
                        "system.memory_used_mb": memory_used_mb,
                        "system.disk_usage_percent": disk_usage_percent,
                        "system.active_connections": connections,
                    }
                )

            # Create metrics
            self._create_metric("system.cpu_percent", cpu_percent, MetricType.GAUGE, "%")
            self._create_metric("system.memory_percent", memory_percent, MetricType.GAUGE, "%")
            self._create_metric("system.memory_used_mb", memory_used_mb, MetricType.GAUGE, "MB")
            self._create_metric(
                "system.disk_usage_percent", disk_usage_percent, MetricType.GAUGE, "%"
            )
            self._create_metric("system.active_connections", connections, MetricType.GAUGE, "count")

        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")

    def _create_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType,
        unit: str = "",
        tags: dict[str, str] = None,
    ) -> None:
        """Create and store a metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.utcnow(),
            tags=tags or {},
            unit=unit,
        )

        with self._lock:
            self.metrics.append(metric)

    def record_custom_metric(self, name: str, value: float, tags: dict[str, str] = None) -> None:
        """Record a custom metric."""
        self._create_metric(name, value, MetricType.GAUGE, tags=tags)

        # Store in custom metrics for analysis
        with self._lock:
            self.custom_metrics[name].append(value)
            # Keep only last 1000 values
            if len(self.custom_metrics[name]) > 1000:
                self.custom_metrics[name] = self.custom_metrics[name][-1000:]

    def record_timing(
        self, operation_name: str, duration: float, tags: dict[str, str] = None
    ) -> None:
        """Record timing metric."""
        self._create_metric(f"timing.{operation_name}", duration, MetricType.TIMER, "ms", tags)

        # Record in trace
        with self.tracer.trace_span("timing_metric") as span:
            span_tags = {"operation.name": operation_name, "operation.duration": duration}
            if tags:
                span_tags.update(tags)
            self.tracer.add_span_tags(span_tags)

    def record_counter(self, name: str, increment: int = 1, tags: dict[str, str] = None) -> None:
        """Record counter metric."""
        self._create_metric(f"counter.{name}", increment, MetricType.COUNTER, "count", tags)

    def get_current_metrics(self) -> list[Metric]:
        """Get current metrics."""
        with self._lock:
            return list(self.metrics)

    def get_metrics_by_name(self, name: str, limit: int = 100) -> list[Metric]:
        """Get metrics by name."""
        with self._lock:
            return [m for m in self.metrics if m.name == name][-limit:]

    def get_performance_stats(self, limit: int = 100) -> list[PerformanceStats]:
        """Get performance statistics."""
        with self._lock:
            return list(self.performance_stats)[-limit:]

    def get_average_metrics(self, time_window_minutes: int = 5) -> dict[str, float]:
        """Get average metrics over time window."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)

        with self._lock:
            recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]

        # Group by name and calculate averages
        metric_groups = defaultdict(list)
        for metric in recent_metrics:
            metric_groups[metric.name].append(metric.value)

        averages = {}
        for name, values in metric_groups.items():
            if values:
                averages[name] = sum(values) / len(values)

        return averages

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance summary."""
        with self._lock:
            if not self.performance_stats:
                return {}

            latest_stats = self.performance_stats[-1]

            # Calculate averages over last hour
            hour_ago = datetime.utcnow() - timedelta(hours=1)
            recent_stats = [s for s in self.performance_stats if s.timestamp >= hour_ago]

            if recent_stats:
                avg_cpu = sum(s.cpu_percent for s in recent_stats) / len(recent_stats)
                avg_memory = sum(s.memory_percent for s in recent_stats) / len(recent_stats)
                avg_disk = sum(s.disk_usage_percent for s in recent_stats) / len(recent_stats)
            else:
                avg_cpu = latest_stats.cpu_percent
                avg_memory = latest_stats.memory_percent
                avg_disk = latest_stats.disk_usage_percent

            return {
                "current": {
                    "cpu_percent": latest_stats.cpu_percent,
                    "memory_percent": latest_stats.memory_percent,
                    "memory_used_mb": latest_stats.memory_used_mb,
                    "disk_usage_percent": latest_stats.disk_usage_percent,
                    "active_connections": latest_stats.active_connections,
                },
                "averages_1h": {
                    "cpu_percent": avg_cpu,
                    "memory_percent": avg_memory,
                    "disk_usage_percent": avg_disk,
                },
                "timestamp": latest_stats.timestamp.isoformat(),
            }

    def export_metrics(self) -> list[dict[str, Any]]:
        """Export metrics for analysis."""
        with self._lock:
            return [asdict(metric) for metric in self.metrics]

    def clear_old_metrics(self, max_age_hours: int = 24) -> int:
        """Clear old metrics."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)

        with self._lock:
            original_count = len(self.metrics)
            self.metrics = deque(
                [m for m in self.metrics if m.timestamp >= cutoff_time], maxlen=10000
            )
            cleared_count = original_count - len(self.metrics)

        if cleared_count > 0:
            self.logger.info(f"Cleared {cleared_count} old metrics")

        return cleared_count


class PerformanceDecorator:
    """Decorator for automatic performance monitoring."""

    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor

    def __call__(self, operation_name: str = None):
        """Decorator for timing functions."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                name = operation_name or f"{func.__module__}.{func.__name__}"
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000  # Convert to ms
                    self.monitor.record_timing(name, duration)
                    return result
                except Exception:
                    duration = (time.time() - start_time) * 1000
                    self.monitor.record_timing(name, duration, {"error": "true"})
                    raise

            return wrapper

        return decorator
