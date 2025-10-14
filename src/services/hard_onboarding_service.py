"""
Hard Onboarding Service - V2 Compliant
=====================================

Handles hard onboarding with RESET protocol:
1. Go to chat input area, press Ctrl+Shift+Backspace (clear/reset)
2. Press Ctrl+Enter (send/execute)
3. Press Ctrl+N (new window/session)
4. Navigate to onboarding input coordinates
5. Send onboarding message (press Enter)

Hard onboarding = Complete reset, no session cleanup required.
Use for major resets, not regular session transitions.

V2 Compliance: < 400 lines, single responsibility
"""

import logging
import time

logger = logging.getLogger(__name__)

# Import template loader for full onboarding with cycle duties
try:
    from .onboarding_template_loader import load_onboarding_template

    TEMPLATE_LOADER_AVAILABLE = True
    logger.info("✅ Onboarding template loader available")
except ImportError:
    TEMPLATE_LOADER_AVAILABLE = False
    logger.warning("⚠️ Onboarding template loader not available")

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("PyAutoGUI not available for hard onboarding")


class HardOnboardingService:
    """Handles hard onboarding with complete reset protocol."""

    def __init__(self):
        """Initialize hard onboarding service."""
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI required for hard onboarding")
        self.pyautogui = pyautogui

    def _load_agent_coordinates(self, agent_id: str) -> tuple[tuple[int, int], tuple[int, int]]:
        """Load chat and onboarding coordinates for agent."""
        from ..core.coordinate_loader import get_coordinate_loader

        coord_loader = get_coordinate_loader()

        # Get both chat and onboarding coordinates
        chat_coords = coord_loader.get_chat_coordinates(agent_id)
        onboarding_coords = coord_loader.get_onboarding_coordinates(agent_id)

        return chat_coords, onboarding_coords

    def _validate_coordinates(self, agent_id: str, coords: tuple[int, int]) -> bool:
        """Validate coordinates before sending."""
        from ..core.messaging_pyautogui import PyAutoGUIMessagingDelivery

        delivery = PyAutoGUIMessagingDelivery()
        return delivery.validate_coordinates(agent_id, coords)

    def step_1_clear_chat(self, agent_id: str) -> bool:
        """
        Step 1: Go to chat input area and press Ctrl+Shift+Backspace.

        Args:
            agent_id: Target agent ID

        Returns:
            True if successful
        """
        try:
            # Get chat coordinates
            chat_coords, _ = self._load_agent_coordinates(agent_id)
            if not chat_coords:
                logger.error(f"❌ No chat coordinates for {agent_id}")
                return False

            # Validate coordinates
            if not self._validate_coordinates(agent_id, chat_coords):
                logger.error(f"❌ Coordinate validation failed for {agent_id}")
                return False

            x, y = chat_coords

            logger.info(f"🗑️ Step 1: Clearing chat for {agent_id} at {chat_coords}")

            # Click chat input
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.3)

            # Press Ctrl+Shift+Backspace
            self.pyautogui.hotkey("ctrl", "shift", "backspace")
            time.sleep(0.5)

            logger.info(f"✅ Chat cleared for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to clear chat: {e}")
            return False

    def step_2_send_execute(self) -> bool:
        """
        Step 2: Press Ctrl+Enter to send/execute.

        Returns:
            True if successful
        """
        try:
            logger.info("⚡ Step 2: Executing Ctrl+Enter")
            self.pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.5)
            logger.info("✅ Ctrl+Enter executed")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to execute Ctrl+Enter: {e}")
            return False

    def step_3_new_window(self) -> bool:
        """
        Step 3: Press Ctrl+N to create new window/session.

        Returns:
            True if successful
        """
        try:
            logger.info("🆕 Step 3: Creating new window (Ctrl+N)")
            self.pyautogui.hotkey("ctrl", "n")
            time.sleep(1.5)  # Wait for new window to initialize
            logger.info("✅ New window created")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to create new window: {e}")
            return False

    def step_4_navigate_to_onboarding(self, agent_id: str) -> bool:
        """
        Step 4: Navigate to onboarding input coordinates.

        Args:
            agent_id: Target agent ID

        Returns:
            True if successful
        """
        try:
            # Get onboarding coordinates
            _, onboarding_coords = self._load_agent_coordinates(agent_id)
            if not onboarding_coords:
                logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False

            # Validate bounds only (not comparing against chat coords)
            x, y = onboarding_coords

            # Simple bounds check
            if x < -2000 or x > 2000 or y < 0 or y > 1500:
                logger.error(
                    f"❌ Onboarding coordinates out of bounds for {agent_id}: {onboarding_coords}"
                )
                return False

            logger.info(
                f"🎯 Step 4: Navigating to onboarding input for {agent_id} at {onboarding_coords}"
            )

            # Move to and click onboarding input
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.3)

            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding input: {e}")
            return False

    def step_5_send_onboarding_message(
        self, agent_id: str, onboarding_message: str, role: str = None
    ) -> bool:
        """
        Step 5: Send onboarding message via Enter.

        Args:
            agent_id: Target agent ID
            onboarding_message: Custom mission/instructions
            role: Agent role (for full template)

        Returns:
            True if successful
        """
        try:
            logger.info(f"📝 Step 5: Sending onboarding message to {agent_id}")

            # Create FULL onboarding message with cycle duties template
            if TEMPLATE_LOADER_AVAILABLE and role:
                full_message = load_onboarding_template(
                    agent_id=agent_id, role=role, custom_message=onboarding_message
                )
                logger.info("✅ Using FULL template with operating cycle duties")
            else:
                full_message = onboarding_message
                logger.warning("⚠️ Using custom message only (template not available)")

            # Small delay before pasting to ensure input is ready
            time.sleep(0.5)

            # Paste onboarding message
            pyperclip.copy(full_message)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)

            # Press Enter to send
            self.pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ Onboarding message sent to {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send onboarding message: {e}")
            return False

    def execute_hard_onboarding(
        self,
        agent_id: str,
        onboarding_message: str,
        role: str | None = None,
    ) -> bool:
        """
        Execute complete hard onboarding protocol (5 steps).

        Args:
            agent_id: Target agent ID
            onboarding_message: Onboarding message for new session
            role: Optional role assignment

        Returns:
            True if all steps completed successfully
        """
        logger.info(f"🚨 Starting HARD ONBOARDING for {agent_id}")

        # Step 1: Clear chat (Ctrl+Shift+Backspace)
        if not self.step_1_clear_chat(agent_id):
            logger.error("❌ Step 1 failed: Clear chat")
            return False

        # Step 2: Send/Execute (Ctrl+Enter)
        if not self.step_2_send_execute():
            logger.error("❌ Step 2 failed: Send/Execute")
            return False

        # Step 3: New window (Ctrl+N)
        if not self.step_3_new_window():
            logger.error("❌ Step 3 failed: New window")
            return False

        # Step 4: Navigate to onboarding input
        if not self.step_4_navigate_to_onboarding(agent_id):
            logger.error("❌ Step 4 failed: Navigate to onboarding input")
            return False

        # Step 5: Send onboarding message (Enter)
        if not self.step_5_send_onboarding_message(agent_id, onboarding_message, role=role):
            logger.error("❌ Step 5 failed: Send onboarding message")
            return False

        logger.info(f"🎉 Hard onboarding complete for {agent_id}!")
        return True


def hard_onboard_agent(agent_id: str, onboarding_message: str, role: str | None = None) -> bool:
    """
    Convenience function for hard onboarding single agent.

    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message
        role: Optional role assignment

    Returns:
        True if onboarding successful
    """
    try:
        service = HardOnboardingService()
        return service.execute_hard_onboarding(agent_id, onboarding_message, role)
    except Exception as e:
        logger.error(f"❌ Hard onboarding failed: {e}")
        return False


def hard_onboard_multiple_agents(
    agents: list[tuple[str, str]], role: str | None = None
) -> dict[str, bool]:
    """
    Hard onboard multiple agents sequentially.

    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents

    Returns:
        Dictionary of {agent_id: success_status}
    """
    results = {}
    service = HardOnboardingService()

    for agent_id, onboarding_message in agents:
        logger.info(f"🚨 Processing {agent_id}...")
        success = service.execute_hard_onboarding(agent_id, onboarding_message, role)
        results[agent_id] = success

        if success:
            logger.info(f"✅ {agent_id} hard onboarded successfully")
        else:
            logger.error(f"❌ {agent_id} hard onboarding failed")

        # Wait between agents
        time.sleep(2.0)

    return results
