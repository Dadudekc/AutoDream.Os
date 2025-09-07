"""Benchmark execution helpers."""
from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Callable

from .setup import BenchmarkResult
from .utils import get_cpu_usage, get_memory_usage


def run_single_benchmark(
    operation_name: str, file_path: str, operation_func: Callable[[], Any]
) -> BenchmarkResult:
    """Execute a single benchmark operation and capture metrics.

    Args:
        operation_name: Descriptive name of the operation being measured.
        file_path: Path to the file being processed.
        operation_func: Callable performing the operation under test.

    Returns:
        BenchmarkResult containing timing and system resource data.
    """
    benchmark_id = f"BENCH_{int(time.time())}"
    start_time = time.time()
    start_mem = get_memory_usage()
    start_cpu = get_cpu_usage()

    operation_func()

    end_time = time.time()
    end_mem = get_memory_usage()
    end_cpu = get_cpu_usage()

    return BenchmarkResult(
        benchmark_id=benchmark_id,
        operation_name=operation_name,
        file_path=file_path,
        execution_time=end_time - start_time,
        memory_usage=max(0.0, end_mem - start_mem),
        cpu_usage=max(start_cpu, end_cpu),
        lines_processed=0,
        efficiency_score=0.0,
        improvement_percentage=0.0,
        timestamp=datetime.now(),
        metadata={},
    )
