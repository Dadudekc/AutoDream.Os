#!/usr/bin/env python3
"""
Performance Metrics Collector - V2 Core Performance System
==========================================================

Handles collection and processing of performance metrics and provides
a lightweight base interface for additional metrics collectors used by
services.
"""

import logging
from typing import Any, Dict, List, Optional

from .types import MetricData, MetricType
from .benchmarks import (
    BenchmarkManager,
    BenchmarkType,
    PerformanceBenchmark,
    PerformanceLevel,
)
from .config import DEFAULT_BENCHMARK_TARGETS, DEFAULT_COLLECTION_INTERVAL
from .analyzers import (
    analyze_latency,
    analyze_reliability,
    analyze_response_times,
    analyze_scalability,
    analyze_throughput,
)


class MetricsCollector:
    """
    Performance metrics collection and processing system.

    This class serves as the single source of truth for metrics collection
    across the project. It provides benchmarking helpers as well as the
    minimal interface expected by service-level collectors.
    """

    def __init__(self, collection_interval: int = DEFAULT_COLLECTION_INTERVAL):
        # Basic collector configuration used by service collectors
        self.collection_interval = collection_interval
        self.enabled = True
        self.running = False
        self.performance_monitor = None

        # Benchmark storage
        self.benchmarks = BenchmarkManager()
        self.benchmark_targets = DEFAULT_BENCHMARK_TARGETS.copy()
        self.logger = logging.getLogger(f"{__name__}.MetricsCollector")

    async def collect_metrics(self) -> List[MetricData]:
        """Collect metrics and return a list of MetricData objects.

        Subclasses should override this method. The default implementation
        raises ``NotImplementedError`` to maintain backwards compatibility with
        previous abstract base class behaviour.
        """
        raise NotImplementedError("collect_metrics must be implemented by subclasses")

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable this collector."""
        self.enabled = enabled
        self.logger.info("Metrics collector %s", "enabled" if enabled else "disabled")

    def collect_response_time_metrics(
        self, response_times: List[float]
    ) -> Dict[str, float]:
        """Collect and process response time metrics."""
        try:
            metrics = analyze_response_times(response_times)
            self.logger.debug(f"Collected response time metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect response time metrics: {e}")
            return {}

    def collect_throughput_metrics(
        self, operations_count: int, duration: float
    ) -> Dict[str, float]:
        """Collect and process throughput metrics."""
        try:
            metrics = analyze_throughput(operations_count, duration)
            self.logger.debug(f"Collected throughput metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect throughput metrics: {e}")
            return {}

    def collect_scalability_metrics(
        self, scalability_results: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Collect and process scalability metrics."""
        try:
            metrics = analyze_scalability(scalability_results, self.benchmarks)
            self.logger.debug(f"Collected scalability metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect scalability metrics: {e}")
            return {}

    def collect_reliability_metrics(
        self, total_operations: int, failed_operations: int, duration: float
    ) -> Dict[str, float]:
        """Collect and process reliability metrics."""
        try:
            metrics = analyze_reliability(total_operations, failed_operations, duration)
            self.logger.debug(f"Collected reliability metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect reliability metrics: {e}")
            return {}

    def collect_latency_metrics(self, latency_times: List[float]) -> Dict[str, float]:
        """Collect and process latency metrics."""
        try:
            metrics = analyze_latency(latency_times)
            self.logger.debug(f"Collected latency metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to collect latency metrics: {e}")
            return {}

    def store_benchmark(self, benchmark: PerformanceBenchmark) -> bool:
        return self.benchmarks.store(benchmark)

    def get_benchmark(self, benchmark_id: str) -> Optional[PerformanceBenchmark]:
        return self.benchmarks.get(benchmark_id)

    def get_all_benchmarks(self) -> Dict[str, PerformanceBenchmark]:
        return self.benchmarks.all()

    def get_benchmarks_by_type(
        self, benchmark_type: BenchmarkType
    ) -> List[PerformanceBenchmark]:
        return self.benchmarks.by_type(benchmark_type)

    def calculate_aggregate_metrics(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> Dict[str, Any]:
        return self.benchmarks.calculate_aggregate_metrics(benchmarks)

    def clear_benchmarks(self) -> None:
        self.benchmarks.clear()

    def get_benchmark_summary(self) -> Dict[str, Any]:
        return self.benchmarks.summary()


__all__ = [
    "MetricsCollector",
    "MetricData",
    "MetricType",
    "BenchmarkType",
    "PerformanceBenchmark",
    "PerformanceLevel",
]
