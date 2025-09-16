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

# Import helper functions from the old models.py for compatibility
try:
    from ..models import map_priority, map_tag
except ImportError:
    # Fallback implementations
    def map_priority(p: str) -> UnifiedMessagePriority:
        priority_map = {
            "LOW": UnifiedMessagePriority.REGULAR,
            "NORMAL": UnifiedMessagePriority.REGULAR,
            "HIGH": UnifiedMessagePriority.URGENT,
            "URGENT": UnifiedMessagePriority.URGENT,
        }
        return priority_map.get((p or "NORMAL").upper(), UnifiedMessagePriority.REGULAR)
    
    def map_tag(t: str) -> UnifiedMessageTag:
        tag_map = {
            "GENERAL": UnifiedMessageTag.CAPTAIN,
            "COORDINATION": UnifiedMessageTag.CAPTAIN,
            "TASK": UnifiedMessageTag.CAPTAIN,
            "STATUS": UnifiedMessageTag.CAPTAIN,
        }
        return tag_map.get((t or "GENERAL").upper(), UnifiedMessageTag.CAPTAIN)

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
    # Helper functions
    "map_priority",
    "map_tag",
]
