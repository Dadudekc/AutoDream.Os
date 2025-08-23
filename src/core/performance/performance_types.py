#!/usr/bin/env python3
"""
Performance Types and Enums - V2 Core Performance System

This module contains all the data structures, enums, and types
for the performance validation system.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any


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


class OptimizationTarget(Enum):
    """Optimization targets"""
    RESPONSE_TIME_IMPROVEMENT = "response_time_improvement"
    THROUGHPUT_INCREASE = "throughput_increase"
    SCALABILITY_ENHANCEMENT = "scalability_enhancement"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"
    RESOURCE_EFFICIENCY = "resource_efficiency"


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


@dataclass
class SystemPerformanceReport:
    """System performance report"""
    report_id: str
    timestamp: str
    overall_performance_level: PerformanceLevel
    benchmark_results: List[PerformanceBenchmark]
    optimization_opportunities: List[OptimizationTarget]
    enterprise_readiness_score: float
    recommendations: List[str]


@dataclass
class BenchmarkTargets:
    """Benchmark performance targets"""
    response_time_target: float = 100.0  # ms
    throughput_target: float = 1000.0    # ops/sec
    scalability_target: float = 100.0    # concurrent users
    reliability_target: float = 99.9     # %
    latency_target: float = 50.0         # ms


@dataclass
class PerformanceThresholds:
    """Performance level thresholds"""
    enterprise_ready: float = 0.95  # 95% of targets met
    production_ready: float = 0.85  # 85% of targets met
    development_ready: float = 0.70  # 70% of targets met
    not_ready: float = 0.0          # Below 70%

