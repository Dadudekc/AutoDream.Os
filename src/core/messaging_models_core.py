#!/usr/bin/env python3
"""
Messaging Models - V2 Compliance Module
=======================================

Core messaging models and enums.
Extracted from messaging_core.py (472→<300 lines)

Author: Agent-1 (Integration & Core Systems Specialist) - LAST CRITICAL V2 FIX
Created: 2025-10-11
License: MIT
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DeliveryMethod(Enum):
    """Delivery methods for messages."""

    INBOX = "inbox"
    PYAUTOGUI = "pyautogui"
    BROADCAST = "broadcast"


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


class RecipientType(Enum):
    """Recipient types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(Enum):
    """Sender types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""

    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    sender_type: SenderType = SenderType.SYSTEM
    recipient_type: RecipientType = RecipientType.AGENT


__all__ = [
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "UnifiedMessage",
]
