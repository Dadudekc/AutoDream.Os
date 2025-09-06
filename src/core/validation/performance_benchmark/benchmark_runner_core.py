#!/usr/bin/env python3
"""
Benchmark Runner Core - V2 Compliance Module
============================================

Core benchmark execution functionality.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from .models import (
    BenchmarkType,
    BenchmarkResult,
    BenchmarkConfig,
    BenchmarkSuite,
    BenchmarkModels,
)
from .metrics import BenchmarkMetrics
from .reporter import BenchmarkReporter


class BenchmarkRunnerCore:
    """Core benchmark execution engine."""

    def __init__(self):
        """Initialize benchmark runner core."""
        self.metrics = BenchmarkMetrics()
        self.reporter = BenchmarkReporter(self.metrics)
        self.suites: List[BenchmarkSuite] = []

    def add_suite(self, suite: BenchmarkSuite) -> None:
        """Add a benchmark suite."""
        self.suites.append(suite)

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
            except Exception as e:
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

    def run_suite(self, suite: BenchmarkSuite) -> List[BenchmarkResult]:
        """Run a benchmark suite."""
        results = []

        for benchmark in suite.benchmarks:
            result = self.run_benchmark(
                benchmark.function,
                benchmark.benchmark_type,
                benchmark.config,
                *benchmark.args,
                **benchmark.kwargs,
            )
            results.append(result)

        return results

    def run_all_suites(self) -> Dict[str, List[BenchmarkResult]]:
        """Run all benchmark suites."""
        all_results = {}

        for suite in self.suites:
            results = self.run_suite(suite)
            all_results[suite.name] = results

        return all_results

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        return self.metrics.get_summary()

    def generate_report(self, output_path: str = None) -> str:
        """Generate benchmark report."""
        return self.reporter.generate_report(output_path)

    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()

    def get_benchmark_history(self) -> List[BenchmarkResult]:
        """Get benchmark history."""
        return self.metrics.get_history()
