"""Utilities for providing mock test data."""

from __future__ import annotations

from typing import Any, Dict


def get_performance_test_data() -> Dict[str, Any]:
    """Return sample performance metrics for tests."""
    return {"metrics": {"latency_ms": 0, "throughput_rps": 0}}
