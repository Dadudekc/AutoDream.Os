"""Scaling forecasting utilities."""

import logging
from typing import Any, Dict, List

from .patterns import analyze_scaling_patterns

logger = logging.getLogger(__name__)


def predict_scaling_needs(
    manager: Any, time_horizon_minutes: int = 30
) -> List[Dict[str, Any]]:
    """Predict potential scaling needs based on current patterns."""
    try:
        predictions: List[Dict[str, Any]] = []
        pattern_analysis = analyze_scaling_patterns(manager, time_horizon_minutes / 60)

        for metric, data in pattern_analysis.get("performance_trends", {}).items():
            if (
                data["trend"] == "increasing"
                and data["average"] > manager.thresholds.get(metric, 100) * 0.8
            ):
                predictions.append(
                    {
                        "metric_name": metric,
                        "issue_type": "performance_pressure",
                        "probability": 0.8,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.6,
                        "severity": "high"
                        if data["average"] > manager.thresholds.get(metric, 100) * 0.9
                        else "medium",
                        "recommended_action": f"Scale up {metric} capacity",
                    }
                )
            if (
                metric in ["cpu_utilization", "memory_utilization"]
                and data["average"] > 85
            ):
                predictions.append(
                    {
                        "metric_name": metric,
                        "issue_type": "resource_exhaustion",
                        "probability": 0.9,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.3,
                        "severity": "critical",
                        "recommended_action": f"Immediate scaling required for {metric}",
                    }
                )

        if pattern_analysis.get("scaling_efficiency", 1.0) < 0.7:
            predictions.append(
                {
                    "metric_name": "scaling_efficiency",
                    "issue_type": "scaling_inefficiency",
                    "probability": 0.7,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.8,
                    "severity": "medium",
                    "recommended_action": "Review and optimize scaling algorithms",
                }
            )

        logger.info(
            "Scaling needs prediction completed: %s predictions identified", len(predictions)
        )
        return predictions
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to predict scaling needs: %s", exc)
        return []
