#!/usr/bin/env python3
"""
V2Message Model - Agent Cellphone V2
====================================

Clean, focused V2Message class extracted from comprehensive system.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..types.v2_message_enums import V2MessageType, V2MessagePriority, V2MessageStatus


@dataclass
class V2Message:
    """V2 message structure - clean and focused"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: V2MessageType = V2MessageType.COORDINATION
    priority: V2MessagePriority = V2MessagePriority.NORMAL
    status: V2MessageStatus = V2MessageStatus.PENDING
    sender_id: str = ""
    recipient_id: str = ""
    subject: str = ""
    content: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    delivered_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    ttl: Optional[int] = None
    sequence_number: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    requires_acknowledgment: bool = False
    is_onboarding_message: bool = False
    phase_number: Optional[int] = None
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None
    
    def __post_init__(self):
        """Ensure required fields are set"""
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.created_at:
            self.created_at = self.timestamp
        if self.payload is None:
            self.payload = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "status": self.status.value,
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
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "ttl": self.ttl,
            "sequence_number": self.sequence_number,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "requires_acknowledgment": self.requires_acknowledgment,
            "is_onboarding_message": self.is_onboarding_message,
            "phase_number": self.phase_number,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'V2Message':
        """Create message from dictionary"""
        # Convert timestamp strings back to datetime objects
        timestamp_fields = ['timestamp', 'created_at', 'delivered_at', 'acknowledged_at', 'read_at']
        for field in timestamp_fields:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values back to enum objects
        if 'message_type' in data and isinstance(data['message_type'], str):
            data['message_type'] = V2MessageType(data['message_type'])
        if 'priority' in data and isinstance(data['priority'], str):
            data['priority'] = V2MessagePriority(data['priority'])
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = V2MessageStatus(data['status'])
        
        return cls(**data)
    
    def mark_delivered(self):
        """Mark message as delivered"""
        self.status = V2MessageStatus.DELIVERED
        self.delivered_at = datetime.now()
    
    def mark_acknowledged(self):
        """Mark message as acknowledged"""
        self.status = V2MessageStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.now()
    
    def mark_read(self):
        """Mark message as read"""
        self.status = V2MessageStatus.READ
        self.read_at = datetime.now()
    
    def increment_retry(self):
        """Increment retry count"""
        self.retry_count += 1
        if self.retry_count >= self.max_retries:
            self.status = V2MessageStatus.FAILED
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        if self.ttl is None:
            return False
        return (datetime.now() - self.timestamp).total_seconds() > self.ttl
    
    def add_dependency(self, dependency_id: str):
        """Add a dependency to the message"""
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)
    
    def remove_dependency(self, dependency_id: str):
        """Remove a dependency from the message"""
        if dependency_id in self.dependencies:
            self.dependencies.remove(dependency_id)
    
    def add_tag(self, tag: str):
        """Add a tag to the message"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the message"""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if message has a specific tag"""
        return tag in self.tags
    
    def get_summary(self) -> str:
        """Get a summary of the message"""
        return f"{self.message_type.value}: {self.subject} ({self.status.value})"
