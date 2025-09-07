"""Simple dashboard orchestration."""
from __future__ import annotations

from .aggregation import average_health_score, status_counts
from .visuals import plot_status_distribution
from .storage import load_reports, save_summary


def generate_dashboard() -> dict:
    """Load reports, aggregate metrics, render visualization, and persist results."""
    reports = load_reports()
    if not reports:
        return {}
    counts = status_counts(reports)
    avg_score = average_health_score(reports)
    chart_path = plot_status_distribution(counts)
    summary = {
        "average_health_score": avg_score,
        "chart_path": str(chart_path),
    }
    save_summary(summary)
    return summary

__all__ = [
    "generate_dashboard",
    "average_health_score",
    "status_counts",
    "plot_status_distribution",
    "load_reports",
    "save_summary",
]
