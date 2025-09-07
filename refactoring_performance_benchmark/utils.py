from pathlib import Path
from typing import Optional

        import psutil  # type: ignore
from __future__ import annotations

"""Shared constants and helper utilities for performance benchmarking.

This module centralizes configuration values and reusable helpers so that
all benchmark components follow a single source of truth (SSOT).
"""


# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

# Base directory for benchmark data relative to a workspace root
DATA_DIR = Path("data")
# Filenames for persisted results and suite definitions
RESULTS_FILENAME = "benchmark_results.json"
SUITES_FILENAME = "benchmark_suites.json"


def get_results_path(workspace: Path) -> Path:
    """Return the path to the benchmark results file.

    Args:
        workspace: Root path of the current workspace.
    """
    return workspace / DATA_DIR / RESULTS_FILENAME


def get_suites_path(workspace: Path) -> Path:
    """Return the path to the benchmark suites file.

    Args:
        workspace: Root path of the current workspace.
    """
    return workspace / DATA_DIR / SUITES_FILENAME


# ---------------------------------------------------------------------------
# System metrics helpers
# ---------------------------------------------------------------------------


def get_memory_usage() -> float:
    """Return current process memory usage in megabytes.

    Returns:
        Memory usage of the running process in MB. Returns ``0.0`` if the
        ``psutil`` dependency is unavailable.
    """
    try:

        return psutil.Process().memory_info().rss / 1024 / 1024
    except Exception:
        return 0.0


def get_cpu_usage() -> float:
    """Return current system-wide CPU utilization percentage.

    Returns:
        CPU usage percentage. Returns ``0.0`` if the ``psutil`` dependency is
        unavailable.
    """
    try:

        return psutil.cpu_percent(interval=0.1)
    except Exception:
        return 0.0
