"""
Performance Metric Models - V2 Compliance Module
===============================================

Performance metric data models.

V2 Compliance: < 300 lines, single responsibility, metric models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

from .metric_types import MetricType


@dataclass
class PerformanceMetric:
    """Individual performance metric."""
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("Metric name is required")
        if self.value < 0:
            raise ValueError("Metric value must be non-negative")
    
    def is_valid(self) -> bool:
        """Check if metric is valid."""
        return bool(self.name and self.value >= 0)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metric summary."""
        return {
            "name": self.name,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "tags_count": len(self.tags),
            "metadata_count": len(self.metadata)
        }
