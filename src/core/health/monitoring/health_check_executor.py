import logging
from typing import Dict

from ..alerting.models import AlertSeverity
from .health_monitoring_config import HealthThreshold
from .health_monitoring_metrics import HealthMetric, HealthMetricType, HealthSnapshot
from .health_notification_manager import HealthNotificationManager

logger = logging.getLogger(__name__)


class HealthCheckExecutor:
    """Evaluates collected metrics against configured thresholds."""

    def __init__(
        self,
        notification_manager: HealthNotificationManager,
        thresholds: Dict[HealthMetricType, HealthThreshold],
    ) -> None:
        self.notification_manager = notification_manager
        self.thresholds = thresholds

    def execute(self, health_data: Dict[str, HealthSnapshot]) -> None:
        """Run health checks for all agents."""
        for agent_id, snapshot in health_data.items():
            for metric_type, metric in snapshot.metrics.items():
                if metric_type in self.thresholds:
                    threshold = self.thresholds[metric_type]
                    self._evaluate_metric(agent_id, metric, threshold)

    def _evaluate_metric(
        self, agent_id: str, metric: HealthMetric, threshold: HealthThreshold
    ) -> None:
        value = metric.value
        if value >= threshold.critical_threshold:
            self.notification_manager.create_alert(
                agent_id, AlertSeverity.CRITICAL, metric, threshold
            )
        elif value >= threshold.warning_threshold:
            self.notification_manager.create_alert(
                agent_id, AlertSeverity.WARNING, metric, threshold
            )
