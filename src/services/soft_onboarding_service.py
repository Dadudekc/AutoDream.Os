"""
Soft Onboarding Service - V2 Compliant
======================================

Handles soft onboarding with 6-STEP SESSION CLEANUP protocol:
1. Click chat input area (get agent's attention)
2. Press Ctrl+Enter (save all changes from session)
3. Send cleanup prompt (closing duties: passdown, devlog, Discord, swarm brain, tool)
4. Press Ctrl+T (open new tab)
5. Navigate to onboarding coords (new tab's input area)
6. Paste onboarding message (send new mission)

All operations go through message queue to prevent race conditions.

V2 Compliance: < 400 lines, single responsibility
"""

import logging
import time

logger = logging.getLogger(__name__)

# Import dependencies
try:
    from .onboarding_template_loader import load_onboarding_template

    TEMPLATE_LOADER_AVAILABLE = True
except ImportError:
    TEMPLATE_LOADER_AVAILABLE = False
    logger.warning("Template loader not available")

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("PyAutoGUI not available")


# Session cleanup message template (Lean Excellence Framework)
# Compact format per STANDARDS.md - focus on essential actions
SESSION_CLEANUP_MESSAGE = """## Agent-{agent_id} Session Cleanup

**Complete Before New Session**:
1. Update `agent_workspaces/{agent_id}/passdown.json` with status/context
2. Create devlog: `devlogs/YYYY-MM-DD_{agent_id}_session.md`
3. Update swarm brain: `python tools/update_swarm_brain.py --insights "..."`

**Optional**: Create tool you wished you had in `tools/`

🐝 WE. ARE. SWARM. ⚡
"""

# Minimal onboarding template (Lean Excellence Framework)
# Use for quick re-onboarding - full template via onboarding_template_loader
ONBOARDING_MIN_TEMPLATE = """# Agent-{agent_id} Onboarding

**Role**: {role}
**Task**: {task}

**Quick Start**:
- Check inbox: `ls agent_workspaces/Agent-{agent_id}/inbox/`
- Update status: `echo '{{...}}' > agent_workspaces/Agent-{agent_id}/status.json`
- Get task: `python -m src.services.messaging_cli --agent Agent-{agent_id} --get-next-task`

**Standards**: See STANDARDS.md | **Full Onboarding**: See AGENTS.md

🚀 Start Working Immediately
"""


