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

    def perform(self, agent_id: str, coords: dict, message: str) -> bool:
        """
        Perform UI onboarding sequence for an agent.

        Args:
            agent_id: The agent identifier
            coords: Dictionary with 'x' and 'y' coordinates
            message: The onboarding message to paste

        Returns:
            bool: True if successful, False otherwise
        """
        if self.dry_run:
            print(f"🧪 DRY-RUN: Would onboard {agent_id} at {coords} with message")
            return True

        try:
            x, y = coords["x"], coords["y"]

            # 1. Click onboarding input coordinates
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)

            # 2. Press ctrl+n to create new tab/window (if needed)
            self.pyautogui.hotkey('ctrl', 'n')
            time.sleep(0.5)

            # 3. Click onboarding input coordinates again
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)

            # 4. Validate mouse position with retries
            for attempt in range(self.retries + 1):
                current_pos = self.pyautogui.position()
                if (abs(current_pos.x - x) <= self.tolerance and
                    abs(current_pos.y - y) <= self.tolerance):
                    # Position is correct - paste message
                    pyperclip.copy(message)
                    self.pyautogui.hotkey('ctrl', 'v')
                    self.pyautogui.press('enter')
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
