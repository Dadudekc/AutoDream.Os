#!/usr/bin/env python3
"""
Metrics Collector - V2 Compliant Module
=======================================

Focused metrics collection and aggregation system for business intelligence.
V2 COMPLIANT: Under 300 lines, focused responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import statistics
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MetricDataPoint:
    """Represents a single metric data point."""
    timestamp: datetime
    metric_name: str
    value: Any
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetricsCollector:

EXAMPLE USAGE:
==============

# Import the service
from src.services.analytics.metrics_collector import Metrics_CollectorService

# Initialize service
service = Metrics_CollectorService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Metrics_CollectorService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

    """Advanced metrics collection and aggregation system."""

    def __init__(self, retention_hours: int = 24):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.retention_hours = retention_hours
        self.collection_stats = {
            "total_metrics_collected": 0,
            "metrics_by_type": defaultdict(int),
            "collection_errors": 0,
            "last_collection_time": None
        }
        self._lock = threading.Lock()

    def collect_metric(self, metric_name: str, value: Any,
                      tags: Dict[str, str] = None, metadata: Dict[str, Any] = None) -> None:
        """Collect a metric data point."""
        try:
            data_point = MetricDataPoint(
                timestamp=datetime.now(),
                metric_name=metric_name,
                value=value,
                tags=tags or {},
                metadata=metadata or {}
            )

            with self._lock:
                self.metrics[metric_name].append(data_point)
                self.collection_stats["total_metrics_collected"] += 1
                self.collection_stats["metrics_by_type"][metric_name] += 1
                self.collection_stats["last_collection_time"] = datetime.now()

                # Clean up old data
                self._cleanup_old_data()

        except Exception as e:
            logger.error(f"Failed to collect metric {metric_name}: {e}")
            self.collection_stats["collection_errors"] += 1

    def get_metric_data(self, metric_name: str, hours_back: int = 1) -> List[MetricDataPoint]:
        """Get metric data for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)

        with self._lock:
            return [dp for dp in self.metrics[metric_name] if dp.timestamp >= cutoff_time]

    def get_metric_stats(self, metric_name: str, hours_back: int = 1) -> Dict[str, Any]:
        """Get statistical summary for a metric."""
        data_points = self.get_metric_data(metric_name, hours_back)
        if not data_points:
            return {"error": "No data available"}

        values = [dp.value for dp in data_points if isinstance(dp.value, (int, float))]

        if not values:
            return {"error": "No numeric data available"}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "latest": values[-1] if values else None,
            "trend": self._calculate_trend(values),
            "period_start": data_points[0].timestamp.isoformat(),
            "period_end": data_points[-1].timestamp.isoformat()
        }

    def _calculate_trend(self, values: List[float], window: int = 10) -> str:
        """Calculate trend direction for a series of values."""
        if len(values) < window * 2:
            return "insufficient_data"

        recent = values[-window:]
        previous = values[-window*2:-window]

        if not recent or not previous:
            return "insufficient_data"

        recent_avg = statistics.mean(recent)
        previous_avg = statistics.mean(previous)

        if recent_avg > previous_avg * 1.05:  # 5% increase
            return "increasing"
        elif recent_avg < previous_avg * 0.95:  # 5% decrease
            return "decreasing"
        else:
            return "stable"

    def _cleanup_old_data(self) -> None:
        """Clean up data older than retention period."""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)

        for metric_name, data_points in self.metrics.items():
            # Remove old data points
            while data_points and data_points[0].timestamp < cutoff_time:
                data_points.popleft()

    def get_all_metric_names(self) -> List[str]:
        """Get list of all collected metric names."""
        with self._lock:
            return list(self.metrics.keys())

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get metrics collection statistics."""
        with self._lock:
            return dict(self.collection_stats)


# Factory function for dependency injection
def create_metrics_collector(retention_hours: int = 24) -> MetricsCollector:
    """Factory function to create metrics collector with optional configuration."""
    return MetricsCollector(retention_hours)


# Export for DI
__all__ = ["MetricsCollector", "MetricDataPoint", "create_metrics_collector"]
