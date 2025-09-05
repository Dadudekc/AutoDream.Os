"""
Extended Metric Types - V2 Compliance Module
===========================================

Extended metric type definitions.

V2 Compliance: < 300 lines, single responsibility, extended types.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from enum import Enum


class MetricStatus(Enum):
    """Metric status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ERROR = "error"


class MetricPriority(Enum):
    """Metric priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
