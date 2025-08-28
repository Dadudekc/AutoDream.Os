"""Common metric definitions for performance modules.

Centralises metric enums and default configurations so that different
performance modules share the same source of truth.  This avoids metric
string duplication throughout the codebase and ensures consistent
behaviour when calculating scores or setting benchmark targets.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict


class BenchmarkType(str, Enum):
    """Supported benchmark categories."""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    RESOURCE_UTILIZATION = "resource_utilization"
    LATENCY = "latency"


class PerformanceLevel(str, Enum):
    """Performance level classifications shared across modules."""

    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"
    DEVELOPMENT_READY = "development_ready"
    NOT_READY = "not_ready"


# Default weights used when calculating overall performance scores.  The
# dictionary keys intentionally use the ``value`` of ``BenchmarkType`` so it
# can be accessed easily even when only the string value is available.
DEFAULT_METRIC_WEIGHTS: Dict[str, float] = {
    BenchmarkType.RESPONSE_TIME.value: 0.25,
    BenchmarkType.THROUGHPUT.value: 0.25,
    BenchmarkType.SCALABILITY.value: 0.20,
    BenchmarkType.RELIABILITY.value: 0.20,
    BenchmarkType.LATENCY.value: 0.10,
}


# Default benchmark targets used by ``MetricsCollector`` and other modules.
# The dictionary uses ``BenchmarkType`` keys because those callers typically
# work directly with the enum.
DEFAULT_BENCHMARK_TARGETS: Dict[BenchmarkType, Dict[str, float]] = {
    BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
    BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
    BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
    BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
    BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
}


__all__ = [
    "BenchmarkType",
    "PerformanceLevel",
    "DEFAULT_METRIC_WEIGHTS",
    "DEFAULT_BENCHMARK_TARGETS",
]

