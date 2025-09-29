#!/usr/bin/env python3
"""
Core Messaging Service
======================

Core messaging functionality for agent-to-agent communication.
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))

from .coordinate_loader import CoordinateLoader

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class MessagingService:
    """Core messaging service for agent communication."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize messaging service with coordinate validation."""
        self.coords_file = coord_path
        self.loader = CoordinateLoader(coord_path)
        self.loader.load()
        self.validation_report = self.loader.validate_all()

        if not self.validation_report.is_all_ok():
            logger.warning("Coordinate validation issues detected")
            for issue in self.validation_report.issues:
                logger.warning(f"  - {issue}")

    def send_message(
        self, agent_id: str, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent via PyAutoGUI automation."""
        if not self._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, message not sent")
            return False

        try:
            # Auto-detect sender if not provided
            if from_agent is None:
                from ..agent_context import get_current_agent

                from_agent = get_current_agent()

            # Get agent coordinates
            try:
                coords = self.loader.get_agent_coordinates(agent_id)
            except ValueError as e:
                logger.error(f"Agent {agent_id} not found in coordinates: {e}")
                return False

            # Format A2A message
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)

            # Send via PyAutoGUI
            success = self._paste_to_coords(coords, formatted_message)

            if success:
                logger.info(f"Message sent to {agent_id} from {from_agent}")
            else:
                logger.error(f"Failed to send message to {agent_id}")

            return success

        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    def broadcast_message(
        self, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> dict[str, bool]:
        """Send message to all active agents."""
        results = {}

        # Auto-detect sender if not provided
        if from_agent is None:
            from ..agent_context import get_current_agent

            from_agent = get_current_agent()

        for agent_id in self.loader.get_agent_ids():
            if self._is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")

        return results

    def get_available_agents(self) -> dict[str, bool]:
        """Get all available agents and their active status."""
        agents_status = {}

        for agent_id in self.loader.get_agent_ids():
            agents_status[agent_id] = self._is_agent_active(agent_id)

        return agents_status

    def _get_quality_guidelines(self) -> str:
        """Get quality guidelines reminder for all agent communications."""
        return """🎯 QUALITY GUIDELINES REMINDER
============================================================
📋 V2 Compliance Requirements:
• File Size: ≤400 lines (hard limit)
• Enums: ≤3 per file
• Classes: ≤5 per file
• Functions: ≤10 per file
• Complexity: ≤10 cyclomatic complexity per function
• Parameters: ≤5 per function
• Inheritance: ≤2 levels deep

🚫 Forbidden Patterns (Red Flags):
• Abstract Base Classes (without 2+ implementations)
• Excessive async operations (without concurrency need)
• Complex inheritance chains (>2 levels)
• Event sourcing for simple operations
• Dependency injection for simple objects
• Threading for synchronous operations
• 20+ fields per entity
• 5+ enums per file

✅ Required Patterns (Green Flags):
• Simple data classes with basic fields
• Direct method calls instead of complex event systems
• Synchronous operations for simple tasks
• Basic validation for essential data
• Simple configuration with defaults
• Basic error handling with clear messages

🎯 KISS Principle: Start with the simplest solution that works!
📊 QUALITY GATES: Run `python quality_gates.py` before submitting code!
============================================================"""

    def _format_a2a_message(
        self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL"
    ) -> str:
        """Format agent-to-agent message with standard template and quality guidelines."""
        quality_guidelines = self._get_quality_guidelines()
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority}
Tags: GENERAL
------------------------------------------------------------
{message}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
{quality_guidelines}
------------------------------------------------------------
"""

    def _paste_to_coords(self, coords, message: str) -> bool:
        """Paste message to coordinates using PyAutoGUI."""
        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or Pyperclip not available")
            return False

        try:
            # Copy message to clipboard
            pyperclip.copy(message)

            # Click coordinates
            pyautogui.click(coords[0], coords[1])
            pyautogui.sleep(0.5)

            # Paste message
            pyautogui.hotkey("ctrl", "v")
            pyautogui.sleep(0.5)

            # Send message
            pyautogui.press("enter")

            return True

        except Exception as e:
            logger.error(f"Error pasting to coordinates: {e}")
            return False

    def _is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        try:
            agents = self.loader.coordinates.get("agents", {})
            agent_data = agents.get(agent_id, {})
            return agent_data.get("active", True)
        except Exception:
            return True  # Default to active if check fails
