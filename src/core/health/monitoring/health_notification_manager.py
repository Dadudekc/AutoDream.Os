import logging
from datetime import datetime
from typing import Callable, Dict, List, Optional, Set

from ..alerting.models import AlertSeverity
from .health_monitoring_alerts import HealthAlert
from .health_monitoring_metrics import HealthMetric, HealthMetricType, HealthSnapshot

logger = logging.getLogger(__name__)


class HealthNotificationManager:
    """Manages health alerts and subscriber notifications."""

    def __init__(self) -> None:
        self.alerts: Dict[str, HealthAlert] = {}
        self.callbacks: Set[Callable] = set()

    def create_alert(
        self,
        agent_id: str,
        severity: AlertSeverity,
        metric: HealthMetric,
        threshold,
    ) -> HealthAlert:
        alert_id = f"health_alert_{agent_id}_{metric.metric_type.value}_{int(datetime.now().timestamp())}"
        alert = HealthAlert(
            alert_id=alert_id,
            agent_id=agent_id,
            severity=severity,
            message=(
                f"{metric.metric_type.value} threshold exceeded: {metric.value}{metric.unit} >= "
                f"{threshold.critical_threshold if severity == AlertSeverity.CRITICAL else threshold.warning_threshold}{threshold.unit}"
            ),
            metric_type=metric.metric_type,
            current_value=metric.value,
            threshold=threshold.critical_threshold
            if severity == AlertSeverity.CRITICAL
            else threshold.warning_threshold,
            timestamp=datetime.now(),
        )
        self.alerts[alert_id] = alert
        logger.warning("Health alert created: %s", alert.message)
        return alert

    def check_alerts(self, health_data: Dict[str, HealthSnapshot]) -> None:
        """Resolve and purge alerts based on latest metrics."""
        current_time = datetime.now()
        expired: List[str] = []
        for alert_id, alert in self.alerts.items():
            if self._is_alert_resolved(alert, health_data):
                alert.resolved = True
                logger.info("Alert %s automatically resolved", alert_id)
            if (current_time - alert.timestamp).days > 7:
                expired.append(alert_id)
        for alert_id in expired:
            del self.alerts[alert_id]

    def _is_alert_resolved(
        self, alert: HealthAlert, health_data: Dict[str, HealthSnapshot]
    ) -> bool:
        if alert.agent_id in health_data:
            snapshot = health_data[alert.agent_id]
            metric = snapshot.metrics.get(alert.metric_type)
            if metric:
                return metric.value < alert.threshold
        return False

    def notify_health_updates(self, health_data: Dict[str, HealthSnapshot]) -> None:
        for callback in list(self.callbacks):
            try:
                callback(health_data, self.alerts)
            except Exception as exc:  # pragma: no cover
                logger.error("Error in health update callback: %s", exc)

    def get_alerts(
        self, severity: Optional[AlertSeverity] = None, agent_id: Optional[str] = None
    ) -> List[HealthAlert]:
        alerts = list(self.alerts.values())
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if agent_id:
            alerts = [a for a in alerts if a.agent_id == agent_id]
        return alerts

    def acknowledge(self, alert_id: str) -> None:
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledged = True

    def resolve(self, alert_id: str) -> None:
        if alert_id in self.alerts:
            self.alerts[alert_id].resolved = True

    def subscribe(self, callback: Callable) -> None:
        self.callbacks.add(callback)

    def unsubscribe(self, callback: Callable) -> None:
        self.callbacks.discard(callback)
