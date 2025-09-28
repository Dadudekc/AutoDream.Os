#!/usr/bin/env python3
"""
Discord Commander UI Integration
================================

Integration of all UI components for the Discord Commander.
"""

import discord
from discord import app_commands
import logging
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.services.discord_bot.ui.views.enhanced_commands import setup_enhanced_commands
from src.services.discord_bot.ui.views.command_views import QuickActionView
from src.services.discord_bot.ui.embed_builder import EmbedBuilder
from src.services.discord_bot.ui.embed_types import EmbedType

logger = logging.getLogger(__name__)


class DiscordCommanderUI:
    """Main UI manager for Discord Commander."""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_builder = EmbedBuilder()
    
    def setup_all_ui_commands(self):
        """Setup all UI-enhanced commands."""
        try:
            # Setup enhanced commands
            setup_enhanced_commands(self.bot)
            
            # Add UI integration to existing commands
            self._enhance_existing_commands()
            
            logger.info("✅ All UI commands setup successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup UI commands: {e}")
            raise
    
    def _enhance_existing_commands(self):
        """Enhance existing commands with UI options."""
        
        # Enhance the basic commands command
        @self.bot.tree.command(name="swarm-help", description="Show interactive help with UI options")
        async def swarm_help(interaction: discord.Interaction):
            """Show interactive help with UI options."""
            embed = self.embed_builder.create_embed({
                "title": "🐝 V2_SWARM Discord Commander Help",
                "description": "**Welcome to the Swarm Commander!**\n\nChoose your action below or use slash commands.",
                "embed_type": EmbedType.HELP,
                "fields": {
                    "🚀 Quick Actions": "Use the buttons below for instant access to all major functions",
                    "📋 Slash Commands": "Use `/commands` for the complete command list",
                    "🎯 Interactive UI": "All major actions have interactive interfaces for easy use"
                }
            })
            
            view = QuickActionView(self.bot)
            await interaction.response.send_message(embed=embed, view=view)
        
        # Enhance the status command
        @self.bot.tree.command(name="interactive-status", description="Show system status with interactive options")
        async def interactive_status(interaction: discord.Interaction):
            """Show system status with interactive options."""
            embed = self.embed_builder.create_embed({
                "title": "📊 V2_SWARM System Status",
                "description": "**Current system status and quick actions:**",
                "embed_type": EmbedType.SYSTEM_STATUS,
                "fields": {
                    "🤖 Bot Status": f"**Name:** {self.bot.user.name} | **Latency:** {round(self.bot.latency * 1000)}ms",
                    "👥 Agent Status": f"**Total:** {len(self.bot.agent_coordinates)} | **Active:** {len([a for a in self.bot.agent_coordinates.values() if a.get('active', True)])}",
                    "🔧 System Health": "✅ Discord Connected | ✅ Devlog Active | ✅ Messaging Active"
                }
            })
            
            view = SystemStatusView(self.bot)
            await interaction.response.send_message(embed=embed, view=view)
    
    def create_welcome_message(self, channel):
        """Create a welcome message with UI options."""
        embed = self.embed_builder.create_embed({
            "title": "🐝 V2_SWARM Commander Online",
            "description": "**Welcome to the Swarm Commander!**\n\nYour central hub for agent coordination and system management.",
            "embed_type": EmbedType.SUCCESS,
            "fields": {
                "🚀 Quick Start": "Use the buttons below to get started immediately",
                "📋 Commands": "Use `/commands` for the complete command list",
                "🎯 Interactive UI": "All major functions have interactive interfaces"
            },
            "footer": "🐝 WE ARE SWARM - Ready for coordination!"
        })
        
        view = QuickActionView(self.bot)
        return embed, view
    
    def create_agent_status_embed(self, agent_id: str, status: str, details: dict = None):
        """Create an agent status embed."""
        embed = self.embed_builder.create_agent_status_embed(
            agent_id=agent_id,
            status=status,
            fields=details or {}
        )
        
        return embed
    
    def create_system_status_embed(self, status_data: dict):
        """Create a system status embed."""
        embed = self.embed_builder.create_embed({
            "title": "📊 System Status Report",
            "description": "**Current system status and health metrics:**",
            "embed_type": EmbedType.SYSTEM_STATUS,
            "fields": status_data
        })
        
        return embed


