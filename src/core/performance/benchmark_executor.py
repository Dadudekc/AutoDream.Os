#!/usr/bin/env python3
"""
Performance Benchmark Executor - Unified Benchmark Execution System
==================================================================

Performance benchmark execution logic extracted from orchestrator.
Follows Single Responsibility Principle with focused execution functionality.

Author: Agent-3 (Performance Refactoring)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .performance_core import BenchmarkResult
from .metrics_collector import PerformanceMetricsCollector, MetricsConfig


@dataclass
class BenchmarkExecutionConfig:
    """Configuration for benchmark execution."""
    benchmark_type: str
    timeout_seconds: int = 300
    max_iterations: int = 5
    warmup_iterations: int = 2
    target_metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.target_metrics is None:
            self.target_metrics = {}


class BenchmarkExecutor:
    """
    Performance benchmark execution system.
    
    Responsibilities:
    - Execute individual benchmarks
    - Manage benchmark lifecycle
    - Coordinate with metrics collector
    - Handle benchmark errors and timeouts
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.BenchmarkExecutor")
        self.metrics_collector = PerformanceMetricsCollector()
        self.execution_history: List[BenchmarkResult] = []
    
    def execute_benchmark(
        self, 
        benchmark_type: str, 
        config: BenchmarkExecutionConfig,
        core_validator: Any
    ) -> Optional[BenchmarkResult]:
        """
        Execute a single benchmark.
        
        Args:
            benchmark_type: Type of benchmark to run
            config: Benchmark execution configuration
            core_validator: Core validation system for creating results
            
        Returns:
            BenchmarkResult if successful, None otherwise
        """
        try:
            self.logger.info(f"Executing {benchmark_type} benchmark...")
            
            # Get benchmark configuration
            if not config:
                self.logger.warning(f"Benchmark type '{benchmark_type}' has no configuration")
                return None
            
            # Execute benchmark with configuration
            start_time = datetime.now()
            
            # Convert to metrics config
            metrics_config = MetricsConfig(
                max_iterations=config.max_iterations,
                warmup_iterations=config.warmup_iterations,
                timeout_seconds=config.timeout_seconds
            )
            
            # Execute benchmark and collect metrics
            metrics = self.metrics_collector.execute_benchmark(benchmark_type, metrics_config)
            
            end_time = datetime.now()
            
            # Create benchmark result
            result = core_validator.create_benchmark_result(
                benchmark_type=benchmark_type,
                metrics=metrics,
                start_time=start_time,
                end_time=end_time
            )
            
            # Store in execution history
            self.execution_history.append(result)
            
            self.logger.info(
                f"Benchmark {benchmark_type} completed: "
                f"{result.performance_level} level in {result.duration:.2f}s"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing {benchmark_type} benchmark: {e}")
            return None
    
    def execute_benchmark_suite(
        self, 
        benchmark_types: List[str], 
        configs: Dict[str, BenchmarkExecutionConfig],
        core_validator: Any
    ) -> List[BenchmarkResult]:
        """
        Execute a suite of benchmarks.
        
        Args:
            benchmark_types: List of benchmark types to execute
            configs: Configuration for each benchmark type
            core_validator: Core validation system for creating results
            
        Returns:
            List of benchmark results
        """
        try:
            self.logger.info(f"Executing benchmark suite with {len(benchmark_types)} benchmarks")
            
            benchmark_results = []
            
            for benchmark_type in benchmark_types:
                try:
                    config = configs.get(benchmark_type)
                    if not config:
                        self.logger.warning(f"No configuration found for {benchmark_type}")
                        continue
                    
                    # Execute individual benchmark
                    result = self.execute_benchmark(benchmark_type, config, core_validator)
                    if result:
                        benchmark_results.append(result)
                    else:
                        self.logger.error(f"Failed to execute {benchmark_type} benchmark")
                    
                except Exception as e:
                    self.logger.error(f"Error executing {benchmark_type} benchmark: {e}")
                    continue
            
            self.logger.info(f"Benchmark suite completed: {len(benchmark_results)} successful")
            return benchmark_results
            
        except Exception as e:
            self.logger.error(f"Error executing benchmark suite: {e}")
            return []
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get summary of benchmark executions.
        
        Returns:
            Execution summary statistics
        """
        if not self.execution_history:
            return {"message": "No benchmark executions in history"}
        
        try:
            # Calculate summary statistics
            total_executions = len(self.execution_history)
            successful_executions = len([r for r in self.execution_history if r is not None])
            failed_executions = total_executions - successful_executions
            
            # Performance level distribution
            performance_levels = {}
            benchmark_types = {}
            
            for result in self.execution_history:
                if result:
                    # Count performance levels
                    level = result.performance_level
                    performance_levels[level] = performance_levels.get(level, 0) + 1
                    
                    # Count benchmark types
                    btype = result.benchmark_type
                    benchmark_types[btype] = benchmark_types.get(btype, 0) + 1
            
            # Calculate average duration
            total_duration = sum(result.duration for result in self.execution_history if result)
            avg_duration = total_duration / successful_executions if successful_executions > 0 else 0
            
            return {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": (successful_executions / total_executions) * 100 if total_executions > 0 else 0,
                "total_duration": total_duration,
                "average_duration": avg_duration,
                "performance_level_distribution": performance_levels,
                "benchmark_type_distribution": benchmark_types
            }
            
        except Exception as e:
            self.logger.error(f"Error generating execution summary: {e}")
            return {"error": str(e)}
    
    def clear_execution_history(self) -> None:
        """Clear the execution history."""
        self.execution_history.clear()
        self.logger.info("Execution history cleared")
    
    def get_benchmark_config(self, benchmark_type: str) -> Optional[BenchmarkExecutionConfig]:
        """
        Get default configuration for a benchmark type.
        
        Args:
            benchmark_type: Type of benchmark
            
        Returns:
            Default configuration or None if not supported
        """
        # Default configurations for common benchmark types
        default_configs = {
            "response_time": BenchmarkExecutionConfig(
                benchmark_type="response_time",
                timeout_seconds=60,
                max_iterations=10,
                warmup_iterations=2
            ),
            "throughput": BenchmarkExecutionConfig(
                benchmark_type="throughput",
                timeout_seconds=120,
                max_iterations=8,
                warmup_iterations=3
            ),
            "scalability": BenchmarkExecutionConfig(
                benchmark_type="scalability",
                timeout_seconds=180,
                max_iterations=6,
                warmup_iterations=2
            ),
            "reliability": BenchmarkExecutionConfig(
                benchmark_type="reliability",
                timeout_seconds=300,
                max_iterations=12,
                warmup_iterations=4
            ),
            "resource": BenchmarkExecutionConfig(
                benchmark_type="resource",
                timeout_seconds=90,
                max_iterations=7,
                warmup_iterations=2
            )
        }
        
        return default_configs.get(benchmark_type)
    
    def validate_benchmark_config(self, config: BenchmarkExecutionConfig) -> List[str]:
        """
        Validate benchmark execution configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if config.timeout_seconds <= 0:
            errors.append("Timeout must be positive")
        
        if config.max_iterations <= 0:
            errors.append("Max iterations must be positive")
        
        if config.warmup_iterations < 0:
            errors.append("Warmup iterations cannot be negative")
        
        if config.warmup_iterations >= config.max_iterations:
            errors.append("Warmup iterations must be less than max iterations")
        
        if config.timeout_seconds < config.max_iterations * 10:  # Rough estimate
            errors.append("Timeout may be too short for the number of iterations")
        
        return errors
