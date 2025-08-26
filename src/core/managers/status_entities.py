from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from .status_types import (
    StatusLevel,
    HealthStatus,
    StatusEventType,
)


@dataclass
class StatusItem:
    """Status item with metadata."""

    id: str
    component: str
    status: str
    level: StatusLevel
    message: str
    timestamp: str
    duration: Optional[float]
    metadata: Dict[str, Any]
    resolved: bool
    resolution_time: Optional[str]


@dataclass
class HealthMetric:
    """Health metric data."""

    name: str
    value: float
    unit: str
    threshold_min: Optional[float]
    threshold_max: Optional[float]
    status: HealthStatus
    timestamp: str
    trend: str  # increasing, decreasing, stable


@dataclass
class ComponentHealth:
    """Component health information."""

    component_id: str
    name: str
    status: HealthStatus
    last_check: str
    uptime: float
    response_time: float
    error_count: int
    success_rate: float
    metrics: List[HealthMetric]
    dependencies: List[str]


@dataclass
class StatusEvent:
    """Status event information."""

    event_id: str
    component_id: str
    event_type: StatusEventType
    old_status: Optional[str]
    new_status: Optional[str]
    message: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class StatusMetrics:
    """Status metrics summary."""

    total_components: int
    healthy_components: int
    warning_components: int
    error_components: int
    critical_components: int
    last_update: str
    uptime_seconds: float


@dataclass
class ActivitySummary:
    """Activity summary information."""

    period: str
    total_events: int
    status_changes: int
    health_alerts: int
    performance_events: int
    error_events: int


__all__ = [
    "StatusItem",
    "HealthMetric",
    "ComponentHealth",
    "StatusEvent",
    "StatusMetrics",
    "ActivitySummary",
]
