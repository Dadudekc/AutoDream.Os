"""Alert management for continuous quality monitoring."""
from __future__ import annotations

import time
from typing import Callable, Dict, List

from services.quality.models import QualityAlert


def generate_alert_recommendations(severity: str, quality_score: float) -> List[str]:
    """Return recommendations based on alert ``severity``."""
    recommendations: List[str] = []
    if severity == "CRITICAL":
        recommendations.extend(
            [
                "Immediate code review required",
                "Consider code refactoring",
                "Implement quality improvement plan",
            ]
        )
    elif severity == "HIGH":
        recommendations.extend(
            [
                "Schedule code review",
                "Address quality violations",
                "Monitor quality trends",
            ]
        )
    elif severity == "MEDIUM":
        recommendations.extend(
            [
                "Review quality metrics",
                "Plan quality improvements",
                "Set quality targets",
            ]
        )
    elif severity == "LOW":
        recommendations.extend(
            [
                "Monitor quality trends",
                "Maintain current standards",
                "Plan incremental improvements",
            ]
        )
    return recommendations


def check_quality_alerts(
    validation_result: Dict,
    config: Dict,
    alert_history: List[QualityAlert],
    alert_callbacks: List[Callable[[QualityAlert], None]],
) -> None:
    """Check validation results and trigger quality alerts."""
    if validation_result.get("status") == "error":
        return

    quality_score = validation_result.get("quality_score", 0)
    thresholds = config["monitoring"]["alert_thresholds"]

    if quality_score <= thresholds["critical"]:
        severity = "CRITICAL"
    elif quality_score <= thresholds["high"]:
        severity = "HIGH"
    elif quality_score <= thresholds["medium"]:
        severity = "MEDIUM"
    elif quality_score <= thresholds["low"]:
        severity = "LOW"
    else:
        return

    alert = QualityAlert(
        alert_id=f"QUALITY-{int(time.time())}",
        severity=severity,
        message=f"Quality score {quality_score:.1f}% below {severity.lower()} threshold",
        file_path=validation_result.get("directory_path", "unknown"),
        quality_score=quality_score,
        threshold=thresholds.get(severity.lower(), 0),
        timestamp=time.time(),
        recommendations=generate_alert_recommendations(severity, quality_score),
    )

    alert_history.append(alert)
    for callback in alert_callbacks:
        try:
            callback(alert)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"❌ Alert callback error: {exc}")

    print(f"🚨 Quality Alert: {severity} - {alert.message}")
