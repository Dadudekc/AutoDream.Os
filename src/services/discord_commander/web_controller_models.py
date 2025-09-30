"""
Discord Commander Web Controller Models
V2 Compliant data models for web controller
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentStatus:
    """Agent status data model"""

    agent_id: str
    status: str
    last_seen: datetime
    current_task: str | None
    performance_score: float


@dataclass
class MessageData:
    """Message data model"""

    content: str
    target_agent: str
    priority: str
    timestamp: datetime


@dataclass
class SystemHealth:
    """System health data model"""

    overall_status: str
    active_agents: int
    total_messages: int
    error_count: int
    uptime: float


@dataclass
class WebControllerConfig:
    """Web controller configuration"""

    host: str
    port: int
    debug_mode: bool
    auto_reload: bool
