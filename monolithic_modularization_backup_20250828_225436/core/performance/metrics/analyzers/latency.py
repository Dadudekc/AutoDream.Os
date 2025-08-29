"""Latency measurement analysis utilities."""

from __future__ import annotations

import logging
import statistics
from typing import Dict, List

logger = logging.getLogger(__name__)


def analyze_latency(latency_times: List[float]) -> Dict[str, float]:
    """Analyze latency measurements.

    Calculates summary statistics and key percentiles for latency samples.
    Values are expected to be in milliseconds.
    """
    if not latency_times:
        return {}

    sorted_latencies = sorted(latency_times)
    n = len(sorted_latencies)
    metrics = {
        "average_latency": statistics.mean(latency_times),
        "min_latency": min(latency_times),
        "max_latency": max(latency_times),
        "median_latency": statistics.median(latency_times),
        "p95_latency": sorted_latencies[int(0.95 * n)] if n > 0 else 0,
        "p99_latency": sorted_latencies[int(0.99 * n)] if n > 0 else 0,
        "latency_std_dev": statistics.stdev(latency_times)
        if len(latency_times) > 1
        else 0,
    }
    logger.debug("Analyzed latency metrics: %s", metrics)
    return metrics
