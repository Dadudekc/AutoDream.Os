#!/usr/bin/env python3
"""
Benchmark Service
================

Core benchmarking functionality for refactoring performance measurement.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import BenchmarkResult, PerformanceMetrics, BenchmarkSuite


class BenchmarkService:
    """Core benchmarking service for performance measurement"""
    
    def __init__(self):
        self.benchmark_results: Dict[str, BenchmarkResult] = {}
        self.benchmark_suites: Dict[str, BenchmarkSuite] = {}
        self.metrics = PerformanceMetrics()
        self.execution_pool = ThreadPoolExecutor(max_workers=4)
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def run_benchmark(self, operation_name: str, operation_func: Callable, 
                     file_path: str, **kwargs) -> BenchmarkResult:
        """Run a performance benchmark for an operation"""
        try:
            benchmark_id = str(uuid.uuid4())
            self.logger.info(f"Starting benchmark {benchmark_id} for {operation_name}")
            
            # Measure before state
            before_memory = self._get_memory_usage()
            before_cpu = self._get_cpu_usage()
            start_time = time.time()
            
            # Execute operation
            result = operation_func(**kwargs)
            
            # Measure after state
            end_time = time.time()
            after_memory = self._get_memory_usage()
            after_cpu = self._get_cpu_usage()
            
            # Calculate metrics
            execution_time = end_time - start_time
            memory_usage = after_memory - before_memory
            cpu_usage = (before_cpu + after_cpu) / 2
            lines_processed = self._count_lines(file_path)
            efficiency_score = self._calculate_efficiency_score(execution_time, memory_usage, lines_processed)
            improvement_percentage = self._calculate_improvement_percentage(execution_time, memory_usage)
            
            # Create benchmark result
            benchmark_result = BenchmarkResult(
                benchmark_id=benchmark_id,
                operation_name=operation_name,
                file_path=file_path,
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                lines_processed=lines_processed,
                efficiency_score=efficiency_score,
                improvement_percentage=improvement_percentage,
                timestamp=datetime.now(),
                metadata={"result": result}
            )
            
            # Store result
            self.benchmark_results[benchmark_id] = benchmark_result
            self._update_metrics(benchmark_result)
            
            self.logger.info(f"Benchmark {benchmark_id} completed: {efficiency_score:.2f}% efficiency")
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Benchmark failed for {operation_name}: {e}")
            raise
    
    def run_benchmark_suite(self, suite: BenchmarkSuite) -> List[BenchmarkResult]:
        """Run a complete benchmark suite"""
        results = []
        self.logger.info(f"Starting benchmark suite: {suite.name}")
        
        try:
            # Execute benchmarks in parallel
            future_to_benchmark = {}
            for benchmark in suite.benchmarks:
                future = self.execution_pool.submit(
                    self._execute_suite_benchmark,
                    benchmark,
                    suite.target_files
                )
                future_to_benchmark[future] = benchmark
            
            # Collect results
            for future in as_completed(future_to_benchmark):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    benchmark = future_to_benchmark[future]
                    self.logger.error(f"Suite benchmark failed: {e}")
            
            # Update suite statistics
            suite.execution_count += 1
            if results:
                suite.average_suite_score = sum(r.efficiency_score for r in results) / len(results)
            
            self.logger.info(f"Benchmark suite {suite.name} completed: {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Benchmark suite failed: {e}")
            return results
    
    def _execute_suite_benchmark(self, benchmark: Dict[str, Any], target_files: List[str]) -> Optional[BenchmarkResult]:
        """Execute a single benchmark from a suite"""
        try:
            operation_name = benchmark.get('operation_name', 'unknown')
            operation_func = benchmark.get('operation_func')
            file_path = benchmark.get('file_path', target_files[0] if target_files else '')
            
            if operation_func and callable(operation_func):
                return self.run_benchmark(operation_name, operation_func, file_path)
            else:
                self.logger.warning(f"Invalid operation function for benchmark: {operation_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Suite benchmark execution failed: {e}")
            return None
    
    def _count_lines(self, file_path: str) -> int:
        """Count lines in a file"""
        try:
            path = Path(file_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return len(f.readlines())
            return 0
        except Exception:
            return 0
    
    def _calculate_efficiency_score(self, execution_time: float, memory_usage: float, lines_processed: int) -> float:
        """Calculate efficiency score (0-100)"""
        try:
            # Base score on execution time and memory usage
            time_score = max(0, 100 - (execution_time * 10))  # Penalize slow operations
            memory_score = max(0, 100 - (memory_usage / 10))  # Penalize high memory usage
            lines_score = min(100, lines_processed / 10)  # Reward processing more lines
            
            # Weighted average
            efficiency = (time_score * 0.4 + memory_score * 0.4 + lines_score * 0.2)
            return max(0, min(100, efficiency))
            
        except Exception:
            return 50.0  # Default score
    
    def _calculate_improvement_percentage(self, execution_time: float, memory_usage: float) -> float:
        """Calculate improvement percentage"""
        try:
            # This is a simplified calculation
            # In a real implementation, you'd compare with baseline metrics
            baseline_time = 1.0  # 1 second baseline
            baseline_memory = 100.0  # 100MB baseline
            
            time_improvement = ((baseline_time - execution_time) / baseline_time) * 100
            memory_improvement = ((baseline_memory - memory_usage) / baseline_memory) * 100
            
            return (time_improvement + memory_improvement) / 2
            
        except Exception:
            return 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0
        except Exception:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0
    
    def _update_metrics(self, result: BenchmarkResult):
        """Update aggregated metrics with new benchmark result"""
        try:
            # Update averages
            n = self.metrics.total_benchmarks
            if n == 0:
                self.metrics.average_execution_time = result.execution_time
                self.metrics.average_memory_usage = result.memory_usage
                self.metrics.average_cpu_usage = result.cpu_usage
                self.metrics.average_efficiency_score = result.efficiency_score
            else:
                self.metrics.average_execution_time = (
                    (self.metrics.average_execution_time * (n-1) + result.execution_time) / n
                )
                self.metrics.average_memory_usage = (
                    (self.metrics.average_memory_usage * (n-1) + result.memory_usage) / n
                )
                self.metrics.average_cpu_usage = (
                    (self.metrics.average_cpu_usage * (n-1) + result.cpu_usage) / n
                )
                self.metrics.average_efficiency_score = (
                    (self.metrics.average_efficiency_score * (n-1) + result.efficiency_score) / n
                )
            
            # Update totals
            self.metrics.total_benchmarks += 1
            self.metrics.total_improvement += result.improvement_percentage
            
            # Update fastest/slowest
            if (not self.metrics.fastest_operation or 
                result.execution_time < self.benchmark_results[self.metrics.fastest_operation].execution_time):
                self.metrics.fastest_operation = result.benchmark_id
            
            if (not self.metrics.slowest_operation or 
                result.execution_time > self.benchmark_results[self.metrics.slowest_operation].execution_time):
                self.metrics.slowest_operation = result.benchmark_id
            
            # Update most efficient
            if (not self.metrics.most_efficient_operation or 
                result.efficiency_score > self.benchmark_results[self.metrics.most_efficient_operation].efficiency_score):
                self.metrics.most_efficient_operation = result.benchmark_id
                
        except Exception as e:
            self.logger.error(f"Failed to update metrics: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        return {
            "performance_metrics": self.metrics.__dict__,
            "recent_benchmarks": [
                result.__dict__ for result in 
                sorted(self.benchmark_results.values(), 
                       key=lambda x: x.timestamp, reverse=True)[:10]
            ],
            "benchmark_suites": len(self.benchmark_suites),
            "total_results": len(self.benchmark_results),
            "system_status": "operational"
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.execution_pool.shutdown(wait=True)
