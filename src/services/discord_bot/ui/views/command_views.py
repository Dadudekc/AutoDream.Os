#!/usr/bin/env python3
"""
Discord Commander UI Views
==========================

Interactive UI Views for enhanced Discord Commander experience.
"""

import discord
from discord import app_commands
from typing import Dict, List, Optional, Any, Callable
import asyncio
import logging

logger = logging.getLogger(__name__)


class AgentSelectionView(discord.ui.View):
    """View for selecting agents with interactive buttons."""
    
    def __init__(self, bot, callback: Callable, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.callback = callback
        self.selected_agents = []
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup agent selection buttons."""
        # Create buttons for each agent
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            coords = self.bot.agent_coordinates.get(agent_id, {})
            status = "🟢" if coords.get("active", True) else "🔴"
            
            button = discord.ui.Button(
                label=f"{status} {agent_id}",
                style=discord.ButtonStyle.secondary,
                custom_id=f"select_agent_{agent_id}"
            )
            button.callback = self._on_agent_select
            self.add_item(button)
        
        # Add control buttons
        select_all_btn = discord.ui.Button(
            label="Select All",
            style=discord.ButtonStyle.success,
            custom_id="select_all_agents"
        )
        select_all_btn.callback = self._on_select_all
        self.add_item(select_all_btn)
        
        confirm_btn = discord.ui.Button(
            label="Confirm Selection",
            style=discord.ButtonStyle.primary,
            custom_id="confirm_agent_selection"
        )
        confirm_btn.callback = self._on_confirm
        self.add_item(confirm_btn)
    
    async def _on_agent_select(self, interaction: discord.Interaction):
        """Handle individual agent selection."""
        custom_id = interaction.data.get('custom_id', '')
        agent_id = custom_id.replace('select_agent_', '')
        
        if agent_id in self.selected_agents:
            self.selected_agents.remove(agent_id)
            status = "❌"
        else:
            self.selected_agents.append(agent_id)
            status = "✅"
        
        # Update button label
        for item in self.children:
            if item.custom_id == custom_id:
                item.label = f"{status} {agent_id}"
                break
        
        await interaction.response.edit_message(view=self)
    
    async def _on_select_all(self, interaction: discord.Interaction):
        """Handle select all agents."""
        self.selected_agents = list(self.bot.agent_coordinates.keys())
        
        # Update all agent buttons
        for item in self.children:
            if item.custom_id and item.custom_id.startswith('select_agent_'):
                agent_id = item.custom_id.replace('select_agent_', '')
                item.label = f"✅ {agent_id}"
        
        await interaction.response.edit_message(view=self)
    
    async def _on_confirm(self, interaction: discord.Interaction):
        """Handle confirmation."""
        if not self.selected_agents:
            await interaction.response.send_message(
                "❌ Please select at least one agent.",
                ephemeral=True
            )
            return
        
        await self.callback(interaction, self.selected_agents)


class PrioritySelectionView(discord.ui.View):
    """View for selecting message priority."""
    
    def __init__(self, callback: Callable, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.callback = callback
        self.selected_priority = "NORMAL"
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup priority selection buttons."""
        priorities = [
            ("🟢 NORMAL", "NORMAL", discord.ButtonStyle.secondary),
            ("🟡 HIGH", "HIGH", discord.ButtonStyle.warning),
            ("🔴 URGENT", "URGENT", discord.ButtonStyle.danger),
            ("⚪ LOW", "LOW", discord.ButtonStyle.secondary)
        ]
        
        for label, priority, style in priorities:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"priority_{priority}"
            )
            button.callback = self._on_priority_select
            self.add_item(button)
        
        confirm_btn = discord.ui.Button(
            label="Confirm Priority",
            style=discord.ButtonStyle.primary,
            custom_id="confirm_priority"
        )
        confirm_btn.callback = self._on_confirm
        self.add_item(confirm_btn)
    
    async def _on_priority_select(self, interaction: discord.Interaction):
        """Handle priority selection."""
        custom_id = interaction.data.get('custom_id', '')
        priority = custom_id.replace('priority_', '')
        self.selected_priority = priority
        
        # Update button styles
        for item in self.children:
            if item.custom_id and item.custom_id.startswith('priority_'):
                if item.custom_id == custom_id:
                    item.style = discord.ButtonStyle.primary
                else:
                    item.style = discord.ButtonStyle.secondary
        
        await interaction.response.edit_message(view=self)
    
    async def _on_confirm(self, interaction: discord.Interaction):
        """Handle confirmation."""
        await self.callback(interaction, self.selected_priority)


