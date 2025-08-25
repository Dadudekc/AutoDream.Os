#!/usr/bin/env python3
"""
Unified Messaging Service - Agent Cellphone V2
==============================================

Main orchestrator for all messaging capabilities.
Single responsibility: Orchestrate messaging modules.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional, Union, List, Tuple

from .interfaces import (
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)
from .coordinate_manager import CoordinateManager
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging

logger = logging.getLogger(__name__)


class UnifiedMessagingService:
    """
    Unified Messaging Service - Single responsibility: Orchestrate messaging modules
    
    This class only handles:
    - Coordinating between messaging modules
    - Providing unified interface
    - Mode selection and routing
    """
    
    def __init__(self, coordinates_file: str = "runtime/agent_comms/cursor_agent_coords.json"):
        """Initialize the unified messaging service with all modules"""
        # Initialize core modules
        self.coordinate_manager = CoordinateManager(coordinates_file)
        self.pyautogui_messaging = UnifiedPyAutoGUIMessaging(self.coordinate_manager)
        self.campaign_messaging = CampaignMessaging(self.coordinate_manager, self.pyautogui_messaging)
        self.yolo_messaging = YOLOMessaging(self.coordinate_manager, self.pyautogui_messaging)
        
        # Set default mode
        self.active_mode = MessagingMode.PYAUTOGUI
        
        logger.info("Unified Messaging Service initialized with all modules")
    
    def set_mode(self, mode: MessagingMode):
        """Set the active messaging mode"""
        self.active_mode = mode
        logger.info(f"Messaging mode set to: {mode.value}")
    
    def send_message(self, recipient: str, message_content: str, 
                    message_type: MessageType = MessageType.TEXT,
                    mode: MessagingMode = None, new_chat: bool = False) -> Union[bool, Dict[str, bool]]:
        """
        Unified message sending interface
        
        Args:
            recipient: Agent to send message to
            message_content: Message content
            message_type: Type of message
            mode: Messaging mode to use
            new_chat: Whether this is a new chat (onboarding) message
        """
        if mode is None:
            mode = self.active_mode
        
        logger.info(f"Sending {message_type.value} message via {mode.value} to {recipient} (new_chat: {new_chat})")
        
        try:
            if mode == MessagingMode.PYAUTOGUI:
                # Check if this is an onboarding message
                is_onboarding = (message_type == MessageType.ONBOARDING_START or new_chat)
                return self.pyautogui_messaging.send_message(recipient, message_content, message_type.value, is_onboarding)
            
            elif mode == MessagingMode.CAMPAIGN:
                return self.campaign_messaging.send_campaign_message(message_content)
            
            elif mode == MessagingMode.YOLO:
                return self.yolo_messaging.activate_yolo_mode(message_content)
            
            else:
                logger.error(f"Unsupported messaging mode: {mode}")
                return False
                
        except Exception as e:
            logger.error(f"Error in unified message sending: {e}")
            return False
    
    def send_campaign_message(self, message_content: str, campaign_type: str = "election") -> Dict[str, bool]:
        """Send campaign message using campaign messaging module"""
        return self.campaign_messaging.send_campaign_message(message_content, campaign_type)
    
    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        """Activate YOLO mode using YOLO messaging module"""
        return self.yolo_messaging.activate_yolo_mode(message_content)
    
    def send_bulk_messages(self, messages: Dict[str, str], mode: str = "8-agent", message_type: MessageType = MessageType.TEXT, new_chat: bool = False) -> Dict[str, bool]:
        """
        Send bulk messages using PyAutoGUI messaging module
        
        Args:
            messages: Dictionary of agent_id: message_content
            mode: Coordinate mode to use
            message_type: Type of message
            new_chat: Whether these are new chat (onboarding) messages
        """
        return self.pyautogui_messaging.send_bulk_messages(messages, mode, message_type.value, new_chat)
    
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate coordinates using coordinate manager"""
        return self.coordinate_manager.validate_coordinates()
    
    def get_available_modes(self) -> list:
        """Get available coordinate modes"""
        return self.coordinate_manager.get_available_modes()
    
    def get_agents_in_mode(self, mode: str) -> list:
        """Get agents available in a specific mode"""
        return self.coordinate_manager.get_agents_in_mode(mode)
    
    def map_coordinates(self, mode: str = "8-agent") -> Dict[str, Any]:
        """Map and display coordinate information for debugging and calibration"""
        logger.info(f"🗺️  Coordinate mapping requested for mode: {mode}")
        return self.coordinate_manager.map_coordinates(mode)
    
    def calibrate_coordinates(self, agent_id: str, input_coords: Tuple[int, int], starter_coords: Tuple[int, int], mode: str = "8-agent") -> bool:
        """Calibrate/update coordinates for a specific agent"""
        logger.info(f"🔧 Coordinate calibration requested for {agent_id}")
        return self.coordinate_manager.calibrate_coordinates(agent_id, input_coords, starter_coords, mode)
    
    def consolidate_coordinate_files(self) -> Dict[str, Any]:
        """Consolidate multiple coordinate files into primary location"""
        logger.info("🔄 Coordinate file consolidation requested")
        return self.coordinate_manager.consolidate_coordinate_files()
    
    def send_onboarding_message(self, agent_id: str, onboarding_message: str, mode: str = "8-agent") -> bool:
        """
        Send onboarding message using the proper sequence:
        starter location → Ctrl+N → validate → paste onboarding message
        
        Args:
            agent_id: Agent to onboard
            onboarding_message: Onboarding message content
            mode: Coordinate mode to use
        """
        logger.info(f"🚀 Sending onboarding message to {agent_id} via unified service")
        return self.pyautogui_messaging.send_onboarding_message(agent_id, onboarding_message, mode)
    
    def send_bulk_onboarding(self, onboarding_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send onboarding messages to multiple agents using the proper sequence
        
        Args:
            onboarding_messages: Dictionary of agent_id: onboarding_message
            mode: Coordinate mode to use
        """
        logger.info(f"🚀 Sending bulk onboarding messages via unified service")
        return self.pyautogui_messaging.send_bulk_onboarding(onboarding_messages, mode)
    
    def send_high_priority_message(self, agent_id: str, urgent_message: str, mode: str = "8-agent") -> bool:
        """
        Send high priority message using Ctrl+Enter 2x sequence for urgent communications
        
        Args:
            agent_id: Agent to send urgent message to
            urgent_message: High priority message content
            mode: Coordinate mode to use
        """
        logger.info(f"🚨 Sending HIGH PRIORITY message to {agent_id} via unified service")
        return self.pyautogui_messaging.send_high_priority_message(agent_id, urgent_message, mode)
    
    def send_bulk_high_priority(self, urgent_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send high priority messages to multiple agents using Ctrl+Enter 2x sequence
        
        Args:
            urgent_messages: Dictionary of agent_id: urgent_message
            mode: Coordinate mode to use
        """
        logger.info(f"🚨 Sending bulk HIGH PRIORITY messages via unified service")
        return self.pyautogui_messaging.send_bulk_high_priority(urgent_messages, mode)
