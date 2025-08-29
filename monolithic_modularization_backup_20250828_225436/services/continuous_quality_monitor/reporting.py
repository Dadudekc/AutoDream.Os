"""Reporting utilities for continuous quality monitoring."""
from __future__ import annotations

import json
import time
from dataclasses import asdict
from typing import Dict, List


def calculate_quality_grade(score: float) -> str:
    """Return quality grade for ``score``."""
    if score >= 95.0:
        return "A+"
    if score >= 90.0:
        return "A"
    if score >= 85.0:
        return "B+"
    if score >= 80.0:
        return "B"
    if score >= 75.0:
        return "C+"
    if score >= 70.0:
        return "C"
    return "D"


def generate_monitoring_recommendations(summary: Dict) -> List[str]:
    """Generate monitoring recommendations from ``summary``."""
    recommendations: List[str] = []
    if summary.get("average_quality_score", 0) < 80.0:
        recommendations.append(
            "Focus on improving overall code quality to meet enterprise standards"
        )
    if summary.get("alert_summary", {}).get("critical_alerts", 0) > 0:
        recommendations.append(
            "Address critical quality alerts immediately to prevent system degradation"
        )
    if summary.get("alert_summary", {}).get("high_alerts", 0) > 2:
        recommendations.append(
            "Implement quality improvement plan to reduce high-severity alerts"
        )
    if summary.get("monitoring_status") != "active":
        recommendations.append(
            "Enable continuous monitoring for proactive quality management"
        )
    if not recommendations:
        recommendations.append(
            "Quality monitoring system is performing well - maintain current standards"
        )
    return recommendations


def export_monitoring_report(
    output_path: str,
    config: Dict,
    quality_history: List[Dict],
    alert_history: List,
    trend_analysis: Dict,
    summary: Dict,
) -> Dict:
    """Export monitoring report to ``output_path`` and return it."""
    report = {
        "timestamp": time.time(),
        "system": "Continuous Quality Monitor System",
        "configuration": config,
        "quality_summary": summary,
        "quality_history": quality_history[-50:],
        "alert_history": [asdict(a) for a in alert_history[-20:]],
        "trend_analysis": {k: asdict(v) for k, v in trend_analysis.items()},
        "recommendations": generate_monitoring_recommendations(summary),
    }
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    return report
