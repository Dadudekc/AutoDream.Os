"""
Performance Benchmark Runner
============================

Main benchmark execution engine.
V2 Compliance: < 300 lines, single responsibility, benchmark execution.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from .models import BenchmarkType, BenchmarkResult, BenchmarkConfig, BenchmarkSuite, BenchmarkModels
from .metrics import BenchmarkMetrics
from .reporter import BenchmarkReporter


class BenchmarkRunner:
    """Main benchmark execution engine."""
    
    def __init__(self):
        """Initialize benchmark runner."""
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
        **kwargs
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
        
        # Run benchmark based on type
        if benchmark_type == BenchmarkType.RESPONSE_TIME:
            result = self.metrics.measure_response_time(func, *args, **kwargs)
        elif benchmark_type == BenchmarkType.THROUGHPUT:
            result = self.metrics.measure_throughput(func, config.iterations, *args, **kwargs)
        elif benchmark_type == BenchmarkType.MEMORY_USAGE:
            result = self.metrics.measure_memory_usage(func, *args, **kwargs)
        elif benchmark_type == BenchmarkType.CPU_USAGE:
            result = self.metrics.measure_cpu_usage(func, *args, **kwargs)
        elif benchmark_type == BenchmarkType.CONCURRENT_OPERATIONS:
            result = self.metrics.measure_concurrent_operations(func, config.concurrent_workers, *args, **kwargs)
        elif benchmark_type == BenchmarkType.ERROR_RATE:
            result = self.metrics.measure_error_rate(func, config.iterations, *args, **kwargs)
        else:
            raise ValueError(f"Unsupported benchmark type: {benchmark_type}")
        
        self.metrics.add_result(result)
        return result
    
    def run_suite(self, suite_name: str) -> List[BenchmarkResult]:
        """Run a benchmark suite."""
        suite = next((s for s in self.suites if s.name == suite_name), None)
        if not suite:
            raise ValueError(f"Benchmark suite not found: {suite_name}")
        
        results = []
        
        for benchmark_func in suite.benchmarks:
            # Determine benchmark type from function name or metadata
            benchmark_type = self._determine_benchmark_type(benchmark_func)
            
            result = self.run_benchmark(
                benchmark_func,
                benchmark_type,
                suite.config
            )
            results.append(result)
        
        return results
    
    def run_all_suites(self) -> Dict[str, List[BenchmarkResult]]:
        """Run all benchmark suites."""
        all_results = {}
        
        for suite in self.suites:
            results = self.run_suite(suite.name)
            all_results[suite.name] = results
        
        return all_results
    
    def run_performance_test(
        self,
        func: Callable,
        test_name: str,
        iterations: int = 10,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Run comprehensive performance test."""
        config = BenchmarkModels.create_benchmark_config(iterations=iterations)
        
        # Run all benchmark types
        results = {}
        for benchmark_type in BenchmarkType:
            result = self.run_benchmark(func, benchmark_type, config, *args, **kwargs)
            results[benchmark_type.value] = result
        
        # Generate performance metrics
        performance_metrics = {}
        for benchmark_type in BenchmarkType:
            metrics = self.metrics.get_performance_metrics(benchmark_type)
            performance_metrics[benchmark_type.value] = metrics.__dict__
        
        return {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'iterations': iterations,
            'results': {k: v.__dict__ for k, v in results.items()},
            'performance_metrics': performance_metrics,
            'summary': self.reporter.generate_summary_report()
        }
    
    def run_load_test(
        self,
        func: Callable,
        test_name: str,
        concurrent_workers: int = 5,
        duration_seconds: int = 60,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Run load test with concurrent workers."""
        results = []
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        def worker():
            while time.time() < end_time:
                try:
                    result = func(*args, **kwargs)
                    results.append({
                        'timestamp': datetime.now().isoformat(),
                        'success': True,
                        'result': result
                    })
                except Exception as e:
                    results.append({
                        'timestamp': datetime.now().isoformat(),
                        'success': False,
                        'error': str(e)
                    })
        
        # Start concurrent workers
        threads = []
        for _ in range(concurrent_workers):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Calculate statistics
        successful_operations = sum(1 for r in results if r['success'])
        total_operations = len(results)
        success_rate = (successful_operations / total_operations * 100) if total_operations > 0 else 0
        
        return {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'concurrent_workers': concurrent_workers,
            'duration_seconds': duration_seconds,
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'success_rate': success_rate,
            'operations_per_second': total_operations / duration_seconds,
            'results': results
        }
    
    def generate_report(self, report_type: str = 'summary') -> Dict[str, Any]:
        """Generate benchmark report."""
        if report_type == 'summary':
            return self.reporter.generate_summary_report()
        elif report_type == 'detailed':
            return self.reporter.generate_detailed_report()
        elif report_type == 'performance':
            return self.reporter.generate_performance_report()
        elif report_type == 'error':
            return self.reporter.generate_error_report()
        else:
            return {'error': f'Unknown report type: {report_type}'}
    
    def export_results(self, format: str = 'json') -> Dict[str, Any]:
        """Export all benchmark results."""
        return self.metrics.export_results(format)
    
    def clear_results(self) -> None:
        """Clear all benchmark results."""
        self.metrics.clear_results()
    
    def _determine_benchmark_type(self, func: Callable) -> BenchmarkType:
        """Determine benchmark type from function."""
        func_name = func.__name__.lower()
        
        if 'response' in func_name or 'time' in func_name:
            return BenchmarkType.RESPONSE_TIME
        elif 'throughput' in func_name or 'ops' in func_name:
            return BenchmarkType.THROUGHPUT
        elif 'memory' in func_name:
            return BenchmarkType.MEMORY_USAGE
        elif 'cpu' in func_name:
            return BenchmarkType.CPU_USAGE
        elif 'concurrent' in func_name or 'parallel' in func_name:
            return BenchmarkType.CONCURRENT_OPERATIONS
        elif 'error' in func_name or 'fail' in func_name:
            return BenchmarkType.ERROR_RATE
        else:
            return BenchmarkType.RESPONSE_TIME  # Default
