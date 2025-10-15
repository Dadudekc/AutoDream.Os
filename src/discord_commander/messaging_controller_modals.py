"""
Discord Messaging Controller Modals
====================================

Discord UI modals for message input and submission.
Extracted from messaging_controller.py for preventive optimization.

Features:
- Message input modal for agent messaging
- Broadcast modal for swarm-wide messages
- Priority selection and validation

Author: Agent-7 (original), Agent-1 (preventive refactor)
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging
from datetime import datetime

# Discord imports with error handling
try:
    import discord

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class MessageModal(discord.ui.Modal):
    """Modal for message input."""

    def __init__(self, agent_id: str, messaging_service):
        super().__init__(title=f"Message Agent {agent_id}")
        self.agent_id = agent_id
        self.messaging_service = messaging_service

        self.message_input = discord.ui.TextInput(
            label="Message",
            placeholder="Type your message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000,
        )
        self.add_item(self.message_input)

        self.priority_select = discord.ui.TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, CRITICAL",
            default="NORMAL",
            required=False,
            max_length=20,
        )
        self.add_item(self.priority_select)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle message submission."""
        message = self.message_input.value
        priority = self.priority_select.value or "NORMAL"

        try:
            # Send message through messaging service
            success = self.messaging_service.send_message(
                agent=self.agent_id,  # Fixed: 'agent' not 'agent_id'
                message=message,
                priority=priority,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Message sent to **{self.agent_id}**",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)
                embed.add_field(name="From", value="Discord User", inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="❌ Message Failed",
                    description=f"Failed to send message to **{self.agent_id}**",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error sending message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class BroadcastModal(discord.ui.Modal):
    """Modal for broadcast messages."""

    def __init__(self, messaging_service):
        super().__init__(title="Broadcast Message to All Agents")
        self.messaging_service = messaging_service

        self.message_input = discord.ui.TextInput(
            label="Broadcast Message",
            placeholder="Type your broadcast message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000,
        )
        self.add_item(self.message_input)

        self.priority_select = discord.ui.TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, CRITICAL",
            default="NORMAL",
            required=False,
            max_length=20,
        )
        self.add_item(self.priority_select)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle broadcast submission."""
        message = self.message_input.value
        priority = self.priority_select.value or "NORMAL"

        try:
            success = self.messaging_service.broadcast_message(
                message=message, from_agent="Discord-User", priority=priority
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Message broadcasted to all agents",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="❌ Broadcast Failed",
                    description="Failed to broadcast message",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error broadcasting message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
