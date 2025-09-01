#!/usr/bin/env python3
"""
Messaging Models - Agent Cellphone V2
===================================

Message models and enums for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any
import uuid


class UnifiedMessageType(Enum):
    """Message types for unified messaging."""
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"


class UnifiedMessagePriority(Enum):
    """Message priority levels."""
    NORMAL = "normal"
    URGENT = "urgent"


class UnifiedMessageStatus(Enum):
    """Message delivery status."""
    SENT = "sent"
    DELIVERED = "delivered"


class UnifiedMessageTag(Enum):
    """Message tags for categorization."""
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"


@dataclass
class UnifiedMessage:
    """Unified message model for all messaging scenarios."""
    
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType = UnifiedMessageType.TEXT
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    tags: List[UnifiedMessageTag] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    message_id: str = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.message_id is None:
            self.message_id = f"msg_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
