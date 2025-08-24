"""Health metric analysis and alert utilities."""

import logging
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional, Set

from .health_monitoring_new_config import (
    HealthAlert,
    HealthMetric,
    HealthMetricType,
    HealthSnapshot,
    HealthStatus,
    HealthThreshold,
)

logger = logging.getLogger(__name__)


def perform_health_checks(
    health_data: Dict[str, HealthSnapshot],
    thresholds: Dict[HealthMetricType, HealthThreshold],
    alerts: Dict[str, HealthAlert],
) -> None:
    """Perform comprehensive health checks."""
    for agent_id, snapshot in health_data.items():
        for metric_type, metric in snapshot.metrics.items():
            if metric_type in thresholds:
                evaluate_metric(agent_id, metric, thresholds[metric_type], alerts)
        update_agent_health_status(health_data, agent_id)


def evaluate_metric(
    agent_id: str,
    metric: HealthMetric,
    threshold: HealthThreshold,
    alerts: Dict[str, HealthAlert],
) -> None:
    """Evaluate a metric against its threshold and create alerts."""
    current_value = metric.value
    if current_value >= threshold.critical_threshold:
        create_alert(agent_id, "CRITICAL", metric, threshold, alerts)
    elif current_value >= threshold.warning_threshold:
        create_alert(agent_id, "WARNING", metric, threshold, alerts)


def create_alert(
    agent_id: str,
    severity: str,
    metric: HealthMetric,
    threshold: HealthThreshold,
    alerts: Dict[str, HealthAlert],
) -> None:
    alert_id = f"health_alert_{agent_id}_{metric.metric_type.value}_{int(time.time())}"
    alert = HealthAlert(
        alert_id=alert_id,
        agent_id=agent_id,
        severity=severity,
        message=(
            f"{metric.metric_type.value} threshold exceeded: {metric.value}{metric.unit} >= "
            f"{threshold.critical_threshold if severity == 'CRITICAL' else threshold.warning_threshold}{threshold.unit}"
        ),
        metric_type=metric.metric_type,
        current_value=metric.value,
        threshold=(
            threshold.critical_threshold if severity == "CRITICAL" else threshold.warning_threshold
        ),
        timestamp=datetime.now(),
    )
    alerts[alert_id] = alert
    logger.warning("Health alert created: %s", alert.message)


def update_agent_health_status(health_data: Dict[str, HealthSnapshot], agent_id: str) -> None:
    if agent_id not in health_data:
        return
    snapshot = health_data[agent_id]
    active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]
    if any(alert.severity == "CRITICAL" for alert in active_alerts):
        snapshot.overall_status = HealthStatus.CRITICAL
    elif any(alert.severity == "WARNING" for alert in active_alerts):
        snapshot.overall_status = HealthStatus.WARNING
    elif snapshot.health_score >= 90:
        snapshot.overall_status = HealthStatus.EXCELLENT
    elif snapshot.health_score >= 75:
        snapshot.overall_status = HealthStatus.GOOD
    else:
        snapshot.overall_status = HealthStatus.WARNING


def update_health_scores(
    health_data: Dict[str, HealthSnapshot],
    thresholds: Dict[HealthMetricType, HealthThreshold],
) -> None:
    for agent_id, snapshot in health_data.items():
        score = calculate_health_score(snapshot, thresholds)
        snapshot.health_score = score
        snapshot.recommendations = generate_health_recommendations(snapshot)


def calculate_health_score(
    snapshot: HealthSnapshot, thresholds: Dict[HealthMetricType, HealthThreshold]
) -> float:
    if not snapshot.metrics:
        return 100.0
    total_score = 0
    metric_count = 0
    for metric_type, metric in snapshot.metrics.items():
        if metric_type in thresholds:
            threshold = thresholds[metric_type]
            if metric.value <= threshold.warning_threshold:
                score = 100.0
            elif metric.value <= threshold.critical_threshold:
                ratio = (
                    metric.value - threshold.warning_threshold
                ) / (threshold.critical_threshold - threshold.warning_threshold)
                score = 100.0 - (ratio * 25.0)
            else:
                score = max(
                    0.0,
                    75.0
                    - ((metric.value - threshold.critical_threshold) / threshold.critical_threshold)
                    * 75.0,
                )
            total_score += score
            metric_count += 1
    active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]
    alert_penalty = sum(20 if a.severity == "CRITICAL" else 10 for a in active_alerts)
    final_score = (total_score / metric_count) - alert_penalty
    return max(0.0, min(100.0, final_score))


