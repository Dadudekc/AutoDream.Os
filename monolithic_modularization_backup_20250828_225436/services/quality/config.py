"""Shared configuration for quality monitoring modules."""

from __future__ import annotations

# Default configuration values for quality monitoring components
DEFAULT_CHECK_INTERVAL: float = 30.0
"""Default interval in seconds between quality checks."""

DEFAULT_ALERT_RULES = {
    "test_failure": {
        "threshold": 0,
        "severity": "high",
        "message": "Test failures detected",
    },
    "performance_degradation": {
        "threshold": 100.0,
        "severity": "medium",
        "message": "Performance degradation detected",
    },
    "low_coverage": {
        "threshold": 80.0,
        "severity": "medium",
        "message": "Test coverage below threshold",
    },
}
"""Default alert rules used by :class:`QualityAlertManager`."""

DEFAULT_HISTORY_WINDOW: int = 100
"""Number of quality data points retained for trend analysis."""

__all__ = [
    "DEFAULT_CHECK_INTERVAL",
    "DEFAULT_ALERT_RULES",
    "DEFAULT_HISTORY_WINDOW",
]
