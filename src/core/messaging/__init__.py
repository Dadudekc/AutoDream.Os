"""
Unified Messaging System - V2 Compliant SSOT
============================================

Single Source of Truth for all messaging functionality.
Consolidated from 84+ files into unified, enterprise-ready architecture.

V2 Compliance: <300 lines per module, single responsibility
Enterprise Ready: High availability, scalability, monitoring
"""

from .core import (
    UnifiedMessagingCore,
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    IMessageDelivery,
    get_messaging_core,
    send_message,
    broadcast_message,
)

__all__ = [
    "UnifiedMessagingCore",
    "UnifiedMessage", 
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "IMessageDelivery",
    "get_messaging_core",
    "send_message",
    "broadcast_message",
]

# Version info
__version__ = "2.0.0"
__author__ = "Agent-4 (Captain) - V2_SWARM"
__license__ = "MIT"