def generate_health_recommendations(snapshot: HealthSnapshot) -> List[str]:
    recommendations: List[str] = []
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
    if snapshot.overall_status == HealthStatus.CRITICAL:
        recommendations.append("CRITICAL: Immediate intervention required")
    elif snapshot.overall_status == HealthStatus.WARNING:
        recommendations.append("WARNING: Monitor closely and address issues promptly")
    return recommendations


def check_alerts(alerts: Dict[str, HealthAlert], health_data: Dict[str, HealthSnapshot]) -> None:
    current_time = datetime.now()
    expired: List[str] = []
    for alert_id, alert in alerts.items():
        if is_alert_resolved(alert, health_data):
            alert.resolved = True
            logger.info("Alert %s automatically resolved", alert_id)
        if (current_time - alert.timestamp).days > 7:
            expired.append(alert_id)
    for alert_id in expired:
        del alerts[alert_id]


def is_alert_resolved(alert: HealthAlert, health_data: Dict[str, HealthSnapshot]) -> bool:
    if alert.resolved:
        return True
    if alert.agent_id in health_data:
        snapshot = health_data[alert.agent_id]
        if alert.metric_type in snapshot.metrics:
            current_value = snapshot.metrics[alert.metric_type].value
            return current_value < alert.threshold
    return False


def notify_health_updates(
    callbacks: Set[Callable],
    health_data: Dict[str, HealthSnapshot],
    alerts: Dict[str, HealthAlert],
) -> None:
    for callback in callbacks:
        try:
            callback(health_data, alerts)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Error in health update callback: %s", exc)


def get_agent_health(
    health_data: Dict[str, HealthSnapshot], agent_id: str
) -> Optional[HealthSnapshot]:
    return health_data.get(agent_id)


def get_all_agent_health(health_data: Dict[str, HealthSnapshot]) -> Dict[str, HealthSnapshot]:
    return health_data.copy()


def get_health_alerts(
    alerts: Dict[str, HealthAlert],
    severity: Optional[str] = None,
    agent_id: Optional[str] = None,
) -> List[HealthAlert]:
    result = list(alerts.values())
    if severity:
        result = [a for a in result if a.severity == severity]
    if agent_id:
        result = [a for a in result if a.agent_id == agent_id]
    return result


def acknowledge_alert(alerts: Dict[str, HealthAlert], alert_id: str) -> None:
    if alert_id in alerts:
        alerts[alert_id].acknowledged = True


def update_threshold(
    thresholds: Dict[HealthMetricType, HealthThreshold], threshold: HealthThreshold
) -> None:
    thresholds[threshold.metric_type] = threshold


def get_health_summary(
    health_data: Dict[str, HealthSnapshot],
    alerts: Dict[str, HealthAlert],
    monitoring_active: bool,
) -> Dict[str, object]:
    total_agents = len(health_data)
    active_alerts = len([a for a in alerts.values() if not a.resolved])
    status_counts = {
        status.value: len(
            [s for s in health_data.values() if s.overall_status == status]
        )
        for status in HealthStatus
    }
    avg_health_score = sum(s.health_score for s in health_data.values()) / max(
        total_agents, 1
    )
    return {
        "total_agents": total_agents,
        "active_alerts": active_alerts,
        "status_distribution": status_counts,
        "average_health_score": round(avg_health_score, 2),
        "monitoring_active": monitoring_active,
        "last_update": datetime.now().isoformat(),
    }
