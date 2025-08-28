"""Compatibility types for performance modules.

This lightweight module provides the core type definitions required by
several performance components.  The original project referenced a
`performance_types` module that was absent from the repository, which
caused import errors during test collection.  The definitions here are
kept intentionally minimal and re-export existing shared enums and
dataclasses from other modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .common_metrics import BenchmarkType, PerformanceLevel
from .metrics.benchmarks import PerformanceBenchmark


class OptimizationTarget(str, Enum):
    """Areas where performance can be improved."""

    RESPONSE_TIME_IMPROVEMENT = "response_time_improvement"
    THROUGHPUT_INCREASE = "throughput_increase"
    SCALABILITY_ENHANCEMENT = "scalability_enhancement"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"
    RESOURCE_EFFICIENCY = "resource_efficiency"


@dataclass
class PerformanceThresholds:
    """Thresholds used to classify performance levels."""

    enterprise_ready: float = 0.9
    production_ready: float = 0.8
    development_ready: float = 0.7


@dataclass
class BenchmarkTargets:
    """Default benchmark targets for the benchmark runner."""

    response_time_target: float = 100.0
    throughput_target: float = 1000.0
    scalability_target: float = 100.0


__all__ = [
    "PerformanceBenchmark",
    "BenchmarkType",
    "PerformanceLevel",
    "OptimizationTarget",
    "PerformanceThresholds",
    "BenchmarkTargets",
]

