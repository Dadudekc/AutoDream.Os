from src.core.health.monitoring.health_status_analyzer import HealthStatusAnalyzer
from src.core.health.monitoring.health_metrics_collector import (
    HealthMetricsCollector,
)
from src.core.health.monitoring.health_monitoring_metrics import (
    HealthMetricType,
    HealthStatus,
)
from src.core.health.monitoring.health_notification_manager import (
    HealthNotificationManager,
)
from src.core.health.monitoring.health_monitoring_config import (
    initialize_default_thresholds,
)
from src.core.health.alerting.models import AlertSeverity


def test_analyzer_updates_scores_and_status():
    health_data = {}
    collector = HealthMetricsCollector(health_data)
    thresholds = initialize_default_thresholds()
    notifier = HealthNotificationManager()
    analyzer = HealthStatusAnalyzer()

    collector.record_metric("agent1", HealthMetricType.RESPONSE_TIME, 2000.0, "ms")

    analyzer.update_health_scores(health_data, thresholds, notifier.alerts)
    analyzer.update_agent_statuses(health_data, notifier.alerts)
    snapshot = health_data["agent1"]
    assert snapshot.health_score < 100
    assert snapshot.overall_status == HealthStatus.EXCELLENT

    metric = snapshot.metrics[HealthMetricType.RESPONSE_TIME]
    threshold = thresholds[HealthMetricType.RESPONSE_TIME]
    notifier.create_alert("agent1", AlertSeverity.CRITICAL, metric, threshold)
    analyzer.update_agent_statuses(health_data, notifier.alerts)
    assert snapshot.overall_status == HealthStatus.CRITICAL
