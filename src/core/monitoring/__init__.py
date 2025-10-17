"""
Unified Monitoring - DUP-014 Consolidation
==========================================

Consolidated monitoring infrastructure.

Exports:
    - UnifiedMetricManager: Metric management (consolidates 2 duplicates)
    - UnifiedWidgetManager: Widget management (consolidates 2 duplicates)
    - MetricType: Metric type enumeration
    - WidgetType: Widget type enumeration
    - PerformanceMetric: Metric data structure
    - DashboardWidget: Widget data structure

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-014 Metric/Widget Managers Consolidation
License: MIT
"""

from .unified_metric_manager import (
    UnifiedMetricManager,
    MetricType,
    PerformanceMetric,
)
from .unified_widget_manager import (
    UnifiedWidgetManager,
    WidgetType,
    DashboardWidget,
)

__all__ = [
    "UnifiedMetricManager",
    "UnifiedWidgetManager",
    "MetricType",
    "WidgetType",
    "PerformanceMetric",
    "DashboardWidget",
]

__version__ = "2.0.0"

