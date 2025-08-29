"""Utility functions for benchmark metric calculations."""
from __future__ import annotations

from typing import Any, Dict, Optional


def calculate_efficiency_score(
    execution_time: float,
    memory_usage: float,
    cpu_usage: float,
    before_state: Optional[Dict[str, Any]],
    after_state: Optional[Dict[str, Any]],
) -> float:
    """Return an efficiency score between 0 and 100.

    The implementation mirrors the simple heuristic used by previous
    benchmarking utilities.  It rewards faster execution and reductions
    in line count while penalising excessive resource usage.
    """
    score = 100.0

    if execution_time > 5.0:
        score -= min(execution_time - 5.0, 30)
    if memory_usage > 100:
        score -= min(memory_usage / 10, 20)
    if cpu_usage > 80:
        score -= min(cpu_usage - 80, 20)

    if before_state and after_state:
        if "line_count" in before_state and "line_count" in after_state:
            reduction = before_state["line_count"] - after_state["line_count"]
            if reduction > 0:
                score += min(reduction / 10, 20)

    return max(0.0, min(100.0, score))


def calculate_improvement_percentage(
    before_state: Optional[Dict[str, Any]],
    after_state: Optional[Dict[str, Any]],
) -> float:
    """Compute percentage improvement between two states."""
    if not before_state or not after_state:
        return 0.0

    if "line_count" in before_state and "line_count" in after_state:
        before_lines = before_state["line_count"]
        after_lines = after_state["line_count"]
        if before_lines > 0:
            return ((before_lines - after_lines) / before_lines) * 100

    return 0.0
