<<<<<<< HEAD
#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery - KISS Simplified
==============================================

Simplified PyAutoGUI-based message delivery for the unified messaging service.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined message delivery.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: V2 SWARM CAPTAIN
=======
from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery - Agent Cellphone V2
===============================================

PyAutoGUI-based message delivery for the unified messaging service.

Author: V2 SWARM CAPTAIN
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
License: MIT
"""

import time
<<<<<<< HEAD
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

# Import validation system - removed for now

try:
    import pyautogui

=======
from typing import Dict, Tuple

try:
    import pyautogui
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ WARNING: PyAutoGUI not available. Install with: pip install pyautogui")

try:
    import pyperclip
<<<<<<< HEAD

=======
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    print("⚠️ WARNING: Pyperclip not available. Install with: pip install pyperclip")

<<<<<<< HEAD

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


def deliver_message_pyautogui(
    message: UnifiedMessage,
    coords: Tuple[int, int],
    new_tab_method: str = "ctrl_t",
    no_paste: bool = False,
) -> bool:
    """Deliver message using PyAutoGUI - simplified."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logging.error("PyAutoGUI not available")
            return False

        if not validate_coordinates_before_delivery(coords, message.recipient):
            logging.error("Invalid coordinates")
            return False

        x, y = coords

        # Move to coordinates and click
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)

        # Clear input
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        time.sleep(0.2)

        # Create new tab/window
        if new_tab_method == "ctrl_t":
            pyautogui.hotkey("ctrl", "t")
        elif new_tab_method == "ctrl_n":
            pyautogui.hotkey("ctrl", "n")
        time.sleep(0.5)

        # Send message content
        if no_paste:
            # Type message line by line
            lines = message.content.split("\n")
            for i, line in enumerate(lines):
                pyautogui.typewrite(line)
                if i < len(lines) - 1:
                    pyautogui.hotkey("shift", "enter")
            pyautogui.press("enter")
        else:
            # Use clipboard paste
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message.content)
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("enter")
            else:
                # Fallback to typing
                pyautogui.typewrite(message.content)
                pyautogui.press("enter")

        logging.info(f"Message delivered to {message.recipient} at {coords}")
        return True

    except Exception as e:
        logging.error(f"Error delivering message: {e}")
        return False


def format_message_for_delivery(message: UnifiedMessage) -> str:
    """Format message for delivery - simplified."""
    try:
        # Basic message formatting
        formatted = f"📨 {message.message_type.value.upper()}\n"
        formatted += f"From: {message.sender}\n"
        formatted += f"To: {message.recipient}\n"
        formatted += f"Priority: {message.priority.value}\n"
        if message.tags:
            formatted += f"Tags: {', '.join(tag.value for tag in message.tags)}\n"
        formatted += f"\n{message.content}\n"
        formatted += f"\nTimestamp: {message.timestamp}"

        return formatted
    except Exception as e:
        logging.error(f"Error formatting message: {e}")
        return message.content


def deliver_bulk_messages_pyautogui(
    messages: list, agent_order: list = None
) -> Dict[str, bool]:
    """Deliver bulk messages using PyAutoGUI - simplified."""
    try:
        if not agent_order:
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


def get_pyautogui_status() -> Dict[str, Any]:
    """Get PyAutoGUI status - simplified."""
    return {
        "pyautogui_available": PYAUTOGUI_AVAILABLE,
        "pyperclip_available": PYPERCLIP_AVAILABLE,
        "status": "ready" if PYAUTOGUI_AVAILABLE else "not_available",
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
=======
from .models.messaging_models import UnifiedMessage


class PyAutoGUIMessagingDelivery:
    """PyAutoGUI-based message delivery system."""
    
    def __init__(self, agents: Dict[str, Dict[str, any]]):
        """Initialize PyAutoGUI delivery with agent coordinates."""
        self.agents = agents
    
    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True,
                                   new_tab_method: str = "ctrl_t", use_new_tab: bool = True) -> bool:
        """Send message via PyAutoGUI to agent coordinates.

        Args:
            message: The message to send
            use_paste: Whether to use clipboard paste (faster) or typing
            new_tab_method: "ctrl_t" for Ctrl+T or "ctrl_n" for Ctrl+N
            use_new_tab: Whether to create new tab/window (True for onboarding, False for regular messages)
        """
        if not PYAUTOGUI_AVAILABLE:
            print("❌ ERROR: PyAutoGUI not available for coordinate delivery")
            return False

        try:
            recipient = message.recipient
            if recipient not in self.agents:
                print(f"❌ ERROR: Unknown recipient {recipient}")
                return False

            coords = self.agents[recipient]["coords"]

            # Move to agent coordinates
            pyautogui.moveTo(coords[0], coords[1], duration=0.5)
            print(f"📍 MOVED TO {recipient} COORDINATES: {coords}")

            # Click to focus
            pyautogui.click()
            time.sleep(0.5)

            # Clear any existing content (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)

            # Create new tab/window ONLY for onboarding messages or when explicitly requested
            if use_new_tab:
                if new_tab_method == "ctrl_n":
                    pyautogui.hotkey('ctrl', 'n')
                    print(f"🆕 NEW WINDOW CREATED FOR {recipient} (Ctrl+N)")
                else:  # default to ctrl_t
                    pyautogui.hotkey('ctrl', 't')
                    print(f"🆕 NEW TAB CREATED FOR {recipient} (Ctrl+T)")

                time.sleep(1.0)  # WAIT FOR NEW TAB/WINDOW

            # Now send the actual message
            if use_paste and PYPERCLIP_AVAILABLE:
                # Fast paste method - copy to clipboard and paste
                pyperclip.copy(message.content)
                time.sleep(0.5 if use_new_tab else 0.1)  # Shorter wait for direct messaging
                pyautogui.hotkey('ctrl', 'v')
                print(f"📋 FAST PASTED MESSAGE TO {recipient}")
            else:
                # Slow type method for special formatting
                content = message.content
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    pyautogui.write(line, interval=0.01)
                    if i < len(lines) - 1:
                        pyautogui.hotkey('shift', 'enter')
                        time.sleep(0.1)
                print(f"⌨️ TYPED MESSAGE TO {recipient} WITH PROPER FORMATTING")

            # Send the message - use Ctrl+Enter for high priority, regular Enter for normal
            from .models.messaging_models import UnifiedMessagePriority
            if message.priority == UnifiedMessagePriority.URGENT:
                # High priority: Send with Ctrl+Enter twice
                pyautogui.hotkey('ctrl', 'enter')
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'enter')
                print(f"🚨 HIGH PRIORITY MESSAGE SENT TO {recipient} (Ctrl+Enter x2)")
            else:
                # Normal priority: Send with regular Enter
                pyautogui.press('enter')
                print(f"📤 MESSAGE SENT VIA PYAUTOGUI TO {recipient}")

            return True

        except Exception as e:
            print(f"❌ ERROR sending via PyAutoGUI: {e}")
            return False
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
