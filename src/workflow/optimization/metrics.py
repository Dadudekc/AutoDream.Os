"""Workflow optimization metrics gathering utilities."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class OptimizationMetrics:
    """Simple container for optimization metrics."""

    timestamp: str
    tasks_processed: int
    errors: int
    duration: float


def gather_metrics(tasks_processed: int, errors: int, duration: float) -> OptimizationMetrics:
    """Gather metrics for a workflow optimization run.

    Args:
        tasks_processed: Number of tasks handled in the run.
        errors: Number of errors encountered.
        duration: Total processing time in seconds.

    Returns:
        OptimizationMetrics instance with timestamp and raw metrics.
    """

    return OptimizationMetrics(
        timestamp=datetime.now().isoformat(),
        tasks_processed=tasks_processed,
        errors=errors,
        duration=duration,
    )
