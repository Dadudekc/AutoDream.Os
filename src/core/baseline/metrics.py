"""Public API for baseline measurement utilities.

This module re-exports domain specific helpers for easier consumption.
"""

from .latency_metrics import average_latency, max_latency, min_latency
from .throughput_metrics import calculate_throughput
from .error_rate_metrics import calculate_error_rate

__all__ = [
    "average_latency",
    "max_latency",
    "min_latency",
    "calculate_throughput",
    "calculate_error_rate",
]
