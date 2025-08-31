"""Workflow optimization analysis algorithms."""
from __future__ import annotations

from typing import Dict

from src.core.metrics import OptimizationRunMetrics


def analyze_metrics(metrics: OptimizationRunMetrics) -> Dict[str, float]:
    """Analyze collected metrics and compute derived values.

    Args:
        metrics: Metrics gathered from a workflow run.

    Returns:
        Dictionary with computed analysis such as success rate.
    """

    if metrics.tasks_processed == 0:
        success_rate = 0.0
    else:
        success_rate = (metrics.tasks_processed - metrics.errors) / metrics.tasks_processed

    return {
        "success_rate": success_rate,
        "tasks_processed": metrics.tasks_processed,
        "errors": metrics.errors,
        "duration": metrics.duration,
    }
