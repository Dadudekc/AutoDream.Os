"""
Messaging Delivery Services - V2 Compliant Delivery Layer
========================================================

V2 compliant delivery services for unified messaging system.
Provides multiple delivery mechanisms with fallback support.

V2 Compliance: <300 lines per module, single responsibility
Enterprise Ready: High availability, reliability, monitoring

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

# PyAutoGUI delivery service
from .pyautogui import (
    PyAutoGUIMessagingDelivery,
    deliver_message_pyautogui,
    deliver_bulk_messages_pyautogui,
    format_message_for_delivery,
    get_agent_coordinates,
    cleanup_pyautogui_resources,
    PYAUTOGUI_AVAILABLE,
    PYPERCLIP_AVAILABLE,
)

# Inbox delivery service
from .inbox import (
    InboxDeliveryService,
    inbox_delivery_service,
    get_inbox_delivery_service,
    send_message_to_inbox,
    get_inbox_status,
    get_all_inbox_status,
    cleanup_old_messages,
)

# Fallback delivery service
from .fallback import (
    FallbackDeliveryService,
    fallback_delivery_service,
    get_fallback_delivery_service,
    send_message_via_fallback,
    set_primary_delivery,
    set_secondary_delivery,
    get_delivery_chain_status,
)

# Delivery service exports
__all__ = [
    # PyAutoGUI delivery
    "PyAutoGUIMessagingDelivery",
    "deliver_message_pyautogui",
    "deliver_bulk_messages_pyautogui",
    "format_message_for_delivery",
    "get_agent_coordinates",
    "cleanup_pyautogui_resources",
    "PYAUTOGUI_AVAILABLE",
    "PYPERCLIP_AVAILABLE",
    
    # Inbox delivery
    "InboxDeliveryService",
    "inbox_delivery_service",
    "get_inbox_delivery_service",
    "send_message_to_inbox",
    "get_inbox_status",
    "get_all_inbox_status",
    "cleanup_old_messages",
    
    # Fallback delivery
    "FallbackDeliveryService",
    "fallback_delivery_service",
    "get_fallback_delivery_service",
    "send_message_via_fallback",
    "set_primary_delivery",
    "set_secondary_delivery",
    "get_delivery_chain_status",
]