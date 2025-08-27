#!/usr/bin/env python3
"""
Performance Metrics Collector - V2 Core Performance System
==========================================================

Handles collection and processing of performance metrics and provides
a lightweight base interface for additional metrics collectors used by
services.
"""

import time
import logging
import statistics
from datetime import datetime
from typing import Any, Dict, List, Optional

from .types import MetricData, MetricType
from .benchmarks import (
    BenchmarkManager,
    BenchmarkType,
    PerformanceBenchmark,
    PerformanceLevel,
)


class MetricsCollector:
    """
    Performance metrics collection and processing system.

    This class serves as the single source of truth for metrics collection
    across the project. It provides benchmarking helpers as well as the
    minimal interface expected by service-level collectors.
    """

    def __init__(self, collection_interval: int = 60):
        # Basic collector configuration used by service collectors
        self.collection_interval = collection_interval
        self.enabled = True
        self.running = False
        self.performance_monitor = None

        # Benchmark storage
        self.benchmarks = BenchmarkManager()
        self.benchmark_targets = {
            BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
            BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
            BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
            BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
            BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
        }
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
        self.logger.info(
            "Metrics collector %s", "enabled" if enabled else "disabled"
        )
    
    def collect_response_time_metrics(self, response_times: List[float]) -> Dict[str, float]:
        """Collect and process response time metrics"""
        try:
            if not response_times:
                return {}
            
            metrics = {
                "average_response_time": statistics.mean(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "response_time_variance": statistics.variance(response_times) if len(response_times) > 1 else 0,
                "median_response_time": statistics.median(response_times),
                "response_time_std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0,
            }
            
            self.logger.debug(f"Collected response time metrics: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect response time metrics: {e}")
            return {}
    
    def collect_throughput_metrics(self, operations_count: int, duration: float) -> Dict[str, float]:
        """Collect and process throughput metrics"""
        try:
            if duration <= 0:
                return {}
            
            throughput = operations_count / duration
            
            metrics = {
                "total_operations": operations_count,
                "test_duration": duration,
                "throughput_ops_per_sec": throughput,
                "operations_per_minute": throughput * 60,
                "operations_per_hour": throughput * 3600,
            }
            
            self.logger.debug(f"Collected throughput metrics: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect throughput metrics: {e}")
            return {}
    
    def collect_scalability_metrics(self, scalability_results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Collect and process scalability metrics"""
        try:
            if not scalability_results:
                return {}
            
            # Calculate scalability score based on performance degradation
            scalability_score = self.benchmarks.calculate_scalability_score(
                scalability_results
            )
            
            max_ops_per_sec = max(
                result.get("operations_per_second", 0) for result in scalability_results
            )
            
            avg_ops_per_sec = statistics.mean([
                result.get("operations_per_second", 0) for result in scalability_results
            ])
            
            metrics = {
                "scalability_score": scalability_score,
                "max_operations_per_second": max_ops_per_sec,
                "average_operations_per_second": avg_ops_per_sec,
                "concurrent_agent_tests": len(scalability_results),
                "performance_degradation": self.benchmarks.calculate_performance_degradation(
                    scalability_results
                ),
            }
            
            self.logger.debug(f"Collected scalability metrics: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect scalability metrics: {e}")
            return {}
    
    def collect_reliability_metrics(self, total_operations: int, failed_operations: int, 
                                  duration: float) -> Dict[str, float]:
        """Collect and process reliability metrics"""
        try:
            if total_operations == 0:
                return {}
            
            success_rate = ((total_operations - failed_operations) / total_operations) * 100
            failure_rate = (failed_operations / total_operations) * 100
            
            metrics = {
                "total_operations": total_operations,
                "successful_operations": total_operations - failed_operations,
                "failed_operations": failed_operations,
                "success_rate_percent": success_rate,
                "failure_rate_percent": failure_rate,
                "uptime_percentage": success_rate,  # Simplified uptime calculation
                "mean_time_between_failures": duration / failed_operations if failed_operations > 0 else float('inf'),
            }
            
            self.logger.debug(f"Collected reliability metrics: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect reliability metrics: {e}")
            return {}
    
    def collect_latency_metrics(self, latency_times: List[float]) -> Dict[str, float]:
        """Collect and process latency metrics"""
        try:
            if not latency_times:
                return {}
            
            sorted_latencies = sorted(latency_times)
            n = len(sorted_latencies)
            
            metrics = {
                "average_latency": statistics.mean(latency_times),
                "min_latency": min(latency_times),
                "max_latency": max(latency_times),
                "median_latency": statistics.median(latency_times),
                "p95_latency": sorted_latencies[int(0.95 * n)] if n > 0 else 0,
                "p99_latency": sorted_latencies[int(0.99 * n)] if n > 0 else 0,
                "latency_std_dev": statistics.stdev(latency_times) if len(latency_times) > 1 else 0,
            }
            
            self.logger.debug(f"Collected latency metrics: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect latency metrics: {e}")
            return {}
    
    # Benchmark management wrappers -------------------------------------
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
