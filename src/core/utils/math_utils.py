"""Math helper utilities for core components."""
from __future__ import annotations
from typing import Iterable


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp *value* to the inclusive range [min_value, max_value]."""
    return max(min_value, min(value, max_value))


def calculate_mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean of *values*.

    An empty iterable returns 0.0.
    """
    items = list(values)
    return sum(items) / len(items) if items else 0.0
