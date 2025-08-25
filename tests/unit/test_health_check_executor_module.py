from src.core.health.monitoring.health_check_executor import HealthCheckExecutor
from src.core.health.monitoring.health_metrics_collector import (
    HealthMetricsCollector,
)
from src.core.health.monitoring.health_monitoring_metrics import HealthMetricType
from src.core.health.monitoring.health_notification_manager import (
    HealthNotificationManager,
)
from src.core.health.monitoring.health_monitoring_config import (
    initialize_default_thresholds,
)


def test_execute_triggers_alert():
    health_data = {}
    collector = HealthMetricsCollector(health_data)
    thresholds = initialize_default_thresholds()
    notifier = HealthNotificationManager()
    executor = HealthCheckExecutor(notifier, thresholds)

    collector.record_metric(
        agent_id="agent1",
        metric_type=HealthMetricType.RESPONSE_TIME,
        value=6000.0,
        unit="ms",
    )

    executor.execute(health_data)

    alerts = notifier.get_alerts()
    assert len(alerts) == 1
    assert alerts[0].agent_id == "agent1"
