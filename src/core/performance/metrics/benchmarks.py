"""Benchmark-related types and helpers."""
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from ..benchmarking.benchmark_types import BenchmarkType


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
    """Manage storage of benchmarks."""

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


__all__ = [
    "BenchmarkManager",
    "BenchmarkType",
    "PerformanceBenchmark",
    "PerformanceLevel",
]
