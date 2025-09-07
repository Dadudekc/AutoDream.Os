"""Benchmark setup utilities.

Contains dataclasses for benchmark entities and helpers for loading,
saving and creating benchmark suites.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .utils import get_results_path, get_suites_path


@dataclass
class BenchmarkResult:
    """Result of a single benchmark execution."""

    benchmark_id: str
    operation_name: str
    file_path: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    lines_processed: int
    efficiency_score: float
    improvement_percentage: float
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class BenchmarkSuite:
    """Collection of related benchmarks to run together."""

    suite_id: str
    name: str
    description: str
    benchmarks: List[Dict[str, Any]]
    target_files: List[str]
    expected_improvements: Dict[str, float]
    created_at: datetime
    execution_count: int = 0
    average_suite_score: float = 0.0


def load_benchmark_data(
    workspace: Path,
) -> Tuple[Dict[str, BenchmarkResult], Dict[str, BenchmarkSuite]]:
    """Load benchmark results and suites from disk."""
    results: Dict[str, BenchmarkResult] = {}
    suites: Dict[str, BenchmarkSuite] = {}

    results_path = get_results_path(workspace)
    suites_path = get_suites_path(workspace)

    if results_path.exists():
        with open(results_path, "r") as f:
            for item in json.load(f).get("benchmark_results", []):
                results[item["benchmark_id"]] = BenchmarkResult(**item)

    if suites_path.exists():
        with open(suites_path, "r") as f:
            for item in json.load(f).get("benchmark_suites", []):
                suites[item["suite_id"]] = BenchmarkSuite(**item)

    return results, suites


def save_benchmark_data(
    workspace: Path,
    results: Dict[str, BenchmarkResult],
    suites: Dict[str, BenchmarkSuite],
) -> None:
    """Persist benchmark results and suites to disk."""
    results_path = get_results_path(workspace)
    suites_path = get_suites_path(workspace)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    suites_path.parent.mkdir(parents=True, exist_ok=True)

    with open(results_path, "w") as f:
        json.dump(
            {"benchmark_results": [asdict(r) for r in results.values()]},
            f,
            indent=2,
            default=str,
        )

    with open(suites_path, "w") as f:
        json.dump(
            {"benchmark_suites": [asdict(s) for s in suites.values()]},
            f,
            indent=2,
            default=str,
        )


def create_benchmark_suite(
    name: str,
    description: str,
    benchmarks: List[Dict[str, Any]],
    target_files: List[str],
    expected_improvements: Dict[str, float],
) -> BenchmarkSuite:
    """Create a new benchmark suite with a unique identifier."""
    suite_id = f"SUITE_{int(time.time())}"
    return BenchmarkSuite(
        suite_id=suite_id,
        name=name,
        description=description,
        benchmarks=benchmarks,
        target_files=target_files,
        expected_improvements=expected_improvements,
        created_at=datetime.now(),
    )
