"""
Performance Metrics - V2 Compliance Module
=========================================

Performance measurement utilities.

V2 Compliance: < 300 lines, single responsibility, performance metrics.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List


def calculate_throughput(requests: int, time_seconds: float) -> float:
    """Calculate throughput (requests per second)."""
    if time_seconds <= 0:
        return 0.0
    return requests / time_seconds


def calculate_error_rate(errors: int, total_requests: int) -> float:
    """Calculate error rate (errors per total requests)."""
    if total_requests <= 0:
        return 0.0
    return errors / total_requests
