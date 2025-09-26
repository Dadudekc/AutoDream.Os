#!/usr/bin/env python3
"""
Advanced Messaging Discord Commands
===================================

Advanced messaging features for Discord bot - history, agent management, and system monitoring.
"""

import discord
from discord import app_commands
from typing import Optional


def setup_messaging_advanced_commands(bot):
    """Setup advanced messaging slash commands."""

    @bot.tree.command(name="message-history", description="View message history for an agent")
    @app_commands.describe(
        agent="Agent ID to show history for (optional - shows all if not specified)",
        limit="Number of messages to show (default: 10)"
    )
    async def view_message_history(interaction: discord.Interaction, agent: Optional[str] = None, limit: int = 10):
        """View message history for an agent."""
        try:
            # Initialize messaging service
            from src.services.messaging.service import MessagingService
            
            messaging_service = MessagingService(dry_run=False)
            
            # Get message history
            if agent:
                # Validate agent ID
                if agent not in bot.agent_coordinates:
                    await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
                    return
                
                messages = messaging_service.show_message_history(agent)
                if not messages:
                    await interaction.response.send_message(f"📋 **No message history found for {agent}.**")
                    return
                
                response = f"📋 **Message History for {agent}:**\n\n"
                for msg in messages[-limit:]:
                    response += f"**{msg.timestamp}** - {msg.sender}: {msg.content}\n"
            else:
                # Show recent messages from all agents
                all_messages = []
                for agent_id in bot.agent_coordinates.keys():
                    agent_messages = messaging_service.show_message_history(agent_id)
                    if agent_messages:
                        all_messages.extend(agent_messages)
                
                if not all_messages:
                    await interaction.response.send_message("📋 **No message history found.**")
                    return
                
                # Sort by timestamp and get recent messages
                all_messages.sort(key=lambda x: x.timestamp, reverse=True)
                recent_messages = all_messages[:limit]
                
                response = f"📋 **Recent Message History (Last {len(recent_messages)} Messages):**\n\n"
                for msg in recent_messages:
                    response += f"**{msg.timestamp}** - {msg.sender} → {getattr(msg, 'recipient', 'Unknown')}: {msg.content}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Message history retrieved!"
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error retrieving message history: {e}")

    @bot.tree.command(name="list-agents", description="List all available agents and their status")
    async def list_agents(interaction: discord.Interaction):
        """List all available agents and their status."""
        try:
            # Initialize messaging service
            from src.services.messaging.service import MessagingService
            
            messaging_service = MessagingService(dry_run=False)
            
            # Get available agents
            agents = messaging_service.list_available_agents()
            
            response = "🤖 **Available Agents:**\n\n"
            
            for agent_id, coords in bot.agent_coordinates.items():
                status_icon = "✅" if coords.get('active', True) else "❌"
                x, y = coords.get('x', 0), coords.get('y', 0)
                response += f"{status_icon} **{agent_id}** - Coordinates: ({x}, {y})\n"
            
            response += f"\n**Total Agents:** {len(agents)}\n"
            response += f"**Active Agents:** {len([a for a in bot.agent_coordinates.values() if a.get('active', True)])}\n"
            response += "\n🐝 **WE ARE SWARM** - Agent list retrieved!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error listing agents: {e}")

    @bot.tree.command(name="send-advanced", description="Send message with advanced options")
    @app_commands.describe(
        agent="Agent ID to send message to",
        message="Message content",
        priority="Message priority (NORMAL, HIGH, URGENT)",
        message_type="Message type (direct, broadcast, system)",
        sender="Sender identifier (default: Discord-Commander)"
    )
    async def send_advanced_message(
        interaction: discord.Interaction,
        agent: str,
        message: str,
        priority: str = "NORMAL",
        message_type: str = "direct",
        sender: str = "Discord-Commander"
    ):
        """Send message with advanced options."""
        try:
            # Validate agent ID
            if agent not in bot.agent_coordinates:
                await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
                return
            
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "URGENT", "LOW"]
            if priority.upper() not in valid_priorities:
                await interaction.response.send_message(f"❌ Invalid priority. Valid options: {', '.join(valid_priorities)}")
                return
            
            # Validate message type
            valid_types = ["direct", "broadcast", "system"]
            if message_type.lower() not in valid_types:
                await interaction.response.send_message(f"❌ Invalid message type. Valid options: {', '.join(valid_types)}")
                return
            
            # Use messaging service to send message
            success = bot.messaging_service.send_message(agent, message, sender, priority.upper())
            
            if success:
                response = f"✅ **Advanced Message Sent Successfully!**\n\n"
                response += f"**To:** {agent}\n"
                response += f"**Message:** {message}\n"
                response += f"**Priority:** {priority.upper()}\n"
                response += f"**Type:** {message_type.upper()}\n"
                response += f"**Sender:** {sender}\n"
                response += "\n🐝 **WE ARE SWARM** - Advanced message delivered!"
            else:
                response = f"❌ **Failed to send advanced message to {agent}**"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending advanced message: {e}")

    @bot.tree.command(name="broadcast-advanced", description="Broadcast message with advanced options")
    @app_commands.describe(
        message="Message content to broadcast",
        priority="Message priority (NORMAL, HIGH, URGENT)",
        sender="Sender identifier (default: Discord-Commander)"
    )
    async def broadcast_advanced_message(
        interaction: discord.Interaction,
        message: str,
        priority: str = "NORMAL",
        sender: str = "Discord-Commander"
    ):
        """Broadcast message with advanced options."""
        try:
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "URGENT", "LOW"]
            if priority.upper() not in valid_priorities:
                await interaction.response.send_message(f"❌ Invalid priority. Valid options: {', '.join(valid_priorities)}")
                return
            
            # Use messaging service to broadcast message
            results = bot.messaging_service.broadcast_message(message, sender, priority.upper())
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📢 **Advanced Broadcast Sent!**\n\n"
            response += f"**Message:** {message}\n"
            response += f"**Priority:** {priority.upper()}\n"
            response += f"**Sender:** {sender}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive broadcast**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Advanced broadcast delivered!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending advanced broadcast: {e}")
