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
from .models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
)

# Backward compatibility aliases
from .models.unified_message import (
    Message,      # Alias for UnifiedMessage
    V2Message,    # Alias for UnifiedMessage
    AgentMessage, # Alias for UnifiedMessage
)

# Core messaging services
from .unified_messaging_service import UnifiedMessagingService
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .coordinate_manager import CoordinateManager

# Specialized messaging services
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging

# Interfaces and types
from .interfaces import (
    MessagingMode,
    MessageType,
    IMessageSender,
    IBulkMessaging,
    ICampaignMessaging,
    IYOLOMessaging,
    ICoordinateManager,
)

# Message Queue System is now consolidated into UnifiedMessagingService
# No separate import needed - all functionality is unified

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
    "ICoordinateManager"
]

# Version info
__version__ = "2.0.0"
__description__ = "Unified Messaging System - SSOT COMPLIANT - Single Source of Truth Restored"
