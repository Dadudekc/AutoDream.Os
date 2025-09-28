#!/usr/bin/env python3
"""
Enhanced Discord Commander Commands
===================================

Enhanced commands with interactive UI views for better user experience.
"""

import discord
from discord import app_commands
from typing import Optional, List
import logging

from .command_views import (
    AgentSelectionView, PrioritySelectionView, MessageTypeSelectionView,
    QuickActionView, DevlogActionView, OnboardingActionView, BroadcastActionView
)
from .modals import (
    DevlogCreateModal, AgentDevlogCreateModal, QuickBroadcastModal,
    AgentMessageModal, ProjectUpdateModal, MilestoneModal
)

logger = logging.getLogger(__name__)


def setup_enhanced_commands(bot):
    """Setup enhanced commands with interactive UI."""
    
    @bot.tree.command(name="swarm-dashboard", description="Open the Swarm Commander Dashboard")
    async def swarm_dashboard(interaction: discord.Interaction):
        """Open the main swarm dashboard with quick actions."""
        embed = discord.Embed(
            title="🐝 V2_SWARM Commander Dashboard",
            description="**Welcome to the Swarm Commander!**\n\nUse the buttons below for quick access to all major functions.",
            color=0x9932cc
        )
        
        embed.add_field(
            name="📊 System Status",
            value=f"**Bot:** {bot.user.name} | **Latency:** {round(bot.latency * 1000)}ms\n**Agents:** {len(bot.agent_coordinates)} configured",
            inline=False
        )
        
        embed.add_field(
            name="🚀 Quick Actions",
            value="Use the buttons below to access all major functions instantly!",
            inline=False
        )
        
        embed.set_footer(text="🐝 WE ARE SWARM - Ready for coordination!")
        
        view = QuickActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="interactive-send", description="Send message to agents with interactive UI")
    async def interactive_send(interaction: discord.Interaction):
        """Send message to agents with interactive selection."""
        embed = discord.Embed(
            title="📨 Interactive Message Sender",
            description="**Select agents to send a message to:**\n\nUse the buttons below to choose recipients, then configure your message.",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📋 Instructions",
            value="1. Select one or more agents\n2. Choose message priority\n3. Enter your message\n4. Send!",
            inline=False
        )
        
        view = AgentSelectionView(bot, _on_agents_selected_for_message)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="interactive-devlog", description="Create devlog with interactive UI")
    async def interactive_devlog(interaction: discord.Interaction):
        """Create devlog with interactive options."""
        embed = discord.Embed(
            title="📝 Interactive Devlog Creator",
            description="**Choose your devlog action:**\n\nSelect from the options below to create devlog entries.",
            color=0xff8c00
        )
        
        embed.add_field(
            name="📋 Available Actions",
            value="• **Create Devlog** - General devlog entry\n• **Agent Devlog** - Agent-specific entry\n• **Test Devlog** - Test functionality",
            inline=False
        )
        
        view = DevlogActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="interactive-onboarding", description="Onboard agents with interactive UI")
    async def interactive_onboarding(interaction: discord.Interaction):
        """Onboard agents with interactive options."""
        embed = discord.Embed(
            title="🚀 Interactive Agent Onboarding",
            description="**Choose your onboarding action:**\n\nSelect from the options below to onboard agents.",
            color=0x00ff00
        )
        
        embed.add_field(
            name="📋 Available Actions",
            value="• **Onboard All** - Onboard all agents\n• **Onboard Agent** - Onboard specific agent\n• **Check Status** - View onboarding status\n• **Info** - Learn about onboarding",
            inline=False
        )
        
        view = OnboardingActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="interactive-broadcast", description="Broadcast messages with interactive UI")
    async def interactive_broadcast(interaction: discord.Interaction):
        """Broadcast messages with interactive options."""
        embed = discord.Embed(
            title="📢 Interactive Broadcast System",
            description="**Choose your broadcast action:**\n\nSelect from the options below to broadcast messages.",
            color=0xffff00
        )
        
        embed.add_field(
            name="📋 Available Actions",
            value="• **Quick Broadcast** - Simple message broadcast\n• **Advanced Broadcast** - Configured broadcast\n• **Broadcast Status** - Check system status",
            inline=False
        )
        
        view = BroadcastActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="interactive-project-update", description="Create project updates with interactive UI")
    async def interactive_project_update(interaction: discord.Interaction):
        """Create project updates with interactive options."""
        embed = discord.Embed(
            title="📋 Interactive Project Update Creator",
            description="**Choose your project update type:**\n\nSelect from the options below to create project updates.",
            color=0x4169e1
        )
        
        embed.add_field(
            name="📋 Available Types",
            value="• **General Update** - Standard project update\n• **Milestone** - Milestone completion\n• **System Status** - System status update\n• **V2 Compliance** - Compliance update\n• **Documentation** - Documentation update\n• **Feature Announce** - Feature announcement",
            inline=False
        )
        
        view = ProjectUpdateActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)
    
    @bot.tree.command(name="agent-quick-message", description="Quick message to specific agent")
    @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
    async def agent_quick_message(interaction: discord.Interaction, agent: str):
        """Quick message to specific agent with modal."""
        # Validate agent ID
        if agent not in bot.agent_coordinates:
            await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
            return
        
        modal = AgentMessageModal(bot, agent)
        await interaction.response.send_modal(modal)
    
    @bot.tree.command(name="quick-devlog", description="Quick devlog creation")
    async def quick_devlog(interaction: discord.Interaction):
        """Quick devlog creation with modal."""
        modal = DevlogCreateModal(bot)
        await interaction.response.send_modal(modal)
    
    @bot.tree.command(name="quick-broadcast", description="Quick broadcast message")
    async def quick_broadcast(interaction: discord.Interaction):
        """Quick broadcast with modal."""
        modal = QuickBroadcastModal(bot)
        await interaction.response.send_modal(modal)
    
    @bot.tree.command(name="quick-project-update", description="Quick project update creation")
    async def quick_project_update(interaction: discord.Interaction):
        """Quick project update with modal."""
        modal = ProjectUpdateModal(bot)
        await interaction.response.send_modal(modal)
    
    @bot.tree.command(name="quick-milestone", description="Quick milestone notification")
    async def quick_milestone(interaction: discord.Interaction):
        """Quick milestone with modal."""
        modal = MilestoneModal(bot)
        await interaction.response.send_modal(modal)


