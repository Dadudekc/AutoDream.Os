"""Metric calculation utilities for health reports."""
from __future__ import annotations

from typing import Any, Dict, List


def average_health_score(reports: List[Dict[str, Any]]) -> float:
    """Compute the average health score from all reports."""
    scores = [r.get("system_health", {}).get("health_score") for r in reports]
    numeric_scores = [s for s in scores if isinstance(s, (int, float))]
    if not numeric_scores:
        return 0.0
    return sum(numeric_scores) / len(numeric_scores)


def status_counts(reports: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count occurrences of agent statuses across reports."""
    counts: Dict[str, int] = {}
    for report in reports:
        agent_status = report.get("agent_status", {})
        for status in agent_status.values():
            state = status.get("status", "unknown")
            counts[state] = counts.get(state, 0) + 1
    return counts
