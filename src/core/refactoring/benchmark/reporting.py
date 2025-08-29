"""Simple reporting helpers for benchmark results."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, List

from .harness import BenchmarkResult


def generate_report(results: Iterable[BenchmarkResult]) -> Dict[str, Any]:
    """Aggregate benchmark ``results`` into a summary dictionary."""
    results_list: List[BenchmarkResult] = list(results)
    if not results_list:
        return {
            "total_benchmarks": 0,
            "average_execution_time": 0.0,
            "average_memory_usage": 0.0,
            "average_cpu_usage": 0.0,
            "average_efficiency_score": 0.0,
            "total_improvement": 0.0,
            "results": [],
        }

    total = len(results_list)
    avg_exec = sum(r.execution_time for r in results_list) / total
    avg_mem = sum(r.memory_usage for r in results_list) / total
    avg_cpu = sum(r.cpu_usage for r in results_list) / total
    avg_eff = sum(r.efficiency_score for r in results_list) / total
    total_improvement = sum(r.improvement_percentage for r in results_list)

    return {
        "total_benchmarks": total,
        "average_execution_time": avg_exec,
        "average_memory_usage": avg_mem,
        "average_cpu_usage": avg_cpu,
        "average_efficiency_score": avg_eff,
        "total_improvement": total_improvement,
        "results": [asdict(r) for r in results_list],
    }
