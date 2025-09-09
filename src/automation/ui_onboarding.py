from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    pyperclip = None


class UIUnavailableError(Exception):
    """Raised when UI automation is not available."""
    pass


class UIOnboarder:
    """Handles UI-based onboarding automation using PyAutoGUI."""

    def __init__(self, tolerance: int=3, retries: int=1, dry_run: bool=False):
        """Initialize UI onboarder with configuration."""
        if not PYAUTOGUI_AVAILABLE:
            raise UIUnavailableError(
                'PyAutoGUI not available for UI automation')
        try:
            import pyautogui
            self.pyautogui = pyautogui
        except ImportError:
            raise UIUnavailableError(
                'PyAutoGUI not available for UI automation')
        self.tolerance = tolerance
        self.retries = retries
        self.dry_run = dry_run

    def perform(self, agent_id: str, coords: tuple[int, int], message: str
        ) ->bool:
        """Perform UI onboarding sequence for an agent.

        Args:
            agent_id: The agent identifier
            coords: Tuple of (x, y) coordinates
            message: The onboarding message to paste

        Returns:
            bool: True if successful, False otherwise
        """
        if self.dry_run:
            logger.info(
                f'🧪 DRY-RUN: Would onboard {agent_id} at {coords} with message'
                )
            return True
        try:
            x, y = coords
            if not self._validate_coordinates(x, y):
                logger.info(f'❌ Invalid coordinates for {agent_id}: ({x}, {y})'
                    )
                return False
            if not self._validate_message_format(agent_id, message):
                logger.info(f'❌ Invalid message format for {agent_id}')
                return False
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)
            self.pyautogui.hotkey('ctrl', 'n')
            time.sleep(0.5)
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.5)
            for attempt in range(self.retries + 1):
                current_pos = self.pyautogui.position()
                if abs(current_pos.x - x) <= self.tolerance and abs(
                    current_pos.y - y) <= self.tolerance:
                    if PYPERCLIP_AVAILABLE and pyperclip:
                        pyperclip.copy(message)
                        self.pyautogui.hotkey('ctrl', 'v')
                    else:
                        logger.info(
                            f'⚠️ Pyperclip not available, typing message for {agent_id}'
                            )
                        self.pyautogui.typewrite(message, interval=0.01)
                    self.pyautogui.press('enter')
                    time.sleep(1)
                    return True
                else:
                    self.pyautogui.moveTo(x, y)
                    time.sleep(0.2)
            logger.info(
                f'❌ Failed to position mouse at coordinates for {agent_id}')
            return False
        except Exception as e:
            logger.info(f'❌ UI automation error for {agent_id}: {e}')
            return False

    def _validate_coordinates(self, x: int, y: int) ->bool:
        """Validate that coordinates are reasonable for screen interaction.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if coordinates are valid, False otherwise
        """
        if x < 0 or y < 0:
            return False
        if x > 5000 or y > 5000:
            return False
        if x == 0 and y == 0:
            logger.info(
                '⚠️  Using default coordinates (0,0) - may not be accurate')
            return True
        return True

    def _validate_message_format(self, agent_id: str, message: str) ->bool:
        """Validate that the message has the correct format.

        Args:
            agent_id: The agent identifier
            message: The message to validate

        Returns:
            True if message format is valid, False otherwise
        """
        if not message.startswith(f'YOU ARE {agent_id}'):
            logger.info(f"❌ Message does not start with 'YOU ARE {agent_id}'")
            return False
        if '[S2A]' in message:
            logger.info(
                "❌ Message contains [S2A] format - should use 'YOU ARE AGENT X' format"
                )
            return False
        if 'ROLE:' not in message:
            logger.info('❌ Message missing ROLE information')
            return False
        if 'PRIMARY RESPONSIBILITIES:' not in message:
            logger.info('❌ Message missing PRIMARY RESPONSIBILITIES')
            return False
        return True
