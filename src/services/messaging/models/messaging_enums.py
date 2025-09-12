#!/usr/bin/env python3
"""
Messaging Enums - V2 Compliant Module
====================================

Message enumerations and types for unified messaging system.
V2 COMPLIANT: Focused types and enums under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from enum import Enum


class DeliveryMethod(Enum):
    """Delivery methods for messages."""

    INBOX = "inbox"
    PYAUTOGUI = "pyautogui"
    BROADCAST = "broadcast"


class UnifiedMessageType(Enum):
    """Types of messages in the unified messaging system."""

    TEXT = "text"
    DIRECT = "direct"
    BROADCAST = "broadcast"
    SYSTEM = "system"
    STATUS = "status"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"


class UnifiedMessagePriority(Enum):
    """Priority levels for messages."""

    REGULAR = "regular"
    URGENT = "urgent"
    # Legacy support
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class MessageStatus(Enum):
    """Status of message delivery."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""

    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "COORDINATION"
    SYSTEM = "system"
    # Legacy support
    GENERAL = "GENERAL"
    TASK = "TASK"
    STATUS = "STATUS"


class RecipientType(Enum):
    """Types of message recipients."""

    AGENT = "agent"
    SWARM = "swarm"
    SYSTEM = "system"
    BROADCAST = "broadcast"
