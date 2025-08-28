"""Report composition utilities."""

from typing import Any, Dict, List
from datetime import datetime


def create_report_summary(patterns: List[Dict[str, Any]], trends: List[Dict[str, Any]], correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create summary statistics for the report."""
    summary = {
        "total_patterns": len(patterns),
        "total_trends": len(trends),
        "total_correlations": len(correlations),
        "analysis_timestamp": datetime.now().isoformat(),
    }

    if patterns:
        summary["average_pattern_occurrences"] = sum(p.get("occurrences", 0) for p in patterns) / len(patterns)
    if trends:
        summary["trend_confidence"] = sum(t.get("trend_confidence", 0) for t in trends) / len(trends)
    if correlations:
        summary["average_correlation_strength"] = sum(c.get("correlation_strength", 0) for c in correlations) / len(correlations)

    return summary


def generate_recommendations(patterns: List[Dict[str, Any]], trends: List[Dict[str, Any]], correlations: List[Dict[str, Any]]) -> List[str]:
    """Generate actionable recommendations based on analytics."""
    recommendations: List[str] = []

    if any(p.get("occurrences", 0) >= 10 for p in patterns):
        recommendations.append("Investigate high-frequency error patterns")
    if any(t.get("trend_direction") == "increasing" for t in trends):
        recommendations.append("Address increasing error trends")
    if any(c.get("correlation_strength", 0) >= 0.8 for c in correlations):
        recommendations.append("Investigate strong error correlations")

    if not recommendations:
        recommendations.append("Monitor error patterns for emerging issues")

    return recommendations


def create_report_metadata(patterns: List[Dict[str, Any]], trends: List[Dict[str, Any]], correlations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create metadata for the report."""
    return {
        "pattern_count": len(patterns),
        "trend_count": len(trends),
        "correlation_count": len(correlations),
        "generation_timestamp": datetime.now().isoformat(),
    }
