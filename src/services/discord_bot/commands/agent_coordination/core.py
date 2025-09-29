#!/usr/bin/env python3
"""
Agent Coordination Core - V2 Compliant
======================================

Core agent coordination functionality for Discord bot.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import logging

import discord

from .messaging import AgentMessagingHandler
from .onboarding import AgentOnboardingHandler
from .status import AgentStatusHandler

logger = logging.getLogger(__name__)


class AgentCoordinationCore:
    """Core agent coordination functionality for Discord bot."""

    def __init__(self, bot):
        """Initialize agent coordination core."""
        self.bot = bot
        self._main_interface_callback = None

        # Initialize specialized handlers
        self.onboarding = AgentOnboardingHandler(self)
        self.messaging = AgentMessagingHandler(self)
        self.status = AgentStatusHandler(self)

    async def agents_cb(self, cb_inter):
        """Enhanced Agent Coordination Interface with onboarding and messaging."""

        # Create main coordination embed
        embed = discord.Embed(
            title="🎯 Agent Coordination Center",
            description="**V2_SWARM Agent Management & Communication Hub**",
            color=0x00FF00,
        )

        # Add agent status information
        agents_info = {
            "Agent-1": "Integration & Core Systems",
            "Agent-2": "Architecture & Design",
            "Agent-3": "Infrastructure & DevOps",
            "Agent-4": "Quality Assurance (CAPTAIN)",
            "Agent-5": "Business Intelligence",
            "Agent-6": "Coordination & Communication",
            "Agent-7": "Web Development",
            "Agent-8": "Operations & Support",
        }

        embed.add_field(
            name="📊 **Agent Status**",
            value="\n".join([f"**{k}** - {v}" for k, v in agents_info.items()]),
            inline=False,
        )

        embed.add_field(
            name="🎓 **Quick Actions**",
            value="• Click agent buttons to onboard\n• Use messaging buttons for communication\n• Select teams/roles for new agents",
            inline=False,
        )

        embed.set_footer(text="🐝 WE ARE SWARM — Advanced Agent Coordination")

        # Create comprehensive view with agent buttons
        view = discord.ui.View(timeout=600)

        # Create agent selection buttons (4 per row)
        agent_rows = [
            ["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
            ["Agent-5", "Agent-6", "Agent-7", "Agent-8"],
        ]

        for row in agent_rows:
            for agent_id in row:
                btn = discord.ui.Button(
                    label=agent_id,
                    style=discord.ButtonStyle.primary,
                    custom_id=f"agent_select:{agent_id}",
                )

                async def agent_callback(interaction, agent=agent_id):
                    await self.handle_agent_selection(interaction, agent)

                btn.callback = agent_callback
                view.add_item(btn)

        # Add utility buttons
        refresh_btn = discord.ui.Button(
            label="🔄 Refresh Status",
            style=discord.ButtonStyle.secondary,
            custom_id="refresh_agents",
        )
        refresh_btn.callback = self.agents_cb
        view.add_item(refresh_btn)

        back_btn = discord.ui.Button(
            label="⬅️ Back to Main", style=discord.ButtonStyle.secondary, custom_id="back_to_main"
        )
        # Store reference to main interface callback
        if hasattr(self, "_main_interface_callback"):
            back_btn.callback = self._main_interface_callback
        else:
            # Fallback - just send a message
            async def fallback_callback(inter):
                await inter.response.send_message(
                    "Main interface callback not set.", ephemeral=True
                )

            back_btn.callback = fallback_callback
        view.add_item(back_btn)

        await cb_inter.response.edit_message(embed=embed, view=view)

    async def handle_agent_selection(self, interaction, agent_id):
        """Handle agent selection and show action options."""

        # Create agent-specific embed
        embed = discord.Embed(
            title=f"🤖 {agent_id} Management",
            description=f"**Managing {agent_id}** - Select an action to perform",
            color=0x0099FF,
        )

        embed.add_field(
            name="📋 **Available Actions**",
            value=f"• **Onboard** - Set up {agent_id} with team assignment\n• **Message** - Send message to {agent_id}\n• **Status** - Check {agent_id} current status",
            inline=False,
        )

        embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Coordination")

        # Create action buttons
        view = discord.ui.View(timeout=300)

        # Onboard button
        onboard_btn = discord.ui.Button(
            label="🎓 Onboard Agent",
            style=discord.ButtonStyle.success,
            custom_id=f"onboard:{agent_id}",
        )

        async def onboard_callback(inter):
            await self.onboarding.handle_agent_onboarding(inter, agent_id)

        onboard_btn.callback = onboard_callback
        view.add_item(onboard_btn)

        # Message button
        message_btn = discord.ui.Button(
            label="💬 Send Message",
            style=discord.ButtonStyle.primary,
            custom_id=f"message:{agent_id}",
        )

        async def message_callback(inter):
            await self.messaging.handle_agent_messaging(inter, agent_id)

        message_btn.callback = message_callback
        view.add_item(message_btn)

        # Status button
        status_btn = discord.ui.Button(
            label="📊 Check Status",
            style=discord.ButtonStyle.secondary,
            custom_id=f"status:{agent_id}",
        )

        async def status_callback(inter):
            await self.status.handle_agent_status_check(inter, agent_id)

        status_btn.callback = status_callback
        view.add_item(status_btn)

        # Back button
        back_btn = discord.ui.Button(
            label="⬅️ Back to Agents", style=discord.ButtonStyle.danger, custom_id="back_to_agents"
        )
        back_btn.callback = self.agents_cb
        view.add_item(back_btn)

        await interaction.response.edit_message(embed=embed, view=view)

    def set_main_interface_callback(self, callback):
        """Set the main interface callback for navigation."""
        self._main_interface_callback = callback

    def get_team_description(self, team_name):
        """Get team description for onboarding."""
        team_descriptions = {
            "Team Alpha": "Core development and architecture team",
            "Team Beta": "Infrastructure and DevOps team",
            "Team Gamma": "Quality assurance and testing team",
            "Team Delta": "Business intelligence and analytics team",
        }
        return team_descriptions.get(team_name, "General purpose team")

    def _is_admin(self, interaction):
        """Check if user is admin."""
        return interaction.user.guild_permissions.administrator

    async def _deny(self, interaction, message):
        """Deny action with message."""
        await interaction.response.send_message(f"❌ {message}", ephemeral=True)
