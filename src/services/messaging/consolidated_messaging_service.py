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
from typing import Any, Dict, List, Optional

try:
    from .cli.messaging_cli import MessagingCLI
    from .interfaces.messaging_interfaces import MessageHistoryProvider
    from .models.messaging_models import AgentCoordinates, UnifiedMessage
    from .models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
    from .providers.inbox_delivery import InboxMessageDelivery
    from .providers.pyautogui_delivery import PyAutoGUIMessageDelivery
except ImportError:
    # Fallback for direct execution
    from cli.messaging_cli import MessagingCLI
    from interfaces.messaging_interfaces import MessageHistoryProvider
    from models.messaging_models import AgentCoordinates, UnifiedMessage
    from models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
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
        self.agent_coordinates: Dict[str, AgentCoordinates] = {}
        self._load_coordinates()

        logger.info("Consolidated Messaging Service initialized")

    def _load_coordinates(self) -> None:
        """Load agent coordinates."""
        # Load from PyAutoGUI provider's coordinate system
        coords_dict = self.pyautogui_delivery._load_coordinates_from_json()

        for agent_id, coords in coords_dict.items():
            self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, coords)

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
                    window_title = target.get('window_title', 'unknown')
                    if ' - ' in window_title:
                        agent_id = window_title.split(' - ')[-1]
                    else:
                        agent_id = window_title
                    
                    unified_message = UnifiedMessage(
                        content=message,
                        recipient=kwargs.get('recipient', agent_id),
                        sender=kwargs.get('sender', 'System'),
                        message_type=UnifiedMessageType.TEXT,
                        priority=UnifiedMessagePriority.REGULAR
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
                    recipient=kwargs.get('recipient', 'unknown'),
                    sender=kwargs.get('sender', 'System'),
                    message_type=UnifiedMessageType.TEXT,
                    priority=UnifiedMessagePriority.REGULAR
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
                    priority=UnifiedMessagePriority.REGULAR
                )

                success = self.send_message(message)
                results[agent_id] = success

            return results

        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            return {}

    def list_available_agents(self) -> List[str]:
        """List all available agents."""
        return list(self.agent_coordinates.keys())

    def show_message_history(self, agent_id: str | None = None) -> List[UnifiedMessage] | None:
        """Show message history for an agent."""
        if agent_id:
            return self.inbox_delivery.get_inbox_messages(agent_id)
        return None

    def get_system_status(self) -> Dict[str, Any]:
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

    def run_cli_interface(self, args: List[str] | None = None) -> None:
        """Run the CLI interface."""
        self.cli.run_cli_interface(args)

    def get_agent_workspaces_status(self) -> Dict[str, Any]:
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
