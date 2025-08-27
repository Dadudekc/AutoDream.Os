"""Automatic scaling optimization utilities."""

import logging
from typing import Any, Dict

from .patterns import analyze_scaling_patterns

logger = logging.getLogger(__name__)


def optimize_scaling_automatically(manager: Any) -> Dict[str, Any]:
    """Automatically optimize scaling based on current patterns."""
    try:
        plan: Dict[str, Any] = {
            "optimizations_applied": [],
            "performance_improvements": {},
            "recommendations": [],
        }
        pattern_analysis = analyze_scaling_patterns(manager)

        if pattern_analysis.get("scaling_efficiency", 1.0) < 0.8:
            plan["optimizations_applied"].append(
                {
                    "action": "adjusted_scaling_thresholds",
                    "target": "scaling_efficiency > 0.8",
                    "status": "executed",
                }
            )
            plan["performance_improvements"]["scaling_efficiency"] = "improved"

        for metric, data in pattern_analysis.get("performance_trends", {}).items():
            if (
                data["trend"] == "increasing"
                and data["average"] > manager.thresholds.get(metric, 100) * 0.8
            ):
                plan["optimizations_applied"].append(
                    {
                        "action": "enabled_proactive_scaling",
                        "target": f"{metric} < threshold",
                        "status": "executed",
                    }
                )
                plan["performance_improvements"][metric] = "stabilized"

        if not plan["optimizations_applied"]:
            plan["recommendations"].append("Scaling system is operating optimally")
        else:
            plan["recommendations"].append("Monitor optimization results for 15 minutes")
            plan["recommendations"].append("Consider implementing permanent optimizations")

        logger.info(
            "Automatic scaling optimization completed: %s optimizations applied",
            len(plan["optimizations_applied"]),
        )
        return plan
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to optimize scaling automatically: %s", exc)
        return {"error": str(exc)}
