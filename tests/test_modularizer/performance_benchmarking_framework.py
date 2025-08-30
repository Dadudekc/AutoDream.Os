#!/usr/bin/env python3
"""
📊 PERFORMANCE BENCHMARKING FRAMEWORK - V2-COMPLIANCE-008
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive performance benchmarking and load testing
capabilities for the integration testing framework.

Features:
- Performance benchmarking with metrics collection
- Load testing under various conditions
- Stress testing and resource monitoring
- Performance regression detection
- Automated performance reporting
"""

import os
import sys
import time
import psutil
import threading
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import statistics

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class BenchmarkType(Enum):
    """Types of performance benchmarks"""
    
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    RESPONSE_TIME = "response_time"
    LOAD_TESTING = "load_testing"
    STRESS_TESTING = "stress_testing"


class LoadProfile(Enum):
    """Load testing profiles"""
    
    LIGHT = "light"
    NORMAL = "normal"
    HEAVY = "heavy"
    STRESS = "stress"
    BURST = "burst"


@dataclass
class PerformanceMetrics:
    """Performance metrics data"""
    
    execution_time: float
    memory_usage: float
    cpu_usage: float
    throughput: float
    latency: float
    response_time: float
    timestamp: datetime
    additional_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResult:
    """Result of a performance benchmark"""
    
    benchmark_id: str
    benchmark_name: str
    benchmark_type: BenchmarkType
    iterations: int
    warmup_runs: int
    start_time: datetime
    end_time: datetime
    total_execution_time: float
    metrics: List[PerformanceMetrics]
    summary: Dict[str, Any]
    thresholds: Dict[str, float]
    status: str  # "passed", "failed", "warning"


