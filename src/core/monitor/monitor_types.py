#!/usr/bin/env python3
"""
Monitor Types - Agent Cellphone V2
==================================

Defines monitor-related enums and dataclasses.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


class AgentStatus(Enum):
    """Agent operational status"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    COORDINATING = "coordinating"
    PROCESSING = "processing"


class AgentCapability(Enum):
    """Agent capability types"""
    DECISION_MAKING = "decision_making"
    TASK_EXECUTION = "task_execution"
    RESOURCE_MANAGEMENT = "resource_management"
    COORDINATION = "coordination"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"
    DEVELOPMENT = "development"
    TESTING = "testing"


@dataclass
class AgentInfo:
    """Agent information and status data"""
    agent_id: str
    name: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    last_seen: float
    uptime: float
    performance_score: float
    current_task: Optional[str]
    resource_usage: Dict[str, Any]
    health_metrics: Dict[str, Any]


@dataclass
class MonitorConfig:
    """Monitor configuration settings"""
    update_interval: float = 5.0
    max_history_size: int = 1000
    health_check_timeout: float = 30.0
    performance_threshold: float = 0.8
