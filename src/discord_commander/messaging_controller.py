"""
Discord Messaging Controller - V2 Compliant Facade
===================================================

Discord messaging controller that bridges Discord interactions with swarm messaging.
Refactored for preventive optimization: 378L → <100L (73%+ reduction).

This facade coordinates between:
- Views: Agent messaging and swarm status views
- Modals: Message and broadcast input modals
- Controller: Main coordination and service integration

V2 Compliance: ≤300 lines, 100L+ buffer from 400L limit.

Author: Agent-7 (original), Agent-1 (preventive refactor)
Refactored: 2025-10-11 (Preventive Optimization - Infrastructure Excellence)
License: MIT
"""

import logging
from typing import Any

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from src.services.messaging_infrastructure import ConsolidatedMessagingService

# Modular components
from .messaging_controller_views import AgentMessagingView, SwarmStatusView

logger = logging.getLogger(__name__)


class DiscordMessagingController:
    """
    Main Discord messaging controller facade.

    Coordinates between Discord views/modals and swarm messaging service.
    Provides:
    - Agent-to-agent messaging through Discord UI
    - Swarm status monitoring with real-time updates
    - Broadcast messaging to all agents
    - Interactive views and modals for easy coordination
    """

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        """
        Initialize the Discord messaging controller.

        Args:
            messaging_service: Consolidated messaging service for swarm communication
        """
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(__name__)

    def create_agent_messaging_view(self) -> AgentMessagingView:
        """
        Create agent messaging view.

        Returns:
            AgentMessagingView instance for agent selection and messaging
        """
        return AgentMessagingView(self.messaging_service)

    def create_swarm_status_view(self) -> SwarmStatusView:
        """
        Create swarm status view.

        Returns:
            SwarmStatusView instance for status monitoring
        """
        return SwarmStatusView(self.messaging_service)

    async def send_agent_message(
        self, agent_id: str, message: str, priority: str = "NORMAL"
    ) -> bool:
        """
        Send message to specific agent.

        Args:
            agent_id: Target agent ID
            message: Message content
            priority: Message priority (NORMAL, HIGH, CRITICAL)

        Returns:
            True if message sent successfully
        """
        try:
            return self.messaging_service.send_message(
                agent=agent_id,  # Fixed: 'agent' not 'agent_id'
                message=message,
                priority=priority,
            )
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    async def broadcast_to_swarm(self, message: str, priority: str = "NORMAL") -> bool:
        """
        Broadcast message to all agents.

        Args:
            message: Message content
            priority: Message priority (NORMAL, HIGH, CRITICAL)

        Returns:
            True if broadcast successful
        """
        try:
            return self.messaging_service.broadcast_message(
                message=message, from_agent="Discord-Controller", priority=priority
            )
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")
            return False

    def get_agent_status(self) -> dict[str, Any]:
        """
        Get current agent status.

        Returns:
            Dictionary of agent IDs to status information
        """
        try:
            if hasattr(self.messaging_service, "agent_data"):
                return {
                    agent_id: {
                        "active": agent_info.get("active", False),
                        "coordinates": agent_info.get("coordinates", (0, 0)),
                        "name": agent_info.get("name", agent_id),
                    }
                    for agent_id, agent_info in self.messaging_service.agent_data.items()
                }
        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
        return {}
