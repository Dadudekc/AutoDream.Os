"""Dashboard types and data structures for performance monitoring."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DashboardType(Enum):
    """Types of monitoring dashboards."""
    OPERATIONAL = "operational"
    CONSOLIDATION = "consolidation"
    PERFORMANCE = "performance"
    SLA_COMPLIANCE = "sla_compliance"
    ALERT_MANAGEMENT = "alert_management"


class MetricType(Enum):
    """Types of performance metrics."""
    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


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