#!/usr/bin/env python3
"""
PyAutoGUI Handler - Handle PyAutoGUI automation for messaging
===========================================================

PyAutoGUI automation functionality extracted from consolidated_messaging_service.py
for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import time

logger = logging.getLogger(__name__)

# Lazy import to prevent hard dep at import time
try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False
    logger.warning(f"PyAutoGUI import failed: {e}")


class PyAutoGUIHandler:
    """Handle PyAutoGUI automation for agent messaging."""

    def __init__(self) -> None:
        """Initialize PyAutoGUI handler."""
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        if self.pyautogui_available:
            # Configure PyAutoGUI settings
            pyautogui.PAUSE = 0.1
            pyautogui.FAILSAFE = True

    def is_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        return self.pyautogui_available

    def focus_agent_window(self, coordinates: list[int]) -> bool:
        """Focus on agent window using coordinates."""
        if not self.pyautogui_available:
            logger.error("PyAutoGUI not available")
            return False

        try:
            x, y = coordinates
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)  # Wait for focus
            return True
        except Exception as e:
            logger.error(f"Error focusing agent window: {e}")
            return False

    def clear_input_area(self) -> bool:
        """Clear the input area."""
        if not self.pyautogui_available:
            return False

        try:
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)
            return True
        except Exception as e:
            logger.error(f"Error clearing input area: {e}")
            return False

    def create_new_tab(self, method: str = "ctrl_t") -> bool:
        """Create new tab or window."""
        if not self.pyautogui_available:
            return False

        try:
            if method == "ctrl_t":
                pyautogui.hotkey("ctrl", "t")
            elif method == "ctrl_n":
                pyautogui.hotkey("ctrl", "n")
            time.sleep(1.0)  # Wait for tab/window creation
            return True
        except Exception as e:
            logger.error(f"Error creating new tab: {e}")
            return False

    def send_message_content(self, message: str, use_paste: bool = True) -> bool:
        """Send message content via typing or paste."""
        if not self.pyautogui_available:
            return False

        try:
            if use_paste and pyperclip:
                pyperclip.copy(message)
                time.sleep(1.0)  # Wait for clipboard
                pyautogui.hotkey("ctrl", "v")
            else:
                pyautogui.typewrite(message, interval=0.01)

            time.sleep(0.5)
            pyautogui.press("enter")
            return True
        except Exception as e:
            logger.error(f"Error sending message content: {e}")
            return False

    def send_message_to_agent(
        self,
        coordinates: list[int],
        message: str,
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
    ) -> bool:
        """Send complete message to agent via PyAutoGUI."""
        if not self.pyautogui_available:
            logger.error("PyAutoGUI not available for message delivery")
            return False

        try:
            # Focus on agent window
            if not self.focus_agent_window(coordinates):
                return False

            # Clear input area
            if not self.clear_input_area():
                return False

            # Create new tab
            if not self.create_new_tab(new_tab_method):
                return False

            # Send message content
            if not self.send_message_content(message, use_paste):
                return False

            logger.info("Message sent successfully via PyAutoGUI")
            return True

        except Exception as e:
            logger.error(f"Error in PyAutoGUI message delivery: {e}")
            return False

    def send_bulk_messages(
        self,
        agent_list: list[tuple],
        message: str,
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
    ) -> dict:
        """Send message to multiple agents."""
        results = {"success": [], "failed": []}

        for agent_id, coordinates in agent_list:
            try:
                success = self.send_message_to_agent(
                    coordinates, message, use_paste, new_tab_method
                )
                if success:
                    results["success"].append(agent_id)
                    time.sleep(1.0)  # Inter-agent delay
                else:
                    results["failed"].append(agent_id)
            except Exception as e:
                logger.error(f"Error sending to {agent_id}: {e}")
                results["failed"].append(agent_id)

        return results

    def get_screen_info(self) -> dict:
        """Get PyAutoGUI screen information."""
        if not self.pyautogui_available:
            return {"available": False}

        try:
            size = pyautogui.size()
            return {
                "available": True,
                "width": size.width,
                "height": size.height,
                "failsafe_enabled": pyautogui.FAILSAFE,
            }
        except Exception as e:
            logger.error(f"Error getting screen info: {e}")
            return {"available": False, "error": str(e)}
