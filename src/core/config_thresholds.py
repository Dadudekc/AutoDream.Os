"""Threshold Configuration - Extracted from unified_config.py | Agent-5 C-056"""

from dataclasses import dataclass
from typing import Any

from .config_core import get_config


@dataclass
class ThresholdConfig:
    """Centralized threshold and alert configurations."""

    # Quality monitoring thresholds
    test_failure_threshold: int = get_config("TEST_FAILURE_THRESHOLD", 0)
    performance_degradation_threshold: float = get_config(
        "PERFORMANCE_DEGRADATION_THRESHOLD", 100.0
    )
    coverage_threshold: float = get_config("COVERAGE_THRESHOLD", 80.0)

    # Performance benchmark targets
    response_time_target: float = get_config("RESPONSE_TIME_TARGET", 100.0)  # ms
    throughput_target: float = get_config("THROUGHPUT_TARGET", 1000.0)  # ops/sec
    scalability_target: int = get_config("SCALABILITY_TARGET", 100)  # concurrent users
    reliability_target: float = get_config("RELIABILITY_TARGET", 99.9)  # %
    latency_target: float = get_config("LATENCY_TARGET", 50.0)  # ms

    # Messaging performance thresholds
    single_message_timeout: float = get_config("SINGLE_MESSAGE_TIMEOUT", 1.0)
    bulk_message_timeout: float = get_config("BULK_MESSAGE_TIMEOUT", 10.0)
    concurrent_message_timeout: float = get_config("CONCURRENT_MESSAGE_TIMEOUT", 5.0)
    min_throughput: float = get_config("MIN_THROUGHPUT", 10.0)
    max_memory_per_message: int = get_config("MAX_MEMORY_PER_MESSAGE", 1024)

    @property
    def alert_rules(self) -> dict[str, dict[str, Any]]:
        """Get quality alert rules."""
        return {
            "test_failure": {
                "threshold": self.test_failure_threshold,
                "severity": "high",
                "message": "Test failures detected",
            },
            "performance_degradation": {
                "threshold": self.performance_degradation_threshold,
                "severity": "medium",
                "message": "Performance degradation detected",
            },
            "low_coverage": {
                "threshold": self.coverage_threshold,
                "severity": "medium",
                "message": "Test coverage below threshold",
            },
        }

    @property
    def benchmark_targets(self) -> dict[str, dict[str, Any]]:
        """Get performance benchmark targets."""
        return {
            "response_time": {"target": self.response_time_target, "unit": "ms"},
            "throughput": {"target": self.throughput_target, "unit": "ops/sec"},
            "scalability": {"target": self.scalability_target, "unit": "concurrent_users"},
            "reliability": {"target": self.reliability_target, "unit": "%"},
            "latency": {"target": self.latency_target, "unit": "ms"},
        }
