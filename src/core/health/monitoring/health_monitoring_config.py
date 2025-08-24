"""Health monitoring configuration and thresholds."""

from dataclasses import dataclass
from typing import Dict

from .health_monitoring_metrics import HealthMetricType


@dataclass
class HealthThreshold:
    """Health threshold configuration."""

    metric_type: HealthMetricType
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


def initialize_default_thresholds() -> Dict[HealthMetricType, "HealthThreshold"]:
    """Return default health thresholds for metrics."""
    default_thresholds = [
        HealthThreshold(
            HealthMetricType.RESPONSE_TIME,
            warning_threshold=1000.0,
            critical_threshold=5000.0,
            unit="ms",
            description="Response time threshold",
        ),
        HealthThreshold(
            HealthMetricType.MEMORY_USAGE,
            warning_threshold=80.0,
            critical_threshold=95.0,
            unit="%",
            description="Memory usage threshold",
        ),
        HealthThreshold(
            HealthMetricType.CPU_USAGE,
            warning_threshold=85.0,
            critical_threshold=95.0,
            unit="%",
            description="CPU usage threshold",
        ),
        HealthThreshold(
            HealthMetricType.ERROR_RATE,
            warning_threshold=5.0,
            critical_threshold=15.0,
            unit="%",
            description="Error rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.TASK_COMPLETION_RATE,
            warning_threshold=90.0,
            critical_threshold=75.0,
            unit="%",
            description="Task completion rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.HEARTBEAT_FREQUENCY,
            warning_threshold=120.0,
            critical_threshold=300.0,
            unit="seconds",
            description="Heartbeat frequency threshold",
        ),
        HealthThreshold(
            HealthMetricType.CONTRACT_SUCCESS_RATE,
            warning_threshold=85.0,
            critical_threshold=70.0,
            unit="%",
            description="Contract success rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.COMMUNICATION_LATENCY,
            warning_threshold=500.0,
            critical_threshold=2000.0,
            unit="ms",
            description="Communication latency threshold",
        ),
    ]

    return {threshold.metric_type: threshold for threshold in default_thresholds}

