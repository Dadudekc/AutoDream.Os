"""Minimal performance type definitions for testing.

This module provides lightweight stand-ins for the broader performance
system types. Only the attributes required by the test suite are
implemented to avoid heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BenchmarkType(Enum):
    """Types of performance benchmarks."""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"


class PerformanceLevel(Enum):
    """Simplified performance readiness levels."""

    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"
    DEVELOPMENT_READY = "development_ready"
    NOT_READY = "not_ready"


@dataclass
class PerformanceBenchmark:
    """Result of a single performance benchmark."""

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


@dataclass
class BenchmarkTargets:
    """Target values for benchmarks.

    Defaults provide generic targets suitable for tests.
    """

    response_time_target: float = 100.0
    throughput_target: float = 50.0
    scalability_target: int = 100


class OptimizationTarget(Enum):
    """Areas where performance can be improved."""

    RESPONSE_TIME_IMPROVEMENT = "response_time_improvement"
    THROUGHPUT_INCREASE = "throughput_increase"
    SCALABILITY_ENHANCEMENT = "scalability_enhancement"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"
    RESOURCE_EFFICIENCY = "resource_efficiency"


@dataclass
class SystemPerformanceReport:
    """Summary output from the performance validation system."""

    report_id: str
    benchmarks: List[PerformanceBenchmark]
    overall_level: PerformanceLevel
    enterprise_score: float
    optimization_opportunities: List[OptimizationTarget]


@dataclass
class PerformanceThresholds:
    """Thresholds for classifying performance levels."""

    enterprise_ready: float = 0.9
    production_ready: float = 0.75
    development_ready: float = 0.5
