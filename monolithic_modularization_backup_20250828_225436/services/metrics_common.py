"""Shared thresholds and utilities for metrics services."""
from __future__ import annotations

from typing import Dict

# Default thresholds for common metrics
THRESHOLDS: Dict[str, float] = {
    "cpu_usage_percent": 85.0,
    "memory_usage_percent": 90.0,
    "disk_usage_percent": 90.0,
}


def above_threshold(metric_name: str, value: float) -> bool:
    """Return True if the metric's value exceeds the configured threshold."""
    threshold = THRESHOLDS.get(metric_name)
    return threshold is not None and value > threshold


__all__ = ["THRESHOLDS", "above_threshold"]
