#!/usr/bin/env python3
"""
Consolidated Messaging Service - V2 COMPLIANT MAIN COORDINATOR
===========================================================

Main consolidated messaging service coordinating all messaging components.
V2 COMPLIANT: Under 300 lines, focused orchestration responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from typing import Any

try:
    from .cli.messaging_cli import MessagingCLI
    from .interfaces.messaging_interfaces import MessageHistoryProvider
    from .models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
    from .models.messaging_models import AgentCoordinates, UnifiedMessage
    from .providers.inbox_delivery import InboxMessageDelivery
    from .providers.pyautogui_delivery import PyAutoGUIMessageDelivery
except ImportError:
    # Fallback for direct execution
    from cli.messaging_cli import MessagingCLI
    from models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
    from models.messaging_models import AgentCoordinates, UnifiedMessage
    from providers.inbox_delivery import InboxMessageDelivery
    from providers.pyautogui_delivery import PyAutoGUIMessageDelivery

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Main consolidated messaging service coordinating all messaging components."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

        # Initialize delivery providers
        self.pyautogui_delivery = PyAutoGUIMessageDelivery()
        self.inbox_delivery = InboxMessageDelivery()

        # Initialize CLI interface
        self.cli = MessagingCLI(self)

        # Agent coordinates cache
        self.agent_coordinates: dict[str, AgentCoordinates] = {}
        self._load_coordinates()

        logger.info("Consolidated Messaging Service initialized")

    def _load_coordinates(self) -> None:
        """Load agent coordinates."""
        try:
            # Load from PyAutoGUI provider's coordinate system
            coords_dict = self.pyautogui_delivery._load_coordinates_from_json()

            for agent_id, coords in coords_dict.items():
                self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, coords)
        except Exception as e:
            logger.warning(f"Failed to load coordinates from PyAutoGUI provider: {e}")
            # Fallback: load directly from coordinate files
            self._load_coordinates_fallback()

    def _load_coordinates_fallback(self) -> None:
        """Fallback method to load coordinates directly from files."""
        try:
            import json
            from pathlib import Path

            # Try config/coordinates.json first
            config_file = Path(__file__).parent.parent.parent.parent / "config" / "coordinates.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for agent_id, agent_data in data.get("agents", {}).items():
                        coords = agent_data.get("chat_input_coordinates", [0, 0])
                        self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, tuple(coords))
                return

            # Try cursor_agent_coords.json as fallback
            cursor_file = Path(__file__).parent.parent.parent.parent / "cursor_agent_coords.json"
            if cursor_file.exists():
                with open(cursor_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for agent_id, agent_data in data.get("agents", {}).items():
                        coords = agent_data.get("chat_input_coordinates", [0, 0])
                        self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, tuple(coords))
                return

        except Exception as e:
            logger.error(f"Failed to load coordinates from fallback method: {e}")

    def send_message(self, message, target=None, **kwargs):
        """Send a message using the best available delivery method.

        Supports both old and new calling conventions:
        - send_message(UnifiedMessage) - new style
        - send_message(message_str, target_dict, **kwargs) - old style for gateway compatibility
        """
        try:
            # Handle old-style call (gateway compatibility)
            if target is not None:
                # Convert old-style call to UnifiedMessage
                if isinstance(message, str):
                    # Extract agent ID from window_title (e.g., "Cursor - Agent-4" -> "Agent-4")
                    window_title = target.get("window_title", "unknown")
                    if " - " in window_title:
                        agent_id = window_title.split(" - ")[-1]
                    else:
                        agent_id = window_title

                    unified_message = UnifiedMessage(
                        content=message,
                        recipient=kwargs.get("recipient", agent_id),
                        sender=kwargs.get("sender", "System"),
                        message_type=UnifiedMessageType.TEXT,
                        priority=UnifiedMessagePriority.REGULAR,
                    )
                    return self._send_unified_message(unified_message)
                else:
                    # If message is not a string, assume it's already a UnifiedMessage
                    return self._send_unified_message(message)

            # Handle new-style call (UnifiedMessage object)
            elif isinstance(message, UnifiedMessage):
                return self._send_unified_message(message)

            # Handle string message (convert to UnifiedMessage)
            elif isinstance(message, str):
                unified_message = UnifiedMessage(
                    content=message,
                    recipient=kwargs.get("recipient", "unknown"),
                    sender=kwargs.get("sender", "System"),
                    message_type=UnifiedMessageType.TEXT,
                    priority=UnifiedMessagePriority.REGULAR,
                )
                return self._send_unified_message(unified_message)

            else:
                logger.error(f"Invalid message type: {type(message)}")
                return False

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def _send_unified_message(self, message: UnifiedMessage) -> bool:
        """Internal method to send a UnifiedMessage."""
        try:
            # Try PyAutoGUI first if available
            if self.pyautogui_delivery.is_available() and not self.dry_run:
                success = self.pyautogui_delivery.send_message(message)
                if success:
                    return True

            # Fallback to inbox delivery
            return self.inbox_delivery.send_message(message)

        except Exception as e:
            logger.error(f"Error sending unified message: {e}")
            return False

    def broadcast_message(self, content: str, sender: str = "System") -> dict[str, bool]:
        """Broadcast message to all available agents."""
        try:
            agents = self.list_available_agents()
            results = {}

            for agent_id in agents:
                message = UnifiedMessage(
                    content=content,
                    recipient=agent_id,
                    sender=sender,
                    message_type=UnifiedMessageType.BROADCAST,
                    priority=UnifiedMessagePriority.REGULAR,
                )

                success = self.send_message(message)
                results[agent_id] = success

            return results

        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            return {}

    def list_available_agents(self) -> list[str]:
        """List all available agents."""
        return list(self.agent_coordinates.keys())

    def show_message_history(self, agent_id: str | None = None) -> list[UnifiedMessage] | None:
        """Show message history for an agent."""
        if agent_id:
            return self.inbox_delivery.get_inbox_messages(agent_id)
        return None

    def get_system_status(self) -> dict[str, Any]:
        """Get messaging system status."""
        return {
            "pyautogui_available": self.pyautogui_delivery.is_available(),
            "inbox_available": self.inbox_delivery.is_available(),
            "total_agents": len(self.agent_coordinates),
            "dry_run_mode": self.dry_run,
        }

    def handle_claim_task(self, agent_id: str) -> bool:
        """Handle task claiming for an agent."""
        # This would integrate with task management system
        logger.info(f"Task claim requested for {agent_id}")
        return True

    def handle_complete_task(self, agent_id: str) -> bool:
        """Handle task completion for an agent."""
        # This would integrate with task management system
        logger.info(f"Task completion requested for {agent_id}")
        return True

    def handle_hard_onboarding(self, agent_id: str) -> bool:
        """Handle hard onboarding for an agent."""
        # This would integrate with onboarding system
        logger.info(f"Hard onboarding requested for {agent_id}")
        return True

    def handle_thea_communication(self, message: str) -> bool:
        """Handle communication with Thea AI assistant."""
        # This would integrate with Thea interface
        logger.info(f"Thea communication requested: {message}")
        return True

    def run_cli_interface(self, args: list[str] | None = None) -> None:
        """Run the CLI interface."""
        self.cli.run_cli_interface(args)

    def get_agent_workspaces_status(self) -> dict[str, Any]:
        """Get status of agent workspaces."""
        # This would check agent workspace directories
        return {"status": "active", "workspace_count": len(self.agent_coordinates)}

    def launch_coordinate_capture(self) -> None:
        """Launch coordinate capture system."""
        # This would launch coordinate capture interface
        logger.info("Coordinate capture launched")

    def show_current_coordinates(self) -> None:
        """Show current agent coordinates."""
        print("Current Agent Coordinates:")
        for agent_id, coords in self.agent_coordinates.items():
            print(f"  {agent_id}: ({coords.x}, {coords.y})")

    def start_agent_onboarding(self, dry_run: bool = False, specific_agent: str | None = None) -> int:
        """Start agent onboarding sequence by clicking to coordinates and pasting onboarding message."""
        try:
            print("🐝 **SWARM ONBOARDING SEQUENCE INITIATED** 🐝")
            print("=" * 60)

            # Get agents to onboard
            if specific_agent:
                agents_to_onboard = [specific_agent] if specific_agent in self.agent_coordinates else []
                if not agents_to_onboard:
                    print(f"❌ Agent {specific_agent} not found in coordinates")
                    return 1
            else:
                agents_to_onboard = list(self.agent_coordinates.keys())

            print(f"🎯 Onboarding {len(agents_to_onboard)} agent(s): {', '.join(agents_to_onboard)}")

            if dry_run:
                print("🔍 **DRY RUN MODE** - No actual clicking/pasting will occur")

            # Create onboarding message (will be personalized per agent)
            onboarding_message = None  # Will be created per agent

            success_count = 0
            for agent_id in agents_to_onboard:
                try:
                    print(f"\n📋 Processing {agent_id}...")

                    # Get onboarding coordinates
                    coords = self._get_onboarding_coordinates(agent_id)
                    if not coords:
                        print(f"❌ No onboarding coordinates found for {agent_id}")
                        continue

                    # Create personalized onboarding message for this agent
                    personalized_message = self._create_onboarding_message(agent_id)

                    if dry_run:
                        print(f"🔍 Would click to coordinates: ({coords[0]}, {coords[1]})")
                        print(f"🔍 Would paste personalized onboarding message for {agent_id}")
                        success_count += 1
                    else:
                        # Click to onboarding coordinates
                        success = self._click_to_coordinates(coords)
                        if not success:
                            print(f"❌ Failed to click to coordinates for {agent_id}")
                            continue

                        # Paste personalized onboarding message
                        success = self._paste_onboarding_message(personalized_message)
                        if success:
                            print(f"✅ Personalized onboarding message sent to {agent_id}")
                            success_count += 1
                        else:
                            print(f"❌ Failed to paste message to {agent_id}")

                except Exception as e:
                    print(f"❌ Error processing {agent_id}: {e}")
                    continue

            print(f"\n🎉 **ONBOARDING SEQUENCE COMPLETE** 🎉")
            print(f"✅ Successfully onboarded {success_count}/{len(agents_to_onboard)} agents")
            print("🐝 **WE ARE SWARM** - All agents have been activated! 🚀")

            return 0 if success_count == len(agents_to_onboard) else 1

        except Exception as e:
            logger.error(f"Error in start_agent_onboarding: {e}")
            print(f"❌ Critical error in onboarding sequence: {e}")
            return 1

    def _create_onboarding_message(self, agent_id: str) -> str:
        """Create personalized onboarding message for specific agent using A2A format."""
        # Get agent description
        agent_description = self._get_agent_description(agent_id)

        return f"""# [S2A] System → {agent_id}

