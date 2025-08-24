"""Health monitoring alert models."""

from dataclasses import dataclass
from datetime import datetime

from ..alerting.models import AlertSeverity
from .health_monitoring_metrics import HealthMetricType


@dataclass
class HealthAlert:
    """Health alert information."""

    alert_id: str
    agent_id: str
    severity: AlertSeverity
    message: str
    metric_type: HealthMetricType
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False

