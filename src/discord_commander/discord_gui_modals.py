#!/usr/bin/env python3
"""
Discord GUI Modals - Agent Messaging Modals
============================================

Discord UI Modals for message composition.

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import logging

# Discord imports with error handling
try:
    import discord

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

from src.services.messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class AgentMessageModal(discord.ui.Modal):
    """Modal for composing message to specific agent."""

    def __init__(self, agent_id: str, messaging_service: ConsolidatedMessagingService):
        super().__init__(title=f"Message to {agent_id}")
        self.agent_id = agent_id
        self.messaging_service = messaging_service

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Message (Shift+Enter for line breaks)",
            placeholder=f"Enter message for {agent_id}...\n\nTip: Use Shift+Enter to add line breaks",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority dropdown (added as text for modal compatibility)
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder="regular",
            default="regular",
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            # Send message
            result = self.messaging_service.send_message(
                agent=self.agent_id, message=message, priority=priority, use_pyautogui=True
            )

            if result.get("success"):
                # Preserve line breaks in confirmation by using code block
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Message sent to {self.agent_id}!\n\n**Message Preview:**\n```\n{message_preview}\n```",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ Failed to send message: {result.get('error')}", ephemeral=True
                )

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


class BroadcastMessageModal(discord.ui.Modal):
    """Modal for broadcasting message to all agents."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        super().__init__(title="Broadcast to All Agents")
        self.messaging_service = messaging_service

        # Message input
        self.message_input = discord.ui.TextInput(
            label="Broadcast Message (Shift+Enter for line breaks)",
            placeholder="Enter message for all agents...\n\nTip: Use Shift+Enter to add line breaks",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000,
        )
        self.add_item(self.message_input)

        # Priority input
        self.priority_input = discord.ui.TextInput(
            label="Priority (regular/urgent)",
            placeholder="regular",
            default="regular",
            required=False,
            max_length=10,
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value or "regular"

            # Broadcast to all agents
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0
            errors = []

            for agent in agents:
                result = self.messaging_service.send_message(
                    agent=agent, message=message, priority=priority, use_pyautogui=True
                )
                if result.get("success"):
                    success_count += 1
                else:
                    errors.append(f"{agent}: {result.get('error')}")

            # Send result
            if success_count == len(agents):
                message_preview = message if len(message) <= 500 else message[:497] + "..."
                await interaction.response.send_message(
                    f"✅ Broadcast sent to all {len(agents)} agents!\n\n**Message Preview:**\n```\n{message_preview}\n```",
                    ephemeral=True,
                )
            else:
                error_msg = "\n".join(errors[:3])  # Show first 3 errors
                message_preview = message if len(message) <= 300 else message[:297] + "..."
                await interaction.response.send_message(
                    f"⚠️ Partial broadcast: {success_count}/{len(agents)} successful\n\n"
                    f"**Message:**\n```\n{message_preview}\n```\n"
                    f"**Errors:**\n{error_msg}",
                    ephemeral=True,
                )

        except Exception as e:
            logger.error(f"Error broadcasting: {e}")
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


__all__ = ["AgentMessageModal", "BroadcastMessageModal"]
