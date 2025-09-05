"""
Performance Benchmark Models
===========================

Data models for performance benchmarking.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum


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
    test_name: str
    value: float
    unit: str
    timestamp: datetime
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark execution."""
    iterations: int = 10
    warmup_iterations: int = 2
    timeout_seconds: int = 30
    concurrent_workers: int = 1
    memory_limit_mb: int = 512
    cpu_limit_percent: int = 80


@dataclass
class BenchmarkSuite:
    """Collection of related benchmarks."""
    name: str
    description: str
    benchmarks: List[Callable]
    config: BenchmarkConfig
    created_at: datetime


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""
    average_value: float
    min_value: float
    max_value: float
    median_value: float
    standard_deviation: float
    percentile_95: float
    percentile_99: float
    total_iterations: int
    successful_iterations: int
    failed_iterations: int
    success_rate: float


class BenchmarkModels:
    """Benchmark models and validation."""
    
    @staticmethod
    def create_benchmark_result(
        benchmark_type: BenchmarkType,
        test_name: str,
        value: float,
        unit: str,
        metadata: Dict[str, Any] = None,
        success: bool = True,
        error_message: str = None
    ) -> BenchmarkResult:
        """Create a benchmark result."""
        return BenchmarkResult(
            benchmark_type=benchmark_type,
            test_name=test_name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            metadata=metadata or {},
            success=success,
            error_message=error_message
        )
    
    @staticmethod
    def create_benchmark_config(
        iterations: int = 10,
        warmup_iterations: int = 2,
        timeout_seconds: int = 30,
        concurrent_workers: int = 1,
        memory_limit_mb: int = 512,
        cpu_limit_percent: int = 80
    ) -> BenchmarkConfig:
        """Create benchmark configuration."""
        return BenchmarkConfig(
            iterations=iterations,
            warmup_iterations=warmup_iterations,
            timeout_seconds=timeout_seconds,
            concurrent_workers=concurrent_workers,
            memory_limit_mb=memory_limit_mb,
            cpu_limit_percent=cpu_limit_percent
        )
    
    @staticmethod
    def create_benchmark_suite(
        name: str,
        description: str,
        benchmarks: List[Callable],
        config: BenchmarkConfig = None
    ) -> BenchmarkSuite:
        """Create a benchmark suite."""
        return BenchmarkSuite(
            name=name,
            description=description,
            benchmarks=benchmarks,
            config=config or BenchmarkModels.create_benchmark_config(),
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_performance_metrics(
        values: List[float],
        total_iterations: int,
        successful_iterations: int
    ) -> PerformanceMetrics:
        """Create performance metrics from values."""
        if not values:
            return PerformanceMetrics(
                average_value=0.0,
                min_value=0.0,
                max_value=0.0,
                median_value=0.0,
                standard_deviation=0.0,
                percentile_95=0.0,
                percentile_99=0.0,
                total_iterations=total_iterations,
                successful_iterations=successful_iterations,
                failed_iterations=total_iterations - successful_iterations,
                success_rate=(successful_iterations / total_iterations * 100) if total_iterations > 0 else 0.0
            )
        
        sorted_values = sorted(values)
        n = len(values)
        
        # Calculate basic statistics
        average_value = sum(values) / n
        min_value = min(values)
        max_value = max(values)
        
        # Calculate median
        if n % 2 == 0:
            median_value = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            median_value = sorted_values[n//2]
        
        # Calculate standard deviation
        variance = sum((x - average_value) ** 2 for x in values) / n
        standard_deviation = variance ** 0.5
        
        # Calculate percentiles
        percentile_95 = sorted_values[int(n * 0.95)] if n > 0 else 0.0
        percentile_99 = sorted_values[int(n * 0.99)] if n > 0 else 0.0
        
        return PerformanceMetrics(
            average_value=average_value,
            min_value=min_value,
            max_value=max_value,
            median_value=median_value,
            standard_deviation=standard_deviation,
            percentile_95=percentile_95,
            percentile_99=percentile_99,
            total_iterations=total_iterations,
            successful_iterations=successful_iterations,
            failed_iterations=total_iterations - successful_iterations,
            success_rate=(successful_iterations / total_iterations * 100) if total_iterations > 0 else 0.0
        )
