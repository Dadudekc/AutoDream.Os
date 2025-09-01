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
    
    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True) -> bool:
        """Send message via PyAutoGUI to agent coordinates."""
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
            
            # OPTIMIZED SEQUENCE: Send Ctrl+T to create new tab (no unnecessary message)
            pyautogui.hotkey('ctrl', 't')
            time.sleep(1.0)  # WAIT FOR NEW TAB
            print(f"🆕 NEW TAB CREATED FOR {recipient}")
            
            # Now send the actual message
            if use_paste and PYPERCLIP_AVAILABLE:
                # Fast paste method - copy to clipboard and paste
                pyperclip.copy(message.content)
                time.sleep(1.0)  # INCREASED WAIT TIME BEFORE PASTING
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
            
            # Press Enter to send
            pyautogui.press('enter')
            print(f"📤 MESSAGE SENT VIA PYAUTOGUI TO {recipient}")
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR sending via PyAutoGUI: {e}")
            return False