class SystemStatusView(discord.ui.View):
    """View for system status with quick actions."""
    
    def __init__(self, bot, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.bot = bot
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Setup system status buttons."""
        actions = [
            ("👥 Agent Status", "agent_status", discord.ButtonStyle.info),
            ("📢 Broadcast", "broadcast", discord.ButtonStyle.warning),
            ("📝 Devlog", "devlog", discord.ButtonStyle.secondary),
            ("🚀 Onboard", "onboard", discord.ButtonStyle.success),
            ("📋 Project Update", "project_update", discord.ButtonStyle.primary),
            ("ℹ️ Help", "help", discord.ButtonStyle.secondary)
        ]
        
        for label, action_id, style in actions:
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=f"status_{action_id}"
            )
            button.callback = self._on_status_action
            self.add_item(button)
    
    async def _on_status_action(self, interaction: discord.Interaction):
        """Handle status action."""
        custom_id = interaction.data.get('custom_id', '')
        action = custom_id.replace('status_', '')
        
        if action == "agent_status":
            await self._show_agent_status(interaction)
        elif action == "broadcast":
            await self._show_broadcast_options(interaction)
        elif action == "devlog":
            await self._show_devlog_options(interaction)
        elif action == "onboard":
            await self._show_onboard_options(interaction)
        elif action == "project_update":
            await self._show_project_update_options(interaction)
        elif action == "help":
            await self._show_help(interaction)
    
    async def _show_agent_status(self, interaction: discord.Interaction):
        """Show agent status."""
        agent_list = "**V2_SWARM Agent Status:**\n\n"
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            coords = self.bot.agent_coordinates.get(agent_id, {})
            status = "🟢" if coords.get('active', True) else "🔴"
            agent_list += f"{status} **{agent_id}**\n"
        
        await interaction.response.send_message(agent_list, ephemeral=True)
    
    async def _show_broadcast_options(self, interaction: discord.Interaction):
        """Show broadcast options."""
        from src.services.discord_bot.ui.views.command_views import BroadcastActionView
        
        embed = discord.Embed(
            title="📢 Broadcast Options",
            description="Choose a broadcast action:",
            color=0xffff00
        )
        
        view = BroadcastActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_devlog_options(self, interaction: discord.Interaction):
        """Show devlog options."""
        from src.services.discord_bot.ui.views.command_views import DevlogActionView
        
        embed = discord.Embed(
            title="📝 Devlog Options",
            description="Choose a devlog action:",
            color=0xff8c00
        )
        
        view = DevlogActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_onboard_options(self, interaction: discord.Interaction):
        """Show onboarding options."""
        from src.services.discord_bot.ui.views.command_views import OnboardingActionView
        
        embed = discord.Embed(
            title="🚀 Onboarding Options",
            description="Choose an onboarding action:",
            color=0x00ff00
        )
        
        view = OnboardingActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_project_update_options(self, interaction: discord.Interaction):
        """Show project update options."""
        from src.services.discord_bot.ui.views.enhanced_commands import ProjectUpdateActionView
        
        embed = discord.Embed(
            title="📋 Project Update Options",
            description="Choose a project update type:",
            color=0x4169e1
        )
        
        view = ProjectUpdateActionView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _show_help(self, interaction: discord.Interaction):
        """Show help information."""
        help_text = """
**V2_SWARM Discord Commander Help:**

**Quick Actions:** Use the buttons above for common tasks
**Slash Commands:** Use `/commands` for full command list
**Interactive UI:** All major actions have interactive interfaces

**Available Commands:**
• `/swarm-dashboard` - Main dashboard
• `/interactive-send` - Send messages with UI
• `/interactive-devlog` - Create devlogs with UI
• `/interactive-onboarding` - Onboard agents with UI
• `/interactive-broadcast` - Broadcast with UI
• `/interactive-project-update` - Project updates with UI

🐝 **Ready for swarm coordination!**
        """
        await interaction.response.send_message(help_text, ephemeral=True)


def integrate_ui_with_bot(bot):
    """Integrate UI components with the Discord bot."""
    try:
        # Initialize UI manager
        ui_manager = DiscordCommanderUI(bot)
        
        # Setup all UI commands
        ui_manager.setup_all_ui_commands()
        
        # Store UI manager in bot for access
        bot.ui_manager = ui_manager
        
        logger.info("✅ Discord Commander UI integration complete")
        
        return ui_manager
        
    except Exception as e:
        logger.error(f"❌ Failed to integrate UI with bot: {e}")
        raise


def create_startup_ui_message(bot):
    """Create startup message with UI options."""
    ui_manager = getattr(bot, 'ui_manager', None)
    if not ui_manager:
        ui_manager = DiscordCommanderUI(bot)
    
    embed, view = ui_manager.create_welcome_message(None)
    return embed, view


def enhance_existing_command_responses(bot):
    """Enhance existing command responses with UI options."""
    
    # Override the existing commands command to include UI options
    @bot.tree.command(name="commands-ui", description="Show commands with interactive UI options")
    async def commands_ui(interaction: discord.Interaction):
        """Show commands with interactive UI options."""
        embed = discord.Embed(
            title="🐝 V2_SWARM Discord Commander Commands",
            description="**Complete command reference with interactive options:**",
            color=0x4169e1
        )
        
        embed.add_field(
            name="🚀 Interactive Commands",
            value="• `/swarm-dashboard` - Main dashboard\n• `/interactive-send` - Send messages with UI\n• `/interactive-devlog` - Create devlogs with UI\n• `/interactive-onboarding` - Onboard agents with UI\n• `/interactive-broadcast` - Broadcast with UI\n• `/interactive-project-update` - Project updates with UI",
            inline=False
        )
        
        embed.add_field(
            name="📋 Quick Commands",
            value="• `/quick-devlog` - Quick devlog creation\n• `/quick-broadcast` - Quick broadcast\n• `/quick-project-update` - Quick project update\n• `/quick-milestone` - Quick milestone\n• `/agent-quick-message` - Quick agent message",
            inline=False
        )
        
        embed.add_field(
            name="🔧 System Commands",
            value="• `/ping` - Test bot responsiveness\n• `/status` - System status\n• `/agents` - List agents\n• `/msg-status` - Messaging status\n• `/info` - Bot information",
            inline=False
        )
        
        embed.add_field(
            name="📝 Devlog Commands",
            value="• `/devlog` - Create devlog\n• `/agent-devlog` - Agent devlog\n• `/test-devlog` - Test devlog",
            inline=False
        )
        
        embed.add_field(
            name="🚀 Onboarding Commands",
            value="• `/onboard-agent` - Onboard agent\n• `/onboard-all` - Onboard all\n• `/onboarding-status` - Check status\n• `/onboarding-info` - Get info",
            inline=False
        )
        
        embed.add_field(
            name="📢 Messaging Commands",
            value="• `/send` - Send message\n• `/broadcast-advanced` - Advanced broadcast\n• `/message-history` - View history\n• `/swarm` - Swarm message",
            inline=False
        )
        
        embed.add_field(
            name="📋 Project Update Commands",
            value="• `/project-update` - General update\n• `/milestone` - Milestone notification\n• `/system-status` - System status\n• `/v2-compliance` - V2 compliance\n• `/doc-cleanup` - Documentation cleanup\n• `/feature-announce` - Feature announcement\n• `/update-history` - View history\n• `/update-stats` - View statistics",
            inline=False
        )
        
        embed.set_footer(text="🐝 WE ARE SWARM - Use interactive commands for better experience!")
        
        view = QuickActionView(bot)
        await interaction.response.send_message(embed=embed, view=view)