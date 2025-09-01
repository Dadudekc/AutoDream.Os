from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Performance Metrics Models - Agent Cellphone V2
==============================================

Data models for performance monitoring and metrics collection.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MetricType(Enum):
    """Types of performance metrics."""
    COUNTER = "counter"           # Incremental count
    GAUGE = "gauge"               # Current value
    HISTOGRAM = "histogram"       # Distribution of values
    TIMER = "timer"               # Time-based measurements


@dataclass
class PerformanceMetric:
    """Individual performance metric."""
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """Snapshot of performance metrics at a point in time."""
    timestamp: datetime
    metrics: Dict[str, float]
    summary: Dict[str, Any]
