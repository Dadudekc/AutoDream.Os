#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Unified Message System - Agent Cellphone V2
=========================================

Consolidates ALL Message classes into single unified system:
- Message (coordination-focused)
- V2Message (comprehensive)
- AgentMessage (V1 compatibility)
- MessageValidator (validation)

Follows V2 standards: OOP, SRP, clean production-grade code.
Eliminates 4 duplicate Message classes for 100% SSOT compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Type
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# UNIFIED MESSAGE ENUMS (Consolidated from all Message classes)
# ============================================================================

class UnifiedMessageType(Enum):
    """Unified message types - consolidated from all systems"""
    # Coordination types
    COORDINATION = "coordination"
    TASK = "task"
    STATUS = "status"
    RESULT = "result"
    ERROR = "error"
    
    # Agent types
    AGENT = "agent"
    BROADCAST = "broadcast"
    DIRECT = "direct"
    
    # System types
    SYSTEM = "system"
    ONBOARDING = "onboarding"
    WORKFLOW = "workflow"
    
    # Legacy V1 types
    NORMAL = "normal"
    COORDINATE = "coordinate"
    RESCUE = "rescue"


class UnifiedMessagePriority(Enum):
    """Unified message priority - consolidated from all systems"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"


class UnifiedMessageStatus(Enum):
    """Unified message status - consolidated from all systems"""
    PENDING = "pending"
    QUEUED = "queued"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    READ = "read"
    FAILED = "failed"
    EXPIRED = "expired"
    RETRYING = "retrying"
    COMPLETED = "completed"


class UnifiedMessageTag(Enum):
    """Unified message tags - consolidated from all systems"""
    NORMAL = "[NORMAL]"
    COORDINATE = "[COORDINATE]"
    RESCUE = "[RESCUE]"
    SYSTEM = "[SYSTEM]"
    TASK = "[TASK]"
    STATUS = "[STATUS]"


# ============================================================================
# UNIFIED MESSAGE CLASS (Consolidated from all Message classes)
# ============================================================================

from .base_message import BaseMessage


@dataclass
class UnifiedMessage(BaseMessage):
    """
    Unified Message - Single source of truth for ALL message functionality

    Consolidates functionality from:
    - Message (coordination system)
    - V2Message (comprehensive system)
    - AgentMessage (V1 compatibility)

    Follows V2 standards: Single responsibility, comprehensive functionality
    """

    message_type: UnifiedMessageType = UnifiedMessageType.COORDINATION
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    status: UnifiedMessageStatus = UnifiedMessageStatus.PENDING
    tag: UnifiedMessageTag = UnifiedMessageTag.NORMAL

    expires_at: Optional[datetime] = None
    is_broadcast: bool = False
    from_agent: Optional[str] = None
    to_agent: Optional[str] = None

    _enum_fields: ClassVar[Dict[str, Type[Enum]]] = {
        "message_type": UnifiedMessageType,
        "priority": UnifiedMessagePriority,
        "status": UnifiedMessageStatus,
        "tag": UnifiedMessageTag,
    }
    
    def __post_init__(self) -> None:
        """Ensure required fields are set and V1 compatibility maintained"""
        super().__post_init__()

        # V1 compatibility: set from_agent/to_agent if not set
        if not self.from_agent and self.sender_id:
            self.from_agent = self.sender_id
        if not self.to_agent and self.recipient_id:
            self.to_agent = self.recipient_id

        # Set V1 compatibility fields
        if self.from_agent and not self.sender_id:
            self.sender_id = self.from_agent
        if self.to_agent and not self.recipient_id:
            self.recipient_id = self.to_agent
    
    # ============================================================================
    # MESSAGE STATE MANAGEMENT METHODS
    # ============================================================================
    
    def mark_delivered(self) -> None:
        """Mark message as delivered"""
        self.status = UnifiedMessageStatus.DELIVERED
        self.delivered_at = datetime.now()
        logger.info(f"Message {self.message_id} marked as delivered")
    
    def mark_acknowledged(self) -> None:
        """Mark message as acknowledged"""
        self.status = UnifiedMessageStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.now()
        logger.info(f"Message {self.message_id} marked as acknowledged")
    
    def mark_read(self) -> None:
        """Mark message as read"""
        self.status = UnifiedMessageStatus.READ
        self.read_at = datetime.now()
        logger.info(f"Message {self.message_id} marked as read")
    
    def mark_failed(self, error_message: str = "Delivery failed") -> None:
        """Mark message as failed"""
        self.status = UnifiedMessageStatus.FAILED
        self.payload["error"] = error_message
        logger.error(f"Message {self.message_id} marked as failed: {error_message}")
    
    def retry_delivery(self) -> bool:
        """Attempt to retry message delivery"""
        if self.retry_count >= self.max_retries:
            self.mark_failed("Max retries exceeded")
            return False
        
        self.retry_count += 1
        self.status = UnifiedMessageStatus.RETRYING
        logger.info(f"Message {self.message_id} retry attempt {self.retry_count}")
        return True
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
    
    def is_ready_for_delivery(self) -> bool:
        """Check if message is ready for delivery"""
        return (
            self.status == UnifiedMessageStatus.PENDING and
            not self.is_expired() and
            self.retry_count < self.max_retries
        )
    
    # ============================================================================
    # SERIALIZATION METHODS
    # ============================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        data = super().to_dict()
        data.update({
            "tag": self.tag.value,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_broadcast": self.is_broadcast,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedMessage":
        """Create message from dictionary"""
        if "expires_at" in data and isinstance(data["expires_at"], str):
            try:
                data["expires_at"] = datetime.fromisoformat(data["expires_at"])
            except ValueError:
                data["expires_at"] = None
        return super().from_dict(data)
    
    # ============================================================================
    # V1 COMPATIBILITY METHODS
    # ============================================================================
    
    def to_v1_format(self) -> Dict[str, Any]:
        """Convert to V1 AgentMessage format for compatibility"""
        return {
            "from_agent": self.from_agent or self.sender_id,
            "to_agent": self.to_agent or self.recipient_id,
            "content": self.content,
            "tag": self.tag.value,
            "timestamp": self.timestamp.timestamp() if self.timestamp else None
        }
    
    @classmethod
    def from_v1_format(cls, v1_data: Dict[str, Any]) -> 'UnifiedMessage':
        """Create from V1 AgentMessage format for compatibility"""
        return cls(
            sender_id=v1_data.get("from_agent", ""),
            recipient_id=v1_data.get("to_agent", ""),
            content=v1_data.get("content", ""),
            tag=UnifiedMessageTag(v1_data.get("tag", "[NORMAL]")),
            timestamp=datetime.fromtimestamp(v1_data["timestamp"]) if v1_data.get("timestamp") else datetime.now()
        )
    
    # ============================================================================
    # COORDINATION METHODS
    # ============================================================================
    
    def add_dependency(self, dependency_id: str) -> None:
        """Add a dependency to this message"""
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)
            logger.info(f"Added dependency {dependency_id} to message {self.message_id}")
    
    def remove_dependency(self, dependency_id: str) -> None:
        """Remove a dependency from this message"""
        if dependency_id in self.dependencies:
            self.dependencies.remove(dependency_id)
            logger.info(f"Removed dependency {dependency_id} from message {self.message_id}")
    
    def has_dependencies(self) -> bool:
        """Check if message has dependencies"""
        return len(self.dependencies) > 0
    
    def are_dependencies_satisfied(self, satisfied_ids: List[str]) -> bool:
        """Check if all dependencies for a task are satisfied"""
        return all(dep_id in satisfied_ids for dep_id in self.dependencies)
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def __str__(self) -> str:
        """String representation for V1 compatibility"""
        return f"{self.from_agent or self.sender_id} → {self.to_agent or self.recipient_id}: {self.tag.value} {self.content}"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return f"UnifiedMessage(id={self.message_id}, type={self.message_type.value}, status={self.status.value})"
    
    def clone(self) -> 'UnifiedMessage':
        """Create a copy of this message"""
        return UnifiedMessage.from_dict(self.to_dict())
    
    def is_system_message(self) -> bool:
        """Check if this is a system message"""
        return self.message_type in [UnifiedMessageType.SYSTEM, UnifiedMessageType.ONBOARDING]
    
    def is_coordination_message(self) -> bool:
        """Check if this is a coordination message"""
        return self.message_type in [UnifiedMessageType.COORDINATION, UnifiedMessageType.TASK, UnifiedMessageType.STATUS]


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Maintain backward compatibility with existing code
Message = UnifiedMessage
V2Message = UnifiedMessage
AgentMessage = UnifiedMessage

# Export all components
__all__ = [
    "UnifiedMessage",
    "UnifiedMessageType",
    "UnifiedMessagePriority", 
    "UnifiedMessageStatus",
    "UnifiedMessageTag",
    # Backward compatibility
    "Message",
    "V2Message", 
    "AgentMessage"
]



