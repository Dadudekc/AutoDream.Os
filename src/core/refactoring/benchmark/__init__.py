"""Lightweight benchmarking framework for refactoring tools."""
from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Tuple, Any

from .harness import BenchmarkHarness, BenchmarkResult
from .reporting import generate_report

BenchmarkSpec = Tuple[str, str, Callable[[], Any], Dict[str, Any], Dict[str, Any]]


def run_benchmarks(benchmarks: Iterable[BenchmarkSpec]) -> Dict[str, Any]:
    """Execute ``benchmarks`` and return an aggregated report.

    Each benchmark specification is a tuple containing
    ``(operation_name, file_path, operation_func, before_state, after_state)``.
    """
    harness = BenchmarkHarness()
    results: List[BenchmarkResult] = []
    for op_name, file_path, func, before, after in benchmarks:
        results.append(
            harness.run(
                operation_name=op_name,
                file_path=file_path,
                operation_func=func,
                before_state=before,
                after_state=after,
            )
        )
    return generate_report(results)


__all__ = ["BenchmarkHarness", "BenchmarkResult", "run_benchmarks"]
