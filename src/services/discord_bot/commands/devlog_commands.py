#!/usr/bin/env python3
"""
Devlog Discord Commands
========================

Devlog-related slash commands for Discord bot.
"""

import discord
from discord import app_commands
import logging
from src.services.discord_bot.commands.basic_commands import safe_command


logger = logging.getLogger(__name__)


def setup_devlog_commands(bot):
    """Setup devlog-related slash commands."""

    @bot.tree.command(name="devlog", description="Create devlog entry")
    @safe_command
    @app_commands.describe(action="Action description for the devlog")
    async def create_devlog(interaction: discord.Interaction, action: str):
        """Create devlog entry."""
        try:
            # Create devlog
            filepath = bot.devlog_service.create_devlog(
                agent_id="Discord-Commander",
                action=action,
                status="completed",
                details={"source": "discord_command", "channel": interaction.channel.name}
            )
            
            # Post to Discord
            success = bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(f"✅ **Devlog Created & Posted!**\n📄 File: `{filepath}`")
            else:
                await interaction.response.send_message(f"✅ **Devlog Created!**\n📄 File: `{filepath}`\n⚠️ Failed to post to Discord")
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating devlog: {e}")

    @bot.tree.command(name="agent-devlog", description="Create devlog for specific agent")
    @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
    @app_commands.describe(action="Action description for the devlog")
    async def create_agent_devlog(interaction: discord.Interaction, agent: str, action: str):
        """Create devlog for specific agent."""
        # Validate agent ID
        if agent not in bot.agent_coordinates:
            await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
            return
            
        try:
            # Create devlog
            filepath = bot.devlog_service.create_devlog(
                agent_id=agent,
                action=action,
                status="completed",
                details={"source": "discord_command", "channel": interaction.channel.name}
            )
            
            # Post to Discord
            success = bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(f"✅ **Agent Devlog Created & Posted!**\n📄 File: `{filepath}`\n🤖 Agent: {agent}")
            else:
                await interaction.response.send_message(f"✅ **Agent Devlog Created!**\n📄 File: `{filepath}`\n🤖 Agent: {agent}\n⚠️ Failed to post to Discord")
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating agent devlog: {e}")

    @bot.tree.command(name="test-devlog", description="Test devlog functionality")
    @safe_command
    async def test_devlog(interaction: discord.Interaction):
        """Test devlog functionality."""
        try:
            # Create test devlog
            filepath = bot.devlog_service.create_devlog(
                agent_id="Discord-Commander",
                action="Discord bot devlog test",
                status="completed",
                details={"source": "discord_test", "channel": interaction.channel.name}
            )
            
            # Post to Discord
            success = bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(f"✅ **Test Devlog Success!**\n📄 File: `{filepath}`\n🐝 Devlog system is working!")
            else:
                await interaction.response.send_message(f"✅ **Test Devlog Created!**\n📄 File: `{filepath}`\n⚠️ Failed to post to Discord")
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Test devlog failed: {e}")