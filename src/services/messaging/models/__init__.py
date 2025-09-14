#!/usr/bin/env python3
"""
Messaging Models Package
=======================

Data models and enumerations for unified messaging system.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .messaging_enums import (
    DeliveryMethod,
    MessageStatus,
    RecipientType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from .messaging_models import (
    AgentCoordinates,
    MessageHistory,
    MessagingMetrics,
    UnifiedMessage,
)

__all__ = [
    # Enums
    "DeliveryMethod",
    "MessageStatus",
    "RecipientType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "UnifiedMessageType",
    # Models
    "AgentCoordinates",
    "MessageHistory",
    "MessagingMetrics",
    "UnifiedMessage",
]
