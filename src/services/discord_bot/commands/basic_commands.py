#!/usr/bin/env python3
"""
Basic Discord Commands
======================

Basic slash commands for Discord bot.
"""

import discord
from discord import app_commands


def setup_basic_commands(bot):
    """Setup basic bot slash commands."""

    @bot.tree.command(name="ping", description="Test bot responsiveness")
    async def ping(interaction: discord.Interaction):
        """Test bot responsiveness."""
        latency = round(bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

    @bot.tree.command(name="commands", description="Show help information")
    async def help_command(interaction: discord.Interaction):
        """Show help information."""
        help_text = """
**V2_SWARM Enhanced Discord Agent Bot Commands:**

**Basic Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show this help message
- `/swarm-help` - Show this help message (alias)
- `/status` - Show system status

**Agent Commands:**
- `/agents` - List all agents and their status
- `/agent-channels` - List agent-specific Discord channels
- `/swarm` - Send message to all agents

**Devlog Commands:**
- `/devlog` - Create devlog entry (main channel)
- `/agent-devlog` - Create devlog for specific agent
- `/test-devlog` - Test devlog functionality

**Messaging Commands:**
- `/send` - Enhanced agent messaging interface with priority and type options
- `/send-help` - Show comprehensive agent messaging help
- `/list-agents` - List all available agents with detailed status
- `/broadcast` - Send message to all active agents
- `/msg-status` - Get messaging system status
- `/message-history` - View message history for agents
- `/system-status` - Get comprehensive messaging system status
- `/send-advanced` - Send message with advanced options
- `/broadcast-advanced` - Broadcast message with advanced options

**Onboarding Commands:**
- `/onboard-agent` - Onboard a specific agent
- `/onboard-all` - Onboard all agents
- `/onboarding-status` - Check onboarding status for agents
- `/onboarding-info` - Get information about the onboarding process

**Project Update Commands:**
- `/project-update` - Send project update to all agents
- `/milestone` - Send milestone completion notification
- `/system-status` - Send system status update
- `/v2-compliance` - Send V2 compliance update
- `/doc-cleanup` - Send documentation cleanup update
- `/feature-announce` - Send feature announcement
- `/update-history` - View project update history
- `/update-stats` - View project update statistics

**System Commands:**
- `/info` - Show bot information

**Usage Examples:**
- `/swarm message:All agents report status`
- `/devlog action:Tools cleanup completed`
- `/agent-devlog agent:Agent-4 action:Mission completed successfully`
- `/send agent:Agent-1 message:Hello from Discord priority:NORMAL message_type:DIRECT`
- `/send agent:Agent-4 message:Status report priority:HIGH message_type:SYSTEM`
- `/send agent:Agent-7 message:Emergency alert priority:URGENT message_type:EMERGENCY`
- `/send-help` - Show comprehensive agent messaging help
- `/list-agents` - List all available agents with status
- `/broadcast message:System maintenance priority:HIGH`
- `/broadcast-advanced message:System maintenance in 1 hour priority:HIGH`
- `/message-history agent:Agent-1 limit:5`
- `/list-agents`
- `/onboard-agent agent:Agent-1 dry_run:false`
- `/onboard-all dry_run:true`
- `/onboarding-status agent:Agent-1`
- `/project-update update_type:milestone title:V2 Compliance Complete description:All agents now V2 compliant`
- `/milestone name:Documentation Cleanup completion:100 description:Removed 13 redundant files`
- `/system-status system:Messaging Service status:Operational details:All systems green`
- `/v2-compliance status:Compliant files_checked:150 violations:0 details:All files under 400 lines`
- `/msg-status`
- `/agent-channels`

**Ready for enhanced swarm coordination!** 🐝
        """
        await interaction.response.send_message(help_text)

    @bot.tree.command(name="swarm-help", description="Show help information")
    async def help_command_simple(interaction: discord.Interaction):
        """Show help information."""
        help_text = """
**V2_SWARM Enhanced Discord Agent Bot Commands:**

**Basic Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show this help message
- `/swarm-help` - Show this help message (alias)
- `/status` - Show system status

**Agent Commands:**
- `/agents` - List all agents and their status
- `/agent-channels` - List agent-specific Discord channels
- `/swarm` - Send message to all agents

**Devlog Commands:**
- `/devlog` - Create devlog entry (main channel)
- `/agent-devlog` - Create devlog for specific agent
- `/test-devlog` - Test devlog functionality

**Messaging Commands:**
- `/send` - Enhanced agent messaging interface with priority and type options
- `/send-help` - Show comprehensive agent messaging help
- `/list-agents` - List all available agents with detailed status
- `/broadcast` - Send message to all active agents
- `/msg-status` - Get messaging system status
- `/message-history` - View message history for agents
- `/system-status` - Get comprehensive messaging system status
- `/send-advanced` - Send message with advanced options
- `/broadcast-advanced` - Broadcast message with advanced options

**Onboarding Commands:**
- `/onboard-agent` - Onboard a specific agent
- `/onboard-all` - Onboard all agents
- `/onboarding-status` - Check onboarding status for agents
- `/onboarding-info` - Get information about the onboarding process

**Project Update Commands:**
- `/project-update` - Send project update to all agents
- `/milestone` - Send milestone completion notification
- `/system-status` - Send system status update
- `/v2-compliance` - Send V2 compliance update
- `/doc-cleanup` - Send documentation cleanup update
- `/feature-announce` - Send feature announcement
- `/update-history` - View project update history
- `/update-stats` - View project update statistics

**System Commands:**
- `/info` - Show bot information

**Usage Examples:**
- `/swarm message:All agents report status`
- `/devlog action:Tools cleanup completed`
- `/agent-devlog agent:Agent-4 action:Mission completed successfully`
- `/send agent:Agent-1 message:Hello from Discord priority:NORMAL message_type:DIRECT`
- `/send agent:Agent-4 message:Status report priority:HIGH message_type:SYSTEM`
- `/send agent:Agent-7 message:Emergency alert priority:URGENT message_type:EMERGENCY`
- `/send-help` - Show comprehensive agent messaging help
- `/list-agents` - List all available agents with status
- `/broadcast message:System maintenance priority:HIGH`
- `/broadcast-advanced message:System maintenance in 1 hour priority:HIGH`
- `/message-history agent:Agent-1 limit:5`
- `/list-agents`
- `/onboard-agent agent:Agent-1 dry_run:false`
- `/onboard-all dry_run:true`
- `/onboarding-status agent:Agent-1`
- `/project-update update_type:milestone title:V2 Compliance Complete description:All agents now V2 compliant`
- `/milestone name:Documentation Cleanup completion:100 description:Removed 13 redundant files`
- `/system-status system:Messaging Service status:Operational details:All systems green`
- `/v2-compliance status:Compliant files_checked:150 violations:0 details:All files under 400 lines`
- `/msg-status`
- `/agent-channels`

**Ready for enhanced swarm coordination!** 🐝
        """
        await interaction.response.send_message(help_text)

