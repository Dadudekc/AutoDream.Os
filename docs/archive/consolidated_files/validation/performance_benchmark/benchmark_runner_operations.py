#!/usr/bin/env python3
"""
Benchmark Runner Operations - V2 Compliance Module
==================================================

Extended operations for benchmark execution.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import threading
import time
from collections.abc import Callable
from datetime import datetime
from typing import Any

from .metrics import BenchmarkMetrics
from .models import BenchmarkConfig, BenchmarkModels, BenchmarkResult, BenchmarkSuite, BenchmarkType
from .reporter import BenchmarkReporter


class BenchmarkRunnerOperations:
    """Extended operations for benchmark execution."""

    def __init__(self):
        """Initialize benchmark runner operations."""
        self.metrics = BenchmarkMetrics()
        self.reporter = BenchmarkReporter(self.metrics)
        self.suites: list[BenchmarkSuite] = []

    def run_parallel_benchmarks(self, benchmarks: list[dict[str, Any]]) -> list[BenchmarkResult]:
        """Run benchmarks in parallel."""
        results = []
        threads = []

        def run_single_benchmark(benchmark_data):
            func = benchmark_data["function"]
            benchmark_type = benchmark_data["benchmark_type"]
            config = benchmark_data.get("config")
            args = benchmark_data.get("args", [])
            kwargs = benchmark_data.get("kwargs", {})

            result = self.run_benchmark(func, benchmark_type, config, *args, **kwargs)
            results.append(result)

        # Create threads for parallel execution
        for benchmark_data in benchmarks:
            thread = threading.Thread(target=run_single_benchmark, args=(benchmark_data,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        return results

    def run_benchmark(
        self,
        func: Callable,
        benchmark_type: BenchmarkType,
        config: BenchmarkConfig = None,
        *args,
        **kwargs,
    ) -> BenchmarkResult:
        """Run a single benchmark."""
        if config is None:
            config = BenchmarkModels.create_benchmark_config()

        # Warmup iterations
        for _ in range(config.warmup_iterations):
            try:
                func(*args, **kwargs)
            except Exception:
                pass

        # Main benchmark iterations
        start_time = time.time()
        results = []

        for _ in range(config.iterations):
            iteration_start = time.time()
            try:
                result = func(*args, **kwargs)
                iteration_time = time.time() - iteration_start
                results.append(iteration_time)
            except Exception:
                iteration_time = time.time() - iteration_start
                results.append(iteration_time)

        total_time = time.time() - start_time

        # Calculate metrics
        avg_time = sum(results) / len(results) if results else 0
        min_time = min(results) if results else 0
        max_time = max(results) if results else 0

        # Create result
        benchmark_result = BenchmarkResult(
            benchmark_type=benchmark_type,
            function_name=func.__name__,
            iterations=config.iterations,
            total_time=total_time,
            average_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            results=results,
            timestamp=datetime.now(),
            config=config,
        )

        # Record metrics
        self.metrics.record_benchmark(benchmark_result)

        return benchmark_result

    def run_stress_test(self, func: Callable, duration_seconds: int = 60) -> BenchmarkResult:
        """Run stress test for specified duration."""
        config = BenchmarkConfig(
            iterations=1000,  # High iteration count for stress test
            warmup_iterations=10,
            timeout_seconds=duration_seconds,
        )

        start_time = time.time()
        results = []

        while time.time() - start_time < duration_seconds:
            iteration_start = time.time()
            try:
                func()
                iteration_time = time.time() - iteration_start
                results.append(iteration_time)
            except Exception:
                iteration_time = time.time() - iteration_start
                results.append(iteration_time)

        total_time = time.time() - start_time

        # Calculate metrics
        avg_time = sum(results) / len(results) if results else 0
        min_time = min(results) if results else 0
        max_time = max(results) if results else 0

        # Create result
        benchmark_result = BenchmarkResult(
            benchmark_type=BenchmarkType.STRESS_TEST,
            function_name=func.__name__,
            iterations=len(results),
            total_time=total_time,
            average_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            results=results,
            timestamp=datetime.now(),
            config=config,
        )

        # Record metrics
        self.metrics.record_benchmark(benchmark_result)

        return benchmark_result

    def compare_benchmarks(self, results: list[BenchmarkResult]) -> dict[str, Any]:
        """Compare multiple benchmark results."""
        if not results:
            return {"error": "No results to compare"}

        # Find best and worst performers
        best_result = min(results, key=lambda r: r.average_time)
        worst_result = max(results, key=lambda r: r.average_time)

        # Calculate statistics
        avg_times = [r.average_time for r in results]
        total_avg = sum(avg_times) / len(avg_times)

        comparison = {
            "total_benchmarks": len(results),
            "best_performer": {
                "function": best_result.function_name,
                "average_time": best_result.average_time,
                "benchmark_type": best_result.benchmark_type.value,
            },
            "worst_performer": {
                "function": worst_result.function_name,
                "average_time": worst_result.average_time,
                "benchmark_type": worst_result.benchmark_type.value,
            },
            "overall_average": total_avg,
            "performance_ratio": (
                worst_result.average_time / best_result.average_time
                if best_result.average_time > 0
                else 0
            ),
        }

        return comparison

    def export_results(self, results: list[BenchmarkResult], format: str = "json") -> str:
        """Export benchmark results to specified format."""
        if format == "json":
            return self.reporter.export_json(results)
        elif format == "csv":
            return self.reporter.export_csv(results)
        elif format == "html":
            return self.reporter.export_html(results)
        else:
            return self.reporter.export_text(results)

    def get_performance_trends(self) -> dict[str, Any]:
        """Get performance trends over time."""
        history = self.metrics.get_history()

        if len(history) < 2:
            return {"error": "Insufficient data for trend analysis"}

        # Group by function name
        function_trends = {}
        for result in history:
            func_name = result.function_name
            if func_name not in function_trends:
                function_trends[func_name] = []
            function_trends[func_name].append(
                {"timestamp": result.timestamp, "average_time": result.average_time}
            )

        # Calculate trends
        trends = {}
        for func_name, data in function_trends.items():
            if len(data) >= 2:
                # Simple linear trend calculation
                first_avg = data[0]["average_time"]
                last_avg = data[-1]["average_time"]
                trend_direction = "improving" if last_avg < first_avg else "degrading"
                trend_percentage = (
                    ((last_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
                )

                trends[func_name] = {
                    "trend_direction": trend_direction,
                    "trend_percentage": trend_percentage,
                    "data_points": len(data),
                }

        return trends