class SoftOnboardingService:
    """Handles soft onboarding with session cleanup protocol."""

    def __init__(self):
        """Initialize soft onboarding service."""
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI required for soft onboarding")
        self.pyautogui = pyautogui

    def _load_agent_coordinates(self, agent_id: str) -> tuple[dict, dict]:
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

    def step_1_click_chat_input(self, agent_id: str) -> bool:
        """Step 1: Click chat input area to get agent's attention."""
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

            logger.info(f"👆 Step 1: Clicking chat input for {agent_id} at {chat_coords}")

            # Click chat input to get attention
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.3)

            logger.info(f"✅ Chat input clicked for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to click chat input: {e}")
            return False

    def step_2_save_session(self) -> bool:
        """Step 2: Press Ctrl+Enter to save all changes from session."""
        try:
            logger.info("💾 Step 2: Saving session (Ctrl+Enter)")
            self.pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.5)
            logger.info("✅ Session saved")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")
            return False

    def step_3_send_cleanup_prompt(self, agent_id: str, custom_message: str | None = None) -> bool:
        """Step 3: Send cleanup (closing duties) prompt to agent."""
        try:
            # Use template or custom message
            message = custom_message or SESSION_CLEANUP_MESSAGE.format(agent_id=agent_id)

            logger.info(f"📝 Step 3: Sending cleanup prompt to {agent_id}")

            # Paste cleanup message
            pyperclip.copy(message)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)

            # Press Enter to send
            self.pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ Cleanup prompt sent to {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send cleanup prompt: {e}")
            return False

    def step_4_open_new_tab(self) -> bool:
        """Step 4: Press Ctrl+T to open new tab."""
        try:
            logger.info("🆕 Step 4: Opening new tab (Ctrl+T)")
            self.pyautogui.hotkey("ctrl", "t")
            time.sleep(1.0)  # Wait for new tab to initialize
            logger.info("✅ New tab opened")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to open new tab: {e}")
            return False

    def step_5_navigate_to_onboarding(self, agent_id: str) -> bool:
        """Step 5: Navigate to new tab's coordinates (onboarding input coords)."""
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
                f"🎯 Step 5: Navigating to onboarding coords for {agent_id} at {onboarding_coords}"
            )

            # Move to onboarding input
            self.pyautogui.moveTo(x, y)
            self.pyautogui.click()
            time.sleep(0.3)

            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding input: {e}")
            return False

    def step_6_paste_onboarding_message(
        self, agent_id: str, onboarding_message: str, role: str = None
    ) -> bool:
        """Step 6: Paste and send onboarding message."""
        try:
            logger.info(f"📝 Step 6: Pasting onboarding message for {agent_id}")

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
            logger.error(f"❌ Failed to paste onboarding message: {e}")
            return False

    def execute_soft_onboarding(
        self,
        agent_id: str,
        onboarding_message: str,
        role: str | None = None,
        custom_cleanup_message: str | None = None,
    ) -> bool:
        """
        Execute complete soft onboarding protocol (6 steps).

        Args:
            agent_id: Target agent ID
            onboarding_message: Onboarding message for new session
            role: Optional role assignment
            custom_cleanup_message: Optional custom session cleanup message

        Returns:
            True if all steps completed successfully
        """
        logger.info(f"🚀 Starting soft onboarding for {agent_id} (6-step protocol)")

        # Step 1: Click chat input area (get attention)
        if not self.step_1_click_chat_input(agent_id):
            logger.error("❌ Step 1 failed: Click chat input")
            return False

        # Step 2: Press Ctrl+Enter (save session changes)
        if not self.step_2_save_session():
            logger.error("❌ Step 2 failed: Save session")
            return False

        # Step 3: Send cleanup prompt (closing duties)
        if not self.step_3_send_cleanup_prompt(agent_id, custom_cleanup_message):
            logger.error("❌ Step 3 failed: Cleanup prompt")
            return False

        logger.info("⏳ Waiting for agent to see cleanup prompt...")
        time.sleep(1.0)  # Brief wait

        # Step 4: Press Ctrl+T (open new tab)
        if not self.step_4_open_new_tab():
            logger.error("❌ Step 4 failed: Open new tab")
            return False

        # Step 5: Navigate to onboarding coords (new tab's input area)
        if not self.step_5_navigate_to_onboarding(agent_id):
            logger.error("❌ Step 5 failed: Navigate to onboarding")
            return False

        # Step 6: Paste onboarding message (with full template if role provided)
        if not self.step_6_paste_onboarding_message(agent_id, onboarding_message, role=role):
            logger.error("❌ Step 6 failed: Paste onboarding message")
            return False

        logger.info(f"🎉 Soft onboarding complete for {agent_id}!")
        return True


def soft_onboard_agent(agent_id: str, onboarding_message: str, role: str | None = None) -> bool:
    """
    Convenience function for soft onboarding single agent.

    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message
        role: Optional role assignment

    Returns:
        True if onboarding successful
    """
    try:
        service = SoftOnboardingService()
        return service.execute_soft_onboarding(agent_id, onboarding_message, role)
    except Exception as e:
        logger.error(f"❌ Soft onboarding failed: {e}")
        return False


def soft_onboard_multiple_agents(
    agents: list[tuple[str, str]], role: str | None = None
) -> dict[str, bool]:
    """
    Soft onboard multiple agents sequentially.

    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents

    Returns:
        Dictionary of {agent_id: success_status}
    """
    results = {}
    service = SoftOnboardingService()

    for agent_id, onboarding_message in agents:
        logger.info(f"📝 Processing {agent_id}...")
        success = service.execute_soft_onboarding(agent_id, onboarding_message, role)
        results[agent_id] = success

        if success:
            logger.info(f"✅ {agent_id} soft onboarded successfully")
        else:
            logger.error(f"❌ {agent_id} soft onboarding failed")

        # Wait between agents
        time.sleep(1.0)

    return results
