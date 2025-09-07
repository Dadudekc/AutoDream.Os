# src/automation/ui_onboarding.py
from __future__ import annotations
import time
import pyperclip
from typing import Tuple


class UIUnavailableError(Exception):
    """Raised when UI automation is not available."""

    pass


class UIOnboarder:
    """Handles UI-based onboarding automation using PyAutoGUI."""

    def __init__(self, tolerance: int = 3, retries: int = 1, dry_run: bool = False):
        """Initialize UI onboarder with configuration."""
        try:
            import pyautogui

            self.pyautogui = pyautogui
        except ImportError:
            raise UIUnavailableError("PyAutoGUI not available for UI automation")

        self.tolerance = tolerance
        self.retries = retries
        self.dry_run = dry_run

    def perform(self, agent_id: str, coords: Tuple[int, int], message: str) -> bool:
        """Perform UI onboarding sequence for an agent.

        Args:
            agent_id: The agent identifier
            coords: Tuple of (x, y) coordinates
            message: The onboarding message to paste

        Returns:
            bool: True if successful, False otherwise
        """
        if self.dry_run:
            print(f"🧪 DRY-RUN: Would onboard {agent_id} at {coords} with message")
            return True

        try:
            x, y = coords

            # Validate coordinates are reasonable
            if not self._validate_coordinates(x, y):
                print(f"❌ Invalid coordinates for {agent_id}: ({x}, {y})")
                return False

            # Validate message format
            if not self._validate_message_format(agent_id, message):
                print(f"❌ Invalid message format for {agent_id}")
                return False

            # 1. Click onboarding input coordinates
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)

            # 2. Press ctrl+n to create new tab/window (if needed)
            self.pyautogui.hotkey("ctrl", "n")
            time.sleep(0.5)

            # 3. Click onboarding input coordinates again
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)

            # 4. Validate mouse position with retries
            for attempt in range(self.retries + 1):
                current_pos = self.pyautogui.position()
                if (
                    abs(current_pos.x - x) <= self.tolerance
                    and abs(current_pos.y - y) <= self.tolerance
                ):
                    # Position is correct - paste message
                    pyperclip.copy(message)
                    self.pyautogui.hotkey("ctrl", "v")
                    self.pyautogui.press("enter")
                    time.sleep(1)
                    return True
                else:
                    # Try to navigate back to coordinates
                    self.pyautogui.moveTo(x, y)
                    time.sleep(0.2)

            # If we get here, validation failed
            print(f"❌ Failed to position mouse at coordinates for {agent_id}")
            return False

        except Exception as e:
            print(f"❌ UI automation error for {agent_id}: {e}")
            return False

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """Validate that coordinates are reasonable for screen interaction.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if coordinates are valid, False otherwise
        """
        # Check if coordinates are within reasonable screen bounds
        # Most screens are at least 800x600, so reject obviously invalid coords
        if x < 0 or y < 0:
            return False
        if x > 5000 or y > 5000:  # Reasonable upper bound
            return False
        if x == 0 and y == 0:  # Default/fallback coordinates
            print("⚠️  Using default coordinates (0,0) - may not be accurate")
            return True
        return True

    def _validate_message_format(self, agent_id: str, message: str) -> bool:
        """Validate that the message has the correct format.
        
        Args:
            agent_id: The agent identifier
            message: The message to validate
            
        Returns:
            True if message format is valid, False otherwise
        """
        # Check for proper agent identification format
        if not message.startswith(f"YOU ARE {agent_id}"):
            print(f"❌ Message does not start with 'YOU ARE {agent_id}'")
            return False
        
        # Check for [S2A] format (should not be present)
        if "[S2A]" in message:
            print("❌ Message contains [S2A] format - should use 'YOU ARE AGENT X' format")
            return False
        
        # Check for role information
        if "ROLE:" not in message:
            print("❌ Message missing ROLE information")
            return False
        
        # Check for responsibilities
        if "PRIMARY RESPONSIBILITIES:" not in message:
            print("❌ Message missing PRIMARY RESPONSIBILITIES")
            return False
        
        return True
