#!/usr/bin/env python3
"""
Discord Embeds - V2 Compliance Module
====================================

Discord embed generation utilities for V2_SWARM Discord Agent Bot.
Provides standardized embed creation for various command responses.

Features:
- Standardized embed formatting
- Color schemes for different states
- Rich embed components (fields, footers, timestamps)
- Error and success state handling

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

from datetime import datetime
from typing import Any

import discord


class EmbedBuilder:
    """Builder for Discord embeds with standardized formatting."""

    # Color scheme
    COLORS = {
        'primary': 0x3498db,      # Blue
        'success': 0x27ae60,      # Green
        'error': 0xe74c3c,        # Red
        'warning': 0xf39c12,      # Orange
        'info': 0x95a5a6,         # Gray
        'agent': 0x9b59b6,        # Purple
        'swarm': 0xe67e22,        # Dark Orange
        'system': 0x34495e        # Dark Blue
    }

    @staticmethod
    def create_base_embed(title: str, description: str = "", color: str = 'primary') -> discord.Embed:
        """Create a basic embed with standard formatting."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=EmbedBuilder.COLORS.get(color, EmbedBuilder.COLORS['primary']),
            timestamp=datetime.utcnow()
        )
        return embed

    @staticmethod
    def add_footer(embed: discord.Embed, author, text: str = None) -> discord.Embed:
        """Add standardized footer to embed."""
        footer_text = text or f"Requested by {author}"
        embed.set_footer(
            text=footer_text,
            icon_url=author.avatar.url if hasattr(author, 'avatar') and author.avatar else None
        )
        return embed

    @classmethod
    def create_prompt_embed(cls, agent_id: str, prompt: str, command_id: str, author) -> discord.Embed:
        """Create embed for agent prompt command."""
        embed = cls.create_base_embed(
            title="🤖 Agent Prompt Sent",
            description=f"Prompting **{agent_id}** with your message...",
            color='agent'
        )

        embed.add_field(name="Agent", value=agent_id, inline=True)
        embed.add_field(
            name="Prompt",
            value=prompt[:500] + "..." if len(prompt) > 500 else prompt,
            inline=False
        )
        embed.add_field(name="Command ID", value=f"`{command_id}`", inline=True)

        return cls.add_footer(embed, author)

    @classmethod
    def update_prompt_embed_success(cls, embed: discord.Embed, agent_id: str) -> discord.Embed:
        """Update prompt embed for successful delivery."""
        embed.color = cls.COLORS['success']
        embed.title = "✅ Agent Prompt Delivered"
        embed.description = f"Prompt successfully delivered to **{agent_id}**'s inbox!"
        embed.add_field(name="📨 Delivery Status", value="✅ Delivered", inline=True)
        return embed

    @classmethod
    def update_prompt_embed_error(cls, embed: discord.Embed, agent_id: str, error: str) -> discord.Embed:
        """Update prompt embed for failed delivery."""
        embed.color = cls.COLORS['error']
        embed.title = "❌ Agent Prompt Failed"
        embed.description = f"Failed to deliver prompt to **{agent_id}**."
        embed.add_field(name="📨 Delivery Status", value="❌ Failed", inline=True)
        embed.add_field(name="Error", value=error, inline=False)
        return embed

    @classmethod
    def create_direct_agent_embed(cls, agent_id: str, message: str, command_id: str, author) -> discord.Embed:
        """Create embed for direct agent messaging."""
        embed = cls.create_base_embed(
            f"📨 Direct Message → {agent_id}",
            f"**Message:** {message}",
            'agent'
        )

        embed.add_field(
            name="🎯 Target Agent",
            value=f"**{agent_id}**",
            inline=True
        )

        if command_id:
            embed.add_field(
                name="🆔 Command ID",
                value=f"`{command_id}`",
                inline=True
            )

        if author:
            embed.add_field(
                name="👤 Requested By",
                value=author.mention if hasattr(author, 'mention') else str(author),
                inline=True
            )

        embed.add_field(
            name="⚡ Status",
            value="📤 Sending message...",
            inline=False
        )

        embed.set_footer(text="V2_SWARM - Direct agent communication")
        return embed

    @classmethod
    def create_urgent_broadcast_embed(cls, message: str, command_id: str, author) -> discord.Embed:
        """Create embed for urgent broadcast to all agents."""
        embed = cls.create_base_embed(
            "🚨 URGENT BROADCAST",
            f"**🚨 URGENT MESSAGE:** {message}",
            'error'  # Red color for urgent
        )

        embed.add_field(
            name="🎯 Target",
            value="**ALL AGENTS** (High Priority)",
            inline=True
        )

        if command_id:
            embed.add_field(
                name="🆔 Command ID",
                value=f"`{command_id}`",
                inline=True
            )

        if author:
            embed.add_field(
                name="👤 Initiated By",
                value=author.mention if hasattr(author, 'mention') else str(author),
                inline=True
            )

        embed.add_field(
            name="⚡ Status",
            value="🔄 Broadcasting to all agents...",
            inline=False
        )

        embed.add_field(
            name="🔥 Priority",
            value="**HIGH** - Using ctrl+enter for immediate delivery",
            inline=False
        )

        embed.set_footer(text="V2_SWARM - Urgent swarm coordination")
        return embed

    @classmethod
    def create_status_embed(cls, agent_id: str, author) -> discord.Embed:
        """Create embed for agent status check."""
        embed = cls.create_base_embed(
            title="📊 Agent Status Check",
            description=f"Checking status for **{agent_id}**...",
            color='info'
        )
        return cls.add_footer(embed, author)

    @classmethod
    def update_status_embed(cls, embed: discord.Embed, agent_id: str, status_info: dict[str, Any]) -> discord.Embed:
        """Update status embed with agent information."""
        embed.title = "📊 Agent Status"
        embed.description = f"Status information for **{agent_id}**"
        embed.color = cls.COLORS['success'] if status_info.get('active', False) else cls.COLORS['warning']

        status_emoji = "🟢 Active" if status_info.get('active', False) else "🟡 Inactive"
        embed.add_field(name="Status", value=status_emoji, inline=True)
        embed.add_field(
            name="Last Activity",
            value=status_info.get('last_activity', 'Unknown'),
            inline=True
        )

        if status_info.get('active_commands', 0) > 0:
            embed.add_field(
                name="Active Commands",
                value=str(status_info['active_commands']),
                inline=True
            )

        return embed

    @classmethod
    def create_swarm_embed(cls, message: str, author) -> discord.Embed:
        """Create embed for swarm broadcast."""
        embed = cls.create_base_embed(
            title="🐝 Swarm Broadcast Sent",
            description="Broadcasting message to all agents...",
            color='swarm'
        )
        embed.add_field(
            name="Message",
            value=message[:500] + "..." if len(message) > 500 else message,
            inline=False
        )
        return cls.add_footer(embed, author)

    @classmethod
    def update_swarm_embed_success(cls, embed: discord.Embed, recipient_count: int) -> discord.Embed:
        """Update swarm embed for successful broadcast."""
        embed.color = cls.COLORS['success']
        embed.title = "✅ Swarm Broadcast Complete"
        embed.description = "Message broadcast to all agents!"
        embed.add_field(name="📨 Recipients", value=f"{recipient_count} agents", inline=True)
        return embed

    @classmethod
    def update_swarm_embed_error(cls, embed: discord.Embed, error: str) -> discord.Embed:
        """Update swarm embed for failed broadcast."""
        embed.color = cls.COLORS['error']
        embed.title = "❌ Swarm Broadcast Failed"
        embed.description = "Failed to broadcast to all agents."
        embed.add_field(name="📨 Status", value="❌ Failed", inline=True)
        embed.add_field(name="Error", value=error, inline=False)
        return embed

    @classmethod
    def update_urgent_embed_success(cls, embed: discord.Embed, recipient_count: int) -> discord.Embed:
        """Update urgent broadcast embed for successful delivery."""
        embed.color = cls.COLORS['success']
        embed.title = "✅ URGENT BROADCAST COMPLETE"
        embed.description = "🚨 Urgent message delivered to all agents!"

        # Update the status field
        for field in embed.fields:
            if field.name == "⚡ Status":
                field.value = f"✅ Delivered to {recipient_count} agents"
                break

        return embed

    @classmethod
    def update_urgent_embed_error(cls, embed: discord.Embed, error: str) -> discord.Embed:
        """Update urgent broadcast embed for failed delivery."""
        embed.color = cls.COLORS['error']
        embed.title = "❌ URGENT BROADCAST FAILED"
        embed.description = "🚨 Failed to deliver urgent broadcast."

        # Update the status field
        for field in embed.fields:
            if field.name == "⚡ Status":
                field.value = "❌ Broadcast failed"
                break

        embed.add_field(name="Error", value=error, inline=False)
        return embed

    @classmethod
    def update_direct_embed_success(cls, embed: discord.Embed, agent_id: str) -> discord.Embed:
        """Update direct agent embed for successful message delivery."""
        embed.color = cls.COLORS['success']
        embed.title = f"✅ Message Sent → {agent_id}"
        embed.description = "Direct message delivered successfully!"

        # Update the status field
        for field in embed.fields:
            if field.name == "⚡ Status":
                field.value = "✅ Message delivered successfully"
                break

        return embed

    @classmethod
    def update_direct_embed_error(cls, embed: discord.Embed, agent_id: str, error: str) -> discord.Embed:
        """Update direct agent embed for failed message delivery."""
        embed.color = cls.COLORS['error']
        embed.title = f"❌ Message Failed → {agent_id}"
        embed.description = "Failed to deliver direct message."

        # Update the status field
        for field in embed.fields:
            if field.name == "⚡ Status":
                field.value = "❌ Message delivery failed"
                break

        embed.add_field(name="Error", value=error, inline=False)
        return embed

    @classmethod
    def create_agents_embed(cls, agents: list[str], author) -> discord.Embed:
        """Create embed listing all available agents."""
        embed = cls.create_base_embed(
            title="🤖 V2_SWARM Agents",
            description="List of all available agents in the swarm",
            color='system'
        )

        agent_list = ""
        for agent in agents:
            # Mock status check - in real implementation, check workspace existence
            status = "🟢 Active"  # This would be dynamic
            agent_list += f"• **{agent}** - {status}\n"

        embed.add_field(name="Agents", value=agent_list, inline=False)
        embed.add_field(name="Total Agents", value=str(len(agents)), inline=True)

        return cls.add_footer(embed, author)

    @classmethod
    def create_help_embed(cls, author) -> discord.Embed:
        """Create comprehensive help embed."""
        embed = cls.create_base_embed(
            title="🐝 V2_SWARM Discord Agent Bot",
            description="**WE ARE SWARM** - Interactive agent coordination through Discord commands\n\n"
                       "Coordinate 8 autonomous agents across dual-monitor Cursor IDE setup",
            color='primary'
        )

        # Main Commands Section
        main_commands = """
**🤖 Agent Communication:**
• `!prompt @agent message` - Send prompt to specific agent
• `!status @agent` - Check agent status and activity
• `!agent1 message` - Send to Agent-1 (Integration)
• `!agent2 message` - Send to Agent-2 (Architecture)
• `!agent3 message` - Send to Agent-3 (Infrastructure)
• `!agent4 message` - Send to Agent-4 (Captain/QA)
• `!agent5 message` - Send to Agent-5 (Business Intel)
• `!agent6 message` - Send to Agent-6 (Coordination)
• `!agent7 message` - Send to Agent-7 (Web Dev)
• `!agent8 message` - Send to Agent-8 (Operations)
        """

        # Swarm Commands Section
        swarm_commands = """
**🐝 Swarm Coordination:**
• `!swarm message` - Broadcast to ALL agents
• `!urgent message` - **URGENT** broadcast (ctrl+enter delivery)
• `!captain message` - Direct to Captain (Agent-4)
• `!broadcast message` - Alternative swarm command
        """

        # Summary Commands Section
        summary_commands = """
**📊 Agent Summaries:**
• `!summary1` - Agent-1 status summary
• `!summary2` - Agent-2 status summary
• `!summary3` - Agent-3 status summary
• `!summary4` - Agent-4 status summary
• `!agentsummary` - Show all summary command options
        """

        # Slash Commands Section
        slash_commands = """
**⚡ Interactive Commands:**
• `/agent` - Interactive agent selection with autocomplete
• `/summary_core` - Request core agent summaries
        """

        # Utility Commands Section
        utility_commands = """
**ℹ️ Utility Commands:**
• `!agents` - List all available agents with status
• `!help` - Show this comprehensive help
• `!ping` - Test bot responsiveness & latency
• `!status` - Show bot operational status
        """

        # Dynamic Aliases Section
        alias_commands = """
**🔄 Dynamic Aliases:**
• All aliases from `config/agent_aliases.json`
• Short forms: `!a1`, `!a2`, `!lead`, etc.
• Custom aliases can be added to config
        """

        embed.add_field(name="🎯 Main Agent Commands", value=main_commands, inline=False)
        embed.add_field(name="🐝 Swarm Broadcasting", value=swarm_commands, inline=False)
        embed.add_field(name="📊 Status Summaries", value=summary_commands, inline=False)
        embed.add_field(name="⚡ Interactive Features", value=slash_commands, inline=False)
        embed.add_field(name="🔧 Utility Tools", value=utility_commands, inline=False)
        embed.add_field(name="🔄 Custom Aliases", value=alias_commands, inline=False)

        # System Information
        embed.add_field(name="📊 System Status", value="🟢 Operational\n8 Agents Ready\nPyAutoGUI Integrated", inline=True)
        embed.add_field(name="⚙️ Configuration", value="Prefix: `!`\nTimeout: 300s\nMax Concurrent: 10", inline=True)
        embed.add_field(name="🎯 Architecture", value="V2_SWARM\nDual-Monitor\nCursor IDE Integration", inline=True)

        return cls.add_footer(embed, author, "V2_SWARM - We are swarm intelligence!")

    @classmethod
    def create_ping_embed(cls, latency: float, active_commands: int) -> discord.Embed:
        """Create ping response embed."""
        embed = cls.create_base_embed(
            title="🏓 Pong!",
            description="Bot is responsive and operational",
            color='success'
        )
        embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="Status", value="🟢 Operational", inline=True)
        embed.add_field(name="Active Commands", value=str(active_commands), inline=True)

        return embed

    @classmethod
    def create_error_embed(cls, title: str, description: str, error: str = None) -> discord.Embed:
        """Create error embed."""
        embed = cls.create_base_embed(
            title=title,
            description=description,
            color='error'
        )

        if error:
            embed.add_field(name="Error Details", value=error, inline=False)

        return embed

    @classmethod
    def create_rate_limit_embed(cls) -> discord.Embed:
        """Create rate limit exceeded embed."""
        embed = cls.create_base_embed(
            title="⚠️ Rate Limit Exceeded",
            description="Too many commands! Please wait before sending another command.",
            color='warning'
        )
        embed.add_field(name="Try Again", value="Wait a few seconds before retrying", inline=True)
        return embed

    @classmethod
    def create_too_many_commands_embed(cls) -> discord.Embed:
        """Create too many active commands embed."""
        embed = cls.create_base_embed(
            title="⚠️ Too Many Active Commands",
            description="The bot is processing too many commands. Please wait for some to complete.",
            color='warning'
        )
        embed.add_field(name="Active Commands", value="Wait for current commands to finish", inline=True)
        return embed


