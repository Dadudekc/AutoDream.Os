#!/usr/bin/env python3
"""
Messaging Data Models - V2 Compliant Module
==========================================

Data models for unified messaging system with V2 compliance validation.
V2 COMPLIANT: Focused data models under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .messaging_enums import (
    MessageStatus,
    RecipientType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)


@dataclass
class UnifiedMessage:
    """Unified message structure for all messaging operations."""

    content: str
    recipient: str
    sender: str = "System"
    message_type: UnifiedMessageType = UnifiedMessageType.TEXT
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")
    delivery_method: str = "inbox"
    status: MessageStatus = MessageStatus.PENDING
    recipient_type: RecipientType = RecipientType.AGENT

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "content": self.content,
            "recipient": self.recipient,
            "sender": self.sender,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "tags": [tag.value for tag in self.tags],
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "delivery_method": self.delivery_method,
            "status": self.status.value,
            "recipient_type": self.recipient_type.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnifiedMessage":
        """Create message from dictionary."""
        return cls(
            content=data["content"],
            recipient=data["recipient"],
            sender=data.get("sender", "System"),
            message_type=UnifiedMessageType(data.get("message_type", "TEXT")),
            priority=UnifiedMessagePriority(data.get("priority", "REGULAR")),
            tags=[UnifiedMessageTag(tag) for tag in data.get("tags", [])],
            metadata=data.get("metadata", {}),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            message_id=data.get("message_id", f"msg_{datetime.now().timestamp()}"),
            delivery_method=data.get("delivery_method", "inbox"),
            status=MessageStatus(data.get("status", "PENDING")),
            recipient_type=RecipientType(data.get("recipient_type", "AGENT")),
        )


@dataclass
class AgentCoordinates:
    """Agent coordinate information for PyAutoGUI delivery."""

    agent_id: str
    x: int
    y: int
    monitor: int = 1

    @classmethod
    def from_tuple(cls, agent_id: str, coords: tuple) -> "AgentCoordinates":
        """Create from tuple (x, y, monitor)."""
        if len(coords) == 2:
            return cls(agent_id, coords[0], coords[1])
        elif len(coords) == 3:
            return cls(agent_id, coords[0], coords[1], coords[2])
        else:
            raise ValueError(f"Invalid coordinates tuple: {coords}")

    def to_tuple(self) -> tuple:
        """Convert to tuple (x, y, monitor)."""
        return (self.x, self.y, self.monitor)


@dataclass
class MessageHistory:
    """Message history entry."""

    message_id: str
    content: str
    sender: str
    recipient: str
    timestamp: datetime
    status: MessageStatus
    delivery_method: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "content": self.content,
            "sender": self.sender,
            "recipient": self.recipient,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "delivery_method": self.delivery_method,
        }


@dataclass
class MessagingMetrics:
    """Messaging system metrics."""

    total_messages_sent: int = 0
    successful_deliveries: int = 0
    failed_deliveries: int = 0
    average_delivery_time: float = 0.0
    last_activity: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_messages_sent": self.total_messages_sent,
            "successful_deliveries": self.successful_deliveries,
            "failed_deliveries": self.failed_deliveries,
            "average_delivery_time": self.average_delivery_time,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
        }

    def update_delivery(self, success: bool, delivery_time: float = 0.0):
        """Update metrics with delivery result."""
        self.total_messages_sent += 1
        if success:
            self.successful_deliveries += 1
        else:
            self.failed_deliveries += 1

        # Update average delivery time
        if self.total_messages_sent > 0:
            self.average_delivery_time = (
                self.average_delivery_time * (self.total_messages_sent - 1) + delivery_time
            ) / self.total_messages_sent

        self.last_activity = datetime.now()
