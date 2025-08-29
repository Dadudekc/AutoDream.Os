"""Benchmark harness for executing refactoring performance tests.

This module provides a small utility for running a single benchmarked
operation.  It measures execution time, memory consumption and CPU
usage, delegating metric calculations to :mod:`metrics`.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from . import metrics


@dataclass
class BenchmarkResult:
    """Simple container for benchmark information."""

    operation_name: str
    file_path: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    efficiency_score: float
    improvement_percentage: float
    timestamp: datetime
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Return the result as a plain dictionary."""
        return asdict(self)


class BenchmarkHarness:
    """Run operations while collecting basic performance data."""

    def run(
        self,
        operation_name: str,
        file_path: str,
        operation_func: Callable[[], Any],
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
    ) -> BenchmarkResult:
        """Execute ``operation_func`` and return a :class:`BenchmarkResult`."""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()

        result = operation_func()

        end_time = time.time()
        end_memory = self._get_memory_usage()
        end_cpu = self._get_cpu_usage()

        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        cpu_usage = (start_cpu + end_cpu) / 2

        efficiency = metrics.calculate_efficiency_score(
            execution_time,
            memory_usage,
            cpu_usage,
            before_state,
            after_state,
        )
        improvement = metrics.calculate_improvement_percentage(
            before_state, after_state
        )

        metadata = result if isinstance(result, dict) else {"result": result}

        return BenchmarkResult(
            operation_name=operation_name,
            file_path=file_path,
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            efficiency_score=efficiency,
            improvement_percentage=improvement,
            timestamp=datetime.now(),
            metadata=metadata,
        )

    @staticmethod
    def _get_memory_usage() -> float:
        """Return the current memory usage in megabytes."""
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0

    @staticmethod
    def _get_cpu_usage() -> float:
        """Return current CPU utilisation percentage."""
        try:
            import psutil

            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0.0
