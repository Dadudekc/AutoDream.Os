#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery
Sends messages to agent chat input coordinates using PyAutoGUI
"""

import logging
import time

logger = logging.getLogger(__name__)

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class PyAutoGUIMessagingDelivery:
    """Delivers messages via PyAutoGUI to agent chat coordinates."""

    def __init__(self):
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI not available")
        self.pyautogui = pyautogui

    def send_message(self, message) -> bool:
        """Send message to agent chat input coordinates."""
        try:
            # Get coordinates for agent
            from .coordinate_loader import get_coordinate_loader

            coord_loader = get_coordinate_loader()

            coords = coord_loader.get_chat_coordinates(message.recipient)
            if not coords:
                logger.error(f"No coordinates for {message.recipient}")
                return False

            x, y = coords

            # Format message content
            msg_content = f"[C2A] CAPTAIN → {message.recipient}\nPriority: {message.priority.value}\n\n{message.content}"

            # Click agent chat input
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.3)

            # Paste message
            pyperclip.copy(msg_content)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)

            # Send message (use Ctrl+Enter for urgent priority)
            if message.priority.value == "urgent":
                self.pyautogui.hotkey("ctrl", "enter")
            else:
                self.pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ Message sent to {message.recipient} at {coords}")
            return True

        except Exception as e:
            logger.error(f"❌ PyAutoGUI delivery failed: {e}")
            return False


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Legacy function for sending messages via PyAutoGUI."""
    try:
        delivery = PyAutoGUIMessagingDelivery()
        from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

        msg = UnifiedMessage(
            content=message,
            sender="CAPTAIN",
            recipient=agent_id,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
        )
        return delivery.send_message(msg)
    except Exception as e:
        logger.error(f"Failed to send PyAutoGUI message: {e}")
        return False


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send message to onboarding coordinates."""
    return send_message_pyautogui(agent_id, message, timeout)