class MessageTypeSelectionView(discord.ui.View):
    """View for selecting message type."""
    
    def __init__(self, callback: Callable, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.callback = callback
        self.selected_type = "direct"
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup message type selection buttons."""
        types = [
            ("📨 Direct", "direct", discord.ButtonStyle.secondary),
            ("📢 Broadcast", "broadcast", discord.ButtonStyle.secondary),
            ("⚙️ System", "system", discord.ButtonStyle.secondary)
        ]
        
        for label, msg_type, style in types:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"type_{msg_type}"
            )
            button.callback = self._on_type_select
            self.add_item(button)
        
        confirm_btn = discord.ui.Button(
            label="Confirm Type",
            style=discord.ButtonStyle.primary,
            custom_id="confirm_type"
        )
        confirm_btn.callback = self._on_confirm
        self.add_item(confirm_btn)
    
    async def _on_type_select(self, interaction: discord.Interaction):
        """Handle message type selection."""
        custom_id = interaction.data.get('custom_id', '')
        msg_type = custom_id.replace('type_', '')
        self.selected_type = msg_type
        
        # Update button styles
        for item in self.children:
            if item.custom_id and item.custom_id.startswith('type_'):
                if item.custom_id == custom_id:
                    item.style = discord.ButtonStyle.primary
                else:
                    item.style = discord.ButtonStyle.secondary
        
        await interaction.response.edit_message(view=self)
    
    async def _on_confirm(self, interaction: discord.Interaction):
        """Handle confirmation."""
        await self.callback(interaction, self.selected_type)


class QuickActionView(discord.ui.View):
    """View for quick actions and shortcuts."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup quick action buttons."""
        actions = [
            ("📊 Status", "quick_status", discord.ButtonStyle.info),
            ("👥 Agents", "quick_agents", discord.ButtonStyle.info),
            ("📝 Devlog", "quick_devlog", discord.ButtonStyle.secondary),
            ("🚀 Onboard All", "quick_onboard", discord.ButtonStyle.success),
            ("📢 Broadcast", "quick_broadcast", discord.ButtonStyle.warning),
            ("📋 Help", "quick_help", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"quick_{action_id}"
            )
            button.callback = self._on_quick_action
            self.add_item(button)
    
    async def _on_quick_action(self, interaction: discord.Interaction):
        """Handle quick action button clicks."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('quick_', '')
        
        if action == "status":
            await self._show_status(interaction)
        elif action == "agents":
            await self._show_agents(interaction)
        elif action == "devlog":
            await self._show_devlog_options(interaction)
        elif action == "onboard":
            await self._show_onboard_options(interaction)
        elif action == "broadcast":
            await self._show_broadcast_options(interaction)
        elif action == "help":
            await self._show_help(interaction)
    
    async def _show_status(self, interaction: discord.Interaction):
        """Show system status."""
        status_text = f"""
**V2_SWARM System Status:**

**Bot:** {self.bot.user.name} | **Latency:** {round(self.bot.latency * 1000)}ms
**Agents:** {len(self.bot.agent_coordinates)} configured
**Active:** {len([a for a in self.bot.agent_coordinates.values() if a.get('active', True)])}

🐝 **System Ready!**
        """
        await interaction.response.send_message(status_text, ephemeral=True)
    
    async def _show_agents(self, interaction: discord.Interaction):
        """Show agent list."""
        agent_list = "**V2_SWARM Agents:**\n\n"
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            coords = self.bot.agent_coordinates.get(agent_id, {})
            status = "🟢" if coords.get('active', True) else "🔴"
            agent_list += f"{status} **{agent_id}**\n"
        
        await interaction.response.send_message(agent_list, ephemeral=True)
    
    async def _show_devlog_options(self, interaction: discord.Interaction):
        """Show devlog options."""
        embed = discord.Embed(
            title="📝 Devlog Options",
            description="Choose a devlog action:",
            color=0xff8c00
        )
        
        view = DevlogActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_onboard_options(self, interaction: discord.Interaction):
        """Show onboarding options."""
        embed = discord.Embed(
            title="🚀 Onboarding Options",
            description="Choose an onboarding action:",
            color=0x00ff00
        )
        
        view = OnboardingActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_broadcast_options(self, interaction: discord.Interaction):
        """Show broadcast options."""
        embed = discord.Embed(
            title="📢 Broadcast Options",
            description="Choose a broadcast action:",
            color=0xffff00
        )
        
        view = BroadcastActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_help(self, interaction: discord.Interaction):
        """Show help information."""
        help_text = """
**V2_SWARM Discord Commander Help:**

**Quick Actions:** Use the buttons above for common tasks
**Slash Commands:** Use `/commands` for full command list
**Interactive UI:** All major actions have interactive interfaces

🐝 **Ready for swarm coordination!**
        """
        await interaction.response.send_message(help_text, ephemeral=True)


class DevlogActionView(discord.ui.View):
    """View for devlog actions."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup devlog action buttons."""
        actions = [
            ("📝 Create Devlog", "create_devlog", discord.ButtonStyle.primary),
            ("🤖 Agent Devlog", "agent_devlog", discord.ButtonStyle.secondary),
            ("🧪 Test Devlog", "test_devlog", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"devlog_{action_id}"
            )
            button.callback = self._on_devlog_action
            self.add_item(button)
    
    async def _on_devlog_action(self, interaction: discord.Interaction):
        """Handle devlog action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('devlog_', '')
        
        if action == "create_devlog":
            await self._show_create_devlog_modal(interaction)
        elif action == "agent_devlog":
            await self._show_agent_devlog_options(interaction)
        elif action == "test_devlog":
            await self._test_devlog(interaction)
    
    async def _show_create_devlog_modal(self, interaction: discord.Interaction):
        """Show create devlog modal."""
        modal = DevlogCreateModal(self.bot)
        await interaction.response.send_modal(modal)
    
    async def _show_agent_devlog_options(self, interaction: discord.Interaction):
        """Show agent devlog options."""
        embed = discord.Embed(
            title="🤖 Agent Devlog",
            description="Select an agent for devlog creation:",
            color=0xff8c00
        )
        
        view = AgentSelectionView(self.bot, self._on_agent_selected_for_devlog)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _test_devlog(self, interaction: discord.Interaction):
        """Test devlog functionality."""
        try:
            filepath = self.bot.devlog_service.create_devlog(
                agent_id="Discord-Commander",
                action="Discord bot devlog test",
                status="completed",
                details={"source": "discord_test", "channel": interaction.channel.name}
            )
            
            success = self.bot.devlog_service.post_devlog_to_discord(filepath)
            
            if success:
                await interaction.response.send_message(
                    f"✅ **Test Devlog Success!**\n📄 File: `{filepath}`\n🐝 Devlog system is working!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"✅ **Test Devlog Created!**\n📄 File: `{filepath}`\n⚠️ Failed to post to Discord",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Test devlog failed: {e}",
                ephemeral=True
            )
    
    async def _on_agent_selected_for_devlog(self, interaction: discord.Interaction, selected_agents: List[str]):
        """Handle agent selection for devlog."""
        if len(selected_agents) == 1:
            agent = selected_agents[0]
            modal = AgentDevlogCreateModal(self.bot, agent)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(
                "❌ Please select exactly one agent for devlog creation.",
                ephemeral=True
            )


class OnboardingActionView(discord.ui.View):
    """View for onboarding actions."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup onboarding action buttons."""
        actions = [
            ("🚀 Onboard All", "onboard_all", discord.ButtonStyle.success),
            ("🤖 Onboard Agent", "onboard_agent", discord.ButtonStyle.primary),
            ("📊 Check Status", "check_status", discord.ButtonStyle.info),
            ("ℹ️ Info", "info", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"onboard_{action_id}"
            )
            button.callback = self._on_onboarding_action
            self.add_item(button)
    
    async def _on_onboarding_action(self, interaction: discord.Interaction):
        """Handle onboarding action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('onboard_', '')
        
        if action == "onboard_all":
            await self._onboard_all_agents(interaction)
        elif action == "onboard_agent":
            await self._show_agent_selection(interaction)
        elif action == "check_status":
            await self._check_onboarding_status(interaction)
        elif action == "info":
            await self._show_onboarding_info(interaction)
    
    async def _onboard_all_agents(self, interaction: discord.Interaction):
        """Onboard all agents."""
        try:
            from src.services.messaging.service import MessagingService
            from src.services.messaging.onboarding.onboarding_service import OnboardingService
            
            messaging_service = MessagingService(dry_run=False)
            onboarding_service = OnboardingService(messaging_service)
            
            results = onboarding_service.hard_onboard_all_agents()
            
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"🚀 **Mass Agent Onboarding Initiated!**\n\n"
            response += f"**Agents Processed:** {successful}/{total}\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully onboarded!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to onboard**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Mass onboarding completed!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error onboarding all agents: {e}",
                ephemeral=True
            )
    
    async def _show_agent_selection(self, interaction: discord.Interaction):
        """Show agent selection for onboarding."""
        embed = discord.Embed(
            title="🤖 Select Agent to Onboard",
            description="Choose an agent to onboard:",
            color=0x00ff00
        )
        
        view = AgentSelectionView(self.bot, self._on_agent_selected_for_onboarding)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _check_onboarding_status(self, interaction: discord.Interaction):
        """Check onboarding status."""
        try:
            from src.services.messaging.service import MessagingService
            
            messaging_service = MessagingService(dry_run=False)
            
            response = "📋 **Onboarding Status for All Agents:**\n\n"
            
            for agent_id in self.bot.agent_coordinates.keys():
                messages = messaging_service.show_message_history(agent_id)
                onboarding_messages = [msg for msg in messages if "ONBOARDING COMPLETE" in msg.content]
                
                if onboarding_messages:
                    latest_onboarding = onboarding_messages[-1]
                    response += f"✅ **{agent_id}** - Onboarded ({latest_onboarding.timestamp})\n"
                else:
                    response += f"❌ **{agent_id}** - Not onboarded\n"
            
            response += "\n🐝 **WE ARE SWARM** - Onboarding status retrieved!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error checking onboarding status: {e}",
                ephemeral=True
            )
    
    async def _show_onboarding_info(self, interaction: discord.Interaction):
        """Show onboarding information."""
        response = "📚 **Agent Onboarding Information:**\n\n"
        response += "**What is Onboarding?**\n"
        response += "Onboarding introduces new agents to the V2_SWARM system.\n\n"
        response += "**Available Commands:**\n"
        response += "• `/onboard-agent` - Onboard a specific agent\n"
        response += "• `/onboard-all` - Onboard all agents\n"
        response += "• `/onboarding-status` - Check onboarding status\n\n"
        response += "🐝 **WE ARE SWARM** - Onboarding system ready!"
        
        await interaction.response.send_message(response, ephemeral=True)
    
    async def _on_agent_selected_for_onboarding(self, interaction: discord.Interaction, selected_agents: List[str]):
        """Handle agent selection for onboarding."""
        if len(selected_agents) == 1:
            agent = selected_agents[0]
            await self._onboard_single_agent(interaction, agent)
        else:
            await interaction.response.send_message(
                "❌ Please select exactly one agent for onboarding.",
                ephemeral=True
            )
    
    async def _onboard_single_agent(self, interaction: discord.Interaction, agent: str):
        """Onboard a single agent."""
        try:
            from src.services.messaging.service import MessagingService
            from src.services.messaging.onboarding.onboarding_service import OnboardingService
            
            messaging_service = MessagingService(dry_run=False)
            onboarding_service = OnboardingService(messaging_service)
            
            success = onboarding_service.hard_onboard_agent(agent)
            
            if success:
                response = f"🚀 **Agent Onboarding Initiated!**\n\n"
                response += f"**Agent:** {agent}\n"
                response += f"**Status:** ✅ Onboarding sequence started\n\n"
                response += "🐝 **WE ARE SWARM** - Agent onboarding in progress!"
            else:
                response = f"❌ **Failed to onboard agent {agent}**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error onboarding agent: {e}",
                ephemeral=True
            )


class BroadcastActionView(discord.ui.View):
    """View for broadcast actions."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup broadcast action buttons."""
        actions = [
            ("📢 Quick Broadcast", "quick_broadcast", discord.ButtonStyle.primary),
            ("⚙️ Advanced Broadcast", "advanced_broadcast", discord.ButtonStyle.secondary),
            ("📊 Broadcast Status", "broadcast_status", discord.ButtonStyle.info)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"broadcast_{action_id}"
            )
            button.callback = self._on_broadcast_action
            self.add_item(button)
    
    async def _on_broadcast_action(self, interaction: discord.Interaction):
        """Handle broadcast action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('broadcast_', '')
        
        if action == "quick_broadcast":
            await self._show_quick_broadcast_modal(interaction)
        elif action == "advanced_broadcast":
            await self._show_advanced_broadcast_options(interaction)
        elif action == "broadcast_status":
            await self._show_broadcast_status(interaction)
    
    async def _show_quick_broadcast_modal(self, interaction: discord.Interaction):
        """Show quick broadcast modal."""
        modal = QuickBroadcastModal(self.bot)
        await interaction.response.send_modal(modal)
    
    async def _show_advanced_broadcast_options(self, interaction: discord.Interaction):
        """Show advanced broadcast options."""
        embed = discord.Embed(
            title="⚙️ Advanced Broadcast",
            description="Configure your broadcast message:",
            color=0xffff00
        )
        
        view = AdvancedBroadcastView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_broadcast_status(self, interaction: discord.Interaction):
        """Show broadcast status."""
        try:
            if not self.bot.messaging_service:
                await interaction.response.send_message(
                    "❌ Messaging service not available",
                    ephemeral=True
                )
                return
            
            status = self.bot.messaging_service.get_status()
            
            response = "**V2_SWARM Messaging System Status:**\n\n"
            response += f"**Service Status:** ✅ Active\n"
            response += f"**Total Agents:** {len(self.bot.agent_coordinates)}\n"
            response += f"**Active Agents:** {len([a for a in self.bot.agent_coordinates.values() if a.get('active', True)])}\n\n"
            response += "🐝 **WE ARE SWARM** - Messaging system ready!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error getting broadcast status: {e}",
                ephemeral=True
            )


class AdvancedBroadcastView(discord.ui.View):
    """View for advanced broadcast configuration."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.message = ""
        self.priority = "NORMAL"
        self.sender = "Discord-Commander"
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup advanced broadcast buttons."""
        # Priority selection
        priority_btn = discord.ui.Button(
            label=f"Priority: {self.priority}",
            style=discord.ButtonStyle.secondary,
            custom_id="select_priority"
        )
        priority_btn.callback = self._on_select_priority
        self.add_item(priority_btn)
        
        # Sender configuration
        sender_btn = discord.ui.Button(
            label=f"Sender: {self.sender}",
            style=discord.ButtonStyle.secondary,
            custom_id="configure_sender"
        )
        sender_btn.callback = self._on_configure_sender
        self.add_item(sender_btn)
        
        # Message input
        message_btn = discord.ui.Button(
            label="Enter Message",
            style=discord.ButtonStyle.primary,
            custom_id="enter_message"
        )
        message_btn.callback = self._on_enter_message
        self.add_item(message_btn)
        
        # Send broadcast
        send_btn = discord.ui.Button(
            label="Send Broadcast",
            style=discord.ButtonStyle.success,
            custom_id="send_broadcast"
        )
        send_btn.callback = self._on_send_broadcast
        self.add_item(send_btn)
    
    async def _on_select_priority(self, interaction: discord.Interaction):
        """Handle priority selection."""
        view = PrioritySelectionView(self._on_priority_selected)
        await interaction.response.send_message(
            "Select message priority:",
            view=view,
            ephemeral=True
        )
    
    async def _on_configure_sender(self, interaction: discord.Interaction):
        """Handle sender configuration."""
        modal = SenderConfigModal(self._on_sender_configured)
        await interaction.response.send_modal(modal)
    
    async def _on_enter_message(self, interaction: discord.Interaction):
        """Handle message input."""
        modal = MessageInputModal(self._on_message_entered)
        await interaction.response.send_modal(modal)
    
    async def _on_send_broadcast(self, interaction: discord.Interaction):
        """Handle broadcast sending."""
        if not self.message:
            await interaction.response.send_message(
                "❌ Please enter a message first.",
                ephemeral=True
            )
            return
        
        try:
            results = self.bot.messaging_service.broadcast_message(
                self.message, self.sender, self.priority
            )
            
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📢 **Advanced Broadcast Sent!**\n\n"
            response += f"**Message:** {self.message}\n"
            response += f"**Priority:** {self.priority}\n"
            response += f"**Sender:** {self.sender}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive broadcast**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Advanced broadcast delivered!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending advanced broadcast: {e}",
                ephemeral=True
            )
    
    async def _on_priority_selected(self, interaction: discord.Interaction, priority: str):
        """Handle priority selection callback."""
        self.priority = priority
        # Update the priority button label
        for item in self.children:
            if item.custom_id == "select_priority":
                item.label = f"Priority: {priority}"
                break
        
        await interaction.response.edit_message(view=self)
    
    async def _on_sender_configured(self, interaction: discord.Interaction, sender: str):
        """Handle sender configuration callback."""
        self.sender = sender
        # Update the sender button label
        for item in self.children:
            if item.custom_id == "configure_sender":
                item.label = f"Sender: {sender}"
                break
        
        await interaction.response.edit_message(view=self)
    
    async def _on_message_entered(self, interaction: discord.Interaction, message: str):
        """Handle message input callback."""
        self.message = message
        # Update the message button label
        for item in self.children:
            if item.custom_id == "enter_message":
                item.label = f"Message: {message[:20]}{'...' if len(message) > 20 else ''}"
                break
        
        await interaction.response.edit_message(view=self)