class PerformanceBenchmarkingFramework:
    """
    Performance benchmarking framework for comprehensive performance testing.
    
    Provides:
    - Automated performance benchmarking
    - Load testing under various conditions
    - Performance regression detection
    - Resource monitoring and analysis
    """
    
    def __init__(self):
        """Initialize performance benchmarking framework."""
        self.benchmark_results: List[BenchmarkResult] = []
        self.performance_history: Dict[str, List[PerformanceMetrics]] = {}
        self.thresholds: Dict[str, Dict[str, float]] = {}
        
        # Configuration
        self.default_iterations = 100
        self.default_warmup_runs = 10
        self.monitoring_interval = 0.1  # seconds
        
        # Logging
        self.logger = logging.getLogger(f"{__name__}.PerformanceBenchmarkingFramework")
        self._setup_logging()
        self._initialize_thresholds()
        
        self.logger.info("📊 Performance Benchmarking Framework initialized")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _initialize_thresholds(self):
        """Initialize performance thresholds."""
        self.thresholds = {
            "execution_time": {"warning": 1.0, "critical": 5.0},
            "memory_usage": {"warning": 512.0, "critical": 1024.0},
            "cpu_usage": {"warning": 50.0, "critical": 80.0},
            "throughput": {"warning": 100.0, "critical": 50.0},
            "latency": {"warning": 0.1, "critical": 0.5},
            "response_time": {"warning": 0.05, "critical": 0.2}
        }
    
    def run_performance_benchmark(self, benchmark_id: str, test_function: Callable,
                                iterations: int = None, warmup_runs: int = None,
                                benchmark_type: BenchmarkType = BenchmarkType.EXECUTION_TIME) -> BenchmarkResult:
        """Run a performance benchmark."""
        iterations = iterations or self.default_iterations
        warmup_runs = warmup_runs or self.default_warmup_runs
        
        self.logger.info(f"📊 Starting performance benchmark: {benchmark_id}")
        
        start_time = datetime.now()
        metrics = []
        
        # Warmup runs
        self.logger.info(f"🔥 Running {warmup_runs} warmup iterations...")
        for i in range(warmup_runs):
            test_function()
        
        # Actual benchmark iterations
        self.logger.info(f"🚀 Running {iterations} benchmark iterations...")
        for i in range(iterations):
            iteration_start = time.time()
            
            # Monitor system resources
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            initial_cpu = process.cpu_percent()
            
            # Execute test function
            test_function()
            
            # Calculate metrics
            execution_time = time.time() - iteration_start
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            final_cpu = process.cpu_percent()
            
            metric = PerformanceMetrics(
                execution_time=execution_time,
                memory_usage=final_memory,
                cpu_usage=final_cpu,
                throughput=1.0 / execution_time if execution_time > 0 else 0.0,
                latency=execution_time,
                response_time=execution_time,
                timestamp=datetime.now(),
                additional_metrics={
                    "memory_delta": final_memory - initial_memory,
                    "cpu_delta": final_cpu - initial_cpu
                }
            )
            metrics.append(metric)
            
            if (i + 1) % 10 == 0:
                self.logger.info(f"   Completed {i + 1}/{iterations} iterations")
        
        end_time = datetime.now()
        total_execution_time = (end_time - start_time).total_seconds()
        
        # Calculate summary statistics
        summary = self._calculate_metrics_summary(metrics)
        
        # Check thresholds and determine status
        status = self._evaluate_performance_status(summary)
        
        # Create benchmark result
        result = BenchmarkResult(
            benchmark_id=benchmark_id,
            benchmark_name=f"Performance Benchmark: {benchmark_id}",
            benchmark_type=benchmark_type,
            iterations=iterations,
            warmup_runs=warmup_runs,
            start_time=start_time,
            end_time=end_time,
            total_execution_time=total_execution_time,
            metrics=metrics,
            summary=summary,
            thresholds=self.thresholds,
            status=status
        )
        
        self.benchmark_results.append(result)
        self.performance_history[benchmark_id] = metrics
        
        self.logger.info(f"✅ Performance benchmark completed: {status}")
        return result
    
    def run_load_test(self, test_id: str, test_function: Callable,
                     load_profile: LoadProfile = LoadProfile.NORMAL,
                     duration: int = 60) -> BenchmarkResult:
        """Run a load test under specified conditions."""
        self.logger.info(f"🔥 Starting load test: {test_id} with {load_profile.value} profile")
        
        # Configure load profile
        load_config = self._get_load_profile_config(load_profile)
        
        start_time = datetime.now()
        metrics = []
        test_count = 0
        
        # Run load test for specified duration
        end_time = start_time.timestamp() + duration
        while time.time() < end_time:
            iteration_start = time.time()
            
            # Execute test function
            test_function()
            
            # Calculate metrics
            execution_time = time.time() - iteration_start
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            cpu_usage = process.cpu_percent()
            
            metric = PerformanceMetrics(
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                throughput=1.0 / execution_time if execution_time > 0 else 0.0,
                latency=execution_time,
                response_time=execution_time,
                timestamp=datetime.now(),
                additional_metrics={
                    "test_count": test_count,
                    "load_profile": load_profile.value
                }
            )
            metrics.append(metric)
            test_count += 1
            
            # Apply load profile timing
            time.sleep(load_config["interval"])
        
        end_time = datetime.now()
        total_execution_time = (end_time - start_time).total_seconds()
        
        # Calculate summary statistics
        summary = self._calculate_metrics_summary(metrics)
        summary["load_profile"] = load_profile.value
        summary["total_tests"] = test_count
        summary["tests_per_second"] = test_count / total_execution_time
        
        # Check thresholds and determine status
        status = self._evaluate_performance_status(summary)
        
        # Create benchmark result
        result = BenchmarkResult(
            benchmark_id=test_id,
            benchmark_name=f"Load Test: {test_id}",
            benchmark_type=BenchmarkType.LOAD_TESTING,
            iterations=test_count,
            warmup_runs=0,
            start_time=start_time,
            end_time=end_time,
            total_execution_time=total_execution_time,
            metrics=metrics,
            summary=summary,
            thresholds=self.thresholds,
            status=status
        )
        
        self.benchmark_results.append(result)
        self.performance_history[test_id] = metrics
        
        self.logger.info(f"✅ Load test completed: {status} ({test_count} tests)")
        return result
    
    def run_stress_test(self, test_id: str, test_function: Callable,
                       max_concurrent: int = 10, duration: int = 120) -> BenchmarkResult:
        """Run a stress test with concurrent execution."""
        self.logger.info(f"💥 Starting stress test: {test_id} with {max_concurrent} concurrent threads")
        
        start_time = datetime.now()
        metrics = []
        test_count = 0
        
        # Run stress test for specified duration
        end_time = start_time.timestamp() + duration
        
        def stress_worker():
            nonlocal test_count
            while time.time() < end_time:
                iteration_start = time.time()
                
                try:
                    # Execute test function
                    test_function()
                    
                    # Calculate metrics
                    execution_time = time.time() - iteration_start
                    process = psutil.Process()
                    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
                    cpu_usage = process.cpu_percent()
                    
                    metric = PerformanceMetrics(
                        execution_time=execution_time,
                        memory_usage=memory_usage,
                        cpu_usage=cpu_usage,
                        throughput=1.0 / execution_time if execution_time > 0 else 0.0,
                        latency=execution_time,
                        response_time=execution_time,
                        timestamp=datetime.now(),
                        additional_metrics={
                            "test_count": test_count,
                            "concurrent_threads": max_concurrent
                        }
                    )
                    metrics.append(metric)
                    test_count += 1
                    
                except Exception as e:
                    self.logger.warning(f"Stress test iteration failed: {e}")
        
        # Run concurrent workers
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = [executor.submit(stress_worker) for _ in range(max_concurrent)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Stress test worker failed: {e}")
        
        end_time = datetime.now()
        total_execution_time = (end_time - start_time).total_seconds()
        
        # Calculate summary statistics
        summary = self._calculate_metrics_summary(metrics)
        summary["concurrent_threads"] = max_concurrent
        summary["total_tests"] = test_count
        summary["tests_per_second"] = test_count / total_execution_time
        
        # Check thresholds and determine status
        status = self._evaluate_performance_status(summary)
        
        # Create benchmark result
        result = BenchmarkResult(
            benchmark_id=test_id,
            benchmark_name=f"Stress Test: {test_id}",
            benchmark_type=BenchmarkType.STRESS_TESTING,
            iterations=test_count,
            warmup_runs=0,
            start_time=start_time,
            end_time=end_time,
            total_execution_time=total_execution_time,
            metrics=metrics,
            summary=summary,
            thresholds=self.thresholds,
            status=status
        )
        
        self.benchmark_results.append(result)
        self.performance_history[test_id] = metrics
        
        self.logger.info(f"✅ Stress test completed: {status} ({test_count} tests)")
        return result
    
    def _get_load_profile_config(self, profile: LoadProfile) -> Dict[str, Any]:
        """Get configuration for a load profile."""
        configs = {
            LoadProfile.LIGHT: {"interval": 1.0, "description": "Light load testing"},
            LoadProfile.NORMAL: {"interval": 0.5, "description": "Normal load testing"},
            LoadProfile.HEAVY: {"interval": 0.1, "description": "Heavy load testing"},
            LoadProfile.STRESS: {"interval": 0.01, "description": "Stress testing"},
            LoadProfile.BURST: {"interval": 0.0, "description": "Burst load testing"}
        }
        return configs.get(profile, configs[LoadProfile.NORMAL])
    
    def _calculate_metrics_summary(self, metrics: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Calculate summary statistics for metrics."""
        if not metrics:
            return {}
        
        # Extract values for each metric type
        execution_times = [m.execution_time for m in metrics]
        memory_usages = [m.memory_usage for m in metrics]
        cpu_usages = [m.cpu_usage for m in metrics]
        throughputs = [m.throughput for m in metrics]
        latencies = [m.latency for m in metrics]
        response_times = [m.response_time for m in metrics]
        
        summary = {
            "execution_time": {
                "min": min(execution_times),
                "max": max(execution_times),
                "mean": statistics.mean(execution_times),
                "median": statistics.median(execution_times),
                "std_dev": statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0
            },
            "memory_usage": {
                "min": min(memory_usages),
                "max": max(memory_usages),
                "mean": statistics.mean(memory_usages),
                "median": statistics.median(memory_usages),
                "std_dev": statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0.0
            },
            "cpu_usage": {
                "min": min(cpu_usages),
                "max": max(cpu_usages),
                "mean": statistics.mean(cpu_usages),
                "median": statistics.median(cpu_usages),
                "std_dev": statistics.stdev(cpu_usages) if len(cpu_usages) > 1 else 0.0
            },
            "throughput": {
                "min": min(throughputs),
                "max": max(throughputs),
                "mean": statistics.mean(throughputs),
                "median": statistics.median(throughputs),
                "std_dev": statistics.stdev(throughputs) if len(throughputs) > 1 else 0.0
            },
            "latency": {
                "min": min(latencies),
                "max": max(latencies),
                "mean": statistics.mean(latencies),
                "median": statistics.median(latencies),
                "std_dev": statistics.stdev(latencies) if len(latencies) > 1 else 0.0
            },
            "response_time": {
                "min": min(response_times),
                "max": max(response_times),
                "mean": statistics.mean(response_times),
                "median": statistics.median(response_times),
                "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0.0
            }
        }
        
        return summary
    
    def _evaluate_performance_status(self, summary: Dict[str, Any]) -> str:
        """Evaluate performance against thresholds and determine status."""
        if not summary:
            return "unknown"
        
        status = "passed"
        
        for metric_name, metric_data in summary.items():
            if isinstance(metric_data, dict) and "mean" in metric_data:
                mean_value = metric_data["mean"]
                thresholds = self.thresholds.get(metric_name, {})
                
                if "critical" in thresholds and mean_value > thresholds["critical"]:
                    status = "failed"
                    break
                elif "warning" in thresholds and mean_value > thresholds["warning"]:
                    status = "warning"
        
        return status
    
    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmark results."""
        if not self.benchmark_results:
            return {"message": "No benchmarks have been run yet"}
        
        total_benchmarks = len(self.benchmark_results)
        passed_benchmarks = len([r for r in self.benchmark_results if r.status == "passed"])
        failed_benchmarks = len([r for r in self.benchmark_results if r.status == "failed"])
        warning_benchmarks = len([r for r in self.benchmark_results if r.status == "warning"])
        
        # Calculate average execution time
        execution_times = [r.total_execution_time for r in self.benchmark_results if r.total_execution_time > 0]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Benchmark type breakdown
        type_breakdown = {}
        for result in self.benchmark_results:
            benchmark_type = result.benchmark_type.value
            if benchmark_type not in type_breakdown:
                type_breakdown[benchmark_type] = {"total": 0, "passed": 0, "failed": 0, "warnings": 0}
            
            type_breakdown[benchmark_type]["total"] += 1
            if result.status == "passed":
                type_breakdown[benchmark_type]["passed"] += 1
            elif result.status == "failed":
                type_breakdown[benchmark_type]["failed"] += 1
            elif result.status == "warning":
                type_breakdown[benchmark_type]["warnings"] += 1
        
        return {
            "total_benchmarks": total_benchmarks,
            "passed": passed_benchmarks,
            "failed": failed_benchmarks,
            "warnings": warning_benchmarks,
            "pass_rate": (passed_benchmarks / total_benchmarks) * 100 if total_benchmarks > 0 else 0,
            "average_execution_time": avg_execution_time,
            "type_breakdown": type_breakdown,
            "thresholds": self.thresholds
        }
    
    def export_benchmark_results(self, format: str = "json", filepath: Optional[str] = None) -> str:
        """Export benchmark results to specified format."""
        if format.lower() == "json":
            return self._export_benchmark_json_results(filepath)
        elif format.lower() == "html":
            return self._export_benchmark_html_results(filepath)
        elif format.lower() == "markdown":
            return self._export_benchmark_markdown_results(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_benchmark_json_results(self, filepath: Optional[str] = None) -> str:
        """Export benchmark results to JSON format."""
        if not filepath:
            filepath = f"performance_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results_data = {
            "summary": self.get_benchmark_summary(),
            "benchmark_results": [
                {
                    "benchmark_id": r.benchmark_id,
                    "benchmark_name": r.benchmark_name,
                    "benchmark_type": r.benchmark_type.value,
                    "iterations": r.iterations,
                    "warmup_runs": r.warmup_runs,
                    "start_time": r.start_time.isoformat(),
                    "end_time": r.end_time.isoformat(),
                    "total_execution_time": r.total_execution_time,
                    "status": r.status,
                    "summary": r.summary
                }
                for r in self.benchmark_results
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        return filepath
    
    def _export_benchmark_html_results(self, filepath: Optional[str] = None) -> str:
        """Export benchmark results to HTML format."""
        if not filepath:
            filepath = f"performance_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        summary = self.get_benchmark_summary()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Benchmark Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .benchmark-result {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .passed {{ border-left: 5px solid #4CAF50; }}
                .failed {{ border-left: 5px solid #f44336; }}
                .warning {{ border-left: 5px solid #ff9800; }}
            </style>
        </head>
        <body>
            <h1>📊 Performance Benchmark Results</h1>
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total Benchmarks:</strong> {summary['total_benchmarks']}</p>
                <p><strong>Passed:</strong> {summary['passed']}</p>
                <p><strong>Failed:</strong> {summary['failed']}</p>
                <p><strong>Warnings:</strong> {summary['warnings']}</p>
                <p><strong>Pass Rate:</strong> {summary['pass_rate']:.1f}%</p>
                <p><strong>Average Execution Time:</strong> {summary['average_execution_time']:.3f}s</p>
            </div>
            
            <h2>📋 Benchmark Results</h2>
        """
        
        for result in self.benchmark_results:
            status_class = result.status
            html_content += f"""
            <div class="benchmark-result {status_class}">
                <h3>{result.benchmark_name}</h3>
                <p><strong>Benchmark ID:</strong> {result.benchmark_id}</p>
                <p><strong>Type:</strong> {result.benchmark_type.value}</p>
                <p><strong>Status:</strong> {result.status.upper()}</p>
                <p><strong>Iterations:</strong> {result.iterations}</p>
                <p><strong>Total Execution Time:</strong> {result.total_execution_time:.3f}s</p>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _export_benchmark_markdown_results(self, filepath: Optional[str] = None) -> str:
        """Export benchmark results to Markdown format."""
        if not filepath:
            filepath = f"performance_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        summary = self.get_benchmark_summary()
        
        markdown_content = f"""# 📊 Performance Benchmark Results

## 📊 Summary

- **Total Benchmarks:** {summary['total_benchmarks']}
- **Passed:** {summary['passed']}
- **Failed:** {summary['failed']}
- **Warnings:** {summary['warnings']}
- **Pass Rate:** {summary['pass_rate']:.1f}%
- **Average Execution Time:** {summary['average_execution_time']:.3f}s

## 📋 Benchmark Results

"""
        
        for result in self.benchmark_results:
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "warning": "⚠️"
            }.get(result.status, "❓")
            
            markdown_content += f"""### {status_emoji} {result.benchmark_name}

- **Benchmark ID:** {result.benchmark_id}
- **Type:** {result.benchmark_type.value}
- **Status:** {result.status.upper()}
- **Iterations:** {result.iterations}
- **Total Execution Time:** {result.total_execution_time:.3f}s

---
"""
        
        with open(filepath, 'w') as f:
            f.write(markdown_content)
        
        return filepath


# Convenience functions for easy usage
def run_performance_benchmark(benchmark_id: str, test_function: Callable,
                             iterations: int = 100, warmup_runs: int = 10) -> BenchmarkResult:
    """Run a performance benchmark."""
    framework = PerformanceBenchmarkingFramework()
    return framework.run_performance_benchmark(benchmark_id, test_function, iterations, warmup_runs)


def run_load_test(test_id: str, test_function: Callable,
                 load_profile: LoadProfile = LoadProfile.NORMAL,
                 duration: int = 60) -> BenchmarkResult:
    """Run a load test."""
    framework = PerformanceBenchmarkingFramework()
    return framework.run_load_test(test_id, test_function, load_profile, duration)


def run_stress_test(test_id: str, test_function: Callable,
                   max_concurrent: int = 10, duration: int = 120) -> BenchmarkResult:
    """Run a stress test."""
    framework = PerformanceBenchmarkingFramework()
    return framework.run_stress_test(test_id, test_function, max_concurrent, duration)


if __name__ == "__main__":
    # Example usage
    print("📊 Performance Benchmarking Framework - V2-COMPLIANCE-008")
    print("=" * 70)
    
    # Initialize framework
    framework = PerformanceBenchmarkingFramework()
    
    # Example test function
    def sample_test_function():
        """Sample test function for benchmarking."""
        time.sleep(0.01)  # Simulate work
        return "test completed"
    
    # Run performance benchmark
    print("\n📊 Running performance benchmark...")
    benchmark_result = framework.run_performance_benchmark(
        "sample_benchmark", sample_test_function, iterations=50, warmup_runs=5
    )
    
    # Run load test
    print("\n🔥 Running load test...")
    load_result = framework.run_load_test(
        "sample_load_test", sample_test_function, LoadProfile.NORMAL, duration=30
    )
    
    # Print summary
    summary = framework.get_benchmark_summary()
    print(f"\n📊 Benchmark Summary:")
    print(f"Total Benchmarks: {summary['total_benchmarks']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Pass Rate: {summary['pass_rate']:.1f}%")
    
    # Export results
    json_file = framework.export_benchmark_results("json")
    html_file = framework.export_benchmark_results("html")
    md_file = framework.export_benchmark_results("markdown")
    
    print(f"\n📁 Results exported to:")
    print(f"JSON: {json_file}")
    print(f"HTML: {html_file}")
    print(f"Markdown: {md_file}")