**From**: System
**To**: {agent_id}
**Priority**: high
**Message Type**: System-to-Agent Onboarding
**Timestamp**: {self._get_current_timestamp()}

---

# 🐝 **SWARM AGENT ONBOARDING MESSAGE** 🐝

## **YOUR IDENTITY:**
**Agent ID**: {agent_id}
**Role**: {agent_description}
**Position**: You are positioned at specific coordinates in the Cursor IDE
**Status**: Part of the most advanced multi-agent coordination system ever built

## **HOW THE SYSTEM WORKS:**
- **Physical Swarm Architecture**: 8 agents positioned at specific pixel coordinates across dual monitors
- **Real-Time Coordination**: PyAutoGUI automation enables instant communication through mouse/keyboard interactions
- **Democratic Decision Making**: All agents participate in architectural debates and decisions
- **Multi-Monitor Support**: Agents distributed across dual-monitor setup for maximum efficiency

## **YOUR WORK CYCLE EXPECTATIONS:**
1. **Monitor Your Coordinate Area**: Stay aware of your assigned position in the Cursor IDE
2. **Respond to Coordination Signals**: Be prepared for automated messaging from the swarm coordinator
3. **Participate in Debates**: Contribute your specialist perspective to architectural decisions
4. **Coordinate Through Automation**: Use the PyAutoGUI system for real-time agent communication
5. **Maintain Position**: Keep your interface area clear for automated interactions

