#!/usr/bin/env python3
"""
Discord GUI Controller - Facade Pattern
========================================

Lightweight facade for Discord GUI components.
Consolidates Discord GUI functionality into a clean, simple interface.

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor (Facade Pattern)
Original: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import logging
from typing import Any

from src.services.messaging_service import ConsolidatedMessagingService

from .discord_gui_modals import AgentMessageModal, BroadcastMessageModal
from .discord_gui_views import AgentMessagingGUIView, SwarmStatusGUIView

logger = logging.getLogger(__name__)


class DiscordGUIController:
    """
    Unified Discord GUI Controller for Agent Messaging System (Facade Pattern).

    Provides complete Discord-based access to:
    - Agent-to-agent messaging
    - Swarm status monitoring
    - Broadcast communications
    - Interactive GUI (views, modals, buttons)

    This is a lightweight facade that delegates to specialized components:
    - discord_gui_views.py: UI views (AgentMessagingGUIView, SwarmStatusGUIView)
    - discord_gui_modals.py: UI modals (AgentMessageModal, BroadcastMessageModal)
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        """Initialize Discord GUI controller."""
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(__name__)

    def create_main_gui(self) -> AgentMessagingGUIView:
        """Create main messaging GUI view."""
        return AgentMessagingGUIView(self.messaging_service)

    def create_status_gui(self) -> SwarmStatusGUIView:
        """Create status monitoring GUI view."""
        return SwarmStatusGUIView(self.messaging_service)

    def create_agent_message_modal(self, agent_id: str) -> AgentMessageModal:
        """Create modal for messaging specific agent."""
        return AgentMessageModal(agent_id, self.messaging_service)

    def create_broadcast_modal(self) -> BroadcastMessageModal:
        """Create modal for broadcasting to all agents."""
        return BroadcastMessageModal(self.messaging_service)

    async def send_message(self, agent_id: str, message: str, priority: str = "regular") -> bool:
        """Send message to specific agent."""
        try:
            result = self.messaging_service.send_message(
                agent=agent_id, message=message, priority=priority, use_pyautogui=True
            )
            return result.get("success", False)
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    async def broadcast_message(self, message: str, priority: str = "regular") -> bool:
        """Broadcast message to all agents."""
        try:
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0

            for agent in agents:
                result = self.messaging_service.send_message(
                    agent=agent, message=message, priority=priority, use_pyautogui=True
                )
                if result.get("success"):
                    success_count += 1

            return success_count == len(agents)
        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            return False

    def get_agent_status(self) -> dict[str, Any]:
        """Get current swarm status."""
        from .status_reader import StatusReader

        try:
            status_reader = StatusReader()
            agents_status = {}

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = status_reader.get_agent_status(agent_id)
                if status:
                    agents_status[agent_id] = status

            return agents_status
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {}


__all__ = [
    "DiscordGUIController",
    "AgentMessagingGUIView",
    "SwarmStatusGUIView",
    "AgentMessageModal",
    "BroadcastMessageModal",
]
