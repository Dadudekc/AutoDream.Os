#!/usr/bin/env python3
"""
Agent Discord Commands
======================

Agent-related slash commands for Discord bot.
"""

import discord
from discord import app_commands


def setup_agent_commands(bot):
    """Setup agent-related slash commands."""

    @bot.tree.command(name="agents", description="List all agents and their status")
    async def list_agents(interaction: discord.Interaction):
        """List all agents and their status."""
        agent_list = "**V2_SWARM Agent Status:**\n\n"
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status = (
                "🟢 Active"
                if bot.agent_coordinates.get(agent_id, {}).get("active", True)
                else "🔴 Inactive"
            )
            description = bot.agent_coordinates.get(agent_id, {}).get("description", f"Agent {i}")
            roles = {
                "Agent-1": "Integration & Core Systems Specialist",
                "Agent-2": "Architecture & Design Specialist",
                "Agent-3": "Infrastructure & DevOps Specialist",
                "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
                "Agent-5": "Business Intelligence Specialist",
                "Agent-6": "Coordination & Communication Specialist",
                "Agent-7": "Web Development Specialist",
                "Agent-8": "Operations & Support Specialist",
            }
            role = roles.get(agent_id, "Specialist")
            agent_list += f"{agent_id}: {status} - {role}\n"
        agent_list += "\n**Captain Agent-4** coordinates all operations.\n"
        agent_list += "**Agent-6** handles communication protocols.\n\n"
        agent_list += "🐝 **WE ARE SWARM** - Ready for coordination!"
        await interaction.response.send_message(agent_list)

    @bot.tree.command(name="agent-channels", description="List agent-specific Discord channels")
    async def list_agent_channels(interaction: discord.Interaction):
        """List agent-specific Discord channels."""
        channels_text = "**V2_SWARM Agent Discord Channels:**\n\n"
        
        for agent_id, channel_id in bot.devlog_service.agent_channels.items():
            channels_text += f"**{agent_id}:** `{channel_id}`\n"
        
        if not bot.devlog_service.agent_channels:
            channels_text += "⚠️ No agent-specific channels configured\n"
            channels_text += "💡 Set DISCORD_CHANNEL_AGENT_X environment variables"
        else:
            channels_text += f"\n**Total:** {len(bot.devlog_service.agent_channels)} agent channels configured"
            channels_text += "\n**Main Channel:** " + (str(bot.devlog_service.channel_id) if bot.devlog_service.channel_id else "Not configured")
        
        channels_text += "\n\n🐝 **WE ARE SWARM** - Agent channels ready!"
        await interaction.response.send_message(channels_text)

    @bot.tree.command(name="swarm", description="Send message to all agents")
    @app_commands.describe(message="Message to send to all agents")
    async def swarm_message(interaction: discord.Interaction, message: str):
        """Send message to all agents."""
        try:
            # Use messaging service to broadcast
            results = bot.messaging_service.broadcast_message(message, "Discord-Commander")
            
            active_agents = [agent for agent, success in results.items() if success]
            failed_agents = [agent for agent, success in results.items() if not success]
            
            response = f"**SWARM MESSAGE SENT** 🐝\n\n"
            response += f"**Message:** {message}\n\n"
            response += f"**Delivered to:** {len(active_agents)} active agents\n"
            
            if active_agents:
                response += f"**Successful:** {', '.join(active_agents)}\n"
            
            if failed_agents:
                response += f"**Failed:** {', '.join(failed_agents)}\n"
            
            response += f"\n**Total agents:** {len(results)}"
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending swarm message: {e}")

