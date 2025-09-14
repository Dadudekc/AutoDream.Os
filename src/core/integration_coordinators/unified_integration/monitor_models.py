#!/usr/bin/env python3
"""
Integration Monitor Models - V2 Compliance Module
================================================

Data models for integration monitoring system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class MonitoringConfig:
    """Configuration for integration monitoring."""

    monitoring_interval: float = 1.0
    alert_thresholds: dict[str, float] = None
    enable_alerts: bool = True
    enable_metrics: bool = True
    enable_logging: bool = True

    def __post_init__(self):
        """Initialize default alert thresholds."""
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "error_rate": 0.1,  # 10%
                "response_time": 5.0,  # 5 seconds
                "throughput": 0.5,  # 0.5 requests per second
            }


@dataclass
class MonitoringAlert:
    """Monitoring alert data structure."""

    alert_id: str
    alert_type: str
    message: str
    severity: str
    timestamp: datetime
    metadata: dict[str, Any] = None

    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MonitoringStats:
    """Monitoring statistics."""

    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    alerts_triggered: int = 0
    last_check_time: datetime | None = None
    uptime_seconds: float = 0.0
