"""Metric data structures and types."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Union


class MetricType(Enum):
    """Types of metrics that can be collected."""

    GAUGE = "gauge"  # Current value (e.g., CPU usage)
    COUNTER = "counter"  # Incrementing value (e.g., request count)
    HISTOGRAM = "histogram"  # Distribution of values
    TIMER = "timer"  # Timing measurements
    SET = "set"  # Unique values count


@dataclass
class MetricData:
    """Individual metric data point."""

    metric_name: str
    metric_type: MetricType
    value: Union[float, int]
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""
    description: str = ""


__all__ = ["MetricType", "MetricData"]
