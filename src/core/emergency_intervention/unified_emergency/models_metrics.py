"""
Emergency Intervention Unified Models Metrics - KISS Simplified
==============================================================

Metrics and analytics models for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency metrics.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .models_enums import AlertLevel, EmergencySeverity


@dataclass
class EmergencyMetrics:
    """Emergency response metrics."""

    metrics_id: str = ""
    time_period: str = ""
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    escalated_emergencies: int = 0
    average_response_time: float = 0.0
    average_resolution_time: float = 0.0
    success_rate: float = 0.0
    severity_distribution: dict[str, int] = field(default_factory=dict)
    type_distribution: dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyConfig:
    """Emergency intervention configuration."""

    config_id: str = ""
    name: str = ""
    description: str = ""
    enabled: bool = True
    severity_threshold: EmergencySeverity = EmergencySeverity.MEDIUM
    auto_intervention: bool = False
    notification_enabled: bool = True
    escalation_enabled: bool = True
    monitoring_interval: int = 60
    max_retry_attempts: int = 3
    retry_delay: int = 300
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyAlert:
    """Emergency alert data structure."""

    alert_id: str = ""
    emergency_id: str = ""
    alert_level: AlertLevel = AlertLevel.WARNING
    title: str = ""
    message: str = ""
    recipients: list[str] = field(default_factory=list)
    sent_at: datetime | None = None
    acknowledged: bool = False
    acknowledged_by: str | None = None
    acknowledged_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyLog:
    """Emergency log entry."""

    log_id: str = ""
    emergency_id: str = ""
    level: str = "info"
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "system"
    context: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyReport:
    """Emergency incident report."""

    report_id: str = ""
    emergency_id: str = ""
    title: str = ""
    summary: str = ""
    incident_timeline: list[dict[str, Any]] = field(default_factory=list)
    root_cause: str = ""
    impact_assessment: str = ""
    resolution_summary: str = ""
    recommendations: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    metadata: dict[str, Any] = field(default_factory=dict)
