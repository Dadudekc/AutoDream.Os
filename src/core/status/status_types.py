#!/usr/bin/env python3
"""
Status Types - Agent Cellphone V2
=================================

Defines status-related enums and dataclasses.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


class UpdateFrequency(Enum):
    """Status update frequency options"""

    REAL_TIME = "real_time"  # Every 1 second
    HIGH_FREQUENCY = "high"  # Every 5 seconds
    MEDIUM_FREQUENCY = "medium"  # Every 15 seconds
    LOW_FREQUENCY = "low"  # Every 60 seconds


class StatusEventType(Enum):
    """Types of status events"""

    AGENT_ONLINE = "agent_online"
    AGENT_OFFLINE = "agent_offline"
    STATUS_CHANGE = "status_change"
    PERFORMANCE_UPDATE = "performance_update"
    TASK_UPDATE = "task_update"
    HEALTH_ALERT = "health_alert"
    COORDINATION_EVENT = "coordination_event"


@dataclass
class StatusEvent:
    """Status event data structure"""

    event_id: str
    event_type: StatusEventType
    agent_id: str
    timestamp: float
    old_status: Optional[str]
    new_status: Optional[str]
    details: Dict[str, Any]
    priority: str


@dataclass
class StatusMetrics:
    """Status performance metrics"""

    system_health: float
    online_ratio: float
    average_performance: float
    total_agents: int
    online_agents: int
    timestamp: float


@dataclass
class ActivitySummary:
    """Agent activity summary"""

    total_agents: int
    status_distribution: Dict[str, int]
    capability_summary: Dict[str, int]
    performance_summary: Dict[str, Any]
