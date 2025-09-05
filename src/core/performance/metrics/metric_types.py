"""
Performance Metric Types - V2 Compliance Refactored
==================================================

Performance metric type definitions.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import modular components
from .types.base_types import MetricType
from .types.extended_types import MetricStatus, MetricPriority

# Re-export for backward compatibility
__all__ = [
    'MetricType',
    'MetricStatus',
    'MetricPriority'
]

# Backward compatibility - create aliases
MetricType = MetricType
MetricStatus = MetricStatus
MetricPriority = MetricPriority