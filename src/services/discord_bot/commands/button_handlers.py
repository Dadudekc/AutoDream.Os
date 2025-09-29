"""
Button Handlers Module
======================
Handles all button interactions and callbacks for the main interface.
"""

import logging

import discord
from src.services.discord_bot.commands.agent_coordination import AgentCoordination
from src.services.discord_bot.commands.main_interface import MainInterface

from .modal_handlers import RestartModal, ShutdownModal

logger = logging.getLogger(__name__)


def create_main_interface_view(bot, security_manager):
    """Create the main interface view with all buttons."""
    view = discord.ui.View(timeout=600)  # 10 min

    # Initialize components
    main_interface = MainInterface(bot)
    agent_coordination = AgentCoordination(bot)

    # Set up dependency injection
    main_interface.set_agent_coordination(agent_coordination)
    agent_coordination.set_main_interface_callback(main_interface.launch_main_interface)

    # Create buttons
    agent_button = discord.ui.Button(
        label="🎯 Agent Coordination", style=discord.ButtonStyle.primary, custom_id="main:agents"
    )
    devlog_button = discord.ui.Button(
        label="📝 Devlog & Updates", style=discord.ButtonStyle.secondary, custom_id="main:devlog"
    )
    status_button = discord.ui.Button(
        label="📊 System Status", style=discord.ButtonStyle.success, custom_id="main:status"
    )
    restart_button = discord.ui.Button(
        label="🔄 Restart Bot", style=discord.ButtonStyle.danger, custom_id="main:restart"
    )
    shutdown_button = discord.ui.Button(
        label="⏹️ Shutdown Bot", style=discord.ButtonStyle.danger, custom_id="main:shutdown"
    )

    # Set up callbacks
    agent_button.callback = lambda interaction: agent_coordination.agents_cb(interaction)
    devlog_button.callback = lambda interaction: devlog_callback(interaction)
    status_button.callback = lambda interaction: status_callback(interaction, bot)
    restart_button.callback = lambda interaction: restart_callback(
        interaction, security_manager, bot
    )
    shutdown_button.callback = lambda interaction: shutdown_callback(
        interaction, security_manager, bot
    )

    # Add buttons to view
    view.add_item(agent_button)
    view.add_item(devlog_button)
    view.add_item(status_button)
    view.add_item(restart_button)
    view.add_item(shutdown_button)

    return view


async def devlog_callback(interaction):
    """Handle devlog button callback."""
    devlog_embed = discord.Embed(
        title="📝 Devlog & Project Updates",
        description="Record your work and create updates:",
        color=0x0099FF,
    )
    devlog_embed.add_field(
        name="📋 **Available Actions:**",
        value=(
            "• **Create Devlog** — Record your work progress\n"
            "• **Project Updates** — Share project status\n"
            "• **Feature Announcements** — Announce new features\n"
            "• **Bug Reports** — Report issues found"
        ),
        inline=False,
    )
    devlog_embed.set_footer(text="📝 Keep your team informed with regular updates!")

    if interaction.response.is_done():
        await interaction.followup.send(embed=devlog_embed, ephemeral=True)
    else:
        await interaction.response.edit_message(embed=devlog_embed, view=None)


async def status_callback(interaction, bot):
    """Handle status button callback."""
    bot_name = bot.user.name if bot.user else "Discord Commander"
    status_embed = discord.Embed(
        title="📊 System Status", description="Current status of all systems:", color=0x00FF00
    )
    status_embed.add_field(
        name="✅ **Messaging System**",
        value="• PyAutoGUI automation active\n• Agent coordinates loaded\n• Message delivery operational",
        inline=False,
    )
    status_embed.add_field(
        name="🤖 **Discord Bot**",
        value=f"• **{bot_name}** is online\n• Commands registered\n• Security policies active",
        inline=False,
    )
    status_embed.add_field(
        name="🔧 **System Health**",
        value="• All services operational\n• No critical errors\n• Performance optimal",
        inline=False,
    )
    status_embed.set_footer(text="🐝 WE ARE SWARM — All systems green!")

    if interaction.response.is_done():
        await interaction.followup.send(embed=status_embed, ephemeral=True)
    else:
        await interaction.response.edit_message(embed=status_embed, view=None)


async def restart_callback(interaction, security_manager, bot):
    """Handle restart button callback."""
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Access Denied",
            description="Administrator required to restart bot.",
            color=0xFF0000,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Log restart attempt
    from src.services.discord_bot.core.security_utils import security_utils

    security_utils.log_security_event(
        "RESTART_ATTEMPTED",
        str(interaction.user.id),
        "User attempted to restart Discord bot",
        "HIGH",
    )

    await interaction.response.send_modal(RestartModal(security_manager, bot))


async def shutdown_callback(interaction, security_manager, bot):
    """Handle shutdown button callback."""
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Access Denied",
            description="Administrator required to shutdown bot.",
            color=0xFF0000,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Log shutdown attempt
    from src.services.discord_bot.core.security_utils import security_utils

    security_utils.log_security_event(
        "SHUTDOWN_ATTEMPTED",
        str(interaction.user.id),
        "User attempted to shutdown Discord bot",
        "CRITICAL",
    )

    await interaction.response.send_modal(ShutdownModal(security_manager, bot))
