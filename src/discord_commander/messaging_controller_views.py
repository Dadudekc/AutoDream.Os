"""
Discord Messaging Controller Views
===================================

Discord UI views for agent messaging and swarm status.
Extracted from messaging_controller.py for preventive optimization.

Features:
- Agent selection and messaging view
- Swarm status monitoring view
- Interactive buttons and dropdowns

Author: Agent-7 (original), Agent-1 (preventive refactor)
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

# Discord imports with error handling
try:
    import discord

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class AgentMessagingView(discord.ui.View):
    """Discord view for easy agent messaging."""

    def __init__(self, messaging_service):
        super().__init__(timeout=300)  # 5 minute timeout
        self.messaging_service = messaging_service
        self.agents = self._load_agent_list()

        # Create agent selection dropdown
        self.agent_select = discord.ui.Select(
            placeholder="Select an agent to message...", options=self._create_agent_options()
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

    def _load_agent_list(self) -> list[dict[str, Any]]:
        """Load list of available agents."""
        try:
            # First try to get agent data from messaging service
            if hasattr(self.messaging_service, "agent_data") and self.messaging_service.agent_data:
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
                if agents:  # Only return if we got agents
                    return agents

            # Fallback: Use StatusReader to get agents from status.json files
            from .status_reader import StatusReader

            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()

            agents = []
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})
                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": "ACTIVE" in str(status_data.get("status", "")).upper(),
                        "coordinates": status_data.get("coordinate_position", f"({i}, {i})"),
                    }
                )

            return agents

        except Exception as e:
            logger.error(f"Error loading agent list: {e}")
            # Emergency fallback: Return static list
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}", "status": True, "coordinates": (i, i)}
                for i in range(1, 9)
            ]

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
        # Import here to avoid circular dependency
        from .messaging_controller_modals import MessageModal

        selected_agent = interaction.data["values"][0]
        modal = MessageModal(selected_agent, self.messaging_service)
        await interaction.response.send_modal(modal)


class SwarmStatusView(discord.ui.View):
    """Discord view for swarm status monitoring."""

    def __init__(self, messaging_service):
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
        # Import here to avoid circular dependency
        from .messaging_controller_modals import BroadcastModal

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
