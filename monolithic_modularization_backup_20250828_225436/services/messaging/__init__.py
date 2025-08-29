from .campaign_messaging import CampaignMessaging
from .coordinate_manager import CoordinateManager
from .interfaces import (
from .message_queue_system import (
from .models.unified_message import (
from .models.unified_message import (
from .unified_messaging_service import UnifiedMessagingService
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .yolo_messaging import YOLOMessaging

#!/usr/bin/env python3
"""
Unified Messaging System - Agent Cellphone V2
============================================

Complete messaging system with unified models, handlers, and services.
All Message classes consolidated into single UnifiedMessage system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Core unified message system
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
)

# Backward compatibility aliases
    Message,      # Alias for UnifiedMessage
    V2Message,    # Alias for UnifiedMessage
    AgentMessage, # Alias for UnifiedMessage
)

# Core messaging services

# Specialized messaging services

# Interfaces and types
    MessagingMode,
    MessageType,
    IMessageSender,
    IBulkMessaging,
    ICampaignMessaging,
    IYOLOMessaging,
    ICoordinateManager,
)

# Message Queue System for 8-agent coordination
    MessageQueueSystem,
    AgentStatus,
    QueuedMessage,
    AgentState,
    message_queue_system
)

# Export all components
__all__ = [
    # Core unified message system
    "UnifiedMessage",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageStatus",
    "UnifiedMessageTag",
    
    # Backward compatibility
    "Message",
    "V2Message",
    "AgentMessage",
    
    # Core services
    "UnifiedMessagingService",
    "UnifiedPyAutoGUIMessaging",
    "CoordinateManager",
    
    # Specialized services
    "CampaignMessaging",
    "YOLOMessaging",
    
    # Interfaces
    "MessagingMode",
    "MessageType",
    "IMessageSender",
    "IBulkMessaging",
    "ICampaignMessaging",
    "IYOLOMessaging",
    "ICoordinateManager",
    'MessageQueueSystem',
    'AgentStatus',
    'QueuedMessage',
    'AgentState',
    'message_queue_system'
]

# Version info
__version__ = "2.0.0"
__description__ = "Unified Messaging System - Single Source of Truth"
