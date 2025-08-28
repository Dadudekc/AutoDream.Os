"""Scalability measurement analysis utilities."""

from __future__ import annotations

import logging
import statistics
from typing import Any, Dict, List

from ..benchmarks import BenchmarkManager

logger = logging.getLogger(__name__)


def analyze_scalability(
    scalability_results: List[Dict[str, Any]],
    benchmarks: BenchmarkManager,
) -> Dict[str, float]:
    """Analyze scalability measurements.

    Args:
        scalability_results: Individual benchmark results for concurrent agent tests.
        benchmarks: Benchmark manager used for advanced calculations.

    Returns:
        Dictionary with scalability score and related statistics.
    """
    if not scalability_results:
        return {}

    scalability_score = benchmarks.calculate_scalability_score(scalability_results)
    max_ops_per_sec = max(
        result.get("operations_per_second", 0) for result in scalability_results
    )
    avg_ops_per_sec = statistics.mean(
        [result.get("operations_per_second", 0) for result in scalability_results]
    )
    metrics = {
        "scalability_score": scalability_score,
        "max_operations_per_second": max_ops_per_sec,
        "average_operations_per_second": avg_ops_per_sec,
        "concurrent_agent_tests": len(scalability_results),
        "performance_degradation": benchmarks.calculate_performance_degradation(
            scalability_results
        ),
    }
    logger.debug("Analyzed scalability metrics: %s", metrics)
    return metrics
