from __future__ import annotations

from typing import List


def calculate_percentile(sorted_values: List[float], percentile: float) -> float:
    """Return the value at the given percentile from a sorted list."""

    if not sorted_values:
        return 0.0
    index = int(len(sorted_values) * percentile)
    index = min(index, len(sorted_values) - 1)
    return sorted_values[index]


def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers, returning 0.0 if denominator is zero."""

    return numerator / denominator if denominator else 0.0
