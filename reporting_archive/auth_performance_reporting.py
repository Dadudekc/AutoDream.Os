"""Reporting utilities for the authentication performance monitor."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List
import time

from .auth_performance_metrics import PerformanceMetric, PerformanceAlert


@dataclass
class PerformanceReport:
    """Performance report data structure."""

    report_id: str
    timestamp: datetime
    time_period: str
    summary: Dict[str, Any]
    detailed_metrics: List[PerformanceMetric]
    alerts: List[PerformanceAlert]
    recommendations: List[str]


def generate_recommendations(summary: Dict[str, Any]) -> List[str]:
    """Generate performance optimization recommendations."""
    recommendations: List[str] = []
    try:
        if "current_success_rate" in summary.get("performance_indicators", {}):
            success_rate = summary["performance_indicators"]["current_success_rate"]
            if success_rate < 0.95:
                recommendations.append(
                    "Investigate authentication failures to improve success rate"
                )
        if "current_auth_duration" in summary.get("performance_indicators", {}):
            auth_duration = summary["performance_indicators"]["current_auth_duration"]
            if auth_duration > 0.5:
                recommendations.append(
                    "Optimize authentication process to reduce response time"
                )
        if len(summary.get("recent_alerts", [])) > 3:
            recommendations.append(
                "Review system configuration to reduce alert frequency"
            )
        system_health = summary.get("performance_indicators", {}).get(
            "system_health", "unknown"
        )
        if system_health in ["fair", "poor"]:
            recommendations.append("Perform system health assessment and optimization")
        if not recommendations:
            recommendations.append("System performance is within acceptable parameters")
            recommendations.append("Continue monitoring for performance trends")
    except Exception as e:
        recommendations.append(f"Unable to generate recommendations: {str(e)}")
    return recommendations


def generate_performance_report(
    monitor, time_period: str = "current"
) -> PerformanceReport:
    """Generate comprehensive performance report."""
    try:
        report_id = f"perf_report_{int(time.time())}"
        timestamp = datetime.now()
        summary = monitor.get_performance_summary()
        detailed_metrics: List[PerformanceMetric] = []
        for metric_name, metrics in monitor.metrics_history.items():
            if metrics:
                detailed_metrics.extend(list(metrics)[-10:])
        alerts = list(monitor.alerts_history)[-20:]
        recommendations = generate_recommendations(summary)
        return PerformanceReport(
            report_id=report_id,
            timestamp=timestamp,
            time_period=time_period,
            summary=summary,
            detailed_metrics=detailed_metrics,
            alerts=alerts,
            recommendations=recommendations,
        )
    except Exception as e:
        monitor.logger.error(f"Failed to generate performance report: {e}")
        return PerformanceReport(
            report_id=f"error_report_{int(time.time())}",
            timestamp=datetime.now(),
            time_period=time_period,
            summary={"error": str(e)},
            detailed_metrics=[],
            alerts=[],
            recommendations=["Investigate system errors"],
        )


__all__ = ["PerformanceReport", "generate_performance_report"]
