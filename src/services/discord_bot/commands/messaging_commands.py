#!/usr/bin/env python3
"""
Messaging Discord Commands
==========================

Messaging-related slash commands for Discord bot.
"""

import discord
from discord import app_commands
import logging
from src.services.discord_bot.commands.basic_commands import safe_command


logger = logging.getLogger(__name__)


def setup_messaging_commands(bot):
    """Setup messaging-related slash commands."""

    @bot.tree.command(name="send", description="Send message to specific agent")
    @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
    @app_commands.describe(message="Message to send to the agent")
    async def send_message(interaction: discord.Interaction, agent: str, message: str):
        """Send message to specific agent."""
        # Validate agent ID
        if agent not in bot.agent_coordinates:
            await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
            return
            
        try:
            # Use messaging service to send message
            success = bot.messaging_service.send_message(agent, message, "Discord-Commander")
            
            if success:
                await interaction.response.send_message(f"✅ **Message Sent Successfully!**\n🤖 **To:** {agent}\n💬 **Message:** {message}")
            else:
                await interaction.response.send_message(f"❌ **Failed to send message to {agent}**")
                
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending message: {e}")

    @bot.tree.command(name="msg-status", description="Get messaging system status")
    @safe_command
    async def messaging_status(interaction: discord.Interaction):
        """Get messaging system status."""
        try:
            # Get messaging service status
            status = bot.messaging_service.get_status()
            
            response = "**V2_SWARM Messaging System Status:**\n\n"
            response += f"**Service Status:** ✅ Active\n"
            response += f"**Total Agents:** {len(bot.agent_coordinates)}\n"
            response += f"**Active Agents:** {len([a for a in bot.agent_coordinates.values() if a.get('active', True)])}\n"
            response += f"**Coordinates Loaded:** ✅ Yes\n\n"
            response += "**Available Agents:**\n"
            
            for agent_id, coords in bot.agent_coordinates.items():
                status_icon = "✅" if coords.get('active', True) else "❌"
                response += f"{status_icon} {agent_id}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Messaging system ready!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting messaging status: {e}")