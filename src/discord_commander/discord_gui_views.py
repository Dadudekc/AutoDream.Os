#!/usr/bin/env python3
"""
Discord GUI Views - Agent Messaging Views
==========================================

Discord UI Views for agent messaging system.

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Agent-3 (Infrastructure & DevOps)
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
    discord = None

from src.services.messaging_service import ConsolidatedMessagingService

from .status_reader import StatusReader

logger = logging.getLogger(__name__)


class AgentMessagingGUIView(discord.ui.View):
    """Complete agent messaging GUI with all controls."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=600)  # 10 minute timeout
        self.messaging_service = messaging_service
        self.agents = self._load_agents()

        # Agent selection dropdown
        self.agent_select = discord.ui.Select(
            placeholder="🎯 Select agent to message...",
            options=self._create_agent_options(),
            custom_id="agent_select",
        )
        self.agent_select.callback = self.on_agent_select
        self.add_item(self.agent_select)

        # Quick action buttons
        self.broadcast_btn = discord.ui.Button(
            label="📢 Broadcast to All",
            style=discord.ButtonStyle.primary,
            custom_id="broadcast_btn",
        )
        self.broadcast_btn.callback = self.on_broadcast
        self.add_item(self.broadcast_btn)

        self.status_btn = discord.ui.Button(
            label="📊 Swarm Status", style=discord.ButtonStyle.secondary, custom_id="status_btn"
        )
        self.status_btn.callback = self.on_status
        self.add_item(self.status_btn)

        self.refresh_btn = discord.ui.Button(
            label="🔄 Refresh", style=discord.ButtonStyle.secondary, custom_id="refresh_btn"
        )
        self.refresh_btn.callback = self.on_refresh
        self.add_item(self.refresh_btn)

    def _load_agents(self) -> list[dict]:
        """Load agent information from status.json."""
        try:
            status_reader = StatusReader()
            all_statuses = status_reader.read_all_statuses()
            agents = []

            # Always include all 8 agents (even if status not available)
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_data = all_statuses.get(agent_id, {})

                agents.append(
                    {
                        "id": agent_id,
                        "name": status_data.get("agent_name", f"Agent-{i}"),
                        "status": status_data.get("status", "unknown"),
                        "points": self._extract_points(status_data.get("points_earned", 0)),
                    }
                )

            return agents
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            # Fallback: return static agent list
            return [
                {"id": f"Agent-{i}", "name": f"Agent-{i}", "status": "unknown", "points": 0}
                for i in range(1, 9)
            ]

    def _create_agent_options(self) -> list[discord.SelectOption]:
        """Create dropdown options for agents."""
        options = []
        for agent in self.agents:
            emoji = self._get_status_emoji(agent.get("status", "unknown"))
            options.append(
                discord.SelectOption(
                    label=agent["id"],
                    description=f"{agent.get('name', 'Unknown')} - {agent.get('points', 0)} pts",
                    emoji=emoji,
                    value=agent["id"],
                )
            )
        return options

    async def on_agent_select(self, interaction: discord.Interaction):
        """Handle agent selection."""
        from .discord_gui_modals import AgentMessageModal

        agent_id = self.agent_select.values[0]
        modal = AgentMessageModal(agent_id, self.messaging_service)
        await interaction.response.send_modal(modal)

    async def on_broadcast(self, interaction: discord.Interaction):
        """Handle broadcast button."""
        from .discord_gui_modals import BroadcastMessageModal

        modal = BroadcastMessageModal(self.messaging_service)
        await interaction.response.send_modal(modal)

    async def on_status(self, interaction: discord.Interaction):
        """Handle status button."""
        status_view = SwarmStatusGUIView(self.messaging_service)

        embed = discord.Embed(
            title="🐝 Swarm Status",
            description="Current agent status across the swarm",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )

        for agent in self.agents:
            emoji = self._get_status_emoji(agent.get("status", "unknown"))
            embed.add_field(
                name=f"{emoji} {agent['id']}",
                value=f"{agent.get('name', 'Unknown')}\n{agent.get('points', 0)} points",
                inline=True,
            )

        await interaction.response.send_message(embed=embed, view=status_view, ephemeral=True)

    async def on_refresh(self, interaction: discord.Interaction):
        """Handle refresh button."""
        self.agents = self._load_agents()
        self.agent_select.options = self._create_agent_options()

        await interaction.response.send_message("✅ Agent list refreshed!", ephemeral=True)

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for agent status."""
        status_emojis = {
            "active": "🟢",
            "idle": "🟡",
            "busy": "🔴",
            "offline": "⚫",
            "unknown": "❓",
        }
        return status_emojis.get(status.lower(), "❓")

    def _extract_points(self, points_value: Any) -> int:
        """Extract points from various formats."""
        if isinstance(points_value, int):
            return points_value
        if isinstance(points_value, str):
            return int(points_value.replace(",", "").replace("pts", "").strip())
        if isinstance(points_value, dict):
            return points_value.get("total", 0)
        return 0


class SwarmStatusGUIView(discord.ui.View):
    """Status monitoring view."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(timeout=300)
        self.messaging_service = messaging_service

        # Refresh button
        refresh_btn = discord.ui.Button(
            label="🔄 Refresh Status", style=discord.ButtonStyle.primary
        )
        refresh_btn.callback = self.on_refresh
        self.add_item(refresh_btn)

    async def on_refresh(self, interaction: discord.Interaction):
        """Refresh status display."""
        try:
            status_reader = StatusReader()
            agents = []

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = status_reader.get_agent_status(agent_id)
                if status:
                    agents.append(
                        {
                            "id": agent_id,
                            "name": status.get("agent_name", agent_id),
                            "status": status.get("status", "unknown"),
                            "points": status.get("points_summary", {}),
                        }
                    )

            embed = discord.Embed(
                title="🐝 Swarm Status (Refreshed)",
                description="Updated agent status",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow(),
            )

            for agent in agents:
                emoji = "🟢" if agent["status"] == "active" else "🟡"
                points = agent["points"] if isinstance(agent["points"], int) else 0
                embed.add_field(
                    name=f"{emoji} {agent['id']}",
                    value=f"{agent['name']}\n{points} points",
                    inline=True,
                )

            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            logger.error(f"Error refreshing status: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


__all__ = ["AgentMessagingGUIView", "SwarmStatusGUIView"]
