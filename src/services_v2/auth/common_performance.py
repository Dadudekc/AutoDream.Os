"""Common performance data structures and utilities for auth services."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""

    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    context: Dict[str, Any]


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""

    alert_id: str
    timestamp: datetime
    alert_type: str  # "warning", "critical", "info"
    message: str
    metric_name: str
    current_value: float
    threshold: float
    severity: int  # 1-5, higher is more severe


def record_metric(monitor, metric_name: str, value: float, unit: str, context: Dict[str, Any]):
    """Record a performance metric on the monitor."""
    metric = PerformanceMetric(
        timestamp=datetime.now(),
        metric_name=metric_name,
        value=value,
        unit=unit,
        context=context,
    )
    monitor.metrics_history[metric_name].append(metric)


__all__ = ["PerformanceMetric", "PerformanceAlert", "record_metric"]
