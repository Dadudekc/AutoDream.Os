from enum import Enum


class StatusLevel(Enum):
    """Status levels for tracking."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SUCCESS = "success"


class HealthStatus(Enum):
    """Health status states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class UpdateFrequency(Enum):
    """Status update frequency levels."""

    REAL_TIME = "real_time"
    HIGH_FREQUENCY = "high_frequency"
    MEDIUM_FREQUENCY = "medium_frequency"
    LOW_FREQUENCY = "low_frequency"


class StatusEventType(Enum):
    """Status event types."""

    STATUS_CHANGE = "status_change"
    HEALTH_ALERT = "health_alert"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SYSTEM_ERROR = "system_error"
    RECOVERY = "recovery"


__all__ = [
    "StatusLevel",
    "HealthStatus",
    "UpdateFrequency",
    "StatusEventType",
]
