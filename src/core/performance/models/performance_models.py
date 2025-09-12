#!/usr/bin/env python3
"""
Performance Models - V2 Compliant Module
=======================================

Data models for performance monitoring system.
V2 COMPLIANT: Focused data models under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .performance_enums import AlertSeverity, AlertStatus, DashboardType, MetricType


@dataclass
class DashboardMetric:
    """Represents a metric for dashboard display."""

    name: str
    value: int | float | str | bool
    unit: str
    metric_type: MetricType
    timestamp: datetime
    category: str
    priority: str = "medium"
    trend: str | None = None  # "up", "down", "stable"
    baseline: int | float | None = None
    threshold_warning: int | float | None = None
    threshold_critical: int | float | None = None


@dataclass
class DashboardWidget:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.performance.models.performance_models import Performance_Models

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Performance_Models(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

    """Represents a dashboard widget."""

    id: str
    title: str
    widget_type: str  # "chart", "gauge", "table", "alert"
    metrics: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)
    position: dict[str, int] = field(default_factory=dict)
    size: dict[str, int] = field(default_factory=dict)


@dataclass
class ConsolidationPhase:
    """Represents a consolidation phase with metrics."""

    name: str
    start_time: datetime
    end_time: datetime | None = None
    status: str = "pending"  # "pending", "active", "completed", "failed"
    metrics: dict[str, Any] = field(default_factory=dict)
    alerts: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Alert:
    """Represents a performance alert."""

    id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    source: str
    metric_name: str
    threshold: int | float
    current_value: int | float
    timestamp: datetime
    acknowledged_by: str | None = None
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None


@dataclass
class PerformanceReport:
    """Represents a performance report."""

    report_id: str
    title: str
    period_start: datetime
    period_end: datetime
    metrics: list[DashboardMetric] = field(default_factory=list)
    alerts: list[Alert] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)


# Export all models for easy import
__all__ = [
    "DashboardMetric",
    "DashboardWidget",
    "ConsolidationPhase",
    "Alert",
    "PerformanceReport",
]
