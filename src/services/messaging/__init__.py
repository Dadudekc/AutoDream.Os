#!/usr/bin/env python3
"""
Messaging Package - Agent Cellphone V2
=====================================

Clean, modular messaging system following V2 coding standards.
Each module has single responsibility and clean interfaces.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .interfaces import (
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)
from .coordinate_manager import CoordinateManager, AgentCoordinates
from .pyautogui_messaging import PyAutoGUIMessaging
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging
from .unified_messaging_service import UnifiedMessagingService
from .cli_interface import MessagingCLI

__all__ = [
    'MessagingMode',
    'MessageType',
    'IMessageSender',
    'IBulkMessaging',
    'ICampaignMessaging',
    'IYOLOMessaging',
    'ICoordinateManager',
    'CoordinateManager',
    'AgentCoordinates',
    'PyAutoGUIMessaging',
    'CampaignMessaging',
    'YOLOMessaging',
    'UnifiedMessagingService',
    'MessagingCLI'
]

__version__ = "2.0.0"
__author__ = "V2 SWARM CAPTAIN"
