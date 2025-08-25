#!/usr/bin/env python3
"""
Unified Messaging System - Agent Cellphone V2
=============================================

This package contains the consolidated messaging system modules
that have been extracted and unified from multiple scattered files.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Import the main classes for easy access
from .unified_messaging_service import UnifiedMessagingService
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .coordinate_manager import CoordinateManager
from .cli_interface import MessagingCLI

# Import consolidated modules from deduplication effort
from .models.v2_message import V2Message
from .types.v2_message_enums import V2MessageType, V2MessagePriority, V2MessageStatus
from .routing.router import V2MessageRouter
from .validation.validator import V2MessageValidator
from .storage.storage import V2MessageStorage
from .queue.message_queue import TDDMessageQueue
from .transformation.message_transformer import MessageTransformer
from .handlers.message_handler import MessageHandlerV2

# Import interfaces
from .interfaces import (
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)

# Import specialized messaging
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging

# Version information
__version__ = "2.0.0"
__author__ = "V2 SWARM CAPTAIN"
__license__ = "MIT"

# Package metadata
__all__ = [
    # Main service
    "UnifiedMessagingService",
    
    # Core messaging
    "UnifiedPyAutoGUIMessaging",
    "CoordinateManager",
    "MessagingCLI",
    
    # Consolidated models and types
    "V2Message",
    "V2MessageType",
    "V2MessagePriority", 
    "V2MessageStatus",
    
    # Consolidated routing and validation
    "V2MessageRouter",
    "V2MessageValidator",
    "V2MessageStorage",
    "TDDMessageQueue",
    "MessageTransformer",
    "MessageHandlerV2",
    
    # Interfaces
    "MessagingMode",
    "MessageType",
    "IMessageSender",
    "IBulkMessaging",
    "ICampaignMessaging",
    "IYOLOMessaging",
    "ICoordinateManager",
    
    # Specialized messaging
    "CampaignMessaging",
    "YOLOMessaging",
    
    # Version info
    "__version__",
    "__author__",
    "__license__"
]

# Convenience function to create a complete messaging system
def create_messaging_system(coordinates_file: str = None):
    """
    Create a complete messaging system with all components.
    
    Args:
        coordinates_file: Optional path to coordinates file
        
    Returns:
        UnifiedMessagingService instance
    """
    return UnifiedMessagingService(coordinates_file)

# Quick access to main functionality
def send_message(recipient: str, message_content: str, message_type: str = "text"):
    """Send a message using the default messaging system."""
    messaging = UnifiedMessagingService()
    return messaging.send_message(recipient, message_content, message_type)

def get_messaging_cli():
    """Get the messaging CLI interface."""
    return MessagingCLI()
