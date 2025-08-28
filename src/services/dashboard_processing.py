"""Processing module for dashboard metrics."""

from __future__ import annotations

from typing import Dict, List, Any

from .dashboard_utils import TIMESTAMP_KEY, iso_timestamp


def summarize_metrics(metrics: Dict[str, List[Dict[str, float]]]) -> Dict[str, Any]:
    """Return summary statistics for collected metrics."""
    total_metrics = sum(len(values) for values in metrics.values())
    return {
        "total_metrics": total_metrics,
        "metrics_tracked": len(metrics),
        TIMESTAMP_KEY: iso_timestamp(),
    }
