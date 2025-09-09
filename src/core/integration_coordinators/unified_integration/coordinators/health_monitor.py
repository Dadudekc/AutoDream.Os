"""
Health Monitor - V2 Compliant Module
===================================

Handles system health monitoring and recommendations.
Extracted from coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

from ..models import IntegrationConfig


class HealthMonitor:
    """Handles system health monitoring and recommendations.

    Manages health status tracking, recommendations, and system health analysis.
    """

    def __init__(self, config: IntegrationConfig):
        """Initialize health monitor."""
        self.config = config
        self.health_history: list[dict[str, Any]] = []
        self.alert_thresholds: dict[str, float] = {}
        self.monitoring_callbacks: list[Callable] = []

    def get_system_health(self, monitor, optimizer) -> dict[str, Any]:
        """Get overall system health."""
        health_status = monitor.get_health_status()
        performance_summary = monitor.get_performance_summary()

        return {
            "overall_health": health_status["health_score"],
            "status": self._get_health_status_text(health_status["health_score"]),
            "active_integrations": health_status["total_integrations"],
            "performance": performance_summary,
            "alerts": health_status["alerts"],
            "recommendations": self._get_health_recommendations(health_status),
        }

    def _get_health_status_text(self, health_score: float) -> str:
        """Get health status text based on score."""
        if health_score >= 90:
            return "excellent"
        elif health_score >= 70:
            return "good"
        elif health_score >= 50:
            return "fair"
        else:
            return "poor"

    def _get_health_recommendations(self, health_status: dict[str, Any]) -> list[str]:
        """Get health recommendations."""
        recommendations = []

        if health_status["health_score"] < 70:
            recommendations.append(
                "System health is below optimal. Review integration performance."
            )

        if health_status["alerts"]:
            recommendations.append(
                f"Active alerts detected: {len(health_status['alerts'])}. Review alert details."
            )

        if health_status["total_integrations"] == 0:
            recommendations.append(
                "No integrations registered. Consider adding integration handlers."
            )

        if not recommendations:
            recommendations.append("System health is good. Continue monitoring.")

        return recommendations

    def add_monitoring_callback(self, callback: Callable) -> None:
        """Add monitoring callback."""
        self.monitoring_callbacks.append(callback)

    def set_alert_threshold(self, metric: str, threshold: float) -> None:
        """Set alert threshold."""
        self.alert_thresholds[metric] = threshold

    def get_alert_thresholds(self) -> dict[str, float]:
        """Get alert thresholds."""
        return self.alert_thresholds.copy()

    def check_health_thresholds(self, metrics: dict[str, Any]) -> list[str]:
        """Check health thresholds and return alerts."""
        alerts = []

        for metric, threshold in self.alert_thresholds.items():
            if metric in metrics:
                value = metrics[metric]
                if value > threshold:
                    alerts.append(f"{metric} exceeded threshold: {value} > {threshold}")

        return alerts

    def record_health_status(self, health_data: dict[str, Any]) -> None:
        """Record health status."""
        self.health_history.append(
            {"timestamp": datetime.now().isoformat(), "health_data": health_data}
        )

        # Keep only last 1000 records
        if len(self.health_history) > 1000:
            self.health_history = self.health_history[-1000:]

    def get_health_trends(self, hours: int = 24) -> dict[str, Any]:
        """Get health trends over time."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        recent_history = [
            record
            for record in self.health_history
            if datetime.fromisoformat(record["timestamp"]).timestamp() >= cutoff_time
        ]

        if not recent_history:
            return {"trend": "no_data", "average_health": 0}

        health_scores = [
            record["health_data"].get("overall_health", 0) for record in recent_history
        ]

        average_health = sum(health_scores) / len(health_scores)

        # Determine trend
        if len(health_scores) >= 2:
            if health_scores[-1] > health_scores[0]:
                trend = "improving"
            elif health_scores[-1] < health_scores[0]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "trend": trend,
            "average_health": average_health,
            "data_points": len(recent_history),
            "time_range_hours": hours,
        }

    def get_monitor_status(self) -> dict[str, Any]:
        """Get health monitor status."""
        return {
            "health_history_count": len(self.health_history),
            "alert_thresholds_count": len(self.alert_thresholds),
            "monitoring_callbacks_count": len(self.monitoring_callbacks),
            "last_health_check": (
                self.health_history[-1]["timestamp"] if self.health_history else None
            ),
        }
