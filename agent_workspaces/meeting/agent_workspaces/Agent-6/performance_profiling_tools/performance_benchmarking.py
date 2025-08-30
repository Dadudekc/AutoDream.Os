#!/usr/bin/env python3
"""
Performance Benchmarking System
Contract: V2-COMPLIANCE-005 - Performance Optimization Implementation
Agent: Agent-6 (Performance Optimization Manager)
Description: Comprehensive performance benchmarking and monitoring system
"""

import time
import statistics
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import cProfile
import pstats
import io
import psutil
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    """Result of a performance benchmark"""
    function_name: str
    execution_count: int
    total_time: float
    average_time: float
    min_time: float
    max_time: float
    standard_deviation: float
    memory_usage_start: float
    memory_usage_end: float
    memory_delta: float
    cpu_usage_start: float
    cpu_usage_end: float
    cpu_delta: float
    timestamp: str
    benchmark_id: str

@dataclass
class BenchmarkSuite:
    """Complete benchmark suite results"""
    suite_name: str
    total_functions: int
    total_executions: int
    total_time: float
    average_function_time: float
    fastest_function: str
    slowest_function: str
    memory_efficiency_rank: List[str]
    cpu_efficiency_rank: List[str]
    timestamp: str
    results: List[BenchmarkResult]

