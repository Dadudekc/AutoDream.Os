#!/usr/bin/env python3
"""
Performance Collector - Agent Cellphone V2
=========================================

Collects and stores performance metrics.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

from datetime import datetime



class PerformanceCollector:
    """Collects and stores performance metrics."""

    def __init__(self, max_history_size: int = 10000):
        """Initialize the performance collector."""
        self.max_history_size = max_history_size
        self.metrics: List[PerformanceMetric] = deque(maxlen=max_history_size)
        self.lock = threading.Lock()

    def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        tags: Dict[str, str] = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Record a performance metric."""
        metric = PerformanceMetric(
            name=name,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {},
            metadata=metadata or {},
        )

        with self.lock:
            self.metrics.append(metric)

    def record_timer(
        self,
        name: str,
        duration: float,
        tags: Dict[str, str] = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Record a timing metric."""
        self.record_metric(name, duration, MetricType.TIMER, tags, metadata)

    def record_counter(
        self,
        name: str,
        increment: float = 1.0,
        tags: Dict[str, str] = None,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """Record a counter metric."""
        self.record_metric(name, increment, MetricType.COUNTER, tags, metadata)

    def get_metrics(
        self, name: str = None, start_time: datetime = None, end_time: datetime = None
    ) -> List[PerformanceMetric]:
        """Get metrics with optional filtering."""
        with self.lock:
            filtered_metrics = self.metrics

            if name:
                filtered_metrics = [m for m in filtered_metrics if m.name == name]

            if start_time:
                filtered_metrics = [
                    m for m in filtered_metrics if m.timestamp >= start_time
                ]

            if end_time:
                filtered_metrics = [
                    m for m in filtered_metrics if m.timestamp <= end_time
                ]

            return list(filtered_metrics)

    def get_latest_metric(self, name: str) -> Optional[PerformanceMetric]:
        """Get the latest metric for a specific name."""
        with self.lock:
            for metric in reversed(self.metrics):
                if metric.name == name:
                    return metric
        return None
