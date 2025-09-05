"""
Performance Benchmark Metrics
============================

Metrics collection and analysis for performance benchmarking.
V2 Compliance: < 300 lines, single responsibility, metrics processing.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import time
import psutil
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from .models import BenchmarkType, BenchmarkResult, BenchmarkConfig, PerformanceMetrics, BenchmarkModels


class BenchmarkMetrics:
    """Metrics collection and analysis for performance benchmarking."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.results: List[BenchmarkResult] = []
        self.monitoring_active = False
        self.monitoring_thread = None
    
    def measure_response_time(self, func: Callable, *args, **kwargs) -> BenchmarkResult:
        """Measure response time of a function."""
        start_time = time.time()
        success = True
        error_message = None
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
            result = None
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.RESPONSE_TIME,
            func.__name__,
            response_time,
            "ms",
            {"function": func.__name__, "args": str(args), "kwargs": str(kwargs)},
            success,
            error_message
        )
    
    def measure_throughput(self, func: Callable, iterations: int, *args, **kwargs) -> BenchmarkResult:
        """Measure throughput of a function over multiple iterations."""
        start_time = time.time()
        success = True
        error_message = None
        
        try:
            for _ in range(iterations):
                func(*args, **kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
        
        end_time = time.time()
        total_time = end_time - start_time
        throughput = iterations / total_time if total_time > 0 else 0
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.THROUGHPUT,
            func.__name__,
            throughput,
            "ops/sec",
            {"function": func.__name__, "iterations": iterations},
            success,
            error_message
        )
    
    def measure_memory_usage(self, func: Callable, *args, **kwargs) -> BenchmarkResult:
        """Measure memory usage of a function."""
        process = psutil.Process()
        
        # Get baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        success = True
        error_message = None
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
            result = None
        
        # Get peak memory
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_usage = peak_memory - baseline_memory
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.MEMORY_USAGE,
            func.__name__,
            memory_usage,
            "MB",
            {"function": func.__name__, "baseline_memory": baseline_memory, "peak_memory": peak_memory},
            success,
            error_message
        )
    
    def measure_cpu_usage(self, func: Callable, *args, **kwargs) -> BenchmarkResult:
        """Measure CPU usage of a function."""
        process = psutil.Process()
        
        # Get baseline CPU
        baseline_cpu = process.cpu_percent()
        
        success = True
        error_message = None
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
            result = None
        
        # Get peak CPU
        peak_cpu = process.cpu_percent()
        cpu_usage = max(peak_cpu, baseline_cpu)
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.CPU_USAGE,
            func.__name__,
            cpu_usage,
            "%",
            {"function": func.__name__, "baseline_cpu": baseline_cpu, "peak_cpu": peak_cpu},
            success,
            error_message
        )
    
    def measure_concurrent_operations(self, func: Callable, concurrent_workers: int, *args, **kwargs) -> BenchmarkResult:
        """Measure performance under concurrent load."""
        results = []
        threads = []
        
        def worker():
            try:
                result = func(*args, **kwargs)
                results.append(True)
            except Exception:
                results.append(False)
        
        start_time = time.time()
        
        # Start concurrent workers
        for _ in range(concurrent_workers):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        successful_operations = sum(results)
        success_rate = (successful_operations / concurrent_workers) * 100 if concurrent_workers > 0 else 0
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.CONCURRENT_OPERATIONS,
            func.__name__,
            success_rate,
            "%",
            {"function": func.__name__, "concurrent_workers": concurrent_workers, "successful_operations": successful_operations},
            success_rate > 0,
            f"Success rate: {success_rate}%" if success_rate < 100 else None
        )
    
    def measure_error_rate(self, func: Callable, iterations: int, *args, **kwargs) -> BenchmarkResult:
        """Measure error rate of a function over multiple iterations."""
        errors = 0
        
        for _ in range(iterations):
            try:
                func(*args, **kwargs)
            except Exception:
                errors += 1
        
        error_rate = (errors / iterations) * 100 if iterations > 0 else 0
        
        return BenchmarkModels.create_benchmark_result(
            BenchmarkType.ERROR_RATE,
            func.__name__,
            error_rate,
            "%",
            {"function": func.__name__, "iterations": iterations, "errors": errors},
            error_rate == 0,
            f"Error rate: {error_rate}%" if error_rate > 0 else None
        )
    
    def add_result(self, result: BenchmarkResult) -> None:
        """Add a benchmark result."""
        self.results.append(result)
    
    def get_results_by_type(self, benchmark_type: BenchmarkType) -> List[BenchmarkResult]:
        """Get results filtered by benchmark type."""
        return [result for result in self.results if result.benchmark_type == benchmark_type]
    
    def get_performance_metrics(self, benchmark_type: BenchmarkType) -> PerformanceMetrics:
        """Get performance metrics for a specific benchmark type."""
        results = self.get_results_by_type(benchmark_type)
        
        if not results:
            return BenchmarkModels.create_performance_metrics([], 0, 0)
        
        values = [result.value for result in results if result.success]
        total_iterations = len(results)
        successful_iterations = len(values)
        
        return BenchmarkModels.create_performance_metrics(values, total_iterations, successful_iterations)
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all benchmark types."""
        summary = {}
        
        for benchmark_type in BenchmarkType:
            metrics = self.get_performance_metrics(benchmark_type)
            summary[benchmark_type.value] = {
                'average': metrics.average_value,
                'min': metrics.min_value,
                'max': metrics.max_value,
                'median': metrics.median_value,
                'std_dev': metrics.standard_deviation,
                'percentile_95': metrics.percentile_95,
                'percentile_99': metrics.percentile_99,
                'success_rate': metrics.success_rate,
                'total_iterations': metrics.total_iterations
            }
        
        return summary
    
    def clear_results(self) -> None:
        """Clear all benchmark results."""
        self.results.clear()
    
    def export_results(self, format: str = 'json') -> Dict[str, Any]:
        """Export results in specified format."""
        if format == 'json':
            return {
                'timestamp': datetime.now().isoformat(),
                'total_results': len(self.results),
                'results': [
                    {
                        'benchmark_type': result.benchmark_type.value,
                        'test_name': result.test_name,
                        'value': result.value,
                        'unit': result.unit,
                        'timestamp': result.timestamp.isoformat(),
                        'success': result.success,
                        'error_message': result.error_message,
                        'metadata': result.metadata
                    }
                    for result in self.results
                ],
                'summary': self.get_summary_statistics()
            }
        else:
            return {'error': f'Unsupported format: {format}'}