class PerformanceBenchmarking:
    """
    Performance Benchmarking System
    
    Features:
    - Automated function benchmarking
    - Memory and CPU usage tracking
    - Statistical analysis of results
    - Performance regression detection
    - Integration with existing profiling tools
    - V2 compliance optimization
    """

    def __init__(self, output_dir: str = "benchmark_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.benchmark_results: List[BenchmarkResult] = []
        self.benchmark_suites: List[BenchmarkSuite] = []
        self.active_benchmarks: Dict[str, Any] = {}
        
        # Benchmarking configuration
        self.default_iterations = 100
        self.warmup_iterations = 10
        self.performance_thresholds = {
            'regression_warning': 0.20,  # 20% performance regression
            'optimization_threshold': 0.10,  # 10% improvement
            'critical_regression': 0.50  # 50% performance regression
        }
        
        logger.info("Performance Benchmarking System initialized")

    def benchmark_function(self, func: Callable, *args, 
                         iterations: Optional[int] = None,
                         warmup: bool = True,
                         **kwargs) -> BenchmarkResult:
        """
        Benchmark a function with comprehensive metrics
        
        Args:
            func: Function to benchmark
            *args, **kwargs: Function arguments
            iterations: Number of benchmark iterations
            warmup: Whether to perform warmup runs
            
        Returns:
            Benchmark result with detailed metrics
        """
        if iterations is None:
            iterations = self.default_iterations
            
        function_name = func.__name__
        benchmark_id = f"{function_name}_{int(time.time())}"
        
        logger.info(f"Starting benchmark for {function_name} with {iterations} iterations")
        
        # Warmup phase
        if warmup:
            for _ in range(self.warmup_iterations):
                func(*args, **kwargs)
        
        # Measure initial system state
        start_memory = psutil.virtual_memory().percent
        start_cpu = psutil.cpu_percent()
        
        # Benchmark execution
        execution_times = []
        for _ in range(iterations):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_times.append(end_time - start_time)
        
        # Measure final system state
        end_memory = psutil.virtual_memory().percent
        end_cpu = psutil.cpu_percent()
        
        # Calculate statistics
        total_time = sum(execution_times)
        average_time = total_time / iterations
        min_time = min(execution_times)
        max_time = max(execution_times)
        std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        
        # Create benchmark result
        benchmark_result = BenchmarkResult(
            function_name=function_name,
            execution_count=iterations,
            total_time=total_time,
            average_time=average_time,
            min_time=min_time,
            max_time=max_time,
            standard_deviation=std_dev,
            memory_usage_start=start_memory,
            memory_usage_end=end_memory,
            memory_delta=end_memory - start_memory,
            cpu_usage_start=start_cpu,
            cpu_usage_end=end_cpu,
            cpu_delta=end_cpu - start_cpu,
            timestamp=datetime.now().isoformat(),
            benchmark_id=benchmark_id
        )
        
        self.benchmark_results.append(benchmark_result)
        logger.info(f"Benchmark completed for {function_name}: avg={average_time:.6f}s")
        
        return benchmark_result

    def benchmark_with_profiler(self, func: Callable, *args, 
                               iterations: int = 10,
                               **kwargs) -> Tuple[BenchmarkResult, Dict[str, Any]]:
        """
        Benchmark function with cProfile integration
        
        Args:
            func: Function to benchmark
            *args, **kwargs: Function arguments
            iterations: Number of profiling iterations
            
        Returns:
            Tuple of (benchmark_result, profiling_stats)
        """
        function_name = func.__name__
        logger.info(f"Starting profiled benchmark for {function_name}")
        
        # Create profiler
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Execute function multiple times
        start_time = time.time()
        for _ in range(iterations):
            result = func(*args, **kwargs)
        end_time = time.time()
        
        profiler.disable()
        
        # Get profiling statistics
        stats = pstats.Stats(profiler)
        stats_stream = io.StringIO()
        stats.stream = stats_stream
        stats.sort_stats('cumulative')
        stats.print_stats()
        
        profiling_stats = {
            'total_calls': stats.total_calls,
            'primitive_calls': stats.primitive_calls,
            'total_time': stats.total_tt,
            'cumulative_time': stats.total_cumulative_time,
            'detailed_stats': stats_stream.getvalue()
        }
        
        # Create benchmark result
        total_execution_time = end_time - start_time
        benchmark_result = BenchmarkResult(
            function_name=function_name,
            execution_count=iterations,
            total_time=total_execution_time,
            average_time=total_execution_time / iterations,
            min_time=total_execution_time / iterations,  # Simplified for profiled runs
            max_time=total_execution_time / iterations,
            standard_deviation=0.0,  # Not calculated for profiled runs
            memory_usage_start=psutil.virtual_memory().percent,
            memory_usage_end=psutil.virtual_memory().percent,
            memory_delta=0.0,
            cpu_usage_start=psutil.cpu_percent(),
            cpu_usage_end=psutil.cpu_percent(),
            cpu_delta=0.0,
            timestamp=datetime.now().isoformat(),
            benchmark_id=f"{function_name}_profiled_{int(time.time())}"
        )
        
        self.benchmark_results.append(benchmark_result)
        logger.info(f"Profiled benchmark completed for {function_name}")
        
        return benchmark_result, profiling_stats

    def run_benchmark_suite(self, functions: List[Tuple[Callable, tuple, dict]], 
                           suite_name: str = "Default Suite") -> BenchmarkSuite:
        """
        Run a complete benchmark suite
        
        Args:
            functions: List of (function, args, kwargs) tuples
            suite_name: Name of the benchmark suite
            
        Returns:
            Complete benchmark suite results
        """
        logger.info(f"Starting benchmark suite: {suite_name}")
        
        suite_results = []
        total_executions = 0
        total_time = 0
        
        for func, args, kwargs in functions:
            result = self.benchmark_function(func, *args, **kwargs)
            suite_results.append(result)
            total_executions += result.execution_count
            total_time += result.total_time
        
        # Analyze suite results
        if suite_results:
            fastest = min(suite_results, key=lambda x: x.average_time)
            slowest = max(suite_results, key=lambda x: x.average_time)
            
            # Rank by memory efficiency
            memory_efficient = sorted(suite_results, key=lambda x: abs(x.memory_delta))
            cpu_efficient = sorted(suite_results, key=lambda x: abs(x.cpu_delta))
            
            suite = BenchmarkSuite(
                suite_name=suite_name,
                total_functions=len(suite_results),
                total_executions=total_executions,
                total_time=total_time,
                average_function_time=total_time / total_executions if total_executions > 0 else 0,
                fastest_function=fastest.function_name,
                slowest_function=slowest.function_name,
                memory_efficiency_rank=[r.function_name for r in memory_efficient],
                cpu_efficiency_rank=[r.function_name for r in cpu_efficient],
                timestamp=datetime.now().isoformat(),
                results=suite_results
            )
            
            self.benchmark_suites.append(suite)
            logger.info(f"Benchmark suite completed: {suite_name}")
            
            return suite
        
        return None

    def detect_performance_regressions(self, baseline_suite: str, 
                                    current_suite: str) -> Dict[str, Any]:
        """
        Detect performance regressions between benchmark suites
        
        Args:
            baseline_suite: Name of baseline suite
            current_suite: Name of current suite
            
        Returns:
            Regression analysis results
        """
        baseline = next((s for s in self.benchmark_suites if s.suite_name == baseline_suite), None)
        current = next((s for s in self.benchmark_suites if s.suite_name == current_suite), None)
        
        if not baseline or not current:
            return {'error': 'One or both suites not found'}
        
        regressions = []
        improvements = []
        
        # Compare function performance
        baseline_results = {r.function_name: r for r in baseline.results}
        current_results = {r.function_name: r for r in current.results}
        
        for func_name in baseline_results:
            if func_name in current_results:
                baseline_time = baseline_results[func_name].average_time
                current_time = current_results[func_name].average_time
                
                if baseline_time > 0:
                    change_percent = (current_time - baseline_time) / baseline_time
                    
                    if change_percent > self.performance_thresholds['critical_regression']:
                        regressions.append({
                            'function': func_name,
                            'change_percent': change_percent * 100,
                            'severity': 'CRITICAL',
                            'baseline_time': baseline_time,
                            'current_time': current_time
                        })
                    elif change_percent > self.performance_thresholds['regression_warning']:
                        regressions.append({
                            'function': func_name,
                            'change_percent': change_percent * 100,
                            'severity': 'WARNING',
                            'baseline_time': baseline_time,
                            'current_time': current_time
                        })
                    elif change_percent < -self.performance_thresholds['optimization_threshold']:
                        improvements.append({
                            'function': func_name,
                            'change_percent': change_percent * 100,
                            'baseline_time': baseline_time,
                            'current_time': current_time
                        })
        
        return {
            'regressions': regressions,
            'improvements': improvements,
            'total_functions_analyzed': len(baseline_results),
            'regression_count': len(regressions),
            'improvement_count': len(improvements),
            'overall_performance_change': 'IMPROVED' if len(improvements) > len(regressions) else 'REGRESSED'
        }

    def generate_benchmark_report(self, suite_name: Optional[str] = None) -> str:
        """
        Generate comprehensive benchmark report
        
        Args:
            suite_name: Optional specific suite to report on
            
        Returns:
            Path to generated report
        """
        if suite_name:
            suite = next((s for s in self.benchmark_suites if s.suite_name == suite_name), None)
            if not suite:
                return f"Suite {suite_name} not found"
            
            report_data = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'benchmarker_version': '1.0.0',
                    'suite_name': suite_name
                },
                'suite_results': asdict(suite)
            }
        else:
            report_data = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'benchmarker_version': '1.0.0',
                    'total_suites': len(self.benchmark_suites),
                    'total_benchmarks': len(self.benchmark_results)
                },
                'all_suites': [asdict(suite) for suite in self.benchmark_suites],
                'all_benchmarks': [asdict(result) for result in self.benchmark_results]
            }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suite_suffix = f"_{suite_name}" if suite_name else ""
        output_file = self.output_dir / f"benchmark_report{suite_suffix}_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Benchmark report generated: {output_file}")
        return str(output_file)

    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmark results"""
        if not self.benchmark_results:
            return {'status': 'No benchmarks run'}
        
        return {
            'total_benchmarks': len(self.benchmark_results),
            'total_suites': len(self.benchmark_suites),
            'total_executions': sum(r.execution_count for r in self.benchmark_results),
            'total_time': sum(r.total_time for r in self.benchmark_results),
            'fastest_function': min(self.benchmark_results, key=lambda x: x.average_time).function_name,
            'slowest_function': max(self.benchmark_results, key=lambda x: x.average_time).function_name,
            'last_benchmark': max(r.timestamp for r in self.benchmark_results) if self.benchmark_results else 'Never'
        }

    def clear_benchmark_data(self):
        """Clear all benchmark data"""
        self.benchmark_results.clear()
        self.benchmark_suites.clear()
        self.active_benchmarks.clear()
        logger.info("Cleared all benchmark data")


# Convenience function for quick benchmarking
def quick_benchmark(func: Callable, *args, iterations: int = 100, **kwargs) -> BenchmarkResult:
    """
    Quick benchmarking of a function
    
    Args:
        func: Function to benchmark
        *args, **kwargs: Function arguments
        iterations: Number of benchmark iterations
        
    Returns:
        Benchmark result
    """
    benchmarker = PerformanceBenchmarking()
    return benchmarker.benchmark_function(func, *args, iterations=iterations, **kwargs)


if __name__ == "__main__":
    # Example usage
    def example_function():
        """Example function for benchmarking demonstration"""
        time.sleep(0.001)
        return sum(range(1000))
    
    def slow_function():
        """Slower function for comparison"""
        time.sleep(0.01)
        return sum(range(10000))
    
    # Create benchmarker instance
    benchmarker = PerformanceBenchmarking()
    
    # Run individual benchmarks
    result1 = benchmarker.benchmark_function(example_function, iterations=50)
    result2 = benchmarker.benchmark_function(slow_function, iterations=50)
    
    # Run benchmark suite
    functions = [
        (example_function, (), {}),
        (slow_function, (), {})
    ]
    
    suite = benchmarker.run_benchmark_suite(functions, "Example Suite")
    
    # Generate report
    report_file = benchmarker.generate_benchmark_report("Example Suite")
    print(f"Benchmark report generated: {report_file}")
    
    # Show summary
    summary = benchmarker.get_benchmark_summary()
    print(f"Benchmark summary: {summary}")
