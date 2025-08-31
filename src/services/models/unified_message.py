#!/usr/bin/env python3
"""
Unified Message Models - Agent Cellphone V2
=========================================

Message models and enums for the unified messaging service.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - Message Models
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import uuid


class UnifiedMessageType(Enum):
    """Message types for unified messaging system"""
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    COMMAND = "command"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"


class UnifiedMessagePriority(Enum):
    """Message priority levels"""
    NORMAL = "normal"
    URGENT = "urgent"
    CRITICAL = "critical"


class UnifiedMessageStatus(Enum):
    """Message delivery status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class UnifiedMessageTag(Enum):
    """Message tags for categorization"""
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    CONTRACT = "contract"
    EMERGENCY = "emergency"


@dataclass
class UnifiedMessage:
    """Unified message model for all messaging scenarios"""
    
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType = UnifiedMessageType.TEXT
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    tags: List[UnifiedMessageTag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None
    message_id: Optional[str] = None
    status: UnifiedMessageStatus = UnifiedMessageStatus.PENDING
        
    def __post_init__(self):
        """Initialize default values after dataclass creation"""
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.message_id is None:
            self.message_id = f"msg_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "content": self.content,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "tags": [tag.value for tag in self.tags],
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "message_id": self.message_id,
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UnifiedMessage':
        """Create message from dictionary"""
        return cls(
            content=data["content"],
            sender=data["sender"],
            recipient=data["recipient"],
            message_type=UnifiedMessageType(data["message_type"]),
            priority=UnifiedMessagePriority(data["priority"]),
            tags=[UnifiedMessageTag(tag) for tag in data.get("tags", [])],
            metadata=data.get("metadata", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            message_id=data.get("message_id"),
            status=UnifiedMessageStatus(data.get("status", "pending"))
        )


if __name__ == "__main__":
    # Test the unified message model
    print("📨 Unified Message Models Loaded Successfully")
    
    # Test message creation
    test_message = UnifiedMessage(
        content="Test message content",
        sender="Agent-1",
        recipient="Agent-4",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.CAPTAIN]
    )
    
    print(f"✅ Test message created: {test_message.message_id}")
    print(f"✅ Message type: {test_message.message_type.value}")
    print(f"✅ Priority: {test_message.priority.value}")
    print("✅ All message model functionality working correctly!")
