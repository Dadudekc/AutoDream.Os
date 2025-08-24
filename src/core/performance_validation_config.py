"""Configuration for Performance Validation benchmarks."""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class PerformanceValidationConfig:
    """Tunable parameters for performance validation tests."""
    response_iterations: int = 10
    response_delay: float = 0.1
    throughput_test_duration: float = 5.0
    throughput_delay: float = 0.01
    scalability_levels: Tuple[int, ...] = (10, 25, 50)
    reliability_operations: int = 100
    latency_iterations: int = 20
