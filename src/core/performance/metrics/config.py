
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration constants for performance metrics."""

from __future__ import annotations

from .benchmarks import BenchmarkType

DEFAULT_COLLECTION_INTERVAL = 60

DEFAULT_BENCHMARK_TARGETS = {
    BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
    BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
    BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
    BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
    BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
}
