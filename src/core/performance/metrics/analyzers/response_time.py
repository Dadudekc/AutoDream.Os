"""Response time measurement analysis utilities."""

from __future__ import annotations

import logging
import statistics
from typing import Dict, List

logger = logging.getLogger(__name__)


def analyze_response_times(response_times: List[float]) -> Dict[str, float]:
    """Analyze response time measurements.

    Calculates common statistics for response time values including
    average, minimum, maximum, variance, median and standard deviation.
    The values are expected to be in milliseconds.
    """
    if not response_times:
        return {}

    metrics = {
        "average_response_time": statistics.mean(response_times),
        "min_response_time": min(response_times),
        "max_response_time": max(response_times),
        "response_time_variance": statistics.variance(response_times)
        if len(response_times) > 1
        else 0,
        "median_response_time": statistics.median(response_times),
        "response_time_std_dev": statistics.stdev(response_times)
        if len(response_times) > 1
        else 0,
    }
    logger.debug("Analyzed response time metrics: %s", metrics)
    return metrics
