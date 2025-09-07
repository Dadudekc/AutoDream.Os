"""Throughput measurement analysis utilities."""

from __future__ import annotations

import logging
from typing import Dict

logger = logging.getLogger(__name__)


def analyze_throughput(operations_count: int, duration: float) -> Dict[str, float]:
    """Analyze throughput measurements.

    Args:
        operations_count: Number of operations performed.
        duration: Time period in seconds during which operations were executed.

    Returns:
        Dictionary with throughput metrics per second, minute and hour.
    """
    if duration <= 0:
        return {}

    throughput = operations_count / duration
    metrics = {
        "total_operations": operations_count,
        "test_duration": duration,
        "throughput_ops_per_sec": throughput,
        "operations_per_minute": throughput * 60,
        "operations_per_hour": throughput * 3600,
    }
    logger.debug("Analyzed throughput metrics: %s", metrics)
    return metrics
