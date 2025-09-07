"""Reliability measurement analysis utilities."""

from __future__ import annotations

import logging
from typing import Dict

logger = logging.getLogger(__name__)


def analyze_reliability(
    total_operations: int, failed_operations: int, duration: float
) -> Dict[str, float]:
    """Analyze reliability measurements.

    Calculates success and failure rates along with mean time between failures.
    Duration is expressed in seconds.
    """
    if total_operations == 0:
        return {}

    success_rate = ((total_operations - failed_operations) / total_operations) * 100
    failure_rate = (failed_operations / total_operations) * 100
    metrics = {
        "total_operations": total_operations,
        "successful_operations": total_operations - failed_operations,
        "failed_operations": failed_operations,
        "success_rate_percent": success_rate,
        "failure_rate_percent": failure_rate,
        "uptime_percentage": success_rate,
        "mean_time_between_failures": duration / failed_operations
        if failed_operations > 0
        else float("inf"),
    }
    logger.debug("Analyzed reliability metrics: %s", metrics)
    return metrics
