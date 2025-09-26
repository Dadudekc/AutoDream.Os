#!/usr/bin/env python3
"""
Discord Commander Modals
========================

Modal components for user input in Discord Commander.
"""

import discord
from discord import app_commands
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


class DevlogCreateModal(discord.ui.Modal):
    """Modal for creating devlog entries."""
    
    def __init__(self, bot):
        super().__init__(title="Create Devlog Entry")
        self.bot = bot
        
        self.action_input = discord.ui.TextInput(
            label="Action Description",
            placeholder="Describe the action performed...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.action_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            action = self.action_input.value
            
            # Create devlog
            filepath = self.bot.devlog_service.create_devlog(
                agent_id="Discord-Commander",
                action=action,
                status="completed",
                details={"source": "discord_command", "channel": interaction.channel.name}
            )
            
            # Post to Discord
            success = self.bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(
                    f"✅ **Devlog Created & Posted!**\n📄 File: `{filepath}`",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"✅ **Devlog Created!**\n📄 File: `{filepath}`\n⚠️ Failed to post to Discord",
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error creating devlog: {e}",
                ephemeral=True
            )


class AgentDevlogCreateModal(discord.ui.Modal):
    """Modal for creating agent-specific devlog entries."""
    
    def __init__(self, bot, agent_id: str):
        super().__init__(title=f"Create Devlog for {agent_id}")
        self.bot = bot
        self.agent_id = agent_id
        
        self.action_input = discord.ui.TextInput(
            label="Action Description",
            placeholder="Describe the action performed...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.action_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            action = self.action_input.value
            
            # Create devlog
            filepath = self.bot.devlog_service.create_devlog(
                agent_id=self.agent_id,
                action=action,
                status="completed",
                details={"source": "discord_command", "channel": interaction.channel.name}
            )
            
            # Post to Discord
            success = self.bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(
                    f"✅ **Agent Devlog Created & Posted!**\n📄 File: `{filepath}`\n🤖 Agent: {self.agent_id}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"✅ **Agent Devlog Created!**\n📄 File: `{filepath}`\n🤖 Agent: {self.agent_id}\n⚠️ Failed to post to Discord",
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error creating agent devlog: {e}",
                ephemeral=True
            )


class QuickBroadcastModal(discord.ui.Modal):
    """Modal for quick broadcast messages."""
    
    def __init__(self, bot):
        super().__init__(title="Quick Broadcast Message")
        self.bot = bot
        
        self.message_input = discord.ui.TextInput(
            label="Message Content",
            placeholder="Enter your message to broadcast to all agents...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.message_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            
            # Use messaging service to broadcast
            results = self.bot.messaging_service.broadcast_message(message, "Discord-Commander")
            
            active_agents = [agent for agent, success in results.items() if success]
            failed_agents = [agent for agent, success in results.items() if not success]
            
            response = f"📢 **Quick Broadcast Sent!**\n\n"
            response += f"**Message:** {message}\n\n"
            response += f"**Delivered to:** {len(active_agents)} active agents\n"
            
            if active_agents:
                response += f"**Successful:** {', '.join(active_agents)}\n"
            
            if failed_agents:
                response += f"**Failed:** {', '.join(failed_agents)}\n"
            
            response += f"\n**Total agents:** {len(results)}"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending quick broadcast: {e}",
                ephemeral=True
            )


class SenderConfigModal(discord.ui.Modal):
    """Modal for configuring sender information."""
    
    def __init__(self, callback: Callable):
        super().__init__(title="Configure Sender")
        self.callback = callback
        
        self.sender_input = discord.ui.TextInput(
            label="Sender Name",
            placeholder="Enter sender identifier...",
            style=discord.TextStyle.short,
            required=True,
            max_length=100,
            default="Discord-Commander"
        )
        self.add_item(self.sender_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        sender = self.sender_input.value
        await self.callback(interaction, sender)


class MessageInputModal(discord.ui.Modal):
    """Modal for message input."""
    
    def __init__(self, callback: Callable):
        super().__init__(title="Enter Message")
        self.callback = callback
        
        self.message_input = discord.ui.TextInput(
            label="Message Content",
            placeholder="Enter your message...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.message_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        message = self.message_input.value
        await self.callback(interaction, message)


class AgentMessageModal(discord.ui.Modal):
    """Modal for sending messages to specific agents."""
    
    def __init__(self, bot, agent_id: str):
        super().__init__(title=f"Send Message to {agent_id}")
        self.bot = bot
        self.agent_id = agent_id
        
        self.message_input = discord.ui.TextInput(
            label="Message Content",
            placeholder="Enter your message...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.message_input)
        
        self.priority_input = discord.ui.TextInput(
            label="Priority (NORMAL, HIGH, URGENT, LOW)",
            placeholder="NORMAL",
            style=discord.TextStyle.short,
            required=False,
            max_length=10,
            default="NORMAL"
        )
        self.add_item(self.priority_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            message = self.message_input.value
            priority = self.priority_input.value.upper()
            
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "URGENT", "LOW"]
            if priority not in valid_priorities:
                await interaction.response.send_message(
                    f"❌ Invalid priority. Valid options: {', '.join(valid_priorities)}",
                    ephemeral=True
                )
                return
            
            # Use messaging service to send message
            success = self.bot.messaging_service.send_message(
                self.agent_id, message, "Discord-Commander", priority
            )
            
            if success:
                response = f"✅ **Message Sent Successfully!**\n"
                response += f"🤖 **To:** {self.agent_id}\n"
                response += f"💬 **Message:** {message}\n"
                response += f"⚡ **Priority:** {priority}\n"
                response += f"👤 **From:** Discord-Commander"
                await interaction.response.send_message(response, ephemeral=True)
            else:
                await interaction.response.send_message(
                    f"❌ **Failed to send message to {self.agent_id}**",
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending message: {e}",
                ephemeral=True
            )


class ProjectUpdateModal(discord.ui.Modal):
    """Modal for creating project updates."""
    
    def __init__(self, bot):
        super().__init__(title="Create Project Update")
        self.bot = bot
        
        self.update_type_input = discord.ui.TextInput(
            label="Update Type",
            placeholder="milestone, status, system_change, etc.",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.update_type_input)
        
        self.title_input = discord.ui.TextInput(
            label="Update Title",
            placeholder="Brief title for the update...",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.title_input)
        
        self.description_input = discord.ui.TextInput(
            label="Update Description",
            placeholder="Detailed description of the update...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.description_input)
        
        self.priority_input = discord.ui.TextInput(
            label="Priority (NORMAL, HIGH, URGENT)",
            placeholder="NORMAL",
            style=discord.TextStyle.short,
            required=False,
            max_length=10,
            default="NORMAL"
        )
        self.add_item(self.priority_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            update_type = self.update_type_input.value
            title = self.title_input.value
            description = self.description_input.value
            priority = self.priority_input.value.upper()
            
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "URGENT"]
            if priority not in valid_priorities:
                await interaction.response.send_message(
                    f"❌ Invalid priority. Valid options: {', '.join(valid_priorities)}",
                    ephemeral=True
                )
                return
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send project update
            results = update_system.send_project_update(
                update_type=update_type,
                title=title,
                description=description,
                priority=priority
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📋 **Project Update Sent!**\n\n"
            response += f"**Type:** {update_type}\n"
            response += f"**Title:** {title}\n"
            response += f"**Priority:** {priority}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Project update delivered!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending project update: {e}",
                ephemeral=True
            )


class MilestoneModal(discord.ui.Modal):
    """Modal for creating milestone notifications."""
    
    def __init__(self, bot):
        super().__init__(title="Create Milestone Notification")
        self.bot = bot
        
        self.name_input = discord.ui.TextInput(
            label="Milestone Name",
            placeholder="Name of the milestone...",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.name_input)
        
        self.description_input = discord.ui.TextInput(
            label="Milestone Description",
            placeholder="Description of the milestone...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.description_input)
        
        self.completion_input = discord.ui.TextInput(
            label="Completion Percentage (0-100)",
            placeholder="100",
            style=discord.TextStyle.short,
            required=True,
            max_length=3,
            default="100"
        )
        self.add_item(self.completion_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            name = self.name_input.value
            description = self.description_input.value
            
            # Validate completion percentage
            try:
                completion = int(self.completion_input.value)
                if completion < 0 or completion > 100:
                    raise ValueError("Completion must be between 0 and 100")
            except ValueError:
                await interaction.response.send_message(
                    "❌ Invalid completion percentage. Must be a number between 0 and 100.",
                    ephemeral=True
                )
                return
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send milestone notification
            results = update_system.send_milestone_notification(
                milestone=name,
                description=description,
                completion_percentage=completion
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"🎯 **Milestone Notification Sent!**\n\n"
            response += f"**Milestone:** {name}\n"
            response += f"**Completion:** {completion}%\n"
            response += f"**Description:** {description}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive notification**\n"
            
            response += "\n🏆 **Milestone achieved and communicated!**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending milestone notification: {e}",
                ephemeral=True
            )