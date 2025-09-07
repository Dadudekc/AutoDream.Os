"""Utilities for aggregating benchmark results."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .setup import BenchmarkResult


@dataclass
class PerformanceMetrics:
    """Aggregated statistics for benchmark executions."""

    total_benchmarks: int = 0
    average_execution_time: float = 0.0
    average_memory_usage: float = 0.0
    average_cpu_usage: float = 0.0
    average_efficiency_score: float = 0.0
    total_improvement: float = 0.0
    fastest_operation: Optional[str] = None
    slowest_operation: Optional[str] = None
    most_efficient_operation: Optional[str] = None


def update_performance_metrics(
    metrics: PerformanceMetrics, result: BenchmarkResult
) -> None:
    """Update aggregate metrics using a new benchmark result."""
    metrics.total_benchmarks += 1
    n = metrics.total_benchmarks

    metrics.average_execution_time = (
        (metrics.average_execution_time * (n - 1)) + result.execution_time
    ) / n
    metrics.average_memory_usage = (
        (metrics.average_memory_usage * (n - 1)) + result.memory_usage
    ) / n
    metrics.average_cpu_usage = (
        (metrics.average_cpu_usage * (n - 1)) + result.cpu_usage
    ) / n
    metrics.average_efficiency_score = (
        (metrics.average_efficiency_score * (n - 1)) + result.efficiency_score
    ) / n
    metrics.total_improvement += result.improvement_percentage

    if (
        not metrics.fastest_operation
        or result.execution_time < metrics.average_execution_time
    ):
        metrics.fastest_operation = result.operation_name
    if (
        not metrics.slowest_operation
        or result.execution_time > metrics.average_execution_time
    ):
        metrics.slowest_operation = result.operation_name
    if (
        not metrics.most_efficient_operation
        or result.efficiency_score > metrics.average_efficiency_score
    ):
        metrics.most_efficient_operation = result.operation_name
