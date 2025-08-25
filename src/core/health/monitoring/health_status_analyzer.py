import logging
from typing import Dict, List

from ..alerting.models import AlertSeverity
from .health_monitoring_metrics import (
    HealthMetricType,
    HealthSnapshot,
    HealthStatus,
)

logger = logging.getLogger(__name__)


class HealthStatusAnalyzer:
    """Derives health scores and status recommendations."""

    def update_agent_statuses(
        self, health_data: Dict[str, HealthSnapshot], alerts: Dict[str, any]
    ) -> None:
        for agent_id, snapshot in health_data.items():
            agent_alerts = [
                a for a in alerts.values() if a.agent_id == agent_id and not a.resolved
            ]
            if any(a.severity == AlertSeverity.CRITICAL for a in agent_alerts):
                snapshot.overall_status = HealthStatus.CRITICAL
            elif any(a.severity == AlertSeverity.WARNING for a in agent_alerts):
                snapshot.overall_status = HealthStatus.WARNING
            elif snapshot.health_score >= 90:
                snapshot.overall_status = HealthStatus.EXCELLENT
            elif snapshot.health_score >= 75:
                snapshot.overall_status = HealthStatus.GOOD
            else:
                snapshot.overall_status = HealthStatus.WARNING

    def update_health_scores(
        self,
        health_data: Dict[str, HealthSnapshot],
        thresholds,
        alerts: Dict[str, any],
    ) -> None:
        for agent_id, snapshot in health_data.items():
            score = self._calculate_score(snapshot, thresholds)
            snapshot.health_score = score
            snapshot.recommendations = self._generate_recommendations(snapshot)

    def _calculate_score(self, snapshot: HealthSnapshot, thresholds) -> float:
        if not snapshot.metrics:
            return 100.0
        total = 0.0
        count = 0
        for metric_type, metric in snapshot.metrics.items():
            if metric_type in thresholds:
                threshold = thresholds[metric_type]
                if metric.value <= threshold.warning_threshold:
                    score = 100.0
                elif metric.value <= threshold.critical_threshold:
                    ratio = (metric.value - threshold.warning_threshold) / (
                        threshold.critical_threshold - threshold.warning_threshold
                    )
                    score = 100.0 - ratio * 25.0
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
                total += score
                count += 1
        return max(0.0, min(100.0, total / max(count, 1)))

    def _generate_recommendations(self, snapshot: HealthSnapshot) -> List[str]:
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
            recommendations.append(
                "WARNING: Monitor closely and address issues promptly"
            )
        return recommendations
