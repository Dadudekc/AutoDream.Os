#!/usr/bin/env python3
"""
Basic Discord Commands
======================

Basic slash commands for Discord bot.
"""

import discord
from discord import app_commands


def setup_basic_commands(bot):
    """Setup basic bot slash commands."""

    @bot.tree.command(name="ping", description="Test bot responsiveness")
    async def ping(interaction: discord.Interaction):
        """Test bot responsiveness."""
        latency = bot.latency
        if latency is None or str(latency) == 'nan':
            latency_ms = 'Unknown'
        else:
            latency_ms = f'{round(latency * 1000)}ms'
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency_ms}")

    @bot.tree.command(name="commands", description="Show help information")
    async def help_command(interaction: discord.Interaction):
        """Show help information."""
        help_text = """
**V2_SWARM Enhanced Discord Agent Bot Commands:**

**Basic Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show this help message
- `/status` - Show system status
- `/info` - Show bot information

**Agent Commands:**
- `/agents` - List all agents with status and coordinates
- `/agent-channels` - List agent-specific Discord channels
- `/swarm` - Send message to all agents

**Messaging Commands:**
- `/send` - Send message to specific agent (with optional priority, type, sender)
- `/broadcast-advanced` - Broadcast message with advanced options
- `/msg-status` - Get comprehensive messaging system status
- `/message-history` - View message history for an agent

**Devlog Commands:**
- `/devlog` - Create devlog entry (main channel)
- `/agent-devlog` - Create devlog for specific agent
- `/test-devlog` - Test devlog functionality

**Onboarding Commands:**
- `/onboard-agent` - Onboard a specific agent
- `/onboard-all` - Onboard all agents
- `/onboarding-status` - Check onboarding status for agents
- `/onboarding-info` - Get information about the onboarding process

**Project Update Commands:**
- `/project-update` - Send project update to all agents
- `/milestone` - Send milestone completion notification
- `/system-status` - Send system status update
- `/v2-compliance` - Send V2 compliance update
- `/doc-cleanup` - Send documentation cleanup update
- `/feature-announce` - Send feature announcement
- `/update-history` - View project update history
- `/update-stats` - View project update statistics

**Usage Examples:**
- `/ping` - Test bot
- `/agents` - List all agents with coordinates
- `/send agent:Agent-1 message:Hello priority:HIGH` - Send high priority message
- `/swarm message:All agents report status` - Broadcast to all agents
- `/devlog action:Tools cleanup completed` - Create devlog entry
- `/msg-status` - Check messaging system status
- `/onboard-agent agent:Agent-1` - Onboard specific agent

**Ready for enhanced swarm coordination!** 🐝
        """
        await interaction.response.send_message(help_text)

