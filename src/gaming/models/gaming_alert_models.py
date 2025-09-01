"""
Gaming Alert Models

Extracted models for gaming alert system to achieve V2 compliance.
Contains AlertSeverity, AlertType, and GamingAlert classes.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Implementation - Gaming Infrastructure Refactoring
"""

from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


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
