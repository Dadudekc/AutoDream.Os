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

    # Note: /send command moved to send_controller.py for enhanced functionality

    @bot.tree.command(name="msg-status", description="Get messaging system status")
    @safe_command
    async def messaging_status(interaction: discord.Interaction):
        """Get comprehensive messaging system status."""
        try:
            if not bot.messaging_service:
                await interaction.response.send_message("❌ Messaging service not available")
                return
            
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
            
            # Add comprehensive status if available
            if isinstance(status, dict) and 'system_status' in status:
                response += f"\n**System Details:**\n"
                response += f"- Messaging Service: {status.get('messaging_service', 'Unknown')}\n"
                response += f"- Status Monitor: {status.get('status_monitor', 'Unknown')}\n"
                response += f"- Onboarding Service: {status.get('onboarding_service', 'Unknown')}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Messaging system ready!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting messaging status: {e}")