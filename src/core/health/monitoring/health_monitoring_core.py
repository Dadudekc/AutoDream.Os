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
        )

        alert = HealthAlert(
            alert_id=alert_id,
            agent_id=agent_id,
            severity=severity,
            message=f"{metric.metric_type.value} threshold exceeded: {metric.value}{metric.unit} >= {threshold.critical_threshold if severity == AlertSeverity.CRITICAL else threshold.warning_threshold}{threshold.unit}",
            metric_type=metric.metric_type,
            current_value=metric.value,
            threshold=threshold.critical_threshold
            if severity == AlertSeverity.CRITICAL
            else threshold.warning_threshold,
            timestamp=datetime.now(),
        )

        with self._lock:
            self.alerts[alert_id] = alert
        logger.warning(f"Health alert created: {alert.message}")

    def _update_agent_health_status(self, agent_id: str):
        """Update overall health status for an agent"""
        with self._lock:
            if agent_id not in self.health_data:
                return

            snapshot = self.health_data[agent_id]
            active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]

            # Determine overall status based on alerts
            if any(alert.severity == AlertSeverity.CRITICAL for alert in active_alerts):
                snapshot.overall_status = HealthStatus.CRITICAL
            elif any(alert.severity == AlertSeverity.WARNING for alert in active_alerts):
                snapshot.overall_status = HealthStatus.WARNING
            elif snapshot.health_score >= 90:
                snapshot.overall_status = HealthStatus.EXCELLENT
            elif snapshot.health_score >= 75:
                snapshot.overall_status = HealthStatus.GOOD
            else:
                snapshot.overall_status = HealthStatus.WARNING

    def _update_health_scores(self):
        """Update health scores for all agents"""
        with self._lock:
            for agent_id, snapshot in self.health_data.items():
                try:
                    # Calculate health score based on metrics and alerts
                    score = self._calculate_health_score(snapshot)
                    snapshot.health_score = score

                    # Generate recommendations
                    recommendations = self._generate_health_recommendations(snapshot)
                    snapshot.recommendations = recommendations

                except Exception as e:
                    logger.error(f"Error updating health score for agent {agent_id}: {e}")

    def _calculate_health_score(self, snapshot: HealthSnapshot) -> float:
        """Calculate health score (0-100) for an agent"""
        if not snapshot.metrics:
            return 100.0  # No metrics available

        total_score = 0
        metric_count = 0

        for metric_type, metric in snapshot.metrics.items():
            if metric_type in self.thresholds:
                threshold = self.thresholds[metric_type]

                # Calculate metric score based on threshold proximity
                if metric.value <= threshold.warning_threshold:
                    score = 100.0  # Excellent
                elif metric.value <= threshold.critical_threshold:
                    # Linear interpolation between warning and critical
                    ratio = (metric.value - threshold.warning_threshold) / (
                        threshold.critical_threshold - threshold.warning_threshold
                    )
                    score = 100.0 - (ratio * 25.0)  # 100 to 75
                else:
                    score = max(
                        0.0,
                        75.0
                        - (
                            (metric.value - threshold.critical_threshold)
                            / threshold.critical_threshold
                        )
                        * 75.0,
                    )

                total_score += score
                metric_count += 1

        if metric_count == 0:
            return 100.0

        # Penalize for active alerts
        active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]
        alert_penalty = 0

        for alert in active_alerts:
            if alert.severity == AlertSeverity.CRITICAL:
                alert_penalty += 20
            elif alert.severity == AlertSeverity.WARNING:
                alert_penalty += 10

        final_score = (total_score / metric_count) - alert_penalty
        return max(0.0, min(100.0, final_score))

    def _generate_health_recommendations(self, snapshot: HealthSnapshot) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []

        # Check for specific issues and provide recommendations
        for metric_type, metric in snapshot.metrics.items():
            if metric_type == HealthMetricType.RESPONSE_TIME and metric.value > 1000:
                recommendations.append(
                    "Consider optimizing response time by reviewing processing logic"
                )

            elif metric_type == HealthMetricType.MEMORY_USAGE and metric.value > 80:
                recommendations.append(
                    "High memory usage detected - consider memory optimization or cleanup"
                )

            elif metric_type == HealthMetricType.CPU_USAGE and metric.value > 85:
                recommendations.append(
                    "High CPU usage detected - consider load balancing or optimization"
                )

            elif metric_type == HealthMetricType.ERROR_RATE and metric.value > 5:
                recommendations.append(
                    "High error rate detected - review error handling and logging"
                )

        # Add general recommendations based on overall status
        if snapshot.overall_status == HealthStatus.CRITICAL:
            recommendations.append("CRITICAL: Immediate intervention required")
        elif snapshot.overall_status == HealthStatus.WARNING:
            recommendations.append(
                "WARNING: Monitor closely and address issues promptly"
            )

        return recommendations

    def _check_alerts(self):
        """Check and manage health alerts"""
        current_time = datetime.now()

        with self._lock:
            # Check for expired alerts
            expired_alerts = []
            for alert_id, alert in self.alerts.items():
                # Mark alerts as resolved if conditions improve
                if self._is_alert_resolved(alert):
                    alert.resolved = True
                    logger.info(f"Alert {alert_id} automatically resolved")

                # Remove very old alerts
                if (current_time - alert.timestamp).days > 7:
                    expired_alerts.append(alert_id)

            # Remove expired alerts
            for alert_id in expired_alerts:
                del self.alerts[alert_id]

    def _is_alert_resolved(self, alert: HealthAlert) -> bool:
        """Check if an alert should be automatically resolved"""
        if alert.resolved:
            return True

        with self._lock:
            # Check if the current metric value is below threshold
            if alert.agent_id in self.health_data:
                snapshot = self.health_data[alert.agent_id]
                if alert.metric_type in snapshot.metrics:
                    current_value = snapshot.metrics[alert.metric_type].value
                    return current_value < alert.threshold

        return False

    def _notify_health_updates(self):
        """Notify subscribers of health updates"""
        with self._lock:
            callbacks = list(self.health_callbacks)
            health_data = self.health_data.copy()
            alerts = self.alerts.copy()

        for callback in callbacks:
            try:
                callback(health_data, alerts)
            except Exception as e:
                logger.error(f"Error in health update callback: {e}")

