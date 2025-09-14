"""
Unified Messaging Core - V2 Compliant Single Source of Truth
===========================================================

SINGLE SOURCE OF TRUTH for all messaging functionality.
Consolidated from multiple messaging modules into unified architecture.

V2 Compliance: <300 lines per module, single responsibility
Enterprise Ready: High availability, scalability, monitoring, security

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

# Core messaging system
from .core import (
    UnifiedMessagingCore,
    get_messaging_core,
    send_message,
    send_message_object,
    broadcast_message,
    generate_onboarding_message,
    onboard_agent,
    onboard_swarm,
    list_agents,
    get_system_status,
    health_check,
    messaging_core,
)

# Models and data structures
from .models import (
    # Enums
    DeliveryMethod,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    RecipientType,
    SenderType,
    MessageStatus,
    
    # Data Classes
    UnifiedMessage,
    AgentCoordinates,
    MessageHistory,
    MessagingMetrics,
    
    # Utility Functions
    create_message,
    create_broadcast_message,
    create_onboarding_message,
)

# Interfaces and protocols
from .interfaces import (
    # Core Interfaces
    IMessageDelivery,
    IOnboardingService,
    ICoordinateProvider,
    IMessageHistory,
    IMessagingMetrics,
    
    # Abstract Base Classes
    BaseMessageDelivery,
    BaseOnboardingService,
    BaseCoordinateProvider,
    
    # Utility Interfaces
    IMessageValidator,
    IMessageFormatter,
    IMessageRouter,
    IRetryHandler,
    
    # Factory Interfaces
    IMessageDeliveryFactory,
    IOnboardingServiceFactory,
    
    # Configuration Interfaces
    IMessagingConfig,
)

# Delivery services
from .delivery.pyautogui import (
    PyAutoGUIMessagingDelivery,
    deliver_message_pyautogui,
    deliver_bulk_messages_pyautogui,
    format_message_for_delivery,
    get_agent_coordinates,
    cleanup_pyautogui_resources,
    PYAUTOGUI_AVAILABLE,
    PYPERCLIP_AVAILABLE,
)

from .delivery.inbox import (
    InboxDeliveryService,
    inbox_delivery_service,
    get_inbox_delivery_service,
    send_message_to_inbox,
    get_inbox_status,
    get_all_inbox_status,
    cleanup_old_messages,
)

from .delivery.fallback import (
    FallbackDeliveryService,
    fallback_delivery_service,
    get_fallback_delivery_service,
    send_message_via_fallback,
    set_primary_delivery,
    set_secondary_delivery,
    get_delivery_chain_status,
)

# Core exports - Single Source of Truth
__all__ = [
    # Core messaging system
    "UnifiedMessagingCore",
    "get_messaging_core",
    "send_message",
    "send_message_object",
    "broadcast_message",
    "generate_onboarding_message",
    "onboard_agent",
    "onboard_swarm",
    "list_agents",
    "get_system_status",
    "health_check",
    "messaging_core",
    
    # Models and data structures
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "MessageStatus",
    "UnifiedMessage",
    "AgentCoordinates",
    "MessageHistory",
    "MessagingMetrics",
    "create_message",
    "create_broadcast_message",
    "create_onboarding_message",
    
    # Interfaces
    "IMessageDelivery",
    "IOnboardingService",
    "ICoordinateProvider",
    "IMessageHistory",
    "IMessagingMetrics",
    "BaseMessageDelivery",
    "BaseOnboardingService",
    "BaseCoordinateProvider",
    "IMessageValidator",
    "IMessageFormatter",
    "IMessageRouter",
    "IRetryHandler",
    "IMessageDeliveryFactory",
    "IOnboardingServiceFactory",
    "IMessagingConfig",
    
    # Delivery services
    "PyAutoGUIMessagingDelivery",
    "deliver_message_pyautogui",
    "deliver_bulk_messages_pyautogui",
    "format_message_for_delivery",
    "get_agent_coordinates",
    "cleanup_pyautogui_resources",
    "PYAUTOGUI_AVAILABLE",
    "PYPERCLIP_AVAILABLE",
    
    "InboxDeliveryService",
    "inbox_delivery_service",
    "get_inbox_delivery_service",
    "send_message_to_inbox",
    "get_inbox_status",
    "get_all_inbox_status",
    "cleanup_old_messages",
    
    "FallbackDeliveryService",
    "fallback_delivery_service",
    "get_fallback_delivery_service",
    "send_message_via_fallback",
    "set_primary_delivery",
    "set_secondary_delivery",
    "get_delivery_chain_status",
]

# Version info
__version__ = "2.0.0"
__author__ = "Agent-4 (Captain) - V2_SWARM"
__license__ = "MIT"