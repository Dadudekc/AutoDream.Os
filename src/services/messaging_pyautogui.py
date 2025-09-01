#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery - Agent Cellphone V2
===============================================

PyAutoGUI-based message delivery for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
from typing import Dict, Tuple

# Import centralized configuration
from src.utils.config_core import get_config

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
            
            # Validate coordinates before PyAutoGUI operations
            from .coordinate_validator import validate_coordinates_before_delivery
            if not validate_coordinates_before_delivery(coords, recipient):
                print(f"❌ ERROR: Coordinate validation failed for {recipient}")
                return False
            
            # Enforce devlog usage for message delivery operations
            from ..core.devlog_enforcement import enforce_devlog_for_operation
            devlog_success = enforce_devlog_for_operation(
                operation_type="message_delivery",
                agent_id=message.sender,
                title=f"Message Delivery to {recipient}",
                content=f"Delivered message via PyAutoGUI to {recipient} at coordinates {coords}",
                category="progress"
            )
            if not devlog_success:
                print(f"⚠️  WARNING: Devlog enforcement failed for message delivery to {recipient}")

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

            # Send the message - use Ctrl+Enter for urgent priority, regular Enter for regular
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
