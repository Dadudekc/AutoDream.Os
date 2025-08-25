import time

from src.core.health.monitoring_new.health_monitoring_new_core import (
    HealthMonitoringOrchestrator,
)
from src.core.health.monitoring.health_monitoring_metrics import (
    HealthMetricType,
    HealthStatus,
)


def test_orchestrator_creates_alert_and_updates_status():
    orchestrator = HealthMonitoringOrchestrator({"health_check_interval": 0.1})
    orchestrator.start()
    orchestrator.record_health_metric(
        "agent1", HealthMetricType.RESPONSE_TIME, 6000.0, "ms"
    )
    time.sleep(0.2)
    orchestrator.stop()

    alerts = orchestrator.get_health_alerts()
    assert alerts
    snapshot = orchestrator.get_agent_health("agent1")
    assert snapshot is not None
    assert snapshot.overall_status == HealthStatus.CRITICAL
