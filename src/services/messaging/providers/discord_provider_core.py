#!/usr/bin/env python3
"""
Discord Provider Core - Core Logic Module
=========================================

Core logic for Discord messaging provider integration.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: discord_provider.py (432 lines) - Core module
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

import discord
from discord.ext import commands

try:
    from ..core.messaging_service import MessagingService
except ImportError:
    from src.services.messaging.core.messaging_service import MessagingService

logger = logging.getLogger(__name__)


class DiscordMessagingProvider:
    """Discord provider for the messaging system."""

    def __init__(self, bot: commands.Bot):
        """Initialize Discord messaging provider."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.DiscordMessagingProvider")
        self.messaging_service = MessagingService("config/coordinates.json")
        self.agent_channels: Dict[str, discord.TextChannel] = {}

    async def manage_messaging(self, action: str, **kwargs) -> Any:
        """Consolidated messaging operations"""
        if action == "send_to_agent":
            return await self._send_message_to_agent(
                kwargs["agent_id"], kwargs["message"], kwargs.get("from_agent")
            )
        elif action == "send_broadcast":
            return await self._send_broadcast_message(
                kwargs["message"], kwargs.get("from_agent"), kwargs.get("exclude_agents", [])
            )
        elif action == "send_to_channel":
            return await self._send_message_to_channel(
                kwargs["channel_id"], kwargs["message"], kwargs.get("from_agent")
            )
        elif action == "get_agent_channel":
            return self.agent_channels.get(kwargs["agent_id"])
        elif action == "register_channel":
            self.agent_channels[kwargs["agent_id"]] = kwargs["channel"]
            return True
        return None

    async def _send_message_to_agent(self, agent_id: str, message: str, from_agent: str = None) -> bool:
        """Send message to specific agent via Discord."""
        try:
            if from_agent is None:
                try:
                    from ..agent_context import get_current_agent
                    from_agent = get_current_agent()
                except ImportError:
                    from_agent = "system"

            channel = self.agent_channels.get(agent_id)
            if not channel:
                self.logger.warning(f"No Discord channel registered for agent {agent_id}")
                return False

            # Create formatted message
            formatted_message = self._format_agent_message(message, from_agent, agent_id)
            
            # Send via Discord
            await channel.send(formatted_message)
            
            # Log to messaging service
            self.messaging_service.log_message(from_agent, agent_id, message, "discord")
            
            self.logger.info(f"Message sent to agent {agent_id} via Discord")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send message to agent {agent_id}: {e}")
            return False

    async def _send_broadcast_message(self, message: str, from_agent: str = None, exclude_agents: list = None) -> int:
        """Send broadcast message to all registered agents."""
        try:
            if from_agent is None:
                try:
                    from ..agent_context import get_current_agent
                    from_agent = get_current_agent()
                except ImportError:
                    from_agent = "system"

            exclude_agents = exclude_agents or []
            sent_count = 0

            for agent_id, channel in self.agent_channels.items():
                if agent_id not in exclude_agents:
                    try:
                        formatted_message = self._format_broadcast_message(message, from_agent)
                        await channel.send(formatted_message)
                        self.messaging_service.log_message(from_agent, agent_id, message, "discord")
                        sent_count += 1
                    except Exception as e:
                        self.logger.error(f"Failed to send broadcast to agent {agent_id}: {e}")

            self.logger.info(f"Broadcast message sent to {sent_count} agents")
            return sent_count

        except Exception as e:
            self.logger.error(f"Failed to send broadcast message: {e}")
            return 0

    async def _send_message_to_channel(self, channel_id: int, message: str, from_agent: str = None) -> bool:
        """Send message to specific Discord channel."""
        try:
            if from_agent is None:
                try:
                    from ..agent_context import get_current_agent
                    from_agent = get_current_agent()
                except ImportError:
                    from_agent = "system"

            channel = self.bot.get_channel(channel_id)
            if not channel:
                self.logger.error(f"Discord channel {channel_id} not found")
                return False

            formatted_message = self._format_channel_message(message, from_agent)
            await channel.send(formatted_message)
            
            self.logger.info(f"Message sent to channel {channel_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send message to channel {channel_id}: {e}")
            return False

    def _format_agent_message(self, message: str, from_agent: str, to_agent: str) -> str:
        """Format message for agent-to-agent communication."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"**[{timestamp}] {from_agent} → {to_agent}**\n{message}"

    def _format_broadcast_message(self, message: str, from_agent: str) -> str:
        """Format message for broadcast communication."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"**[{timestamp}] BROADCAST from {from_agent}**\n{message}"

    def _format_channel_message(self, message: str, from_agent: str) -> str:
        """Format message for channel communication."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"**[{timestamp}] {from_agent}**\n{message}"

    def get_provider_status(self) -> Dict[str, Any]:
        """Get Discord provider status."""
        return {
            "provider_type": "discord",
            "bot_connected": self.bot.is_ready(),
            "registered_agents": len(self.agent_channels),
            "agent_channels": list(self.agent_channels.keys()),
            "messaging_service_connected": self.messaging_service is not None,
        }
