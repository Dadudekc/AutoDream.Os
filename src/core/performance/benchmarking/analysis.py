"""Benchmark result analysis utilities."""
from __future__ import annotations

import logging
import statistics
from typing import Any, Dict, List

from .benchmark_types import BenchmarkResult

logger = logging.getLogger(__name__)


class BenchmarkAnalyzer:
    """Analyze benchmark results."""

    def calculate_aggregate_metrics(self, benchmarks: List[BenchmarkResult]) -> Dict[str, Any]:
        """Aggregate metrics for a list of benchmarks."""
        try:
            if not benchmarks:
                return {}

            by_type: Dict[str, List[BenchmarkResult]] = {}
            for benchmark in benchmarks:
                by_type.setdefault(benchmark.name, []).append(benchmark)

            aggregate: Dict[str, Any] = {}
            for bench_name, type_benchmarks in by_type.items():
                type_metrics: List[float] = []
                for benchmark in type_benchmarks:
                    type_metrics.extend(v for v in benchmark.metrics.values() if isinstance(v, (int, float)))

                if type_metrics:
                    aggregate[bench_name] = {
                        "count": len(type_benchmarks),
                        "average": statistics.mean(type_metrics),
                        "min": min(type_metrics),
                        "max": max(type_metrics),
                        "std_dev": statistics.stdev(type_metrics) if len(type_metrics) > 1 else 0,
                    }
            return aggregate
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to calculate aggregate metrics: %s", exc)
            return {}

    def calculate_scalability_score(self, scalability_results: List[Dict[str, Any]]) -> float:
        """Calculate scalability score from scalability benchmark results."""
        try:
            if len(scalability_results) < 2:
                return 100.0

            sorted_results = sorted(scalability_results, key=lambda x: x.get("concurrent_agents", 0))
            baseline_ops = sorted_results[0].get("operations_per_second", 1)
            final_ops = sorted_results[-1].get("operations_per_second", 1)
            if baseline_ops == 0:
                return 0.0

            baseline_agents = sorted_results[0].get("concurrent_agents", 1)
            final_agents = sorted_results[-1].get("concurrent_agents", 1)
            expected_ops = baseline_ops * (final_agents / baseline_agents) if baseline_agents > 0 else 0
            actual_efficiency = (final_ops / expected_ops) * 100 if expected_ops > 0 else 0
            return min(100.0, max(0.0, actual_efficiency))
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to calculate scalability score: %s", exc)
            return 0.0

    def calculate_performance_degradation(self, scalability_results: List[Dict[str, Any]]) -> float:
        """Calculate performance degradation percentage."""
        try:
            if len(scalability_results) < 2:
                return 0.0

            sorted_results = sorted(scalability_results, key=lambda x: x.get("concurrent_agents", 0))
            baseline_ops = sorted_results[0].get("operations_per_second", 1)
            final_ops = sorted_results[-1].get("operations_per_second", 1)
            if baseline_ops == 0:
                return 100.0

            degradation = ((baseline_ops - final_ops) / baseline_ops) * 100
            return max(0.0, degradation)
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to calculate performance degradation: %s", exc)
            return 0.0

    def summary(self, benchmarks: Dict[str, BenchmarkResult]) -> Dict[str, Any]:
        """Return a summary for stored benchmarks."""
        try:
            total = len(benchmarks)
            if total == 0:
                return {"total_benchmarks": 0}

            type_counts: Dict[str, int] = {}
            for benchmark in benchmarks.values():
                bt = benchmark.name
                type_counts[bt] = type_counts.get(bt, 0) + 1

            latest = max(benchmarks.values(), key=lambda x: x.start_time).id
            return {
                "total_benchmarks": total,
                "benchmarks_by_type": type_counts,
                "latest_benchmark": latest,
            }
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to summarize benchmarks: %s", exc)
            return {"error": str(exc)}

__all__ = ["BenchmarkAnalyzer"]
