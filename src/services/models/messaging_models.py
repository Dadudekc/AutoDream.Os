#!/usr/bin/env python3
"""
Unified Messaging Models - Agent Cellphone V2
============================================

Core data models for the unified messaging system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


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


class RecipientType(Enum):
    """Recipient types for unified messaging."""
    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(Enum):
    """Sender types for unified messaging."""
    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


@dataclass
class UnifiedMessage:
    """Unified message model."""
    content: str
    recipient: str
    recipient_type: RecipientType
    sender: str
    sender_type: SenderType
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority
    tags: List[UnifiedMessageTag] = None
    message_id: str = None
    timestamp: str = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MessageDeliveryResult:
    """Result of message delivery attempt."""
    success: bool
    message_id: str
    recipient: str
    delivery_method: str
    timestamp: str
    error_message: str = None


@dataclass
class BulkDeliveryResult:
    """Result of bulk message delivery."""
    total_messages: int
    successful_deliveries: int
    failed_deliveries: int
    results: Dict[str, MessageDeliveryResult]
    timestamp: str