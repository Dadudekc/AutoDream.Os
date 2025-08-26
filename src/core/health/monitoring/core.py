"""Unified Health Monitoring Core - Consolidated from monitoring/ and monitoring_new/"""

# Import unified monitoring functionality from consolidated core
from .health_core import (
    AgentHealthCoreMonitor,
    HealthMonitoringOrchestrator,
)

# Import monitoring functions from monitoring_new (preserved functionality)
from ..monitoring_new.health_monitoring_new_collector import (
    collect_health_metrics,
    record_health_metric,
)
from ..monitoring_new.health_monitoring_new_analyzer import (
    perform_health_checks,
    update_health_scores,
    check_alerts,
    notify_health_updates,
    get_agent_health,
    get_all_agent_health,
    get_health_alerts,
    acknowledge_alert,
    update_threshold,
    get_health_summary,
)
from ..monitoring_new.health_monitoring_new_config import (
    HealthStatus,
    HealthMetricType,
    HealthMetric,
    HealthSnapshot,
    HealthAlert,
    HealthThreshold,
    initialize_default_thresholds,
)

__all__ = [
    # Core monitoring functionality
    "AgentHealthCoreMonitor",
    "HealthMonitoringOrchestrator",
    
    # Monitoring functions
    "collect_health_metrics",
    "record_health_metric",
    "perform_health_checks",
    "update_health_scores",
    "check_alerts",
    "notify_health_updates",
    "get_agent_health",
    "get_all_agent_health",
    "get_health_alerts",
    "acknowledge_alert",
    "update_threshold",
    "get_health_summary",
    
    # Data models
    "HealthStatus",
    "HealthMetricType",
    "HealthMetric",
    "HealthSnapshot",
    "HealthAlert",
    "HealthThreshold",
    "initialize_default_thresholds",
]
