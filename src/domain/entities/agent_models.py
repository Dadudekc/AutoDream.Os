"""
Agent Entity Models - V2 Compliant
==================================

Data models for agent entity system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AgentStatus(Enum):
    """Agent status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentType(Enum):
    """Agent type enumeration."""

    CORE = "core"
    SERVICE = "service"
    INTEGRATION = "integration"
    UTILITY = "utility"


class AgentCapability(Enum):
    """Agent capability enumeration."""

    MESSAGING = "messaging"
    COMMAND_EXECUTION = "command_execution"
    DATA_PROCESSING = "data_processing"
    COORDINATION = "coordination"
    USER_INTERFACE = "user_interface"
    SECURITY = "security"
    SYSTEM_INTEGRATION = "system_integration"


@dataclass
class AgentMetrics:
    """Agent performance metrics."""

    tasks_completed: int = 0
    tasks_failed: int = 0
    average_response_time: float = 0.0
    uptime_seconds: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    last_activity: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "average_response_time": self.average_response_time,
            "uptime_seconds": self.uptime_seconds,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "last_activity": self.last_activity.isoformat(),
        }


@dataclass
class AgentConfig:
    """Agent configuration."""

    agent_id: str
    name: str
    agent_type: AgentType
    capabilities: list[AgentCapability]
    status: AgentStatus = AgentStatus.INACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    metrics: AgentMetrics = field(default_factory=AgentMetrics)

