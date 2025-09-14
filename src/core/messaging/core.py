#!/usr/bin/env python3
"""
Unified Messaging Core - V2 Compliant SSOT
==========================================

Single Source of Truth for all messaging functionality.
V2 COMPLIANT: <300 lines, single responsibility.

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Protocol
import uuid

logger = logging.getLogger(__name__)

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

class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "coordination"
    SYSTEM = "system"

@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = None
    metadata: dict[str, Any] = None
    message_id: str = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()

class IMessageDelivery(Protocol):
    """Interface for message delivery mechanisms."""
    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message."""
        ...

class UnifiedMessagingCore:
    """SINGLE SOURCE OF TRUTH for all messaging functionality."""
    
    def __init__(self, delivery_service: IMessageDelivery = None):
        """Initialize the unified messaging core."""
        self.delivery_service = delivery_service
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, content: str, sender: str, recipient: str,
                    message_type: UnifiedMessageType,
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                    tags: list[UnifiedMessageTag] = None,
                    metadata: dict[str, Any] = None) -> bool:
        """Send a message using the unified messaging system."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        return self.send_message_object(message)
    
    def send_message_object(self, message: UnifiedMessage) -> bool:
        """Send a UnifiedMessage object."""
        try:
            if self.delivery_service:
                return self.delivery_service.send_message(message)
            else:
                self.logger.error("No delivery service configured")
                return False
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    def broadcast_message(self, content: str, sender: str, 
                         priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> bool:
        """Broadcast message to all agents."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST,
            priority=priority,
            tags=[UnifiedMessageTag.SYSTEM]
        )
        
        return self.send_message_object(message)

# SINGLE GLOBAL INSTANCE - THE ONE TRUE MESSAGING CORE
messaging_core = UnifiedMessagingCore()

# PUBLIC API - Single point of access for all messaging
def get_messaging_core() -> UnifiedMessagingCore:
    """Get the SINGLE SOURCE OF TRUTH messaging core."""
    return messaging_core

def send_message(content: str, sender: str, recipient: str,
                message_type: UnifiedMessageType,
                priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                tags: list[UnifiedMessageTag] = None,
                metadata: dict[str, Any] = None) -> bool:
    """Send message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message(content, sender, recipient, message_type, priority, tags, metadata)

def broadcast_message(content: str, sender: str, 
                     priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> bool:
    """Broadcast message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.broadcast_message(content, sender, priority)

# MESSAGING MODELS EXPORTS - Single source for all messaging models
__all__ = [
    # Core classes
    "UnifiedMessagingCore",
    "UnifiedMessage",
    
    # Enums
    "UnifiedMessageType",
    "UnifiedMessagePriority", 
    "UnifiedMessageTag",
    
    # Interfaces
    "IMessageDelivery",
    
    # Public API functions
    "get_messaging_core",
    "send_message",
    "broadcast_message",
]
