"""
Health Metrics Package

This package contains modules for health metrics collection and processing.
"""

from .collector import (
    HealthMetricsCollector,
    MetricSource,
    MetricCollectionMethod,
    MetricCollectionConfig,
    CollectedMetric,
    MetricCollectionResult,
)
from .adapters import MetricSourceAdapter, SystemMetricsAdapter, Metric
from .aggregation import MetricAggregator
from .scheduler import AsyncScheduler
from .collector_facade import CollectorFacade

__all__ = [
    "HealthMetricsCollector",
    "MetricSource",
    "MetricCollectionMethod",
    "MetricCollectionConfig",
    "CollectedMetric",
    "MetricCollectionResult",
    "MetricSourceAdapter",
    "SystemMetricsAdapter",
    "Metric",
    "MetricAggregator",
    "AsyncScheduler",
    "CollectorFacade",
]
