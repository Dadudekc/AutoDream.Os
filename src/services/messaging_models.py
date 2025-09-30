"""
Consolidated Messaging Service Models
V2 Compliant data models for messaging service
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    """Message status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"


class MessageType(Enum):
    """Message types"""
    TEXT = "text"
    COMMAND = "command"
    STATUS = "status"
    COORDINATION = "coordination"
    ONBOARDING = "onboarding"


@dataclass
class Message:
    """Message structure"""
    message_id: str
    sender: str
    recipient: str
    content: str
    message_type: MessageType
    priority: MessagePriority
    status: MessageStatus
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class AgentStatus:
    """Agent status structure"""
    agent_id: str
    status: str
    last_seen: datetime
    coordinates: tuple[int, int]
    current_task: Optional[str]
    performance_score: float


@dataclass
class MessagingMetrics:
    """Messaging performance metrics"""
    total_messages: int
    successful_messages: int
    failed_messages: int
    average_response_time: float
    active_agents: int
    coordination_requests: int
