#!/usr/bin/env python3
"""
Messaging Models - V2 Compliant Core Data Structures
==================================================

Core data models and enums for the unified messaging system.
Consolidated from src/core/messaging_core.py for better organization.

V2 Compliance: <300 lines, single responsibility for data models
Enterprise Ready: Comprehensive type definitions, validation, serialization

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# ============================================================================
# ENUMS - Message Properties
# ============================================================================

class DeliveryMethod(Enum):
    """Delivery methods for messages."""
    INBOX = "inbox"
    PYAUTOGUI = "pyautogui"
    BROADCAST = "broadcast"
    FALLBACK = "fallback"

class UnifiedMessageType(Enum):
    """Message types for unified messaging."""
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"

class UnifiedMessagePriority(Enum):
    """Message priorities for unified messaging."""
    REGULAR = "regular"
    URGENT = "urgent"
    LOW = "low"
    HIGH = "high"

class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "coordination"
    SYSTEM = "system"
    GENERAL = "general"
    TASK = "task"
    EMERGENCY = "emergency"

class RecipientType(Enum):
    """Recipient types for unified messaging."""
    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"
    SWARM = "swarm"

class SenderType(Enum):
    """Sender types for unified messaging."""
    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"
    SERVICE = "service"

class MessageStatus(Enum):
    """Message delivery status."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"

# ============================================================================
# DATA CLASSES - Core Message Structures
# ============================================================================

@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: List[UnifiedMessageTag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    sender_type: SenderType = SenderType.SYSTEM
    recipient_type: RecipientType = RecipientType.AGENT
    status: MessageStatus = MessageStatus.PENDING
    delivery_method: Optional[DeliveryMethod] = None
    retry_count: int = 0
    max_retries: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "content": self.content,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "tags": [tag.value for tag in self.tags],
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "sender_type": self.sender_type.value,
            "recipient_type": self.recipient_type.value,
            "status": self.status.value,
            "delivery_method": self.delivery_method.value if self.delivery_method else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UnifiedMessage:
        """Create message from dictionary."""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            content=data["content"],
            sender=data["sender"],
            recipient=data["recipient"],
            message_type=UnifiedMessageType(data["message_type"]),
            priority=UnifiedMessagePriority(data.get("priority", "regular")),
            tags=[UnifiedMessageTag(tag) for tag in data.get("tags", [])],
            metadata=data.get("metadata", {}),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            sender_type=SenderType(data.get("sender_type", "system")),
            recipient_type=RecipientType(data.get("recipient_type", "agent")),
            status=MessageStatus(data.get("status", "pending")),
            delivery_method=DeliveryMethod(data["delivery_method"]) if data.get("delivery_method") else None,
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3)
        )

@dataclass
class AgentCoordinates:
    """Agent coordinate information."""
    agent_id: str
    x: int
    y: int
    window_title: Optional[str] = None
    is_active: bool = True
    last_updated: datetime = field(default_factory=datetime.now)

    def to_tuple(self) -> tuple[int, int]:
        """Convert to coordinate tuple."""
        return (self.x, self.y)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "x": self.x,
            "y": self.y,
            "window_title": self.window_title,
            "is_active": self.is_active,
            "last_updated": self.last_updated.isoformat()
        }

@dataclass
class MessageHistory:
    """Message history entry."""
    message_id: str
    agent_id: str
    message_type: UnifiedMessageType
    status: MessageStatus
    timestamp: datetime
    content_preview: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "agent_id": self.agent_id,
            "message_type": self.message_type.value,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "content_preview": self.content_preview,
            "metadata": self.metadata
        }

@dataclass
class MessagingMetrics:
    """Messaging system metrics."""
    total_messages_sent: int = 0
    successful_deliveries: int = 0
    failed_deliveries: int = 0
    retry_attempts: int = 0
    last_activity: Optional[datetime] = None
    average_delivery_time: float = 0.0
    success_rate: float = 0.0

    def update_success_rate(self) -> None:
        """Update success rate calculation."""
        total = self.total_messages_sent
        if total > 0:
            self.success_rate = (self.successful_deliveries / total) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_messages_sent": self.total_messages_sent,
            "successful_deliveries": self.successful_deliveries,
            "failed_deliveries": self.failed_deliveries,
            "retry_attempts": self.retry_attempts,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "average_delivery_time": self.average_delivery_time,
            "success_rate": self.success_rate
        }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_message(content: str, sender: str, recipient: str, 
                  message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                  priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                  tags: Optional[List[UnifiedMessageTag]] = None,
                  metadata: Optional[Dict[str, Any]] = None) -> UnifiedMessage:
    """Create a new unified message with default values."""
    return UnifiedMessage(
        content=content,
        sender=sender,
        recipient=recipient,
        message_type=message_type,
        priority=priority,
        tags=tags or [],
        metadata=metadata or {}
    )

def create_broadcast_message(content: str, sender: str = "Captain Agent-4",
                           priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> UnifiedMessage:
    """Create a broadcast message."""
    return UnifiedMessage(
        content=content,
        sender=sender,
        recipient="ALL_AGENTS",
        message_type=UnifiedMessageType.BROADCAST,
        priority=priority,
        tags=[UnifiedMessageTag.CAPTAIN],
        recipient_type=RecipientType.SWARM
    )

def create_onboarding_message(content: str, agent_id: str, 
                            sender: str = "Captain Agent-4") -> UnifiedMessage:
    """Create an onboarding message."""
    return UnifiedMessage(
        content=content,
        sender=sender,
        recipient=agent_id,
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.ONBOARDING, UnifiedMessageTag.CAPTAIN],
        sender_type=SenderType.CAPTAIN
    )

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Enums
    "DeliveryMethod",
    "UnifiedMessageType", 
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "MessageStatus",
    
    # Data Classes
    "UnifiedMessage",
    "AgentCoordinates",
    "MessageHistory",
    "MessagingMetrics",
    
    # Utility Functions
    "create_message",
    "create_broadcast_message",
    "create_onboarding_message",
]