=======
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
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules
    def record_health_metric(
        self,
        agent_id: str,
        metric_type: HealthMetricType,
        value: float,
        unit: str,
        threshold: Optional[float] = None,
<<<<<<< HEAD
    ):
        """Record a health metric for an agent"""
        try:
            with self._lock:
                # Create or update health snapshot
                if agent_id not in self.health_data:
                    self.health_data[agent_id] = HealthSnapshot(
                        agent_id=agent_id,
                        timestamp=datetime.now(),
                        overall_status=HealthStatus.GOOD,
                        health_score=100.0,
                    )

                snapshot = self.health_data[agent_id]

                # Create metric
                metric = HealthMetric(
                    agent_id=agent_id,
                    metric_type=metric_type,
                    value=value,
                    unit=unit,
                    timestamp=datetime.now(),
                    threshold=threshold,
                )

                # Update snapshot
                snapshot.metrics[metric_type] = metric
                snapshot.timestamp = datetime.now()

            logger.debug(
                f"Health metric recorded: {agent_id} - {metric_type.value}: {value}{unit}"
            )

        except Exception as e:
            logger.error(f"Error recording health metric: {e}")

    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Get health snapshot for a specific agent"""
        with self._lock:
            return self.health_data.get(agent_id)

    def get_all_agent_health(self) -> Dict[str, HealthSnapshot]:
        """Get health snapshots for all agents"""
        with self._lock:
            return self.health_data.copy()

    def get_health_alerts(
        self, severity: Optional[AlertSeverity] = None, agent_id: Optional[str] = None
    ) -> List[HealthAlert]:
        """Get health alerts with optional filtering"""
        with self._lock:
            alerts = list(self.alerts.values())
=======
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
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules

    def acknowledge_alert(self, alert_id: str) -> None:
        self.notification_manager.acknowledge(alert_id)

    def resolve_alert(self, alert_id: str) -> None:
        self.notification_manager.resolve(alert_id)

    def subscribe_to_health_updates(self, callback) -> None:
        self.notification_manager.subscribe(callback)

<<<<<<< HEAD
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].acknowledged = True
                logger.info(f"Alert {alert_id} acknowledged")

    def resolve_alert(self, alert_id: str):
        """Manually resolve a health alert"""
        with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].resolved = True
                logger.info(f"Alert {alert_id} manually resolved")

    def subscribe_to_health_updates(self, callback: Callable):
        """Subscribe to health update notifications"""
        with self._lock:
            self.health_callbacks.add(callback)

    def unsubscribe_from_health_updates(self, callback: Callable):
        """Unsubscribe from health update notifications"""
        with self._lock:
            self.health_callbacks.discard(callback)
=======
    def unsubscribe_from_health_updates(self, callback) -> None:
        self.notification_manager.unsubscribe(callback)
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules

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
<<<<<<< HEAD
        """Get comprehensive health summary"""
        with self._lock:
            total_agents = len(self.health_data)
            active_alerts = len(
                [alert for alert in self.alerts.values() if not alert.resolved]
            )

            status_counts = {
                status.value: len(
                    [s for s in self.health_data.values() if s.overall_status == status]
                )
                for status in HealthStatus
            }

            avg_health_score = sum(
                s.health_score for s in self.health_data.values()
            ) / max(total_agents, 1)

=======
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
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules
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
<<<<<<< HEAD
            with self._lock:
                assert "test_agent" in self.health_data
            logger.info("Metric recording passed")

            # Test health snapshot retrieval
            logger.info("Testing health snapshot retrieval...")
            health = self.get_agent_health("test_agent")
            assert health is not None
            assert health.agent_id == "test_agent"
            logger.info("Health snapshot retrieval passed")

            # Test alert creation
            logger.info("Testing alert creation...")
            # Start monitoring with shorter intervals for testing
            self.health_check_interval = 1
            self.alert_check_interval = 1
            self.metrics_interval = 1
=======
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules
            self.start()
            time.sleep(1)
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 6000.0, "ms"
            )
            time.sleep(1)
            alerts = self.get_health_alerts()
            self.stop()
<<<<<<< HEAD

            # Test health summary
            logger.info("Testing health summary...")
            summary = self.get_health_summary()
            assert "total_agents" in summary
            assert "active_alerts" in summary
            logger.info("Health summary passed")

            # Cleanup
            logger.info("Cleaning up...")
            with self._lock:
                if "test_agent" in self.health_data:
                    del self.health_data["test_agent"]

            logger.info("✅ AgentHealthCoreMonitor smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ AgentHealthCoreMonitor smoke test FAILED: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
=======
            return bool(alerts)
        except Exception as exc:  # pragma: no cover
            logger.error("Smoke test failed: %s", exc)
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules
            return False

    def shutdown(self) -> None:
        self.stop()


<<<<<<< HEAD
def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Health Core Monitor CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        monitor = AgentHealthCoreMonitor()
        success = monitor.run_smoke_test()
        monitor.shutdown()
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
=======
__all__ = ["HealthMonitoringOrchestrator"]
>>>>>>> origin/codex/refactor-health-check-and-metrics-modules
