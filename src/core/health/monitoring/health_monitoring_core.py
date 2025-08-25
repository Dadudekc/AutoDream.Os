import logging
import threading
import time
from datetime import datetime
from typing import Any, Dict, Optional

from ..alerting.models import AlertSeverity
from .health_monitoring_config import (
    HealthThreshold,
    initialize_default_thresholds,
)
from .health_monitoring_metrics import HealthMetricType, HealthSnapshot, HealthStatus
from .health_check_executor import HealthCheckExecutor
from .health_metrics_collector import HealthMetricsCollector
from .health_notification_manager import HealthNotificationManager
from .health_status_analyzer import HealthStatusAnalyzer

logger = logging.getLogger(__name__)


class HealthMonitoringOrchestrator:
    """Coordinates health monitoring activities."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.monitoring_active = False
        self.health_data: Dict[str, HealthSnapshot] = {}
        self.thresholds: Dict[
            HealthMetricType, HealthThreshold
        ] = initialize_default_thresholds()

        self.notification_manager = HealthNotificationManager()
        self.metrics_collector = HealthMetricsCollector(self.health_data)
        self.check_executor = HealthCheckExecutor(
            self.notification_manager, self.thresholds
        )
        self.status_analyzer = HealthStatusAnalyzer()

        self.health_check_interval = self.config.get("health_check_interval", 60)
        self.monitor_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._loop, daemon=True)
        self.monitor_thread.start()

    def stop(self) -> None:
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

    # Core loop -------------------------------------------------------------
    def _loop(self) -> None:
        while self.monitoring_active:
            try:
                self.metrics_collector.collect_metrics()
                self.check_executor.execute(self.health_data)
                self.notification_manager.check_alerts(self.health_data)
                self.status_analyzer.update_health_scores(
                    self.health_data, self.thresholds, self.notification_manager.alerts
                )
                self.status_analyzer.update_agent_statuses(
                    self.health_data, self.notification_manager.alerts
                )
                self.notification_manager.notify_health_updates(self.health_data)
                time.sleep(self.health_check_interval)
            except Exception as exc:  # pragma: no cover
                logger.error("Error in health monitoring loop: %s", exc)
                time.sleep(10)

    # Delegated operations --------------------------------------------------
    def record_health_metric(
        self,
        agent_id: str,
        metric_type: HealthMetricType,
        value: float,
        unit: str,
        threshold: Optional[float] = None,
    ) -> None:
        self.metrics_collector.record_metric(
            agent_id, metric_type, value, unit, threshold
        )

    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        return self.metrics_collector.get_agent_health(agent_id)

    def get_all_agent_health(self) -> Dict[str, HealthSnapshot]:
        return self.metrics_collector.get_all_health()

    def get_health_alerts(
        self, severity: Optional[AlertSeverity] = None, agent_id: Optional[str] = None
    ) -> list:
        return self.notification_manager.get_alerts(severity, agent_id)

    def acknowledge_alert(self, alert_id: str) -> None:
        self.notification_manager.acknowledge(alert_id)

    def resolve_alert(self, alert_id: str) -> None:
        self.notification_manager.resolve(alert_id)

    def subscribe_to_health_updates(self, callback) -> None:
        self.notification_manager.subscribe(callback)

    def unsubscribe_from_health_updates(self, callback) -> None:
        self.notification_manager.unsubscribe(callback)

    def set_health_threshold(
        self,
        metric_type: HealthMetricType,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ) -> None:
        threshold = HealthThreshold(
            metric_type=metric_type,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            unit=unit,
            description=description,
        )
        self.thresholds[metric_type] = threshold
        self.check_executor.thresholds = self.thresholds

    def get_health_summary(self) -> Dict[str, Any]:
        total_agents = len(self.health_data)
        active_alerts = len(
            [
                alert
                for alert in self.notification_manager.alerts.values()
                if not alert.resolved
            ]
        )
        status_counts = {
            status.value: len(
                [s for s in self.health_data.values() if s.overall_status == status]
            )
            for status in HealthStatus
        }
        avg_score = sum(s.health_score for s in self.health_data.values()) / max(
            total_agents, 1
        )
        return {
            "total_agents": total_agents,
            "active_alerts": active_alerts,
            "status_distribution": status_counts,
            "average_health_score": round(avg_score, 2),
            "monitoring_active": self.monitoring_active,
            "last_update": datetime.now().isoformat(),
        }

    # Convenience -----------------------------------------------------------
    def run_smoke_test(self) -> bool:
        try:
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 500.0, "ms"
            )
            self.start()
            time.sleep(1)
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 6000.0, "ms"
            )
            time.sleep(1)
            alerts = self.get_health_alerts()
            self.stop()
            return bool(alerts)
        except Exception as exc:  # pragma: no cover
            logger.error("Smoke test failed: %s", exc)
            return False

    def shutdown(self) -> None:
        self.stop()


__all__ = ["HealthMonitoringOrchestrator"]
