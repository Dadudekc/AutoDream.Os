#!/usr/bin/env python3
"""
Performance Benchmark Runner - V2 Modular Architecture
=====================================================

Handles all benchmark execution logic.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List

from .benchmark_types import BenchmarkType, BenchmarkResult, BenchmarkMetrics
from .templates import TEMPLATES
from ..validation.validation_types import ValidationRule, ValidationSeverity


logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """
    Benchmark Runner - Single responsibility: Execute performance benchmarks
    
    Handles all benchmark execution logic including:
    - CPU, Memory, Disk, Network benchmarks
    - Response time and throughput testing
    - Concurrency and stress testing
    - Result validation and classification
    """

    def __init__(self):
        """Initialize benchmark runner"""
        self.logger = logging.getLogger(f"{__name__}.BenchmarkRunner")
        self.benchmark_history: List[BenchmarkResult] = []
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0

    def run_benchmark(self, benchmark_type: BenchmarkType, duration: int = 30, **kwargs) -> BenchmarkResult:
        """Run a performance benchmark"""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            self.logger.info(f"🚀 Starting {benchmark_type.value} benchmark: {benchmark_id}")

            # Execute benchmark using templates
            template = TEMPLATES.get(benchmark_type, TEMPLATES[BenchmarkType.GENERIC])
            metrics = template(duration, **kwargs)
            
            end_time = datetime.now()
            duration_actual = (end_time - start_time).total_seconds()
            
            # Create benchmark result
            result = BenchmarkResult(
                id=benchmark_id,
                name=benchmark_type.value,
                component=benchmark_type.value,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration_actual,
                iterations=1,
                metrics=metrics,
                success=True,
                error_message=None
            )
            
            # Store result
            self.benchmark_history.append(result)
            self.total_benchmarks_run += 1
            self.successful_benchmarks += 1
            
            self.logger.info(f"✅ Benchmark {benchmark_id} completed successfully in {duration_actual:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Benchmark failed: {e}")
            
            # Create failed result
            result = BenchmarkResult(
                id=benchmark_id if 'benchmark_id' in locals() else str(uuid.uuid4()),
                name=benchmark_type.value,
                component=benchmark_type.value,
                start_time=start_time.isoformat() if 'start_time' in locals() else datetime.now().isoformat(),
                end_time=datetime.now().isoformat(),
                duration=0.0,
                iterations=0,
                metrics={},
                success=False,
                error_message=str(e)
            )
            
            self.benchmark_history.append(result)
            self.total_benchmarks_run += 1
            self.failed_benchmarks += 1
            
            return result


    def get_benchmark(self, benchmark_id: str) -> Optional[BenchmarkResult]:
        """Get specific benchmark result"""
        for benchmark in self.benchmark_history:
            if benchmark.id == benchmark_id:
                return benchmark
        return None

    def list_benchmarks(self) -> List[BenchmarkResult]:
        """List all benchmark results"""
        return self.benchmark_history.copy()

    def clear_history(self) -> None:
        """Clear benchmark history"""
        self.benchmark_history.clear()
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.logger.info("✅ Benchmark history cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """Get benchmark statistics"""
        return {
            "total_benchmarks": self.total_benchmarks_run,
            "successful_benchmarks": self.successful_benchmarks,
            "failed_benchmarks": self.failed_benchmarks,
            "success_rate": round(self.successful_benchmarks / max(self.total_benchmarks_run, 1), 3)
        }
