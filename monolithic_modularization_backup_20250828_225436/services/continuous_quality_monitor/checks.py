"""Quality validation and trend analysis helpers."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QualityTrend:
    """Represents trend information for a quality metric."""

    metric_name: str
    current_value: float
    previous_value: float
    trend_direction: str
    change_percentage: float
    trend_strength: str


def perform_quality_validation(
    quality_gates, directory_path: str, history: List[Dict]
) -> Dict:
    """Run quality gate validation and add metadata."""
    if not quality_gates:
        return {"status": "error", "message": "Quality gates not available"}
    try:
        result = quality_gates.validate_directory(directory_path)
        result["monitor_timestamp"] = time.time()
        result["monitor_cycle"] = len(history) + 1
        return result
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
            "monitor_timestamp": time.time(),
            "monitor_cycle": len(history) + 1,
        }


def analyze_quality_trends(
    history: List[Dict], config: Dict
) -> Dict[str, QualityTrend]:
    """Analyze recent quality score trends."""
    if len(history) < 2:
        return {}

    window_days = config["trend_analysis"]["history_window_days"]
    cutoff_time = time.time() - (window_days * 24 * 3600)
    recent = [h for h in history if h.get("monitor_timestamp", 0) > cutoff_time]
    if len(recent) < 2:
        return {}

    current_score = recent[-1].get("quality_score", 0)
    previous_score = recent[-2].get("quality_score", 0)
    change_percentage = (
        ((current_score - previous_score) / previous_score * 100)
        if previous_score > 0
        else 0
    )

    threshold = config["trend_analysis"]["trend_threshold"]
    if change_percentage > threshold:
        direction = "IMPROVING"
        strength = "STRONG" if abs(change_percentage) > 10 else "MODERATE"
    elif change_percentage < -threshold:
        direction = "DECLINING"
        strength = "STRONG" if abs(change_percentage) > 10 else "MODERATE"
    else:
        direction = "STABLE"
        strength = "WEAK"

    return {
        "quality_score": QualityTrend(
            metric_name="quality_score",
            current_value=current_score,
            previous_value=previous_score,
            trend_direction=direction,
            change_percentage=change_percentage,
            trend_strength=strength,
        )
    }
