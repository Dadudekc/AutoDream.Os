#!/usr/bin/env python3
"""
Messaging Core - Base classes and enums for messaging system
===========================================================

Core messaging classes and enums used by the PyAutoGUI messaging system.

Author: Agent-8 (Operations & Swarm Coordinator)
License: MIT
"""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


class UnifiedMessageType(Enum):
    """Message type enumeration with formatting support."""
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"


class UnifiedMessagePriority(Enum):
    """Message priority levels."""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class UnifiedMessageTag(Enum):
    """Message tags for categorization."""
    GENERAL = "GENERAL"
    COORDINATION = "COORDINATION"
    TASK = "TASK"
    STATUS = "STATUS"
    CLEANUP = "CLEANUP"
    MODULARIZATION = "MODULARIZATION"


@dataclass
class UnifiedMessage:
    """Unified message structure with formatting support."""
    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority
    tags: List[UnifiedMessageTag]
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