class EmbedManager:
    """Manager for Discord embed operations."""

    def __init__(self):
        """Initialize embed manager."""
        self.builder = EmbedBuilder()

    def create_response_embed(self, command_type: str, **kwargs) -> discord.Embed:
        """Create appropriate embed based on command type."""
        author = kwargs.get('author')

        if command_type == 'prompt':
            return self.builder.create_prompt_embed(
                kwargs.get('agent_id', ''),
                kwargs.get('prompt', ''),
                kwargs.get('command_id', ''),
                author
            )
        elif command_type == 'status':
            return self.builder.create_status_embed(
                kwargs.get('agent_id', ''),
                author
            )
        elif command_type == 'swarm':
            return self.builder.create_swarm_embed(
                kwargs.get('message', ''),
                author
            )
        elif command_type == 'agents':
            return self.builder.create_agents_embed(
                kwargs.get('agents', []),
                author
            )
        elif command_type == 'help':
            return self.builder.create_help_embed(author)
        elif command_type == 'ping':
            return self.builder.create_ping_embed(
                kwargs.get('latency', 0),
                kwargs.get('active_commands', 0)
            )
        elif command_type == 'error':
            return self.builder.create_error_embed(
                kwargs.get('title', 'Error'),
                kwargs.get('description', ''),
                kwargs.get('error', None)
            )
        elif command_type == 'rate_limit':
            return self.builder.create_rate_limit_embed()
        elif command_type == 'too_many_commands':
            return self.builder.create_too_many_commands_embed()
        elif command_type == 'direct_agent':
            return self.builder.create_direct_agent_embed(
                kwargs.get('agent_id', ''),
                kwargs.get('message', ''),
                kwargs.get('command_id', ''),
                author
            )
        elif command_type == 'urgent_broadcast':
            return self.builder.create_urgent_broadcast_embed(
                kwargs.get('message', ''),
                kwargs.get('command_id', ''),
                author
            )

        # Default fallback
        return self.builder.create_base_embed("Unknown Command", "Command type not recognized")


# Factory functions for dependency injection
def create_embed_builder() -> EmbedBuilder:
    """Factory function to create embed builder."""
    return EmbedBuilder()


def create_embed_manager() -> EmbedManager:
    """Factory function to create embed manager."""
    return EmbedManager()


# Export for DI
__all__ = ["EmbedBuilder", "EmbedManager", "create_embed_builder", "create_embed_manager"]
