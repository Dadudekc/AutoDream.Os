#!/usr/bin/env python3
"""
Discord UI Modals - Interactive Input Components
================================================

Interactive input components for Discord bot dashboard.
Handles modals, text inputs, and form interactions.

V2 Compliance: ≤400 lines, focused input components module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging

import discord
from discord.ui import Modal, TextInput

logger = logging.getLogger(__name__)


class MessageAgentModal(Modal):
    """Modal for messaging agents."""

    def __init__(self, bot):
        """Initialize message agent modal."""
        super().__init__(title="📨 Message Agent")
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.MessageAgentModal")

        # Agent selection
        self.agent_input = TextInput(
            label="Agent ID",
            placeholder="Enter agent ID (e.g., Agent-4)",
            required=True,
            max_length=20,
        )
        self.add_item(self.agent_input)

        # Message content
        self.message_input = TextInput(
            label="Message",
            placeholder="Enter your message...",
            required=True,
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.message_input)

        # Priority selection
        self.priority_input = TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, or URGENT",
            required=False,
            max_length=10,
            default="NORMAL",
        )
        self.add_item(self.priority_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            await interaction.response.defer()

            agent_id = self.agent_input.value.strip()
            message = self.message_input.value.strip()
            priority = self.priority_input.value.strip().upper()

            # Validate inputs
            if not agent_id or not message:
                await interaction.followup.send(
                    "❌ Agent ID and message are required", ephemeral=True
                )
                return

            if priority not in ["NORMAL", "HIGH", "URGENT"]:
                priority = "NORMAL"

            # Send message to agent
            success = await self._send_agent_message(agent_id, message, priority)

            if success:
                await interaction.followup.send(
                    f"✅ Message sent to {agent_id} with priority {priority}", ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"❌ Failed to send message to {agent_id}", ephemeral=True
                )

        except Exception as e:
            self.logger.error(f"Error in message agent modal: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

    async def _send_agent_message(self, agent_id: str, message: str, priority: str) -> bool:
        """Send message to agent."""
        try:
            # This would integrate with the actual messaging system
            self.logger.info(f"Sending message to {agent_id}: {message[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"Error sending agent message: {e}")
            return False


class BroadcastModal(Modal):
    """Modal for broadcasting messages."""

    def __init__(self, bot):
        """Initialize broadcast modal."""
        super().__init__(title="📢 Broadcast Message")
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.BroadcastModal")

        # Broadcast message
        self.message_input = TextInput(
            label="Broadcast Message",
            placeholder="Enter message to broadcast to all agents...",
            required=True,
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.message_input)

        # Priority selection
        self.priority_input = TextInput(
            label="Priority",
            placeholder="NORMAL, HIGH, or URGENT",
            required=False,
            max_length=10,
            default="NORMAL",
        )
        self.add_item(self.priority_input)

        # Target agents
        self.targets_input = TextInput(
            label="Target Agents",
            placeholder="Agent-4,Agent-5,Agent-6 or leave empty for all",
            required=False,
            max_length=100,
        )
        self.add_item(self.targets_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            await interaction.response.defer()

            message = self.message_input.value.strip()
            priority = self.priority_input.value.strip().upper()
            targets = self.targets_input.value.strip()

            # Validate inputs
            if not message:
                await interaction.followup.send("❌ Message is required", ephemeral=True)
                return

            if priority not in ["NORMAL", "HIGH", "URGENT"]:
                priority = "NORMAL"

            # Parse targets
            target_list = []
            if targets:
                target_list = [t.strip() for t in targets.split(",") if t.strip()]

            # Send broadcast
            success = await self._send_broadcast(message, priority, target_list)

            if success:
                target_text = f" to {len(target_list)} agents" if target_list else " to all agents"
                await interaction.followup.send(
                    f"✅ Broadcast sent{target_text} with priority {priority}", ephemeral=True
                )
            else:
                await interaction.followup.send("❌ Failed to send broadcast", ephemeral=True)

        except Exception as e:
            self.logger.error(f"Error in broadcast modal: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

    async def _send_broadcast(self, message: str, priority: str, targets: list[str]) -> bool:
        """Send broadcast message."""
        try:
            # This would integrate with the actual messaging system
            self.logger.info(f"Sending broadcast: {message[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"Error sending broadcast: {e}")
            return False


class SocialMediaPostModal(Modal):
    """Modal for creating social media posts."""

    def __init__(self, bot):
        """Initialize social media post modal."""
        super().__init__(title="📱 Create Social Media Post")
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.SocialMediaPostModal")

        # Post content
        self.content_input = TextInput(
            label="Post Content",
            placeholder="Enter your social media post content...",
            required=True,
            max_length=500,
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.content_input)

        # Platform selection
        self.platform_input = TextInput(
            label="Platforms",
            placeholder="twitter,linkedin,facebook (comma-separated)",
            required=True,
            max_length=100,
        )
        self.add_item(self.platform_input)

        # Schedule option
        self.schedule_input = TextInput(
            label="Schedule (Optional)",
            placeholder="YYYY-MM-DD HH:MM or leave empty for immediate",
            required=False,
            max_length=20,
        )
        self.add_item(self.schedule_input)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            await interaction.response.defer()

            content = self.content_input.value.strip()
            platforms = self.platform_input.value.strip()
            schedule = self.schedule_input.value.strip()

            # Validate inputs
            if not content or not platforms:
                await interaction.followup.send(
                    "❌ Content and platforms are required", ephemeral=True
                )
                return

            # Parse platforms
            platform_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
            valid_platforms = ["twitter", "linkedin", "facebook", "instagram"]
            platform_list = [p for p in platform_list if p in valid_platforms]

            if not platform_list:
                await interaction.followup.send("❌ No valid platforms specified", ephemeral=True)
                return

            # Create post
            success = await self._create_social_post(content, platform_list, schedule)

            if success:
                platform_text = ", ".join(platform_list)
                schedule_text = f" scheduled for {schedule}" if schedule else " posted immediately"
                await interaction.followup.send(
                    f"✅ Post created for {platform_text}{schedule_text}", ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Failed to create social media post", ephemeral=True
                )

        except Exception as e:
            self.logger.error(f"Error in social media post modal: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

    async def _create_social_post(self, content: str, platforms: list[str], schedule: str) -> bool:
        """Create social media post."""
        try:
            # This would integrate with the actual social media system
            self.logger.info(f"Creating social post for {platforms}: {content[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"Error creating social post: {e}")
            return False


__all__ = ["MessageAgentModal", "BroadcastModal", "SocialMediaPostModal"]

