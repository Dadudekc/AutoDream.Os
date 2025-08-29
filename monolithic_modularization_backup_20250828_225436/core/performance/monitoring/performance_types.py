#!/usr/bin/env python3
"""Performance monitoring data types."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MetricType(Enum):
    """Common metric categories used throughout the project."""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    NETWORK_LATENCY = "network_latency"
    AGENT_HEALTH = "agent_health"
    TASK_COMPLETION = "task_completion"
    SYSTEM_LOAD = "system_load"


@dataclass
class MonitorMetric:
    """Single metric data point."""

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    unit: str = "units"
    agent_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class MonitorSnapshot:
    """Snapshot of collected metrics."""

    timestamp: datetime
    system_metrics: Dict[str, float] = field(default_factory=dict)
    agent_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    custom_metrics: Dict[str, float] = field(default_factory=dict)
