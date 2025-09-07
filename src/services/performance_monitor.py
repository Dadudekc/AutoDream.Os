from src.core.performance.monitoring import MetricData, MetricSeries
from src.core.performance.monitoring.performance_alerts import (
from src.core.performance.monitoring.performance_monitor import (
from src.core.performance.monitoring.performance_types import (

"""Compatibility wrapper for deprecated services.performance_monitor module.

This module re-exports the unified PerformanceMonitor implementation from
``src.core.performance.monitoring.performance_monitor``. It preserves the
original import path for legacy code while ensuring a single source of truth.
"""

    PerformanceMonitor,
    PerformanceLevel,
)
    MetricType,
    MonitorMetric,
    MonitorSnapshot,
)
    AlertSeverity,
    AlertCondition,
    PerformanceAlert,
)

__all__ = [
    "PerformanceMonitor",
    "MonitorMetric",
    "MonitorSnapshot",
    "PerformanceLevel",
    "AlertSeverity",
    "AlertCondition",
    "PerformanceAlert",
    "MetricData",
    "MetricSeries",
    "MetricType",
]
