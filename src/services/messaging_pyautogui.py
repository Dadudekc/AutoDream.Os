#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery - KISS Simplified
==============================================

Simplified PyAutoGUI-based message delivery for the unified messaging service.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined message delivery.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging
import json
import os
from typing import Dict, Tuple, Any, Optional

# Import messaging models
from .models.messaging_models import (
    UnifiedMessage,
    RecipientType,
    SenderType,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ WARNING: PyAutoGUI not available. Install with: pip install pyautogui")

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    print("⚠️ WARNING: Pyperclip not available. Install with: pip install pyperclip")


def load_coordinates_from_json() -> Dict[str, Tuple[int, int]]:
<<<<<<< Updated upstream
    """Load agent coordinates from cursor_agent_coords.json."""
    try:
        config_path = "cursor_agent_coords.json"
        if not os.path.exists(config_path):
            logging.warning(f"Coordinates file not found: {config_path}")
            return {}

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
=======
    """Load agent coordinates using SSOT coordinate loader."""
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()

>>>>>>> Stashed changes
        coordinates = {}
        for agent_id in loader.get_all_agents():
            if loader.is_agent_active(agent_id):
                try:
                    coords = loader.get_chat_coordinates(agent_id)
                    coordinates[agent_id] = coords
                    logging.debug(f"Loaded coordinates for {agent_id}: {coords}")
                except ValueError:
                    logging.warning(f"Invalid coordinates for {agent_id}")

        return coordinates
    except Exception as e:
        logging.error(f"Error loading coordinates: {e}")
        return {}


def get_agent_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Get coordinates for a specific agent using SSOT loader."""
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        return loader.get_chat_coordinates(agent_id)
    except ValueError:
        logging.warning(f"Invalid coordinates for {agent_id}")
        return None


def validate_coordinates_before_delivery(coords, recipient):
    """Validate coordinates before delivery."""
    if not coords:
        logging.error(f"No coordinates found for {recipient}")
        return False
    
    x, y = coords
    # Allow negative X coordinates for multi-monitor setups
    if x < -2000 or x > 2000 or y < 0 or y > 1200:
        logging.error(f"Invalid coordinates for {recipient}: {coords}")
        return False
    
    return True


def deliver_message_pyautogui(message: UnifiedMessage, coords: Tuple[int, int]) -> bool:
    """Deliver message via PyAutoGUI to specific coordinates."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logging.error("PyAutoGUI not available")
            return False

        if not validate_coordinates_before_delivery(coords, message.recipient):
            logging.error("Invalid coordinates")
            return False

        x, y = coords

        # Move to coordinates and focus
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)

        # Clear existing content
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)

        # Format and send message
        formatted_message = format_message_for_delivery(message)

        if PYPERCLIP_AVAILABLE:
            # Fast paste method
            pyperclip.copy(formatted_message)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
        else:
            # Fallback to typing
            pyautogui.typewrite(formatted_message)

        # Press Enter to send the message
        time.sleep(0.2)
        pyautogui.press('enter')

        logging.info(f"Message delivered to {message.recipient} at {coords}")
        return True

    except Exception as e:
        logging.error(f"Error delivering message: {e}")
        return False


def format_message_for_delivery(message: UnifiedMessage) -> str:
    """Format message for delivery with agent identification."""
    try:
        # Get agent identification tag based on message type
        agent_tag = ''
        if message.message_type.value == 'agent_to_agent':
            agent_tag = '[A2A]'
        elif message.message_type.value == 'captain_to_agent':
            agent_tag = '[C2A]'
        elif message.message_type.value == 'system_to_agent':
            agent_tag = '[S2A]'
        elif message.message_type.value == 'human_to_agent':
            agent_tag = '[H2A]'
        elif message.message_type.value == 'broadcast':
            agent_tag = '[BROADCAST]'
        elif message.message_type.value == 'onboarding':
            agent_tag = '[ONBOARDING]'
        else:
            agent_tag = '[TEXT]'
        
        # Format message with agent identification
        formatted = f"{agent_tag} {message.sender} → {message.recipient}\n"
        formatted += f"Priority: {message.priority.value.upper()}\n"
        if message.tags:
            tag_values = ', '.join(tag.value for tag in message.tags)
            formatted += f"Tags: {tag_values}\n"
        formatted += f"\n{message.content}\n"
        formatted += f"\nYou are {message.recipient}\n"
        formatted += f"Timestamp: {message.timestamp}"
        
        return formatted
    except Exception as e:
        logging.error(f"Error formatting message: {e}")
        return message.content


def deliver_bulk_messages_pyautogui(messages: list, agent_order: list = None) -> Dict[str, bool]:
    """Deliver multiple messages via PyAutoGUI."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logging.error("PyAutoGUI not available")
            return {}

        if agent_order is None:
            agent_order = [f"Agent-{i}" for i in range(1, 9)]

        results = {}

        for message in messages:
            if message.recipient in agent_order:
                coords = get_agent_coordinates(message.recipient)
                if coords:
                    success = deliver_message_pyautogui(message, coords)
                    results[message.recipient] = success
                    time.sleep(1)  # Delay between messages
                else:
                    results[message.recipient] = False
            else:
                results[message.recipient] = False

        return results

    except Exception as e:
        logging.error(f"Error delivering bulk messages: {e}")
        return {}


def cleanup_pyautogui_resources():
    """Cleanup PyAutoGUI resources."""
    try:
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            logging.info("PyAutoGUI resources cleaned up")
        return True
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        return False


class PyAutoGUIMessagingDelivery:
    """Simple wrapper class for PyAutoGUI messaging functions."""

    def __init__(self, agents=None):
        """Initialize the delivery service."""
        self.agents = agents or {}

    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True,
                                  new_tab_method: str = "ctrl_t", use_new_tab: bool = None) -> bool:
        """Send message via PyAutoGUI."""
        try:
            coords = get_agent_coordinates(message.recipient)
            if coords:
                return deliver_message_pyautogui(message, coords)
            return False
        except Exception as e:
            logging.error(f"Error sending message via PyAutoGUI: {e}")
            return False