"""
Performance Metrics Models - V2 Compliance Refactored
====================================================

Data models for performance monitoring and metrics collection.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

# Import modular components
from .metrics.metric_types import MetricType
from .metrics.metric_models import PerformanceMetric

# Re-export for backward compatibility
__all__ = [
    'MetricType',
    'PerformanceMetric'
]

# Backward compatibility - create aliases
MetricType = MetricType
PerformanceMetric = PerformanceMetric