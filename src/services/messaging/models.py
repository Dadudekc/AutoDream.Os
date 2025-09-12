from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any


class DeliveryMethod(str, Enum):
    INBOX = "inbox"
    PYAUTOGUI = "pyautogui"
    BROADCAST = "broadcast"


class UnifiedMessageType(str, Enum):
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"


class UnifiedMessagePriority(str, Enum):
    REGULAR = "regular"
    URGENT = "urgent"
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class UnifiedMessageTag(str, Enum):
    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "COORDINATION"
    SYSTEM = "system"
    GENERAL = "GENERAL"
    TASK = "TASK"
    STATUS = "STATUS"


class RecipientType(str, Enum):
    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(str, Enum):
    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class UnifiedMessage:
    """Core message DTO"""

    def __init__(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
        message_id: str | None = None,
        timestamp: str | None = None,
        sender_type: SenderType = SenderType.SYSTEM,
        recipient_type: RecipientType = RecipientType.AGENT,
    ):
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type
        self.priority = priority
        self.tags = tags or []
        self.metadata = metadata or {}
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")
        self.sender_type = sender_type
        self.recipient_type = recipient_type


# Helpers
PRIORITY_MAP = {
    "LOW": UnifiedMessagePriority.LOW,
    "NORMAL": UnifiedMessagePriority.NORMAL,
    "HIGH": UnifiedMessagePriority.HIGH,
    "URGENT": UnifiedMessagePriority.URGENT,
}
TAG_MAP = {
    "GENERAL": UnifiedMessageTag.GENERAL,
    "COORDINATION": UnifiedMessageTag.COORDINATION,
    "TASK": UnifiedMessageTag.TASK,
    "STATUS": UnifiedMessageTag.STATUS,
}


def map_priority(p: str) -> UnifiedMessagePriority:
    return PRIORITY_MAP.get((p or "NORMAL").upper(), UnifiedMessagePriority.NORMAL)


def map_tag(t: str) -> UnifiedMessageTag:
    return TAG_MAP.get((t or "GENERAL").upper(), UnifiedMessageTag.GENERAL)
