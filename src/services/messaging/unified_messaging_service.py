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

from src.utils.stability_improvements import safe_import  # stability_manager removed due to abstract class issues
from typing import Dict, Any, Optional, Union, List, Tuple

from .interfaces import (
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)
from .coordinate_manager import CoordinateManager
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging
from .campaign_messaging import CampaignMessaging
from .yolo_messaging import YOLOMessaging
from .message_queue_system import message_queue_system, AgentStatus
from .models.unified_message import UnifiedMessagePriority

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
        return self.pyautogui_messaging.send_bulk_messages(messages, mode, message_type.value, "normal", new_chat)
    
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate coordinates using coordinate manager"""
        return self.coordinate_manager.validate_coordinates()
    
    def validate_agent_coordinates(self, agent_id: str, mode: str = "8-agent") -> Dict[str, Any]:
        """
        Validate coordinates for a specific agent before sending message
        
        Args:
            agent_id: Agent to validate coordinates for
            mode: Coordinate mode to use
            
        Returns:
            Dict with validation results including 'valid' boolean and 'error' if any
        """
        logger.info(f"🔍 Validating coordinates for {agent_id} in {mode} mode")
        
        try:
            # Get agent coordinates
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                return {
                    "valid": False,
                    "error": f"No coordinates found for {agent_id} in {mode} mode"
                }
            
            # Test if coordinates are within multi-monitor bounds
            try:
                import pyautogui
                
                # For multi-monitor setups, we need to account for negative coordinates
                # Since PyAutoGUI 0.9.54 doesn't have getAllMonitors(), we'll use a heuristic approach
                screen_width, screen_height = pyautogui.size()
                
                # Check if coordinates suggest multi-monitor setup (negative X values)
                has_negative_x = any([
                    coords.input_box[0] < 0,
                    coords.starter_location[0] < 0
                ])
                
                if has_negative_x:
                    # Multi-monitor setup detected (negative X coordinates indicate left monitor)
                    # Assume left monitor is roughly the same size as primary monitor
                    min_x = -screen_width  # Left monitor extends to negative X
                    max_x = screen_width   # Right monitor extends to positive X
                    min_y = 0
                    max_y = screen_height
                    
                    logger.info(f"🔍 Multi-monitor setup detected (negative X coordinates)")
                    logger.info(f"   Extended bounds: X({min_x} to {max_x}), Y({min_y} to {max_y})")
                    logger.info(f"   Primary monitor: {screen_width}x{screen_height}")
                    
                else:
                    # Single monitor setup
                    min_x, max_x = 0, screen_width
                    min_y, max_y = 0, screen_height
                    logger.info(f"🔍 Single monitor setup: {screen_width}x{screen_height}")
                
                # Check input box coordinates
                input_x, input_y = coords.input_box
                if not (min_x <= input_x <= max_x and min_y <= input_y <= max_y):
                    return {
                        "valid": False,
                        "error": f"Input box coordinates ({input_x}, {input_y}) out of multi-monitor bounds (X: {min_x} to {max_x}, Y: {min_y} to {max_y})"
                    }
                
                # Check starter location coordinates
                starter_x, starter_y = coords.starter_location
                if not (min_x <= starter_x <= max_x and min_y <= starter_y <= max_y):
                    return {
                        "valid": False,
                        "error": f"Starter coordinates ({starter_x}, {starter_y}) out of multi-monitor bounds (X: {min_x} to {max_x}, Y: {min_y} to {max_y})"
                    }
                
                logger.info(f"✅ Coordinates validated for {agent_id}")
                return {
                    "valid": True,
                    "coordinates": coords,
                    "monitor_bounds": (min_x, max_x, min_y, max_y),
                    "monitor_count": 2 if has_negative_x else 1
                }
                
            except ImportError:
                logger.warning("PyAutoGUI not available - coordinate validation skipped")
                return {
                    "valid": True,
                    "coordinates": coords,
                    "warning": "PyAutoGUI not available, validation limited"
                }
                
        except Exception as e:
            logger.error(f"Error validating coordinates for {agent_id}: {e}")
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
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
    
    def send_coordinated_messages(self, messages: Dict[str, str], priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL) -> Dict[str, bool]:
        """
        Send coordinated messages to all 8 agents through the message queue system
        
        Args:
            messages: Dictionary of agent_id: message_content
            priority: Priority level for all messages
            
        Returns:
            Dict with queuing results for each agent
        """
        logger.info(f"📡 Sending coordinated messages to all agents via queue system (Priority: {priority.value})")
        
        results = {}
        for agent_id, message in messages.items():
            # Queue message through the message queue system
            success = message_queue_system.queue_message(
                agent_id=agent_id,
                message=message,
                message_type="text",
                priority=priority,
                requires_response=True
            )
            
            # Update agent state to working
            if success:
                message_queue_system.update_agent_state(agent_id, AgentStatus.WORKING, "Coordinated message processing")
            
            results[agent_id] = success
            
            logger.info(f"Message queued for {agent_id}: {'✅ Success' if success else '❌ Failed'}")
        
        return results
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current status of the message queue system
        
        Returns:
            Dict with queue status and agent states
        """
        return {
            "queue_size": message_queue_system.message_queue.qsize(),
            "agent_states": message_queue_system.get_all_agent_statuses(),
            "keyboard_conflicts": message_queue_system.check_keyboard_conflicts()
        }
