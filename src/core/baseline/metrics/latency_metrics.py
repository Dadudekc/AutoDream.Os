"""
Latency Metrics - V2 Compliance Module
=====================================

Latency measurement utilities.

V2 Compliance: < 300 lines, single responsibility, latency metrics.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List


def average_latency(latencies: List[float]) -> float:
    """Calculate average latency."""
    if not latencies:
        return 0.0
    return sum(latencies) / len(latencies)


def max_latency(latencies: List[float]) -> float:
    """Calculate maximum latency."""
    if not latencies:
        return 0.0
    return max(latencies)


def min_latency(latencies: List[float]) -> float:
    """Calculate minimum latency."""
    if not latencies:
        return 0.0
    return min(latencies)
