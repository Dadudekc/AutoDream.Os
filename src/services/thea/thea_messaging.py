#!/usr/bin/env python3
"""
Thea Messenger - PyAutoGUI Message Sending
===========================================

Handles message sending using PyAutoGUI (proven reliable method).

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import logging
import time

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

from .thea_config import TheaConfig

logger = logging.getLogger(__name__)


class TheaMessenger:
    """
    PyAutoGUI-based message sender.

    Responsibilities:
    - Clear input field
    - Send message via clipboard paste
    - Submit message
    - Error handling and retries
    """

    def __init__(self, config: TheaConfig):
        """Initialize messenger."""
        self.config = config

        if not PYAUTOGUI_AVAILABLE:
            logger.warning("⚠️  PyAutoGUI not available - messaging disabled")

        # Set PyAutoGUI settings
        if PYAUTOGUI_AVAILABLE:
            pyautogui.PAUSE = self.config.pyautogui_typing_interval

    def send_message(self, message: str) -> bool:
        """
        Send message using PyAutoGUI.

        Args:
            message: Message text to send

        Returns:
            bool: True if sent successfully
        """
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available")
            return False

        try:
            logger.info("📤 Sending message via PyAutoGUI...")

            # Clear any existing input
            if not self.clear_input():
                logger.warning("⚠️  Failed to clear input, continuing anyway")

            # Copy message to clipboard
            pyperclip.copy(message)
            time.sleep(0.5)  # Wait for clipboard

            # Paste message
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)  # Wait for paste

            logger.info("✅ Message pasted successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    def submit(self) -> bool:
        """
        Submit the message (press Enter).

        Returns:
            bool: True if submitted successfully
        """
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available")
            return False

        try:
            logger.info("📨 Submitting message...")
            pyautogui.press("enter")
            time.sleep(0.5)
            logger.info("✅ Message submitted")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to submit message: {e}")
            return False

    def clear_input(self) -> bool:
        """
        Clear the input field.

        Returns:
            bool: True if cleared successfully
        """
        if not PYAUTOGUI_AVAILABLE:
            return False

        try:
            # Select all and delete
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)
            return True

        except Exception as e:
            logger.debug(f"Clear input error: {e}")
            return False

    def send_and_submit(self, message: str) -> bool:
        """
        Send message and submit in one operation.

        Args:
            message: Message text to send

        Returns:
            bool: True if sent and submitted successfully
        """
        if not self.send_message(message):
            return False

        time.sleep(0.5)  # Brief pause before submit

        return self.submit()

    def type_message(self, message: str, interval: float | None = None) -> bool:
        """
        Type message character-by-character (slower but more reliable).

        Args:
            message: Message to type
            interval: Delay between keystrokes (default: config value)

        Returns:
            bool: True if typed successfully
        """
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available")
            return False

        try:
            logger.info("⌨️  Typing message character-by-character...")

            # Clear input first
            self.clear_input()

            # Type message
            interval = interval or self.config.pyautogui_typing_interval
            pyautogui.write(message, interval=interval)

            logger.info("✅ Message typed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to type message: {e}")
            return False

