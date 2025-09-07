from datetime import datetime
from typing import ClassVar, Dict, Type

from ..types.v2_message_enums import (
from .base_message import BaseMessage
from dataclasses import dataclass
from enum import Enum

#!/usr/bin/env python3
"""
V2Message Model - Agent Cellphone V2
====================================

Clean, focused V2Message class extracted from comprehensive system.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""


    V2MessageType,
    V2MessagePriority,
    V2MessageStatus,
)


@dataclass
class V2Message(BaseMessage):
    """V2 message structure - clean and focused"""

    message_type: V2MessageType = V2MessageType.COORDINATION
    priority: V2MessagePriority = V2MessagePriority.NORMAL
    status: V2MessageStatus = V2MessageStatus.PENDING

    _enum_fields: ClassVar[Dict[str, Type[Enum]]] = {
        "message_type": V2MessageType,
        "priority": V2MessagePriority,
        "status": V2MessageStatus,
    }
    
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
