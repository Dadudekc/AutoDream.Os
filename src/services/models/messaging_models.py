#!/usr/bin/env python3
"""
Messaging Models - Agent Cellphone V2
===================================

Message models and enums for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

<<<<<<< HEAD
import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
=======
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any
import uuid
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65


class UnifiedMessageType(Enum):
    """Message types for unified messaging."""
<<<<<<< HEAD

    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    A2A = "agent_to_agent"  # Agent-to-Agent communication
    S2A = "system_to_agent"  # System-to-Agent communication (onboarding, pre-made messages)
    H2A = "human_to_agent"  # Human-to-Agent communication (Discord messages)
    C2A = "captain_to_agent"  # Captain-to-Agent communication (custom onboarding, directives)
=======
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65


class UnifiedMessagePriority(Enum):
    """Message priority levels."""
<<<<<<< HEAD

    REGULAR = "regular"
=======
    NORMAL = "normal"
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    URGENT = "urgent"


class UnifiedMessageStatus(Enum):
    """Message delivery status."""
<<<<<<< HEAD

    PENDING = "pending"
=======
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    SENT = "sent"
    DELIVERED = "delivered"


<<<<<<< HEAD
class UnifiedSenderType(Enum):
    """Sender types for unified messaging."""

    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


class UnifiedRecipientType(Enum):
    """Recipient types for unified messaging."""

    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


class UnifiedMessageTag(Enum):
    """Message tags for categorization."""

=======
class UnifiedMessageTag(Enum):
    """Message tags for categorization."""
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"


<<<<<<< HEAD
class DeliveryMethod(Enum):
    """Delivery method for messages."""

    PYAUTOGUI = "pyautogui"
    INBOX = "inbox"


class SenderType(Enum):
    """Sender type classification for message routing."""

    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


class RecipientType(Enum):
    """Recipient type classification for message routing."""

    AGENT = "agent"
    SYSTEM = "system"
    HUMAN = "human"


@dataclass
class UnifiedMessage:
    """Unified message model for all messaging scenarios."""

=======
@dataclass
class UnifiedMessage:
    """Unified message model for all messaging scenarios."""
    
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType = UnifiedMessageType.TEXT
<<<<<<< HEAD
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    delivery_method: DeliveryMethod = DeliveryMethod.PYAUTOGUI
    tags: List[UnifiedMessageTag] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    created_at: datetime = None  # Alias for timestamp for backward compatibility
    message_id: str = None
    sender_type: SenderType = None
    recipient_type: RecipientType = None
    status: UnifiedMessageStatus = None

=======
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    tags: List[UnifiedMessageTag] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    message_id: str = None
    
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
<<<<<<< HEAD
        if self.created_at is None:
            self.created_at = self.timestamp
        if self.message_id is None:
            self.message_id = f"msg_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
        if self.sender_type is None:
            self.sender_type = self._infer_sender_type()
        if self.recipient_type is None:
            self.recipient_type = self._infer_recipient_type()
        if self.status is None:
            self.status = UnifiedMessageStatus.PENDING

    def _infer_sender_type(self) -> SenderType:
        """Infer sender type based on sender name and message type."""
        if self.sender.startswith("Agent-"):
            return SenderType.AGENT
        elif self.sender in ["Captain Agent-4", "System"]:
            return SenderType.SYSTEM
        else:
            return SenderType.HUMAN

    def _infer_recipient_type(self) -> RecipientType:
        """Infer recipient type based on recipient name."""
        if self.recipient.startswith("Agent-"):
            return RecipientType.AGENT
        elif self.recipient in ["System", "All Agents"]:
            return RecipientType.SYSTEM
        else:
            return RecipientType.HUMAN
=======
        if self.message_id is None:
            self.message_id = f"msg_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
