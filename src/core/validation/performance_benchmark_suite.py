#!/usr/bin/env python3
"""
Performance Benchmark Suite - Agent Cellphone V2
===============================================

Comprehensive performance validation and benchmarking framework for V2 compliance.
Provides advanced metrics collection, analysis, and reporting capabilities.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import time
import asyncio
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationIssue, ValidationSeverity


class BenchmarkType(Enum):
    """Types of performance benchmarks."""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    CONCURRENT_OPERATIONS = "concurrent_operations"
    ERROR_RATE = "error_rate"


@dataclass
class BenchmarkResult:
    """Result of a performance benchmark."""
    benchmark_type: BenchmarkType
    component_name: str
    metric_value: float
    threshold: float
    passed: bool
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics."""
    response_time_ms: float
    throughput_ops_per_sec: float
    memory_usage_mb: float
    cpu_usage_percent: float
    error_rate_percent: float
    concurrent_operations: int
    timestamp: datetime


class PerformanceBenchmarkSuite:
    """
    Advanced performance benchmarking and validation suite.
    
    Provides comprehensive performance testing capabilities with:
    - Multi-metric benchmarking
    - Threshold validation
    - Statistical analysis
    - Performance regression detection
    - Automated reporting
    """

    def __init__(self):
        """Initialize the performance benchmark suite."""
        self.benchmark_results: List[BenchmarkResult] = []
        self.performance_thresholds = {
            BenchmarkType.RESPONSE_TIME: 100.0,  # 100ms
            BenchmarkType.THROUGHPUT: 1000.0,    # 1000 ops/sec
            BenchmarkType.MEMORY_USAGE: 512.0,   # 512MB
            BenchmarkType.CPU_USAGE: 80.0,       # 80%
            BenchmarkType.ERROR_RATE: 1.0,       # 1%
        }
        self.benchmark_history: Dict[str, List[BenchmarkResult]] = {}

    async def benchmark_component(
        self,
        component_name: str,
        operation: Callable,
        benchmark_type: BenchmarkType,
        iterations: int = 100,
        concurrent_operations: int = 1
    ) -> BenchmarkResult:
        """
        Benchmark a component operation.
        
        Args:
            component_name: Name of the component being benchmarked
            operation: Async operation to benchmark
            benchmark_type: Type of benchmark to perform
            iterations: Number of iterations to run
            concurrent_operations: Number of concurrent operations
            
        Returns:
            BenchmarkResult with performance metrics
        """
        start_time = time.time()
        results = []
        errors = 0
        
        try:
            if concurrent_operations > 1:
                # Run concurrent operations
                tasks = []
                for _ in range(iterations):
                    task = asyncio.create_task(self._run_operation_with_metrics(operation))
                    tasks.append(task)
                    
                    if len(tasks) >= concurrent_operations:
                        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                        results.extend([r for r in batch_results if not isinstance(r, Exception)])
                        errors += sum(1 for r in batch_results if isinstance(r, Exception))
                        tasks = []
                
                # Process remaining tasks
                if tasks:
                    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                    results.extend([r for r in batch_results if not isinstance(r, Exception)])
                    errors += sum(1 for r in batch_results if isinstance(r, Exception))
            else:
                # Run sequential operations
                for _ in range(iterations):
                    try:
                        result = await self._run_operation_with_metrics(operation)
                        results.append(result)
                    except Exception:
                        errors += 1
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Calculate metrics based on benchmark type
            metric_value = self._calculate_metric(benchmark_type, results, total_time, iterations, errors)
            threshold = self.performance_thresholds[benchmark_type]
            passed = self._evaluate_threshold(benchmark_type, metric_value, threshold)
            
            result = BenchmarkResult(
                benchmark_type=benchmark_type,
                component_name=component_name,
                metric_value=metric_value,
                threshold=threshold,
                passed=passed,
                timestamp=datetime.now(),
                details={
                    "iterations": iterations,
                    "concurrent_operations": concurrent_operations,
                    "errors": errors,
                    "total_time": total_time,
                    "raw_results": results[:10]  # Store first 10 results for analysis
                },
                metadata={
                    "operation_name": operation.__name__ if hasattr(operation, '__name__') else str(operation),
                    "benchmark_suite_version": "2.0.0"
                }
            )
            
            self.benchmark_results.append(result)
            self._update_history(component_name, result)
            
            return result
            
        except Exception as e:
            # Create failed result
            result = BenchmarkResult(
                benchmark_type=benchmark_type,
                component_name=component_name,
                metric_value=float('inf'),
                threshold=self.performance_thresholds[benchmark_type],
                passed=False,
                timestamp=datetime.now(),
                details={"error": str(e)},
                metadata={"benchmark_suite_version": "2.0.0"}
            )
            
            self.benchmark_results.append(result)
            return result

    async def _run_operation_with_metrics(self, operation: Callable) -> Dict[str, Any]:
        """Run operation and collect performance metrics."""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            result = await operation() if asyncio.iscoroutinefunction(operation) else operation()
            
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            return {
                "execution_time": end_time - start_time,
                "memory_delta": end_memory - start_memory,
                "success": True,
                "result": result
            }
        except Exception as e:
            end_time = time.time()
            return {
                "execution_time": end_time - start_time,
                "memory_delta": 0,
                "success": False,
                "error": str(e)
            }

    def _calculate_metric(
        self,
        benchmark_type: BenchmarkType,
        results: List[Dict[str, Any]],
        total_time: float,
        iterations: int,
        errors: int
    ) -> float:
        """Calculate metric value based on benchmark type."""
        if not results:
            return float('inf')
        
        successful_results = [r for r in results if r.get("success", False)]
        
        if benchmark_type == BenchmarkType.RESPONSE_TIME:
            if successful_results:
                response_times = [r["execution_time"] for r in successful_results]
                return statistics.mean(response_times) * 1000  # Convert to milliseconds
            return float('inf')
        
        elif benchmark_type == BenchmarkType.THROUGHPUT:
            successful_operations = len(successful_results)
            return successful_operations / total_time if total_time > 0 else 0
        
        elif benchmark_type == BenchmarkType.MEMORY_USAGE:
            if successful_results:
                memory_deltas = [r["memory_delta"] for r in successful_results]
                return statistics.mean(memory_deltas) / (1024 * 1024)  # Convert to MB
            return 0
        
        elif benchmark_type == BenchmarkType.ERROR_RATE:
            return (errors / iterations) * 100 if iterations > 0 else 100
        
        elif benchmark_type == BenchmarkType.CONCURRENT_OPERATIONS:
            return len(successful_results)
        
        return 0.0

    def _evaluate_threshold(self, benchmark_type: BenchmarkType, value: float, threshold: float) -> bool:
        """Evaluate if metric value passes threshold."""
        if benchmark_type in [BenchmarkType.RESPONSE_TIME, BenchmarkType.MEMORY_USAGE, BenchmarkType.CPU_USAGE, BenchmarkType.ERROR_RATE]:
            return value <= threshold
        else:  # THROUGHPUT, CONCURRENT_OPERATIONS
            return value >= threshold

    def _get_memory_usage(self) -> float:
        """Get current memory usage in bytes."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            # Fallback for systems without psutil
            return 0

    def _update_history(self, component_name: str, result: BenchmarkResult) -> None:
        """Update benchmark history for trend analysis."""
        if component_name not in self.benchmark_history:
            self.benchmark_history[component_name] = []
        
        self.benchmark_history[component_name].append(result)
        
        # Keep only last 100 results per component
        if len(self.benchmark_history[component_name]) > 100:
            self.benchmark_history[component_name] = self.benchmark_history[component_name][-100:]

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        total_benchmarks = len(self.benchmark_results)
        passed_benchmarks = sum(1 for r in self.benchmark_results if r.passed)
        success_rate = (passed_benchmarks / total_benchmarks * 100) if total_benchmarks > 0 else 0
        
        # Group results by component
        component_results = {}
        for result in self.benchmark_results:
            if result.component_name not in component_results:
                component_results[result.component_name] = []
            component_results[result.component_name].append(result)
        
        # Calculate component performance scores
        component_scores = {}
        for component, results in component_results.items():
            component_passed = sum(1 for r in results if r.passed)
            component_scores[component] = (component_passed / len(results) * 100) if results else 0
        
        # Identify performance regressions
        regressions = self._detect_performance_regressions()
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_benchmarks": total_benchmarks,
                "passed_benchmarks": passed_benchmarks,
                "success_rate": round(success_rate, 2),
                "performance_regressions": len(regressions)
            },
            "component_performance": component_scores,
            "performance_regressions": regressions,
            "benchmark_details": [
                {
                    "component": r.component_name,
                    "type": r.benchmark_type.value,
                    "value": round(r.metric_value, 2),
                    "threshold": r.threshold,
                    "passed": r.passed,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in self.benchmark_results[-20:]  # Last 20 results
            ]
        }

    def _detect_performance_regressions(self) -> List[Dict[str, Any]]:
        """Detect performance regressions by comparing recent results with historical data."""
        regressions = []
        
        for component, history in self.benchmark_history.items():
            if len(history) < 10:  # Need sufficient history
                continue
            
            # Compare last 5 results with previous 10
            recent_results = history[-5:]
            baseline_results = history[-15:-5]
            
            for benchmark_type in BenchmarkType:
                recent_values = [r.metric_value for r in recent_results if r.benchmark_type == benchmark_type]
                baseline_values = [r.metric_value for r in baseline_results if r.benchmark_type == benchmark_type]
                
                if recent_values and baseline_values:
                    recent_avg = statistics.mean(recent_values)
                    baseline_avg = statistics.mean(baseline_values)
                    
                    # Calculate regression percentage
                    if baseline_avg > 0:
                        regression_pct = ((recent_avg - baseline_avg) / baseline_avg) * 100
                        
                        # Consider it a regression if performance degraded by more than 20%
                        if regression_pct > 20:
                            regressions.append({
                                "component": component,
                                "benchmark_type": benchmark_type.value,
                                "baseline_avg": round(baseline_avg, 2),
                                "recent_avg": round(recent_avg, 2),
                                "regression_percentage": round(regression_pct, 2)
                            })
        
        return regressions

    def validate_performance_compliance(self) -> List[ValidationIssue]:
        """Validate performance compliance and return validation issues."""
        issues = []
        
        for result in self.benchmark_results:
            if not result.passed:
                severity = ValidationSeverity.ERROR if result.metric_value > result.threshold * 2 else ValidationSeverity.WARNING
                
                issues.append(ValidationIssue(
                    rule_id=f"performance_{result.benchmark_type.value}",
                    rule_name=f"Performance {result.benchmark_type.value.replace('_', ' ').title()}",
                    severity=severity,
                    message=f"{result.component_name} {result.benchmark_type.value} exceeds threshold: {result.metric_value:.2f} > {result.threshold}",
                    details={
                        "component": result.component_name,
                        "metric_value": result.metric_value,
                        "threshold": result.threshold,
                        "benchmark_type": result.benchmark_type.value
                    },
                    timestamp=result.timestamp,
                    component=result.component_name
                ))
        
        return issues

    def set_performance_threshold(self, benchmark_type: BenchmarkType, threshold: float) -> None:
        """Set custom performance threshold for a benchmark type."""
        self.performance_thresholds[benchmark_type] = threshold

    def get_benchmark_summary(self) -> str:
        """Get human-readable benchmark summary."""
        total = len(self.benchmark_results)
        passed = sum(1 for r in self.benchmark_results if r.passed)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        summary = f"Performance Benchmark Summary:\n"
        summary += f"Total Benchmarks: {total}\n"
        summary += f"Passed: {passed}\n"
        summary += f"Success Rate: {success_rate:.1f}%\n"
        
        if self.benchmark_results:
            latest = self.benchmark_results[-1]
            summary += f"Latest: {latest.component_name} - {latest.benchmark_type.value}: {latest.metric_value:.2f} ({'PASS' if latest.passed else 'FAIL'})\n"
        
        return summary
