#!/usr/bin/env python3
"""
Performance Metrics Collector - V2 Core Performance System
==========================================================

Handles collection and processing of performance metrics.
Follows Single Responsibility Principle - metrics collection only.
"""

import time
import uuid
import logging
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import


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


class MetricsCollector:
    """
    Performance metrics collection and processing system
    
    Responsibilities:
    - Collect performance metrics from various benchmarks
    - Process and aggregate metric data
    - Calculate performance statistics
    - Store benchmark results
    """
    
    def __init__(self):
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.benchmark_targets = {
            BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
            BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
            BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
            BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
            BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
        }
        self.logger = logging.getLogger(f"{__name__}.MetricsCollector")
    
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
            scalability_score = self._calculate_scalability_score(scalability_results)
            
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
                "performance_degradation": self._calculate_performance_degradation(scalability_results),
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
    
    def store_benchmark(self, benchmark: PerformanceBenchmark) -> bool:
        """Store a benchmark result"""
        try:
            self.benchmarks[benchmark.benchmark_id] = benchmark
            self.logger.info(f"Stored benchmark: {benchmark.benchmark_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store benchmark: {e}")
            return False
    
    def get_benchmark(self, benchmark_id: str) -> Optional[PerformanceBenchmark]:
        """Retrieve a specific benchmark"""
        return self.benchmarks.get(benchmark_id)
    
    def get_all_benchmarks(self) -> Dict[str, PerformanceBenchmark]:
        """Get all stored benchmarks"""
        return self.benchmarks.copy()
    
    def get_benchmarks_by_type(self, benchmark_type: BenchmarkType) -> List[PerformanceBenchmark]:
        """Get benchmarks filtered by type"""
        return [
            benchmark for benchmark in self.benchmarks.values()
            if benchmark.benchmark_type == benchmark_type
        ]
    
    def calculate_aggregate_metrics(self, benchmarks: List[PerformanceBenchmark]) -> Dict[str, Any]:
        """Calculate aggregate metrics across multiple benchmarks"""
        try:
            if not benchmarks:
                return {}
            
            # Group by benchmark type
            by_type = {}
            for benchmark in benchmarks:
                if benchmark.benchmark_type not in by_type:
                    by_type[benchmark.benchmark_type] = []
                by_type[benchmark.benchmark_type].append(benchmark)
            
            aggregate = {}
            for benchmark_type, type_benchmarks in by_type.items():
                type_metrics = []
                for benchmark in type_benchmarks:
                    type_metrics.extend(benchmark.metrics.values())
                
                if type_metrics:
                    aggregate[benchmark_type.value] = {
                        "count": len(type_benchmarks),
                        "average": statistics.mean(type_metrics),
                        "min": min(type_metrics),
                        "max": max(type_metrics),
                        "std_dev": statistics.stdev(type_metrics) if len(type_metrics) > 1 else 0,
                    }
            
            return aggregate
            
        except Exception as e:
            self.logger.error(f"Failed to calculate aggregate metrics: {e}")
            return {}
    
    def _calculate_scalability_score(self, scalability_results: List[Dict[str, Any]]) -> float:
        """Calculate scalability score based on performance degradation"""
        try:
            if len(scalability_results) < 2:
                return 100.0  # Perfect score if only one data point
            
            # Sort by concurrent agents
            sorted_results = sorted(scalability_results, key=lambda x: x.get("concurrent_agents", 0))
            
            # Calculate performance degradation
            baseline_ops = sorted_results[0].get("operations_per_second", 1)
            final_ops = sorted_results[-1].get("operations_per_second", 1)
            
            if baseline_ops == 0:
                return 0.0
            
            # Ideal scaling would maintain ops/sec per agent
            baseline_agents = sorted_results[0].get("concurrent_agents", 1)
            final_agents = sorted_results[-1].get("concurrent_agents", 1)
            
            expected_ops = baseline_ops * (final_agents / baseline_agents)
            actual_efficiency = (final_ops / expected_ops) * 100 if expected_ops > 0 else 0
            
            return min(100.0, max(0.0, actual_efficiency))
            
        except Exception as e:
            self.logger.error(f"Failed to calculate scalability score: {e}")
            return 0.0
    
    def _calculate_performance_degradation(self, scalability_results: List[Dict[str, Any]]) -> float:
        """Calculate performance degradation percentage"""
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
            
        except Exception as e:
            self.logger.error(f"Failed to calculate performance degradation: {e}")
            return 0.0
    
    def clear_benchmarks(self) -> None:
        """Clear all stored benchmarks"""
        self.benchmarks.clear()
        self.logger.info("Cleared all benchmarks")
    
    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks"""
        try:
            total_benchmarks = len(self.benchmarks)
            
            if total_benchmarks == 0:
                return {"total_benchmarks": 0}
            
            # Count by type
            type_counts = {}
            performance_levels = {}
            
            for benchmark in self.benchmarks.values():
                benchmark_type = benchmark.benchmark_type.value
                type_counts[benchmark_type] = type_counts.get(benchmark_type, 0) + 1
                
                level = benchmark.performance_level.value
                performance_levels[level] = performance_levels.get(level, 0) + 1
            
            return {
                "total_benchmarks": total_benchmarks,
                "benchmarks_by_type": type_counts,
                "performance_levels": performance_levels,
                "latest_benchmark": max(self.benchmarks.values(), 
                                      key=lambda x: x.start_time).benchmark_id if self.benchmarks else None,
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get benchmark summary: {e}")
            return {"error": str(e)}
