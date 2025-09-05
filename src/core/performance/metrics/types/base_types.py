"""
Base Metric Types - V2 Compliance Module
=======================================

Base metric type definitions.

V2 Compliance: < 300 lines, single responsibility, base types.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from enum import Enum


class MetricType(Enum):
    """Types of performance metrics."""
    COUNTER = "counter"  # Incremental count
    GAUGE = "gauge"  # Current value
    HISTOGRAM = "histogram"  # Distribution of values
    TIMER = "timer"  # Time-based measurements
