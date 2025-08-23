#!/usr/bin/env python3
"""
Message Delivery Core for V2 Message Delivery Service
Handles actual message delivery using PyAutoGUI or simulation
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Import PyAutoGUI for actual message delivery
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logging.warning("⚠️ PyAutoGUI not available - message delivery will be simulated")

# Optional clipboard library for paste-based delivery
try:
    import pyperclip  # type: ignore
    PYPERCLIP_AVAILABLE = True
except Exception:
    PYPERCLIP_AVAILABLE = False

logger = logging.getLogger(__name__)


class MessageDeliveryCore:
    """Core message delivery functionality"""

    def __init__(self):
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        self.pyperclip_available = PYPERCLIP_AVAILABLE

    def deliver_message(
        self, 
        agent_coords: Dict[str, Any], 
        message_type: str, 
        message_content: str, 
        message_data: Dict[str, Any]
    ) -> bool:
        """Deliver a message to agent coordinates"""
        try:
            if not agent_coords:
                logger.error("❌ No agent coordinates provided")
                return False

            logger.info(
                f"📤 Delivering {message_type} message to coordinates ({agent_coords['input_x']}, {agent_coords['input_y']})"
            )

            # Format message for delivery
            formatted_message = self._format_message_for_delivery(
                message_type, message_content, message_data
            )

            # Actually deliver the message
            if self.pyautogui_available:
                success = self._deliver_via_pyautogui(agent_coords, formatted_message)
            else:
                success = self._simulate_delivery(agent_coords, formatted_message)

            if success:
                logger.info("✅ Message delivered successfully")
            else:
                logger.error("❌ Failed to deliver message")

            return success

        except Exception as e:
            logger.error(f"❌ Error delivering message: {e}")
            return False

    def _format_message_for_delivery(
        self, message_type: str, message_content: str, message_data: Dict[str, Any]
    ) -> str:
        """Format message for delivery to agent"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")

            if message_type == "task_assigned":
                return f"[{timestamp}] 📋 TASK ASSIGNED: {message_data.get('title', 'Unknown Task')}\n\n{message_data.get('description', 'No description')}\n\nPriority: {message_data.get('priority', 'Normal').upper()}\n\nPlease acknowledge receipt."

            elif message_type == "task_progress_update":
                return f"[{timestamp}] 📈 PROGRESS UPDATE: {message_data.get('task_title', 'Unknown Task')}\n\nProgress: {message_data.get('old_progress', 0)}% → {message_data.get('new_progress', 0)}%\nStatus: {message_data.get('status', 'Unknown')}\n\nPlease update your progress tracking."

            elif message_type == "collaboration_session_started":
                return f"[{timestamp}] 🤝 COLLABORATION SESSION: {message_data.get('title', 'Unknown Session')}\n\nObjective: {message_data.get('objective', 'No objective')}\n\nSession ID: {message_data.get('session_id', 'Unknown')}\n\nPlease join the session."

            elif message_type == "presidential_decision_proposed":
                return f"[{timestamp}] 🏛️ PRESIDENTIAL DECISION: {message_data.get('title', 'Unknown Decision')}\n\n{message_data.get('description', 'No description')}\n\nPresident: {message_data.get('president', 'Unknown')}\n\nPlease review and provide feedback."

            elif message_type == "significant_progress":
                return f"[{timestamp}] 🎯 SIGNIFICANT PROGRESS: {message_data.get('task_title', 'Unknown Task')}\n\nProgress: {message_data.get('progress', 0)}% complete\n\nThis is a major milestone! Please coordinate with team members."

            elif message_type == "task_completed":
                return f"[{timestamp}] 🎉 TASK COMPLETED: {message_data.get('task_title', 'Unknown Task')}\n\nCongratulations! Task has been marked as complete.\n\nAssigned Agents: {', '.join(message_data.get('assigned_agents', []))}\n\nPlease update your records."

            elif message_type == "multimedia_update":
                return f"[{timestamp}] 🎬 MULTIMEDIA UPDATE: {message_data.get('message', 'No message')}\n\nMultimedia services are now available.\n\nPlease test your multimedia capabilities."

            else:
                # Generic message format
                return f"[{timestamp}] {message_type.upper()}: {message_content}"

        except Exception as e:
            logger.error(f"❌ Error formatting message: {e}")
            return f"Message delivery error: {str(e)}"

    def _deliver_via_pyautogui(
        self, agent_coords: Dict[str, Any], message: str
    ) -> bool:
        """Actually deliver message using PyAutoGUI"""
        try:
            input_x = agent_coords["input_x"]
            input_y = agent_coords["input_y"]

            # Move to agent input coordinates
            pyautogui.moveTo(input_x, input_y, duration=0.5)
            time.sleep(0.2)

            # Click to focus the input area
            pyautogui.click(input_x, input_y)
            time.sleep(0.2)

            # Clear any existing text (Ctrl+A, Delete)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)

            # Keystroke typing with Shift+Enter for line breaks
            lines = message.split("\n")
            for i, line in enumerate(lines):
                content = line if line is not None else ""
                pyautogui.write(content)
                if i < len(lines) - 1:
                    pyautogui.hotkey("shift", "enter")
                    time.sleep(0.1)

            time.sleep(0.2)

            # Press Enter to send the message
            pyautogui.press("enter")
            time.sleep(0.5)  # Wait for message to be processed

            logger.info(f"✅ Message delivered via PyAutoGUI to ({input_x}, {input_y})")
            return True

        except Exception as e:
            logger.error(f"❌ PyAutoGUI delivery failed: {e}")
            return False

    def _simulate_delivery(self, agent_coords: Dict[str, Any], message: str) -> bool:
        """Simulate message delivery when PyAutoGUI is not available"""
        try:
            logger.info(
                f"🎭 SIMULATED DELIVERY to ({agent_coords['input_x']}, {agent_coords['input_y']}): {message[:100]}..."
            )
            time.sleep(0.5)  # Simulate delivery time
            return True

        except Exception as e:
            logger.error(f"❌ Simulated delivery failed: {e}")
            return False

    def deliver_via_clipboard(
        self, agent_coords: Dict[str, Any], message: str
    ) -> bool:
        """Alternative delivery method using clipboard paste"""
        if not self.pyperclip_available:
            logger.warning("⚠️ PyPerClip not available for clipboard delivery")
            return False

        try:
            input_x = agent_coords["input_x"]
            input_y = agent_coords["input_y"]

            # Copy message to clipboard
            pyperclip.copy(message)

            # Move to coordinates and click
            pyautogui.moveTo(input_x, input_y, duration=0.5)
            pyautogui.click(input_x, input_y)
            time.sleep(0.2)

            # Clear existing text
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)

            # Paste from clipboard
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)

            # Send message
            pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ Message delivered via clipboard to ({input_x}, {input_y})")
            return True

        except Exception as e:
            logger.error(f"❌ Clipboard delivery failed: {e}")
            return False

    def is_pyautogui_available(self) -> bool:
        """Check if PyAutoGUI is available"""
        return self.pyautogui_available

    def is_pyperclip_available(self) -> bool:
        """Check if PyPerClip is available"""
        return self.pyperclip_available

    def get_delivery_methods(self) -> Dict[str, bool]:
        """Get available delivery methods"""
        return {
            "pyautogui": self.pyautogui_available,
            "pyperclip": self.pyperclip_available,
            "simulation": True,  # Always available as fallback
        }

