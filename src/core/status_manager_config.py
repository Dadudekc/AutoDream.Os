#!/usr/bin/env python3
"""Configuration and shared models for the Status Manager.

Contains enum and dataclass definitions used across the status
management modules.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from .agent_manager import AgentStatus
from .health_models import HealthStatus
from .health.core import AlertLevel


class StatusTransition(Enum):
    """Status transition types."""

    ONLINE_TO_OFFLINE = "online_to_offline"
    OFFLINE_TO_ONLINE = "offline_to_online"
    IDLE_TO_BUSY = "idle_to_busy"
    BUSY_TO_IDLE = "busy_to_idle"
    HEALTHY_TO_WARNING = "healthy_to_warning"
    WARNING_TO_CRITICAL = "warning_to_critical"


@dataclass
class HealthCheck:
    """Health check result."""

    check_id: str
    agent_id: str
    check_type: str
    status: HealthStatus
    message: str
    timestamp: str
    details: Dict[str, Any]


@dataclass
class Alert:
    """System alert."""

    alert_id: str
    level: AlertLevel
    message: str
    source: str
    timestamp: str
    acknowledged: bool
    metadata: Dict[str, Any]


@dataclass
class StatusEvent:
    """Status change event."""

    event_id: str
    agent_id: str
    old_status: AgentStatus
    new_status: AgentStatus
    transition: StatusTransition
    timestamp: str
    metadata: Dict[str, Any]


__all__ = [
    "StatusTransition",
    "HealthCheck",
    "Alert",
    "StatusEvent",
]
