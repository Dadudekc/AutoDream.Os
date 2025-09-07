"""Scaling pattern analysis utilities."""

import logging
import time
from typing import Any, Dict

logger = logging.getLogger(__name__)


def analyze_scaling_patterns(manager: Any, time_range_hours: int = 24) -> Dict[str, Any]:
    """Analyze scaling patterns using manager state."""
    try:
        recent_metrics = [
            m
            for m in manager.metrics_history
            if m.timestamp > time.time() - (time_range_hours * 3600)
        ]

        analysis: Dict[str, Any] = {
            "total_metrics": len(recent_metrics),
            "scaling_events": len(manager.decision_history),
            "performance_trends": {},
            "optimization_opportunities": [],
            "scaling_efficiency": 0.0,
        }

        if recent_metrics:
            metrics = [
                "cpu_utilization",
                "memory_utilization",
                "response_time",
                "error_rate",
            ]
            for metric in metrics:
                values = [getattr(m, metric) for m in recent_metrics]
                if not values:
                    continue
                analysis["performance_trends"][metric] = {
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "trend": "stable",
                }
                if len(values) > 10:
                    first = values[: len(values) // 2]
                    second = values[len(values) // 2 :]
                    first_avg = sum(first) / len(first)
                    second_avg = sum(second) / len(second)
                    if second_avg > first_avg * 1.1:
                        analysis["performance_trends"][metric]["trend"] = "increasing"
                    elif second_avg < first_avg * 0.9:
                        analysis["performance_trends"][metric]["trend"] = "decreasing"

            if manager.decision_history:
                successful = len(
                    [d for d in manager.decision_history if d.confidence > 0.7]
                )
                analysis["scaling_efficiency"] = successful / len(manager.decision_history)

            if analysis["scaling_efficiency"] < 0.8:
                analysis["optimization_opportunities"].append(
                    "Low scaling efficiency - review decision algorithms"
                )

            for metric, data in analysis["performance_trends"].items():
                if (
                    data["trend"] == "increasing"
                    and data["average"] > manager.thresholds.get(metric, 100)
                ):
                    analysis["optimization_opportunities"].append(
                        f"Performance degradation in {metric} - consider scaling up"
                    )

        logger.info("Scaling pattern analysis completed")
        return analysis
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to analyze scaling patterns: %s", exc)
        return {"error": str(exc)}
