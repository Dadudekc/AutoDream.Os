#!/usr/bin/env python3
"""
Unified Messaging System - V2 Compliant Consolidation
===================================================

Consolidated messaging system providing unified messaging functionality.
V2 COMPLIANT: This module consolidates 1404 lines into modular components.

Previously monolithic implementation refactored into focused modules:
- models/ (data models and enums)
- interfaces/ (abstract interfaces)
- providers/ (delivery providers)
- cli/ (command-line interface)
- consolidated_messaging_service.py (main coordinator)

All modules are V2 compliant (<300 lines, focused responsibilities).

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .cli import MessagingCLI
from .consolidated_messaging_service import (
    ConsolidatedMessagingService,
    get_consolidated_messaging_service,
    get_messaging_service,
)
from .interfaces import (
    FileBasedMessageHistoryProvider,
    InboxDeliveryProvider,
    MessageDeliveryProvider,
    MessageHistoryProvider,
    PyAutoGUIDeliveryProvider,
)
from .models import (
    AgentCoordinates,
    DeliveryMethod,
    MessageHistory,
    MessageStatus,
    MessagingMetrics,
    RecipientType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from .providers import InboxMessageDelivery as InboxDelivery, PyAutoGUIMessageDelivery

# Maintain backward compatibility
__all__ = [
    # Main service
    "ConsolidatedMessagingService",
    "get_consolidated_messaging_service",
    "get_messaging_service",

    # CLI
    "MessagingCLI",

    # Models and enums
    "UnifiedMessage",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "DeliveryMethod",
    "MessageStatus",
    "RecipientType",
    "AgentCoordinates",
    "MessageHistory",
    "MessagingMetrics",

    # Interfaces
    "MessageDeliveryProvider",
    "PyAutoGUIDeliveryProvider",
    "InboxDeliveryProvider",
    "MessageHistoryProvider",
    "FileBasedMessageHistoryProvider",

    # Providers
    "InboxDelivery",
    "PyAutoGUIMessageDelivery",
]