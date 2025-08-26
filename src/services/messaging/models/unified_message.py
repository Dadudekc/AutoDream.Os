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

import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
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

    # V2 specialized types
    TASK_ASSIGNMENT = "task_assignment"
    TASK_UPDATE = "task_update"
    DECISION_MAKING = "decision_making"
    ALERT = "alert"
    ONBOARDING_PHASE = "onboarding_phase"
    STATUS_UPDATE = "status_update"
    WORKFLOW_UPDATE = "workflow_update"
    CONTRACT_ASSIGNMENT = "contract_assignment"
    VALIDATION = "validation"

    # Legacy V1 types
    NORMAL = "normal"
    COORDINATE = "coordinate"
    RESCUE = "rescue"


class UnifiedMessagePriority(Enum):
    """Unified message priority - consolidated from all systems"""
    LOW = "low"
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"


class UnifiedMessageStatus(Enum):
    """Unified message status - consolidated from all systems"""
    PENDING = "pending"
    QUEUED = "queued"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    PROCESSED = "processed"
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

@dataclass
class UnifiedMessage:
    """
    Unified Message - Single source of truth for ALL message functionality
    
    Consolidates functionality from:
    - Message (coordination system)
    - V2Message (comprehensive system)
    - AgentMessage (V1 compatibility)
    
    Follows V2 standards: Single responsibility, comprehensive functionality
    """
    
    # Core identification
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: UnifiedMessageType = UnifiedMessageType.COORDINATION
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    status: UnifiedMessageStatus = UnifiedMessageStatus.PENDING
    tag: UnifiedMessageTag = UnifiedMessageTag.NORMAL
    
    # Sender and recipient
    sender_id: str = ""
    recipient_id: str = ""
    
    # Content and payload
    subject: str = ""
    content: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    timestamp: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    delivered_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Delivery and retry
    retry_count: int = 0
    max_retries: int = 3
    ttl: Optional[int] = None
    
    # Coordination and workflow
    sequence_number: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None
    phase_number: Optional[int] = None
    
    # Metadata and flags
    tags: List[str] = field(default_factory=list)
    requires_acknowledgment: bool = False
    is_onboarding_message: bool = False
    is_broadcast: bool = False
    
    # V1 compatibility fields
    from_agent: Optional[str] = None
    to_agent: Optional[str] = None
    
    def __post_init__(self):
        """Ensure required fields are set and V1 compatibility maintained"""
        # Set message_id if not provided
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        
        # Set timestamps if not provided
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.created_at:
            self.created_at = self.timestamp
        
        # Initialize collections if None
        if self.payload is None:
            self.payload = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        
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
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "tag": self.tag.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "subject": self.subject,
            "content": self.content,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "ttl": self.ttl,
            "sequence_number": self.sequence_number,
            "dependencies": self.dependencies,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
            "phase_number": self.phase_number,
            "tags": self.tags,
            "requires_acknowledgment": self.requires_acknowledgment,
            "is_onboarding_message": self.is_onboarding_message,
            "is_broadcast": self.is_broadcast,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UnifiedMessage':
        """Create message from dictionary"""
        # Convert timestamp strings back to datetime objects
        timestamp_fields = ['timestamp', 'created_at', 'delivered_at', 'acknowledged_at', 'read_at', 'expires_at']
        for field in timestamp_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except ValueError:
                    data[field] = None
        
        # Convert enum values back to enum objects
        if 'message_type' in data and isinstance(data['message_type'], str):
            data['message_type'] = UnifiedMessageType(data['message_type'])
        if 'priority' in data and isinstance(data['priority'], str):
            data['priority'] = UnifiedMessagePriority(data['priority'])
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = UnifiedMessageStatus(data['status'])
        if 'tag' in data and isinstance(data['tag'], str):
            data['tag'] = UnifiedMessageTag(data['tag'])
        
        return cls(**data)
    
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