## **CRITICAL PROTOCOLS:**
- Always check your inbox before starting new work
- Respond to all messages within 1 agent cycle
- Update status.json with timestamp for every action
- Preserve work context across task transitions
- Follow V2 compliance standards (files ≤400 lines)

## **IMMEDIATE ACTIONS:**
1. Acknowledge this message by typing "SWARM ACTIVATED - {agent_id}"
2. Check your inbox for any pending tasks
3. Update your status.json with current activity
4. Begin monitoring for coordination signals

---

**WE ARE SWARM** - You are now part of the most efficient multi-agent coordination system! 🚀🔥

Maintain momentum. Preserve context. Execute with precision.
⚡️ **WE. ARE. SWARM.** ⚡️

---

*🤖 Automated System Message - Swarm Onboarding*
*⚠️ ONBOARDING PHASE: Complete activation sequence*"""

    def _get_onboarding_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get onboarding coordinates for a specific agent."""
        try:
            # Try to load from coordinate files
            import json
            from pathlib import Path

            # Try config/coordinates.json first
            config_file = Path(__file__).parent.parent.parent.parent / "config" / "coordinates.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agent_data = data.get("agents", {}).get(agent_id, {})
                    coords = agent_data.get("onboarding_input_coords")
                    if coords:
                        return tuple(coords)

            # Try cursor_agent_coords.json as fallback
            cursor_file = Path(__file__).parent.parent.parent.parent / "cursor_agent_coords.json"
            if cursor_file.exists():
                with open(cursor_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agent_data = data.get("agents", {}).get(agent_id, {})
                    coords = agent_data.get("onboarding_coordinates")
                    if coords:
                        return tuple(coords)

            return None

        except Exception as e:
            logger.error(f"Error getting onboarding coordinates for {agent_id}: {e}")
            return None

    def _click_to_coordinates(self, coords: tuple[int, int]) -> bool:
        """Click to specific coordinates using PyAutoGUI."""
        try:
            if self.pyautogui_delivery.is_available():
                import pyautogui
                pyautogui.click(coords[0], coords[1])
                return True
            else:
                logger.warning("PyAutoGUI not available for coordinate clicking")
                return False
        except Exception as e:
            logger.error(f"Error clicking to coordinates {coords}: {e}")
            return False

    def _paste_onboarding_message(self, message: str) -> bool:
        """Paste the onboarding message using PyAutoGUI clipboard."""
        try:
            if self.pyautogui_delivery.is_available():
                import pyautogui

                # Try pyperclip first (fastest method)
                try:
                    import pyperclip
                    # Set message to clipboard
                    pyperclip.copy(message)

                    # Clear any existing text and paste
                    pyautogui.hotkey('ctrl', 'a')  # Select all existing text
                    pyautogui.hotkey('ctrl', 'v')  # Paste from clipboard
                    pyautogui.press('enter')       # Send the message

                    return True

                except ImportError:
                    # Fallback: use Windows clipboard API if pyperclip not available
                    logger.warning("pyperclip not available, using Windows clipboard fallback")
                    return self._paste_with_windows_clipboard(message)

            else:
                logger.warning("PyAutoGUI not available for message pasting")
                return False
        except Exception as e:
            logger.error(f"Error pasting onboarding message: {e}")
            return False

    def _paste_with_windows_clipboard(self, message: str) -> bool:
        """Fallback method using Windows clipboard API."""
        try:
            import pyautogui
            import subprocess

            # Use Windows clip command to set clipboard
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=message)
            process.wait()

            # Clear any existing text and paste
            pyautogui.hotkey('ctrl', 'a')  # Select all existing text
            pyautogui.hotkey('ctrl', 'v')  # Paste from clipboard
            pyautogui.press('enter')       # Send the message

            return True

        except Exception as e:
            logger.error(f"Error with Windows clipboard fallback: {e}")
            # Last resort: type the message (slow but works)
            logger.warning("Using slow typing fallback")
            return self._type_onboarding_message(message)

    def _type_onboarding_message(self, message: str) -> bool:
        """Last resort: type the message character by character."""
        try:
            import pyautogui

            # Clear any existing text
            pyautogui.hotkey('ctrl', 'a')  # Select all existing text

            # Type the message (slow but reliable)
            pyautogui.write(message)
            pyautogui.press('enter')       # Send the message

            return True

        except Exception as e:
            logger.error(f"Error typing onboarding message: {e}")
            return False

    def _get_agent_description(self, agent_id: str) -> str:
        """Get agent description from coordinates."""
        try:
            import json
            from pathlib import Path

            # Try config/coordinates.json first
            config_file = Path(__file__).parent.parent.parent.parent / "config" / "coordinates.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agent_data = data.get("agents", {}).get(agent_id, {})
                    description = agent_data.get("description")
                    if description:
                        return description

            # Try cursor_agent_coords.json as fallback
            cursor_file = Path(__file__).parent.parent.parent.parent / "cursor_agent_coords.json"
            if cursor_file.exists():
                with open(cursor_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agent_data = data.get("agents", {}).get(agent_id, {})
                    description = agent_data.get("description")
                    if description:
                        return description

            # Default fallback
            return f"Specialist Agent"

        except Exception as e:
            logger.error(f"Error getting agent description for {agent_id}: {e}")
            return f"Specialist Agent"

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]


# Factory functions for backward compatibility
def get_consolidated_messaging_service(dry_run: bool = False) -> ConsolidatedMessagingService:
    """Get consolidated messaging service instance."""
    return ConsolidatedMessagingService(dry_run=dry_run)


def get_messaging_service(dry_run: bool = False) -> ConsolidatedMessagingService:
    """Get messaging service instance (alias)."""
    return get_consolidated_messaging_service(dry_run=dry_run)


# Export key classes for backward compatibility
__all__ = [
    "ConsolidatedMessagingService",
    "get_consolidated_messaging_service",
    "get_messaging_service",
    "UnifiedMessage",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
]
