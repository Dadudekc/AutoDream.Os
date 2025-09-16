#!/usr/bin/env python3
"""
Consolidated Messaging Service - V2 COMPLIANT REDIRECT
=====================================================

V2 COMPLIANT: This file now redirects to the modular messaging system.
The original monolithic implementation has been refactored into focused modules:
- messaging/models/ (data models and enums)
- messaging/interfaces/ (abstract interfaces)
- messaging/providers/ (delivery providers)
- messaging/cli/ (command-line interface)
- messaging/consolidated_messaging_service.py (main coordinator)

All modules are V2 compliant (<300 lines, focused responsibilities).

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

# Redirect to the new modular messaging system
try:
    from src.services.messaging.consolidated_messaging_service import (
        ConsolidatedMessagingService,
        get_consolidated_messaging_service,
    )
    from src.services.messaging.models.messaging_models import (
        UnifiedMessage,
        AgentCoordinates,
        MessageHistory,
        MessagingMetrics,
    )
    from src.services.messaging.models.messaging_enums import (
        UnifiedMessageType,
        UnifiedMessagePriority,
        UnifiedMessageTag,
        MessageStatus,
        RecipientType,
    )
    from src.services.messaging.cli.messaging_cli import MessagingCLI
    from src.services.messaging.interfaces.messaging_interfaces import (
        MessageDeliveryProvider,
        PyAutoGUIDeliveryProvider,
        InboxDeliveryProvider,
        MessageHistoryProvider,
        FileBasedMessageHistoryProvider,
    )
    from src.services.messaging.providers.inbox_delivery import InboxMessageDelivery
    from src.services.messaging.providers.pyautogui_delivery import PyAutoGUIMessageDelivery
except ImportError as e:
    # Fallback for when imports fail
    logger.warning(f"Messaging system import failed: {e}")
    ConsolidatedMessagingService = None
    get_consolidated_messaging_service = None
    get_messaging_service = None
    UnifiedMessage = None
    UnifiedMessageType = None
    UnifiedMessagePriority = None
    UnifiedMessageTag = None
    DeliveryMethod = None
    MessageStatus = None
    RecipientType = None
    AgentCoordinates = None
    MessageHistory = None
    MessagingMetrics = None
    MessagingCLI = None
    MessageDeliveryProvider = None
    PyAutoGUIDeliveryProvider = None
    InboxDeliveryProvider = None
    MessageHistoryProvider = None
    FileBasedMessageHistoryProvider = None
    InboxMessageDelivery = None
    PyAutoGUIMessageDelivery = None

# Maintain backward compatibility - re-export all key classes and functions
__all__ = [
    # Main service
    "ConsolidatedMessagingService",
    "get_consolidated_messaging_service",
    "get_messaging_service",

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

    # CLI
    "MessagingCLI",

    # Interfaces
    "MessageDeliveryProvider",
    "PyAutoGUIDeliveryProvider",
    "InboxDeliveryProvider",
    "MessageHistoryProvider",
    "FileBasedMessageHistoryProvider",

    # Providers
    "InboxMessageDelivery",
    "PyAutoGUIMessageDelivery",
]


# ============================================================================
# MISSING FUNCTIONS FOR CLI COMPATIBILITY
# ============================================================================

def broadcast_message(content: str, sender: str = "System") -> dict[str, bool]:
    """Broadcast message to all agents (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    return service.broadcast_message(content, sender)


def get_messaging_core() -> ConsolidatedMessagingService:
    """Get messaging core service (CLI compatibility function)."""
    return get_consolidated_messaging_service()


def list_agents() -> list[str]:
    """List all available agents (CLI compatibility function)."""
    # Return hardcoded list for CLI compatibility
    return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]


def send_message(content: str, recipient: str, priority: str = "normal") -> bool:
    """Send message to specific agent (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    # Convert string priority to enum
    from .messaging.models import UnifiedMessagePriority
    prio = UnifiedMessagePriority.URGENT if priority == "urgent" else UnifiedMessagePriority.NORMAL
    return service.send_message(content, recipient, prio)


def send_message_inbox(content: str, recipient: str, priority: str = "normal") -> bool:
    """Send message via inbox delivery (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    from .messaging.models import UnifiedMessagePriority
    prio = UnifiedMessagePriority.URGENT if priority == "urgent" else UnifiedMessagePriority.NORMAL
    return service.send_message_inbox(content, recipient, prio)


def send_message_pyautogui(content: str, recipient: str, priority: str = "normal", timeout: int = 30) -> bool:
    """Send message via PyAutoGUI delivery (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    from .messaging.models import UnifiedMessagePriority
    prio = UnifiedMessagePriority.URGENT if priority == "urgent" else UnifiedMessagePriority.NORMAL
    return service.send_message_pyautogui(content, recipient, prio, timeout)


def send_message_with_fallback(content: str, recipient: str, priority: str = "normal") -> bool:
    """Send message with fallback delivery (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    from .messaging.models import UnifiedMessagePriority
    prio = UnifiedMessagePriority.URGENT if priority == "urgent" else UnifiedMessagePriority.NORMAL
    return service.send_message_with_fallback(content, recipient, prio)


def show_message_history(recipient: str = None, limit: int = 10) -> list:
    """Show message history (CLI compatibility function)."""
    service = get_consolidated_messaging_service()
    return service.show_message_history(recipient, limit)


def main():
    """Main entry point for CLI usage."""
    import sys
    messaging_service = get_consolidated_messaging_service()
    if messaging_service is None:
        print("Messaging service not available")
        sys.exit(1)
    cli = MessagingCLI(messaging_service)
    sys.exit(cli.run_cli_interface())


if __name__ == "__main__":
    main()
