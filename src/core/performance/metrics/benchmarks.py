"""Benchmark-related types and helpers."""
import logging
import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class BenchmarkType(Enum):
    """Performance benchmark types"""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    RESOURCE_UTILIZATION = "resource_utilization"
    LATENCY = "latency"


class PerformanceLevel(Enum):
    """Performance level classifications"""

    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"
    DEVELOPMENT_READY = "development_ready"
    NOT_READY = "not_ready"


@dataclass
class PerformanceBenchmark:
    """Performance benchmark result"""

    benchmark_id: str
    benchmark_type: BenchmarkType
    test_name: str
    start_time: str
    end_time: str
    duration: float
    metrics: Dict[str, float]
    target_metrics: Dict[str, float]
    performance_level: PerformanceLevel
    optimization_recommendations: List[str]


class BenchmarkManager:
    """Manage storage and analysis of benchmarks."""

    def __init__(self) -> None:
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.logger = logging.getLogger(f"{__name__}.BenchmarkManager")

    # Storage operations -------------------------------------------------
    def store(self, benchmark: PerformanceBenchmark) -> bool:
        try:
            self.benchmarks[benchmark.benchmark_id] = benchmark
            self.logger.info(f"Stored benchmark: {benchmark.benchmark_id}")
            return True
        except Exception as exc:  # pragma: no cover - logging only
            self.logger.error(f"Failed to store benchmark: {exc}")
            return False

    def get(self, benchmark_id: str) -> Optional[PerformanceBenchmark]:
        return self.benchmarks.get(benchmark_id)

    def all(self) -> Dict[str, PerformanceBenchmark]:
        return self.benchmarks.copy()

    def by_type(self, benchmark_type: BenchmarkType) -> List[PerformanceBenchmark]:
        return [
            b for b in self.benchmarks.values() if b.benchmark_type == benchmark_type
        ]

    def clear(self) -> None:
        self.benchmarks.clear()
        self.logger.info("Cleared all benchmarks")

    # Aggregate calculations --------------------------------------------
    def calculate_aggregate_metrics(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> Dict[str, Any]:
        try:
            if not benchmarks:
                return {}

            by_type: Dict[BenchmarkType, List[PerformanceBenchmark]] = {}
            for benchmark in benchmarks:
                by_type.setdefault(benchmark.benchmark_type, []).append(benchmark)

            aggregate: Dict[str, Any] = {}
            for benchmark_type, type_benchmarks in by_type.items():
                type_metrics: List[float] = []
                for benchmark in type_benchmarks:
                    type_metrics.extend(benchmark.metrics.values())

                if type_metrics:
                    aggregate[benchmark_type.value] = {
                        "count": len(type_benchmarks),
                        "average": statistics.mean(type_metrics),
                        "min": min(type_metrics),
                        "max": max(type_metrics),
                        "std_dev": statistics.stdev(type_metrics)
                        if len(type_metrics) > 1
                        else 0,
                    }
            return aggregate
        except Exception as exc:  # pragma: no cover - logging only
            self.logger.error(f"Failed to calculate aggregate metrics: {exc}")
            return {}

    # Scalability helpers ------------------------------------------------
    def calculate_scalability_score(self, scalability_results: List[Dict[str, Any]]) -> float:
        try:
            if len(scalability_results) < 2:
                return 100.0  # Perfect score if only one data point

            sorted_results = sorted(
                scalability_results, key=lambda x: x.get("concurrent_agents", 0)
            )
            baseline_ops = sorted_results[0].get("operations_per_second", 1)
            final_ops = sorted_results[-1].get("operations_per_second", 1)
            if baseline_ops == 0:
                return 0.0

            baseline_agents = sorted_results[0].get("concurrent_agents", 1)
            final_agents = sorted_results[-1].get("concurrent_agents", 1)
            expected_ops = baseline_ops * (final_agents / baseline_agents)
            actual_efficiency = (
                (final_ops / expected_ops) * 100 if expected_ops > 0 else 0
            )
            return min(100.0, max(0.0, actual_efficiency))
        except Exception as exc:  # pragma: no cover - logging only
            self.logger.error(f"Failed to calculate scalability score: {exc}")
            return 0.0

    def calculate_performance_degradation(
        self, scalability_results: List[Dict[str, Any]]
    ) -> float:
        try:
            if len(scalability_results) < 2:
                return 0.0

            sorted_results = sorted(
                scalability_results, key=lambda x: x.get("concurrent_agents", 0)
            )
            baseline_ops = sorted_results[0].get("operations_per_second", 1)
            final_ops = sorted_results[-1].get("operations_per_second", 1)
            if baseline_ops == 0:
                return 100.0

            degradation = ((baseline_ops - final_ops) / baseline_ops) * 100
            return max(0.0, degradation)
        except Exception as exc:  # pragma: no cover - logging only
            self.logger.error(f"Failed to calculate performance degradation: {exc}")
            return 0.0

    # Summary ------------------------------------------------------------
    def summary(self) -> Dict[str, Any]:
        try:
            total = len(self.benchmarks)
            if total == 0:
                return {"total_benchmarks": 0}

            type_counts: Dict[str, int] = {}
            performance_levels: Dict[str, int] = {}
            for benchmark in self.benchmarks.values():
                bt = benchmark.benchmark_type.value
                type_counts[bt] = type_counts.get(bt, 0) + 1
                level = benchmark.performance_level.value
                performance_levels[level] = performance_levels.get(level, 0) + 1

            latest = max(
                self.benchmarks.values(), key=lambda x: x.start_time
            ).benchmark_id
            return {
                "total_benchmarks": total,
                "benchmarks_by_type": type_counts,
                "performance_levels": performance_levels,
                "latest_benchmark": latest,
            }
        except Exception as exc:  # pragma: no cover - logging only
            self.logger.error(f"Failed to get benchmark summary: {exc}")
            return {"error": str(exc)}


__all__ = [
    "BenchmarkManager",
    "BenchmarkType",
    "PerformanceBenchmark",
    "PerformanceLevel",
]
