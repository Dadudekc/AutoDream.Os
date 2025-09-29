#!/usr/bin/env python3
"""
Agent Messaging Handler - V2 Compliant
======================================

Handles agent messaging functionality for Discord bot.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import discord
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AgentMessagingHandler:
    """Handles agent messaging functionality."""
    
    def __init__(self, core):
        """Initialize messaging handler."""
        self.core = core
    
    async def handle_agent_messaging(self, interaction, agent_id):
        """Handle agent messaging interface."""
        
        # Create messaging embed
        embed = discord.Embed(
            title=f"💬 Message {agent_id}",
            description=f"**Send a message to {agent_id}** - Select priority and enter your message",
            color=0x0099FF
        )
        
        embed.add_field(
            name="📋 **Message Priority**",
            value="• **NORMAL** - Standard communication\n• **HIGH** - Urgent matters\n• **URGENT** - Critical issues requiring immediate attention",
            inline=False
        )
        
        embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Messaging")
        
        # Create messaging view with priority selection
        view = MessagePriorityView(self, agent_id)
        
        await interaction.response.edit_message(embed=embed, view=view)


class MessagePriorityView(discord.ui.View):
    """View for selecting message priority."""
    
    def __init__(self, parent_instance, agent_id):
        """Initialize priority selection view."""
        super().__init__(timeout=300)
        self.parent = parent_instance
        self.agent_id = agent_id
    
    @discord.ui.select(
        placeholder="Select message priority...",
        options=[
            discord.SelectOption(label="NORMAL", value="normal", description="Standard communication"),
            discord.SelectOption(label="HIGH", value="high", description="Urgent matters"),
            discord.SelectOption(label="URGENT", value="urgent", description="Critical issues")
        ]
    )
    async def priority_select(self, select_interaction: discord.Interaction, select: discord.ui.Select):
        """Handle priority selection."""
        priority = select.values[0]
        await self.parent.show_message_input(select_interaction, self.agent_id, priority)
    
    @discord.ui.button(label="⬅️ Back to Agent", style=discord.ButtonStyle.secondary)
    async def enter_message(self, button_interaction: discord.Interaction, button: discord.ui.Button):
        """Back to agent selection."""
        await self.parent.core.handle_agent_selection(button_interaction, self.agent_id)


class MessageInputModal(discord.ui.Modal):
    """Modal for entering message content."""
    
    def __init__(self, parent_instance, agent_id, priority):
        """Initialize message input modal."""
        super().__init__(title=f"Message {agent_id}")
        self.parent = parent_instance
        self.agent_id = agent_id
        self.priority = priority
        
        self.message_input = discord.ui.TextInput(
            label="Message Content",
            placeholder="Enter your message here...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.message_input)
    
    async def on_submit(self, inter: discord.Interaction):
        """Handle message submission."""
        message_content = self.message_input.value
        await self.parent.execute_agent_message(inter, self.agent_id, message_content, self.priority)


class AgentMessagingHandler:
    """Extended messaging handler with message input functionality."""
    
    async def show_message_input(self, interaction, agent_id, priority):
        """Show message input modal."""
        modal = MessageInputModal(self, agent_id, priority)
        await interaction.response.send_modal(modal)
    
    async def execute_agent_message(self, interaction, agent_id, message, priority):
        """Execute sending message to agent."""
        
        try:
            # Create success embed
            embed = discord.Embed(
                title=f"✅ Message Sent to {agent_id}",
                description=f"Your message has been successfully sent to **{agent_id}**",
                color=0x00FF00
            )
            
            embed.add_field(
                name="📋 **Message Details**",
                value=f"• **To:** {agent_id}\n• **Priority:** {priority.upper()}\n• **Content:** {message[:100]}{'...' if len(message) > 100 else ''}",
                inline=False
            )
            
            embed.set_footer(text=f"🐝 WE ARE SWARM — {agent_id} Messaging Complete")
            
            # Create completion view
            view = discord.ui.View(timeout=300)
            
            # Back to agent button
            back_btn = discord.ui.Button(
                label="⬅️ Back to Agent",
                style=discord.ButtonStyle.primary,
                custom_id="back_to_agent"
            )
            
            async def back_callback(inter):
                await self.core.handle_agent_selection(inter, agent_id)
            
            back_btn.callback = back_callback
            view.add_item(back_btn)
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            
            # Log successful message
            logger.info(f"Message sent to agent {agent_id} with priority {priority}")
            
        except Exception as e:
            logger.error(f"Failed to send message to agent {agent_id}: {e}")
            
            # Create error embed
            error_embed = discord.Embed(
                title=f"❌ Message Failed",
                description=f"Failed to send message to **{agent_id}**",
                color=0xFF0000
            )
            
            error_embed.add_field(
                name="🔍 **Error Details**",
                value="An error occurred while sending the message. Please try again.",
                inline=False
            )
            
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
