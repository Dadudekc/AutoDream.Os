"""Workflow optimization package coordinating metrics, analysis and reporting."""
from __future__ import annotations

from src.core.metrics import gather_run_metrics as gather_metrics
from .analysis import analyze_metrics
from .reporting import generate_report


def run_workflow_optimization(tasks_processed: int, errors: int, duration: float) -> str:
    """Coordinate metrics gathering, analysis and reporting."""

    metrics = gather_metrics(tasks_processed, errors, duration)
    analysis = analyze_metrics(metrics)
    return generate_report(analysis)


__all__ = [
    "run_workflow_optimization",
    "gather_metrics",
    "analyze_metrics",
    "generate_report",
]
