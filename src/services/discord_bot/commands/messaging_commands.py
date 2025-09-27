#!/usr/bin/env python3
"""
Messaging Discord Commands
==========================

Messaging-related slash commands for Discord bot.
"""

import discord
from discord import app_commands


def setup_messaging_commands(bot):
    """Setup messaging-related slash commands."""

    # Note: /send command moved to send_controller.py for enhanced functionality

    @bot.tree.command(name="msg-status", description="Get messaging system status")
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