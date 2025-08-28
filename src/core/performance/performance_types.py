"""Compatibility layer providing performance type definitions."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .types.enums import BenchmarkType, PerformanceLevel, OptimizationTarget


@dataclass
class BenchmarkTargets:
    """Default benchmark target thresholds."""
    response_time_target: float = 100.0
    throughput_target: float = 1000.0
    scalability_target: float = 1.0


@dataclass
class PerformanceBenchmark:
    """Result of a performance benchmark run."""
    benchmark_id: str
    benchmark_type: BenchmarkType
    test_name: str
    start_time: str
    end_time: str
    duration: float
    metrics: Dict[str, Any]
    target_metrics: Dict[str, Any]
    performance_level: PerformanceLevel
    optimization_recommendations: List[str] = field(default_factory=list)


@dataclass
class SystemPerformanceReport:
    """Aggregated performance report."""
    report_id: str
    generated_at: str
    benchmarks: List[PerformanceBenchmark] = field(default_factory=list)
    performance_level: PerformanceLevel = PerformanceLevel.NOT_READY


@dataclass
class PerformanceThresholds:
    """Threshold values for performance level classification."""
    enterprise_ready: float = 0.9
    production_ready: float = 0.8
    development_ready: float = 0.7


__all__ = [
    "BenchmarkType",
    "PerformanceLevel",
    "OptimizationTarget",
    "BenchmarkTargets",
    "PerformanceBenchmark",
    "SystemPerformanceReport",
    "PerformanceThresholds",
]
