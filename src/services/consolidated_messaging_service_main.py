#!/usr/bin/env python3
"""
Consolidated Messaging Service - Unified Interface
=================================================

Unified interface for consolidated messaging service.
Provides backward compatibility and easy access to all messaging components.

V2 Compliance: ≤400 lines, unified interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

from src.services.consolidated_messaging_service_core import (
    ConsolidatedMessagingServiceCore,
    ScreenshotManager,
)
from src.services.consolidated_messaging_service_utils import (
    AgentOnboarder,
    MessageFormatter,
    MessageSender,
)

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService(ConsolidatedMessagingServiceCore):
    """
    Unified consolidated messaging service.

    Integrates core messaging with utilities and CLI functionality.
    """

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize complete messaging service."""
        super().__init__(coord_path)

        # Initialize screenshot manager
        self.screenshot_manager = ScreenshotManager()

        # Initialize utility components
        self.formatter = MessageFormatter()
        self.sender = MessageSender(self.enhanced_handler, self.enhanced_validator)
        self.onboarder = AgentOnboarder(self.coord_path)
        self.logger = logging.getLogger(f"{__name__}.ConsolidatedMessagingService")

    def check_screenshot_trigger(self, cycle_type: str, event_type: str = "NORMAL") -> bool:
        """Check if screenshot should be taken based on messaging cycle."""
        return self.screenshot_manager.should_take_screenshot(cycle_type, event_type)

    def increment_messaging_cycle(self):
        """Increment messaging cycle counter."""
        self.screenshot_manager.increment_cycle()

    def get_screenshot_context(self, trigger_reason: str) -> dict:
        """Get screenshot context for messaging system."""
        return self.screenshot_manager.get_screenshot_context(trigger_reason)

    def get_agent_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get coordinates for specific agent."""
        try:
            return super().get_agent_coordinates(agent_id)
        except Exception as e:
            self.logger.error(f"Error getting coordinates for {agent_id}: {e}")
            return None

    def send_message(
        self, agent_id: str, message: str, from_agent: str = "Agent-4", priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent."""
        try:
            formatted_message = self.formatter.format_a2a_message(
                from_agent, agent_id, message, priority
            )
            coords = self.get_agent_coordinates(agent_id)
            if coords:
                return self.sender.paste_to_coords(coords, formatted_message)
            else:
                self.logger.error(f"Could not get coordinates for {agent_id}")
                return False
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    def broadcast_message(
        self, message: str, from_agent: str = "Agent-4", priority: str = "NORMAL"
    ) -> bool:
        """Broadcast message to all agents."""
        try:
            formatted_message = self.formatter.format_message(message, from_agent, priority)
            return self.sender.broadcast_message(formatted_message)
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")
            return False

    def _create_devlog_entry(self, action: str, details: str) -> None:
        """Create devlog entry for messaging actions."""
        self.logger.info(f"Devlog: {action} - {details}")

    def stall_agent(self, agent_id: str) -> bool:
        """Stall specific agent."""
        try:
            return self.onboarder.stall_agent(agent_id)
        except Exception as e:
            self.logger.error(f"Error stalling agent {agent_id}: {e}")
            return False

    def unstall_agent(self, agent_id: str) -> bool:
        """Unstall specific agent."""
        try:
            return self.onboarder.unstall_agent(agent_id)
        except Exception as e:
            self.logger.error(f"Error unstalling agent {agent_id}: {e}")
            return False

    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard specific agent."""
        try:
            return self.onboarder.hard_onboard_agent(agent_id)
        except Exception as e:
            self.logger.error(f"Error hard onboarding agent {agent_id}: {e}")
            return False

    def hard_onboard_all_agents(self) -> bool:
        """Hard onboard all agents."""
        try:
            return self.onboarder.hard_onboard_all_agents()
        except Exception as e:
            self.logger.error(f"Error hard onboarding all agents: {e}")
            return False

    def get_status(self) -> dict:
        """Get messaging service status."""
        try:
            return {
                "service": "ConsolidatedMessagingService",
                "status": "active",
                "agents_configured": len(self.agent_data),
                "active_agents": len(
                    [
                        agent_id
                        for agent_id, agent in self.agent_data.items()
                        if agent.get("active", True)
                    ]
                ),
                "pyautogui_available": pyautogui is not None,
                "pyperclip_available": pyperclip is not None,
            }
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {"error": str(e)}

    def check_protocol_compliance(self) -> list[str]:
        """Check protocol compliance."""
        try:
            violations = []

            # Check agent coordinates
            for agent_id, agent in self.agent_data.items():
                if not agent.get("active", True):
                    violations.append(f"Agent {agent_id} is inactive")

            return violations
        except Exception as e:
            self.logger.error(f"Error checking protocol compliance: {e}")
            return [f"Protocol check error: {e}"]

    def send_cued_message(
        self, agent_ids: list[str], message: str, cue_id: str, from_agent: str = "Agent-4"
    ) -> bool:
        """Send cued message to multiple agents."""
        try:
            formatted_message = self.formatter.format_cued_message(message, cue_id, from_agent)
            success_count = 0

            for agent_id in agent_ids:
                if self.sender.send_message(agent_id, formatted_message):
                    success_count += 1

            return success_count == len(agent_ids)
        except Exception as e:
            self.logger.error(f"Error sending cued message: {e}")
            return False


# Re-export all components for backward compatibility
__all__ = ["ConsolidatedMessagingService"]