async def _on_agents_selected_for_message(interaction: discord.Interaction, selected_agents: List[str]):
    """Handle agent selection for message sending."""
    if len(selected_agents) == 1:
        # Single agent - show message modal
        agent = selected_agents[0]
        modal = AgentMessageModal(interaction.client, agent)
        await interaction.response.send_modal(modal)
    else:
        # Multiple agents - show broadcast options
        embed = discord.Embed(
            title="📢 Multiple Agents Selected",
            description=f"**Selected Agents:** {', '.join(selected_agents)}\n\nChoose how to send your message:",
            color=0xffff00
        )
        
        view = MultipleAgentMessageView(interaction.client, selected_agents)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class ProjectUpdateActionView(discord.ui.View):
    """View for project update actions."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup project update action buttons."""
        actions = [
            ("📋 General Update", "general_update", discord.ButtonStyle.primary),
            ("🎯 Milestone", "milestone", discord.ButtonStyle.success),
            ("📊 System Status", "system_status", discord.ButtonStyle.info),
            ("📏 V2 Compliance", "v2_compliance", discord.ButtonStyle.secondary),
            ("📚 Documentation", "documentation", discord.ButtonStyle.secondary),
            ("🚀 Feature Announce", "feature_announce", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"project_{action_id}"
            )
            button.callback = self._on_project_action
            self.add_item(button)
    
    async def _on_project_action(self, interaction: discord.Interaction):
        """Handle project update action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('project_', '')
        
        if action == "general_update":
            modal = ProjectUpdateModal(self.bot)
            await interaction.response.send_modal(modal)
        elif action == "milestone":
            modal = MilestoneModal(self.bot)
            await interaction.response.send_modal(modal)
        elif action == "system_status":
            await self._show_system_status_modal(interaction)
        elif action == "v2_compliance":
            await self._show_v2_compliance_modal(interaction)
        elif action == "documentation":
            await self._show_documentation_modal(interaction)
        elif action == "feature_announce":
            await self._show_feature_announce_modal(interaction)
    
    async def _show_system_status_modal(self, interaction: discord.Interaction):
        """Show system status modal."""
        modal = SystemStatusModal(self.bot)
        await interaction.response.send_modal(modal)
    
    async def _show_v2_compliance_modal(self, interaction: discord.Interaction):
        """Show V2 compliance modal."""
        modal = V2ComplianceModal(self.bot)
        await interaction.response.send_modal(modal)
    
    async def _show_documentation_modal(self, interaction: discord.Interaction):
        """Show documentation modal."""
        modal = DocumentationModal(self.bot)
        await interaction.response.send_modal(modal)
    
    async def _show_feature_announce_modal(self, interaction: discord.Interaction):
        """Show feature announce modal."""
        modal = FeatureAnnounceModal(self.bot)
        await interaction.response.send_modal(modal)


class MultipleAgentMessageView(discord.ui.View):
    """View for handling messages to multiple agents."""
    
    def __init__(self, bot, selected_agents: List[str], timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.selected_agents = selected_agents
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup multiple agent message buttons."""
        actions = [
            ("📢 Broadcast to All", "broadcast_all", discord.ButtonStyle.primary),
            ("📨 Send Individually", "send_individual", discord.ButtonStyle.secondary),
            ("⚙️ Advanced Options", "advanced_options", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"multi_{action_id}"
            )
            button.callback = self._on_multi_action
            self.add_item(button)
    
    async def _on_multi_action(self, interaction: discord.Interaction):
        """Handle multiple agent action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('multi_', '')
        
        if action == "broadcast_all":
            modal = QuickBroadcastModal(self.bot)
            await interaction.response.send_modal(modal)
        elif action == "send_individual":
            await self._show_individual_message_modal(interaction)
        elif action == "advanced_options":
            await self._show_advanced_options(interaction)
    
    async def _show_individual_message_modal(self, interaction: discord.Interaction):
        """Show individual message modal."""
        modal = IndividualMessageModal(self.bot, self.selected_agents)
        await interaction.response.send_modal(modal)
    
    async def _show_advanced_options(self, interaction: discord.Interaction):
        """Show advanced options."""
        embed = discord.Embed(
            title="⚙️ Advanced Message Options",
            description="**Configure advanced message settings:**",
            color=0x9932cc
        )
        
        view = AdvancedMessageView(self.bot, self.selected_agents)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# Additional modal classes for project updates
class SystemStatusModal(discord.ui.Modal):
    """Modal for system status updates."""
    
    def __init__(self, bot):
        super().__init__(title="System Status Update")
        self.bot = bot
        
        self.system_input = discord.ui.TextInput(
            label="System Name",
            placeholder="Database, API, Web Server, etc.",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.system_input)
        
        self.status_input = discord.ui.TextInput(
            label="Status",
            placeholder="Operational, Down, Maintenance, etc.",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.status_input)
        
        self.details_input = discord.ui.TextInput(
            label="Status Details",
            placeholder="Detailed status information...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.details_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            system = self.system_input.value
            status = self.status_input.value
            details = self.details_input.value
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send system status update
            results = update_system.send_system_status_update(
                system_name=system,
                status=status,
                details=details
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            # Status emoji
            status_emoji = "✅" if status.lower() in ["operational", "online", "active"] else "⚠️" if status.lower() in ["maintenance", "degraded"] else "❌"
            
            response = f"📊 **System Status Update Sent!**\n\n"
            response += f"**System:** {system}\n"
            response += f"**Status:** {status_emoji} {status}\n"
            response += f"**Details:** {details}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🔧 **System status communicated to all agents!**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending system status update: {e}",
                ephemeral=True
            )


class V2ComplianceModal(discord.ui.Modal):
    """Modal for V2 compliance updates."""
    
    def __init__(self, bot):
        super().__init__(title="V2 Compliance Update")
        self.bot = bot
        
        self.status_input = discord.ui.TextInput(
            label="Compliance Status",
            placeholder="Compliant, Non-Compliant, etc.",
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        self.add_item(self.status_input)
        
        self.files_input = discord.ui.TextInput(
            label="Files Checked",
            placeholder="Number of files checked",
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        self.add_item(self.files_input)
        
        self.violations_input = discord.ui.TextInput(
            label="Violations Found",
            placeholder="Number of violations found",
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        self.add_item(self.violations_input)
        
        self.details_input = discord.ui.TextInput(
            label="Compliance Details",
            placeholder="Detailed compliance information...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.details_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            status = self.status_input.value
            files_checked = int(self.files_input.value)
            violations = int(self.violations_input.value)
            details = self.details_input.value
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send V2 compliance update
            results = update_system.send_v2_compliance_update(
                compliance_status=status,
                files_checked=files_checked,
                violations_found=violations,
                details=details
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            # Compliance emoji
            compliance_emoji = "✅" if violations == 0 else "⚠️" if violations < 5 else "❌"
            
            response = f"📏 **V2 Compliance Update Sent!**\n\n"
            response += f"**Status:** {compliance_emoji} {status}\n"
            response += f"**Files Checked:** {files_checked}\n"
            response += f"**Violations:** {violations}\n"
            response += f"**Details:** {details}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n📋 **V2 compliance status communicated to all agents!**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending V2 compliance update: {e}",
                ephemeral=True
            )


class DocumentationModal(discord.ui.Modal):
    """Modal for documentation updates."""
    
    def __init__(self, bot):
        super().__init__(title="Documentation Update")
        self.bot = bot
        
        self.files_removed_input = discord.ui.TextInput(
            label="Files Removed",
            placeholder="Number of files removed",
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        self.add_item(self.files_removed_input)
        
        self.files_kept_input = discord.ui.TextInput(
            label="Files Kept",
            placeholder="Number of files kept",
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        self.add_item(self.files_kept_input)
        
        self.summary_input = discord.ui.TextInput(
            label="Cleanup Summary",
            placeholder="Summary of documentation cleanup...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.summary_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            files_removed = int(self.files_removed_input.value)
            files_kept = int(self.files_kept_input.value)
            summary = self.summary_input.value
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send documentation cleanup update
            results = update_system.send_documentation_cleanup_update(
                files_removed=files_removed,
                files_kept=files_kept,
                cleanup_summary=summary
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📚 **Documentation Cleanup Update Sent!**\n\n"
            response += f"**Files Removed:** {files_removed}\n"
            response += f"**Files Kept:** {files_kept}\n"
            response += f"**Summary:** {summary}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive update**\n"
            
            response += "\n🧹 **Documentation cleanup communicated to all agents!**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending documentation cleanup update: {e}",
                ephemeral=True
            )


class FeatureAnnounceModal(discord.ui.Modal):
    """Modal for feature announcements."""
    
    def __init__(self, bot):
        super().__init__(title="Feature Announcement")
        self.bot = bot
        
        self.name_input = discord.ui.TextInput(
            label="Feature Name",
            placeholder="Name of the new feature...",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.name_input)
        
        self.description_input = discord.ui.TextInput(
            label="Feature Description",
            placeholder="Description of the feature...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )
        self.add_item(self.description_input)
        
        self.usage_input = discord.ui.TextInput(
            label="Usage Instructions (Optional)",
            placeholder="How to use the feature...",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=1000
        )
        self.add_item(self.usage_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            name = self.name_input.value
            description = self.description_input.value
            usage = self.usage_input.value or None
            
            # Initialize project update system
            from src.services.messaging.service import MessagingService
            from src.services.messaging.project_update_system import ProjectUpdateSystem
            
            messaging_service = MessagingService(dry_run=False)
            update_system = ProjectUpdateSystem(messaging_service)
            
            # Send feature announcement
            results = update_system.send_feature_announcement(
                feature_name=name,
                description=description,
                usage_instructions=usage
            )
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"🚀 **Feature Announcement Sent!**\n\n"
            response += f"**Feature:** {name}\n"
            response += f"**Description:** {description}\n"
            if usage:
                response += f"**Usage:** {usage}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive announcement**\n"
            
            response += "\n🎉 **New feature announced to all agents!**"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending feature announcement: {e}",
                ephemeral=True
            )


class IndividualMessageModal(discord.ui.Modal):
    """Modal for individual messages to multiple agents."""
    
    def __init__(self, bot, selected_agents: List[str]):
        super().__init__(title=f"Message to {len(selected_agents)} Agents")
        self.bot = bot
        self.selected_agents = selected_agents
        
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
            
            # Send messages to each agent
            results = {}
            for agent in self.selected_agents:
                success = self.bot.messaging_service.send_message(
                    agent, message, "Discord-Commander", priority
                )
                results[agent] = success
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📨 **Individual Messages Sent!**\n\n"
            response += f"**Message:** {message}\n"
            response += f"**Priority:** {priority}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive message**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Individual messages delivered!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending individual messages: {e}",
                ephemeral=True
            )


class AdvancedMessageView(discord.ui.View):
    """View for advanced message options."""
    
    def __init__(self, bot, selected_agents: List[str], timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.selected_agents = selected_agents
        self.message = ""
        self.priority = "NORMAL"
        self.sender = "Discord-Commander"
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup advanced message buttons."""
        # Message input
        message_btn = discord.ui.Button(
            label="Enter Message",
            style=discord.ButtonStyle.primary,
            custom_id="enter_message"
        )
        message_btn.callback = self._on_enter_message
        self.add_item(message_btn)
        
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
        
        # Send messages
        send_btn = discord.ui.Button(
            label="Send Messages",
            style=discord.ButtonStyle.success,
            custom_id="send_messages"
        )
        send_btn.callback = self._on_send_messages
        self.add_item(send_btn)
    
    async def _on_enter_message(self, interaction: discord.Interaction):
        """Handle message input."""
        modal = MessageInputModal(self._on_message_entered)
        await interaction.response.send_modal(modal)
    
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
    
    async def _on_send_messages(self, interaction: discord.Interaction):
        """Handle message sending."""
        if not self.message:
            await interaction.response.send_message(
                "❌ Please enter a message first.",
                ephemeral=True
            )
            return
        
        try:
            # Send messages to each agent
            results = {}
            for agent in self.selected_agents:
                success = self.bot.messaging_service.send_message(
                    agent, self.message, self.sender, self.priority
                )
                results[agent] = success
            
            # Format response
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            response = f"📨 **Advanced Messages Sent!**\n\n"
            response += f"**Message:** {self.message}\n"
            response += f"**Priority:** {self.priority}\n"
            response += f"**Sender:** {self.sender}\n"
            response += f"**Recipients:** {successful}/{total} agents notified\n\n"
            
            if successful == total:
                response += "✅ **All agents successfully notified!**\n"
            else:
                response += f"⚠️ **{total - successful} agents failed to receive message**\n"
            
            response += "\n🐝 **WE ARE SWARM** - Advanced messages delivered!"
            
            await interaction.response.send_message(response, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending advanced messages: {e}",
                ephemeral=True
            )
    
    async def _on_message_entered(self, interaction: discord.Interaction, message: str):
        """Handle message input callback."""
        self.message = message
        # Update the message button label
        for item in self.children:
            if item.custom_id == "enter_message":
                item.label = f"Message: {message[:20]}{'...' if len(message) > 20 else ''}"
                break
        
        await interaction.response.edit_message(view=self)
    
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