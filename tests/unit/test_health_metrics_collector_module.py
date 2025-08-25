from src.core.health.monitoring.health_metrics_collector import (
    HealthMetricsCollector,
)
from src.core.health.monitoring.health_monitoring_metrics import (
    HealthMetricType,
    HealthStatus,
)


def test_record_metric_and_retrieve():
    health_data = {}
    collector = HealthMetricsCollector(health_data)

    collector.record_metric(
        agent_id="agent1",
        metric_type=HealthMetricType.RESPONSE_TIME,
        value=100.0,
        unit="ms",
    )

    snapshot = collector.get_agent_health("agent1")
    assert snapshot is not None
    assert snapshot.metrics[HealthMetricType.RESPONSE_TIME].value == 100.0
    assert snapshot.overall_status == HealthStatus.GOOD

    all_data = collector.get_all_health()
    assert "agent1" in all_data
