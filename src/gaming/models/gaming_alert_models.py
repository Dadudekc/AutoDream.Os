"""
Gaming Alert Models

Data models and enums for gaming and entertainment system alerts.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance Emergency Re-Onboarding - Phase 2 Remediation
Status: V2_COMPLIANCE_REMEDIATION_ACTIVE
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class AlertSeverity(Enum):
    """Alert severity levels for gaming systems."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts for gaming and entertainment systems."""
    PERFORMANCE = "performance"
    SYSTEM_HEALTH = "system_health"
    USER_ENGAGEMENT = "user_engagement"
    GAME_STATE = "game_state"
    ENTERTAINMENT_SYSTEM = "entertainment_system"
    INTEGRATION_ERROR = "integration_error"


@dataclass
class GamingAlert:
    """Represents a gaming system alert."""
    id: str
    type: AlertType
    severity: AlertSeverity
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


@dataclass
class AlertThreshold:
    """Represents alert threshold configuration."""
    alert_type: AlertType
    severity: AlertSeverity
    threshold: int
    enabled: bool = True


@dataclass
class AlertSummary:
    """Represents alert summary statistics."""
    total_alerts: int
    active_alerts: int
    resolved_alerts: int
    alerts_by_type: Dict[str, int]
    alerts_by_severity: Dict[str, int]
    alert_counters: Dict[str, int]


@dataclass
class PerformanceMetrics:
    """Represents performance metrics for alert generation."""
    fps: float
    memory_usage: float
    cpu_usage: float
    network_latency: float
    disk_io: float


@dataclass
class SystemHealthMetrics:
    """Represents system health metrics for alert generation."""
    disk_usage: float
    network_status: str
    memory_available: float
    cpu_temperature: float
    power_status: str


__all__ = [
    "AlertSeverity",
    "AlertType", 
    "GamingAlert",
    "AlertThreshold",
    "AlertSummary",
    "PerformanceMetrics",
    "SystemHealthMetrics"
]
