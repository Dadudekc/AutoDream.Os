#!/usr/bin/env python3
"""
Messaging Coordinator - V2 Compliant
===================================

Core messaging coordination logic.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from typing import Any, Dict, Optional

from ..interfaces.messaging_interfaces import MessageHistoryProvider
from ..models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
from ..models.messaging_models import AgentCoordinates, UnifiedMessage
from ..providers.inbox_delivery import InboxMessageDelivery
from ..providers.pyautogui_delivery import PyAutoGUIMessageDelivery

logger = logging.getLogger(__name__)


class MessagingCoordinator:
    """Core messaging coordination logic."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        
        # Initialize delivery providers
        self.pyautogui_delivery = PyAutoGUIMessageDelivery()
        self.inbox_delivery = InboxMessageDelivery()
        
        # Agent coordinates cache
        self.agent_coordinates: Dict[str, AgentCoordinates] = {}
        self._load_coordinates()
        
        logger.info("Messaging Coordinator initialized")
    
    def _load_coordinates(self) -> None:
        """Load agent coordinates."""
        try:
            # Load from PyAutoGUI provider's coordinate system
            coords_dict = self.pyautogui_delivery._load_coordinates_from_json()
            
            for agent_id, coords in coords_dict.items():
                self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, coords)
        except Exception as e:
            logger.warning(f"Failed to load coordinates from PyAutoGUI provider: {e}")
            # Fallback: load directly from coordinate files
            self._load_coordinates_fallback()
    
    def _load_coordinates_fallback(self) -> None:
        """Fallback method to load coordinates directly from files."""
        try:
            import json
            from pathlib import Path
            
            # Try config/coordinates.json first
            config_file = Path(__file__).parent.parent.parent.parent.parent / "config" / "coordinates.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for agent_id, agent_data in data.get("agents", {}).items():
                        coords = agent_data.get("chat_input_coordinates", [0, 0])
                        self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, tuple(coords))
                return
            
            # Try cursor_agent_coords.json as fallback
            cursor_file = Path(__file__).parent.parent.parent.parent.parent / "cursor_agent_coords.json"
            if cursor_file.exists():
                with open(cursor_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for agent_id, agent_data in data.get("agents", {}).items():
                        coords = agent_data.get("chat_input_coordinates", [0, 0])
                        self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, tuple(coords))
                return
                
        except Exception as e:
            logger.error(f"Failed to load coordinates from fallback method: {e}")
    
    def send_message(self, message, target=None, **kwargs):
        """Send a message using the best available delivery method.
        
        Supports both old and new calling conventions:
        - send_message(UnifiedMessage) - new style
        - send_message(message_str, target_dict, **kwargs) - old style for gateway compatibility
        """
        try:
            # Handle different input formats
            if isinstance(message, UnifiedMessage):
                unified_message = message
            else:
                # Convert old format to new format
                unified_message = self._convert_to_unified_message(message, target, **kwargs)
            
            # Choose delivery method based on target type
            if unified_message.target_agent and unified_message.target_agent in self.agent_coordinates:
                # Use PyAutoGUI for agent-to-agent communication
                result = self.pyautogui_delivery.send_message(unified_message)
            else:
                # Use inbox delivery for other cases
                result = self.inbox_delivery.send_message(unified_message)
            
            logger.info(f"Message sent successfully: {unified_message.message_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
    
    def _convert_to_unified_message(self, message, target=None, **kwargs) -> UnifiedMessage:
        """Convert old format parameters to UnifiedMessage."""
        # Extract parameters with defaults
        priority = kwargs.get('priority', UnifiedMessagePriority.NORMAL)
        message_type = kwargs.get('message_type', UnifiedMessageType.TEXT)
        target_agent = kwargs.get('target_agent')
        
        if isinstance(target, dict):
            target_agent = target.get('agent_id') or target.get('target_agent')
        
        return UnifiedMessage(
            message=message,
            priority=priority,
            message_type=message_type,
            target_agent=target_agent,
            metadata=kwargs.get('metadata', {})
        )
    
    def get_agent_coordinates(self, agent_id: str) -> Optional[AgentCoordinates]:
        """Get coordinates for a specific agent."""
        return self.agent_coordinates.get(agent_id)
    
    def list_available_agents(self) -> list[str]:
        """List all available agents with coordinates."""
        return list(self.agent_coordinates.keys())
    
    def get_delivery_status(self) -> Dict[str, Any]:
        """Get status of delivery providers."""
        return {
            "pyautogui_delivery": {
                "available": hasattr(self.pyautogui_delivery, 'send_message'),
                "agents": len(self.agent_coordinates)
            },
            "inbox_delivery": {
                "available": hasattr(self.inbox_delivery, 'send_message')
            },
            "dry_run": self.dry_run
        }

