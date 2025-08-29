"""Latency measurement utilities.

Provides basic statistical helpers for latency samples.
"""

from statistics import mean
from typing import Sequence


def average_latency(samples: Sequence[float]) -> float:
    """Return the average latency from a sequence of samples.

    Returns 0.0 when *samples* is empty to avoid ZeroDivisionError.
    """
    if not samples:
        return 0.0
    return mean(samples)


def max_latency(samples: Sequence[float]) -> float:
    """Return the maximum latency value or 0.0 for empty input."""
    return max(samples) if samples else 0.0


def min_latency(samples: Sequence[float]) -> float:
    """Return the minimum latency value or 0.0 for empty input."""
    return min(samples) if samples else 0.0
