"""
Public API for baseline measurement utilities - V2 Compliance Refactored
=======================================================================

This module re-exports domain specific helpers for easier consumption.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import modular components
from .metrics.latency_metrics import average_latency, max_latency, min_latency
from .metrics.performance_metrics import calculate_throughput, calculate_error_rate

# Re-export for backward compatibility
__all__ = [
    "average_latency",
    "max_latency",
    "min_latency",
    "calculate_throughput",
    "calculate_error_rate",
]

# Backward compatibility - create aliases
average_latency = average_latency
max_latency = max_latency
min_latency = min_latency
calculate_throughput = calculate_throughput
calculate_error_rate = calculate_error_rate
