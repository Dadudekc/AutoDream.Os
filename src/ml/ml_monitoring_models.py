#!/usr/bin/env python3
"""
ML Monitoring Models
===================

Data models for ML monitoring system.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


class MetricType(Enum):
    """Types of metrics that can be recorded."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertSeverity(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MetricData:
    """Represents a single metric data point."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str]
    model_name: Optional[str] = None
    model_version: Optional[str] = None


@dataclass
class Alert:
    """Represents an alert."""
    id: str
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None



