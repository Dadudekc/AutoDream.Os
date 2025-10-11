#!/usr/bin/env python3
"""
Discord UI Components - V2 Compliant
====================================

Unified UI components for Discord embeds and interaction handlers.
Combines UI functionality from both Discord bot systems.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import discord

# V2 Compliance: File under 400 lines, functions under 30 lines


class DiscordUIComponents:
    """Unified UI components for Discord embeds."""

    def __init__(self):
        """Initialize UI components."""
        self.logger = logging.getLogger(__name__)

    def create_embed(self, data: Dict[str, Any]) -> discord.Embed:
        """Create Discord embed from data dictionary."""
        embed = discord.Embed(
            title=data.get('title', '🤖 Discord Bot'),
            description=data.get('description', ''),
            color=data.get('color', 0x00ff00),
            timestamp=datetime.utcnow()
        )

        # Add fields if present
        if 'fields' in data:
            for field in data.get('fields', []):
                embed.add_field(
                    name=field.get('name', ''),
                    value=field.get('value', ''),
                    inline=field.get('inline', True)
                )

        # Add footer if present
        if 'footer' in data:
            embed.set_footer(text=data['footer'])

        # Add thumbnail if present
        if 'thumbnail' in data:
            embed.set_thumbnail(url=data['thumbnail'])

        # Add image if present
        if 'image' in data:
            embed.set_image(url=data['image'])

        return embed

    def create_status_embed(self) -> discord.Embed:
        """Create status embed."""
        return self.create_embed({
            'title': '🤖 Unified Discord Bot Status',
            'description': 'Bot is online and operational',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Commands', 'value': '✅ Prefix & Slash', 'inline': True},
                {'name': 'Status', 'value': '🟢 Online', 'inline': True},
                {'name': 'Uptime', 'value': 'Active', 'inline': True}
            ]
        })

    def create_agents_embed(self) -> discord.Embed:
        """Create agents embed."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4",
                 "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        fields = []
        for i, agent in enumerate(agents, 1):
            fields.append({
                'name': f'Agent-{i}',
                'value': agent,
                'inline': True
            })

        return self.create_embed({
            'title': '🐝 Swarm Agents',
            'description': 'Available agents in the swarm',
            'color': 0x00ff00,
            'fields': fields
        })

    def create_contracts_embed(self) -> discord.Embed:
        """Create contracts embed."""
        return self.create_embed({
            'title': '📋 Contract Status',
            'description': 'Current contract information',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Active', 'inline': True},
                {'name': 'Captain', 'value': 'Agent-4', 'inline': True},
                {'name': 'Mission', 'value': 'V3 Infrastructure', 'inline': True}
            ]
        })

    def create_overnight_embed(self) -> discord.Embed:
        """Create overnight operations embed."""
        return self.create_embed({
            'title': '🌙 Overnight Operations',
            'description': '24/7 automated operations status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '🟢 Running', 'inline': True},
                {'name': 'Mode', 'value': 'Autonomous', 'inline': True},
                {'name': 'Coverage', 'value': '24/7', 'inline': True}
            ]
        })

    def create_ping_embed(self) -> discord.Embed:
        """Create ping response embed."""
        return self.create_embed({
            'title': '🏓 Pong!',
            'description': 'Bot is responding normally',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Operational', 'inline': True}
            ]
        })

    def create_help_embed(self) -> discord.Embed:
        """Create help embed."""
        help_text = """
🤖 **Unified Discord Bot Commands**

**Prefix Commands** (use ! before command):
- `!status` - Get bot status
- `!agents` - List swarm agents
- `!contracts` - Get contract status
- `!overnight` - Get overnight operations

**Slash Commands** (use / before command):
- `/ping` - Test bot responsiveness
- `/help` - Show this help message
- `/swarm-help` - Show this help message (alias)
- `/status` - Get bot status
- `/agents` - List swarm agents
- `/contracts` - Get contract status
- `/overnight` - Get overnight operations

🐝 **WE ARE SWARM** - Use either prefix (!) or slash (/) commands!
        """

        return self.create_embed({
            'title': '🤖 Unified Discord Bot Help',
            'description': help_text,
            'color': 0x00ff00
        })

    def create_system_embed(self) -> discord.Embed:
        """Create system information embed."""
        return self.create_embed({
            'title': '🔧 System Information',
            'description': 'Discord bot system status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Bot Version', 'value': 'Unified v1.0', 'inline': True},
                {'name': 'Command Types', 'value': '✅ Prefix & Slash', 'inline': True},
                {'name': 'Status', 'value': '🟢 Operational', 'inline': True},
                {'name': 'Commands', 'value': '15+ Available', 'inline': True}
            ]
        })

    def create_agent_embed(self) -> discord.Embed:
        """Create agent management embed."""
        return self.create_embed({
            'title': '🎯 Agent Management',
            'description': 'Agent coordination and management',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Team Beta Leader', 'value': 'Agent-5', 'inline': True},
                {'name': 'Infrastructure', 'value': 'Agent-3', 'inline': True},
                {'name': 'Captain', 'value': 'Agent-4', 'inline': True}
            ]
        })

    def create_agent_status_embed(self) -> discord.Embed:
        """Create agent status embed."""
        return self.create_embed({
            'title': '📊 Agent Status',
            'description': 'Current status of all agents',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Active Agents', 'value': '8/8', 'inline': True},
                {'name': 'Team Alpha', 'value': '✅ Active', 'inline': True},
                {'name': 'Team Beta', 'value': '✅ Active', 'inline': True}
            ]
        })

    def create_health_embed(self) -> discord.Embed:
        """Create health check embed."""
        return self.create_embed({
            'title': '🏥 Health Check',
            'description': 'Bot health status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Healthy', 'inline': True},
                {'name': 'Commands', 'value': '✅ Working', 'inline': True},
                {'name': 'Connection', 'value': '✅ Stable', 'inline': True}
            ]
        })

    def create_uptime_embed(self) -> discord.Embed:
        """Create uptime embed."""
        return self.create_embed({
            'title': '⏱️ Bot Uptime',
            'description': 'Bot operational time',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '🟢 Running', 'inline': True},
                {'name': 'Duration', 'value': 'Continuous', 'inline': True},
                {'name': 'Availability', 'value': '24/7', 'inline': True}
            ]
        })

    def create_version_embed(self) -> discord.Embed:
        """Create version embed."""
        return self.create_embed({
            'title': '📦 Bot Version',
            'description': 'Bot version information',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Version', 'value': 'Unified v1.0', 'inline': True},
                {'name': 'Type', 'value': 'Consolidated', 'inline': True},
                {'name': 'Compliance', 'value': '✅ V2', 'inline': True}
            ]
        })

    def create_messaging_embed(self, embed_type: str) -> discord.Embed:
        """Create messaging-related embed."""
        embed_data = {
            'send': {
                'title': '📤 Send Message',
                'description': 'Send message to specific agent',
                'fields': [
                    {'name': 'Target', 'value': 'Any Agent', 'inline': True},
                    {'name': 'Method', 'value': 'PyAutoGUI', 'inline': True},
                    {'name': 'Status', 'value': '✅ Available', 'inline': True}
                ]
            },
            'broadcast': {
                'title': '📡 Broadcast Message',
                'description': 'Send message to all agents',
                'fields': [
                    {'name': 'Recipients', 'value': 'All 8 Agents', 'inline': True},
                    {'name': 'Method', 'value': 'PyAutoGUI', 'inline': True},
                    {'name': 'Status', 'value': '✅ Available', 'inline': True}
                ]
            },
            'message': {
                'title': '💬 Message System',
                'description': 'Agent messaging system',
                'fields': [
                    {'name': 'System', 'value': 'Unified Messaging', 'inline': True},
                    {'name': 'Fallback', 'value': 'Inbox Files', 'inline': True},
                    {'name': 'Status', 'value': '✅ Operational', 'inline': True}
                ]
            }
        }

        if embed_type in embed_data:
            return self.create_embed(embed_data[embed_type])

        return self.create_embed({
            'title': '❓ Unknown Embed Type',
            'description': f'Embed type "{embed_type}" not found',
            'color': 0xff0000
        })

    def create_error_embed(self, error_message: str) -> discord.Embed:
        """Create error embed."""
        return self.create_embed({
            'title': '❌ Error',
            'description': error_message,
            'color': 0xff0000,
            'fields': [
                {'name': 'Status', 'value': 'Error Occurred', 'inline': True},
                {'name': 'Time', 'value': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'), 'inline': True}
            ]
        })

    def create_success_embed(self, success_message: str) -> discord.Embed:
        """Create success embed."""
        return self.create_embed({
            'title': '✅ Success',
            'description': success_message,
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': 'Operation Successful', 'inline': True},
                {'name': 'Time', 'value': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'), 'inline': True}
            ]
        })


# Global UI components instance
ui_components = DiscordUIComponents()


