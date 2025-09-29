#!/usr/bin/env python3
"""
ML Monitoring Models
===================

Data models for ML monitoring system.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
    labels: dict[str, str]
    model_name: str | None = None
    model_version: str | None = None


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
    resolved_at: datetime | None = None
