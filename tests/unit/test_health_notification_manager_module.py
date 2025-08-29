from src.core.health.alerting.models import AlertSeverity
from src.core.health.monitoring.health_metrics_collector import (
from src.core.health.monitoring.health_monitoring_config import (
from src.core.health.monitoring.health_monitoring_metrics import HealthMetricType
from src.core.health.monitoring.health_notification_manager import (

    HealthNotificationManager,
)
    HealthMetricsCollector,
)
    initialize_default_thresholds,
)


def test_create_and_resolve_alert():
    health_data = {}
    collector = HealthMetricsCollector(health_data)
    thresholds = initialize_default_thresholds()
    notifier = HealthNotificationManager()

    collector.record_metric("agent1", HealthMetricType.RESPONSE_TIME, 6000.0, "ms")
    metric = health_data["agent1"].metrics[HealthMetricType.RESPONSE_TIME]
    threshold = thresholds[HealthMetricType.RESPONSE_TIME]
    alert = notifier.create_alert("agent1", AlertSeverity.WARNING, metric, threshold)

    assert alert in notifier.get_alerts()

    notifier.acknowledge(alert.alert_id)
    assert notifier.alerts[alert.alert_id].acknowledged

    notifier.resolve(alert.alert_id)
    assert notifier.alerts[alert.alert_id].resolved

    # After lowering metric value, check_alerts should keep alert resolved
    collector.record_metric("agent1", HealthMetricType.RESPONSE_TIME, 100.0, "ms")
    notifier.check_alerts(health_data)
    assert notifier.alerts[alert.alert_id].resolved
