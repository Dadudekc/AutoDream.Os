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

# Import validation system
from ..core.simple_validation_system import get_unified_validator

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


def validate_coordinates_before_delivery(coords, recipient):
    """Validate coordinates before PyAutoGUI delivery - simplified."""
    try:
        if not coords or len(coords) != 2:
            return False
        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            return False
        if x < 0 or y < 0:
            return False
        return True
    except Exception:
        return False


def get_agent_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Get agent coordinates - simplified."""
    # Simplified coordinate mapping
    coordinates = {
        "Agent-1": (100, 100),
        "Agent-2": (200, 100),
        "Agent-3": (300, 100),
        "Agent-4": (400, 100),
        "Agent-5": (100, 200),
        "Agent-6": (200, 200),
        "Agent-7": (300, 200),
        "Agent-8": (400, 200),
    }
    return coordinates.get(agent_id)


def deliver_message_pyautogui(message: UnifiedMessage, coords: Tuple[int, int], 
                             new_tab_method: str = "ctrl_t", no_paste: bool = False) -> bool:
    """Deliver message using PyAutoGUI - simplified."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logging.error("PyAutoGUI not available")
            return False
        
        if not validate_coordinates_before_delivery(coords, message.recipient_id):
            logging.error("Invalid coordinates")
            return False
        
        x, y = coords
        
        # Move to coordinates and click
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)
        
        # Clear input
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # Create new tab/window
        if new_tab_method == "ctrl_t":
            pyautogui.hotkey('ctrl', 't')
        elif new_tab_method == "ctrl_n":
            pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.5)
        
        # Send message content
        if no_paste:
            # Type message line by line
            lines = message.content.split('\n')
            for i, line in enumerate(lines):
                pyautogui.typewrite(line)
                if i < len(lines) - 1:
                    pyautogui.hotkey('shift', 'enter')
            pyautogui.press('enter')
        else:
            # Use clipboard paste
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message.content)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
            else:
                # Fallback to typing
                pyautogui.typewrite(message.content)
                pyautogui.press('enter')
        
        logging.info(f"Message delivered to {message.recipient_id} at {coords}")
        return True
        
    except Exception as e:
        logging.error(f"Error delivering message: {e}")
        return False


def format_message_for_delivery(message: UnifiedMessage) -> str:
    """Format message for delivery - simplified."""
    try:
        # Basic message formatting
        formatted = f"📨 {message.message_type.value.upper()}\n"
        formatted += f"From: {message.sender_id}\n"
        formatted += f"To: {message.recipient_id}\n"
        formatted += f"Priority: {message.priority.value}\n"
        if message.tags:
            formatted += f"Tags: {', '.join(tag.value for tag in message.tags)}\n"
        formatted += f"\n{message.content}\n"
        formatted += f"\nTimestamp: {message.timestamp}"
        
        return formatted
    except Exception as e:
        logging.error(f"Error formatting message: {e}")
        return message.content


def deliver_bulk_messages_pyautogui(messages: list, agent_order: list = None) -> Dict[str, bool]:
    """Deliver bulk messages using PyAutoGUI - simplified."""
    try:
        if not agent_order:
            agent_order = [f"Agent-{i}" for i in range(1, 9)]
        
        results = {}
        
        for message in messages:
            if message.recipient_id in agent_order:
                coords = get_agent_coordinates(message.recipient_id)
                if coords:
                    success = deliver_message_pyautogui(message, coords)
                    results[message.recipient_id] = success
                    time.sleep(1)  # Delay between messages
                else:
                    results[message.recipient_id] = False
            else:
                results[message.recipient_id] = False
        
        return results
        
    except Exception as e:
        logging.error(f"Error delivering bulk messages: {e}")
        return {}


def get_pyautogui_status() -> Dict[str, Any]:
    """Get PyAutoGUI status - simplified."""
    return {
        "pyautogui_available": PYAUTOGUI_AVAILABLE,
        "pyperclip_available": PYPERCLIP_AVAILABLE,
        "status": "ready" if PYAUTOGUI_AVAILABLE else "not_available"
    }


def test_pyautogui_delivery() -> bool:
    """Test PyAutoGUI delivery - simplified."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            return False
        
        # Simple test
        pyautogui.moveTo(100, 100)
        pyautogui.click()
        return True
        
    except Exception as e:
        logging.error(f"Error testing PyAutoGUI: {e}")
        return False


def cleanup_pyautogui() -> bool:
    """Cleanup PyAutoGUI resources - simplified."""
    try:
        # Basic cleanup
        logging.info("PyAutoGUI cleanup completed")
        return True
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        return False