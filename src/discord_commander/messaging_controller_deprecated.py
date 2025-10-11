#!/usr/bin/env python3
"""
Discord Messaging Controller
============================

Discord messaging controller that bridges Discord interactions with the swarm messaging system.
Provides easy-to-use Discord views for agent communication.

Features:
- Discord views for intuitive agent interaction
- Bridge between Discord commands and messaging system
- Real-time agent status and communication
- Swarm coordination through Discord interface

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
from datetime import datetime
from typing import Any

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from src.services.messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class AgentMessagingView(discord.ui.View):
    """Discord view for easy agent messaging."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=300)  # 5 minute timeout
        self.messaging_service = messaging_service
        self.agents = self._load_agent_list()

        # Create agent selection dropdown
        self.agent_select = discord.ui.Select(
            placeholder="Select an agent to message...", options=self._create_agent_options()
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

        # Create message input
        self.message_input = discord.ui.TextInput(
            label="Message",
            placeholder="Type your message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000,
        )

    def _load_agent_list(self) -> list[dict[str, Any]]:
        """Load list of available agents."""
        try:
            # Get agent data from messaging service
            if hasattr(self.messaging_service, "agent_data"):
                agents = []
                for agent_id, agent_info in self.messaging_service.agent_data.items():
                    agents.append(
                        {
                            "id": agent_id,
                            "name": agent_info.get("name", agent_id),
                            "status": agent_info.get("active", False),
                            "coordinates": agent_info.get("coordinates", (0, 0)),
                        }
                    )
                return agents
        except Exception as e:
            logger.error(f"Error loading agent list: {e}")
        return []

    def _create_agent_options(self) -> list[discord.SelectOption]:
        """Create Discord select options for agents."""
        options = []
        for agent in self.agents:
            status_emoji = "🟢" if agent["status"] else "🔴"
            label = f"{status_emoji} {agent['name']}"
            options.append(
                discord.SelectOption(
                    label=label, value=agent["id"], description=f"Agent {agent['id']}"
                )
            )
        return options

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        selected_agent = interaction.data["values"][0]

        # Create modal for message input
        modal = MessageModal(selected_agent, self.messaging_service)
        await interaction.response.send_modal(modal)


class MessageModal(discord.ui.Modal):
    """Modal for message input."""

    def __init__(self, agent_id: str, messaging_service: ConsolidatedMessagingService):
        super().__init__(title=f"Message Agent {agent_id}")
        self.agent_id = agent_id
        self.messaging_service = messaging_service

        self.message_input = discord.ui.TextInput(
            label="Message",
            placeholder="Type your message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000,
        )
        self.add_item(self.message_input)

        self.priority_select = discord.ui.TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, CRITICAL",
            default="NORMAL",
            required=False,
            max_length=20,
        )
        self.add_item(self.priority_select)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle message submission."""
        message = self.message_input.value
        priority = self.priority_select.value or "NORMAL"

        try:
            # Send message through messaging service
            success = self.messaging_service.send_message(
                agent_id=self.agent_id,
                message=message,
                from_agent="Discord-User",
                priority=priority,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Message sent to **{self.agent_id}**",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)
                embed.add_field(name="From", value="Discord User", inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="❌ Message Failed",
                    description=f"Failed to send message to **{self.agent_id}**",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error sending message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class SwarmStatusView(discord.ui.View):
    """Discord view for swarm status monitoring."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=300)
        self.messaging_service = messaging_service

        # Refresh button
        self.refresh_button = discord.ui.Button(
            label="🔄 Refresh Status", style=discord.ButtonStyle.primary
        )
        self.refresh_button.callback = self.refresh_status
        self.add_item(self.refresh_button)

        # Broadcast message button
        self.broadcast_button = discord.ui.Button(
            label="📢 Broadcast Message", style=discord.ButtonStyle.secondary
        )
        self.broadcast_button.callback = self.broadcast_message
        self.add_item(self.broadcast_button)

    async def refresh_status(self, interaction: discord.Interaction):
        """Refresh swarm status."""
        try:
            embed = await self._create_status_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            logger.error(f"Error refreshing status: {e}")
            await interaction.response.send_message("Error refreshing status", ephemeral=True)

    async def broadcast_message(self, interaction: discord.Interaction):
        """Broadcast message to all agents."""
        modal = BroadcastModal(self.messaging_service)
        await interaction.response.send_modal(modal)

    async def _create_status_embed(self) -> discord.Embed:
        """Create status embed."""
        embed = discord.Embed(
            title="🤖 Swarm Status",
            description="Current status of all agents",
            color=discord.Color.blue(),
            timestamp=datetime.now(),
        )

        try:
            if hasattr(self.messaging_service, "agent_data"):
                active_count = 0
                total_count = len(self.messaging_service.agent_data)

                for agent_id, agent_info in self.messaging_service.agent_data.items():
                    if agent_info.get("active", False):
                        active_count += 1
                        embed.add_field(
                            name=f"🟢 {agent_id}",
                            value=f"Status: Active\nCoordinates: {agent_info.get('coordinates', 'Unknown')}",
                            inline=True,
                        )
                    else:
                        embed.add_field(
                            name=f"🔴 {agent_id}", value="Status: Inactive", inline=True
                        )

                embed.add_field(
                    name="Summary", value=f"Active: {active_count}/{total_count}", inline=False
                )
        except Exception as e:
            embed.add_field(
                name="Error", value=f"Failed to load agent data: {str(e)}", inline=False
            )

        return embed


class BroadcastModal(discord.ui.Modal):
    """Modal for broadcast messages."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="Broadcast Message to All Agents")
        self.messaging_service = messaging_service

        self.message_input = discord.ui.TextInput(
            label="Broadcast Message",
            placeholder="Type your broadcast message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000,
        )
        self.add_item(self.message_input)

        self.priority_select = discord.ui.TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, CRITICAL",
            default="NORMAL",
            required=False,
            max_length=20,
        )
        self.add_item(self.priority_select)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle broadcast submission."""
        message = self.message_input.value
        priority = self.priority_select.value or "NORMAL"

        try:
            success = self.messaging_service.broadcast_message(
                message=message, from_agent="Discord-User", priority=priority
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Message broadcasted to all agents",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="❌ Broadcast Failed",
                    description="Failed to broadcast message",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error broadcasting message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class DiscordMessagingController:
    """Main Discord messaging controller."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        """Initialize the Discord messaging controller."""
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(__name__)

    def create_agent_messaging_view(self) -> AgentMessagingView:
        """Create agent messaging view."""
        return AgentMessagingView(self.messaging_service)

    def create_swarm_status_view(self) -> SwarmStatusView:
        """Create swarm status view."""
        return SwarmStatusView(self.messaging_service)

    async def send_agent_message(
        self, agent_id: str, message: str, priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent."""
        try:
            return self.messaging_service.send_message(
                agent_id=agent_id,
                message=message,
                from_agent="Discord-Controller",
                priority=priority,
            )
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    async def broadcast_to_swarm(self, message: str, priority: str = "NORMAL") -> bool:
        """Broadcast message to all agents."""
        try:
            return self.messaging_service.broadcast_message(
                message=message, from_agent="Discord-Controller", priority=priority
            )
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")
            return False

    def get_agent_status(self) -> dict[str, Any]:
        """Get current agent status."""
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
