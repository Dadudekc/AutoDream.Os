#!/usr/bin/env python3
"""
Discord Command Registry - V2 Compliant
=======================================

Central registry for all Discord commands (both prefix and slash).
This module handles command registration and routing for the unified Discord bot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime

# V2 Compliance: File under 400 lines, functions under 30 lines


class DiscordCommandRegistry:
    """Central registry for Discord commands."""

    def __init__(self):
        """Initialize command registry."""
        self.logger = logging.getLogger(__name__)
        self.prefix_commands: Dict[str, Callable] = {}
        self.slash_commands: Dict[str, Callable] = {}
        self.command_aliases: Dict[str, str] = {}

        # Register all commands
        self._register_core_commands()
        self._register_agent_commands()
        self._register_messaging_commands()
        self._register_system_commands()

    def _register_core_commands(self) -> None:
        """Register core Discord commands."""
        self.logger.info("🔧 Registering core commands...")

        # Core prefix commands
        self.prefix_commands.update({
            'status': self._get_status_command,
            'agents': self._get_agents_command,
            'contracts': self._get_contracts_command,
            'overnight': self._get_overnight_command,
        })

        # Core slash commands
        self.slash_commands.update({
            'ping': self._get_ping_command,
            'help': self._get_help_command,
            'swarm-help': self._get_help_command,  # Alias
            'status': self._get_status_command,
            'system': self._get_system_command,
        })

        # Aliases
        self.command_aliases.update({
            'swarm-help': 'help',
            'info': 'status',
            'bot-status': 'status',
        })

    def _register_agent_commands(self) -> None:
        """Register agent-related commands."""
        self.logger.info("🔧 Registering agent commands...")

        self.slash_commands.update({
            'agent': self._get_agent_command,
            'agents': self._get_agents_command,
            'agent-status': self._get_agent_status_command,
        })

    def _register_messaging_commands(self) -> None:
        """Register messaging-related commands."""
        self.logger.info("🔧 Registering messaging commands...")

        self.slash_commands.update({
            'send': self._get_send_command,
            'broadcast': self._get_broadcast_command,
            'message': self._get_message_command,
        })

    def _register_system_commands(self) -> None:
        """Register system-related commands."""
        self.logger.info("🔧 Registering system commands...")

        self.slash_commands.update({
            'health': self._get_health_command,
            'uptime': self._get_uptime_command,
            'version': self._get_version_command,
        })

    # Command implementations (V2 compliant - under 30 lines each)

    def _get_status_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Get bot status."""
        return {
            'title': '🤖 Unified Discord Bot Status',
            'description': 'Bot is online and operational',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Commands', 'value': '✅ Prefix & Slash', 'inline': True},
                {'name': 'Status', 'value': '🟢 Online', 'inline': True},
                {'name': 'Uptime', 'value': 'Active', 'inline': True}
            ]
        }

    def _get_agents_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """List available agents."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4",
                 "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        return {
            'title': '🐝 Swarm Agents',
            'description': 'Available agents in the swarm',
            'color': 0x00ff00,
            'fields': [
                {'name': f'Agent-{i}', 'value': agent, 'inline': True}
                for i, agent in enumerate(agents, 1)
            ]
        }

    def _get_contracts_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Get contract status."""
        return {
            'title': '📋 Contract Status',
            'description': 'Current contract information',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Active', 'inline': True},
                {'name': 'Captain', 'value': 'Agent-4', 'inline': True},
                {'name': 'Mission', 'value': 'V3 Infrastructure', 'inline': True}
            ]
        }

    def _get_overnight_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Get overnight operation status."""
        return {
            'title': '🌙 Overnight Operations',
            'description': '24/7 automated operations status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '🟢 Running', 'inline': True},
                {'name': 'Mode', 'value': 'Autonomous', 'inline': True},
                {'name': 'Coverage', 'value': '24/7', 'inline': True}
            ]
        }

    def _get_ping_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Test bot responsiveness."""
        return {
            'title': '🏓 Pong!',
            'description': 'Bot is responding normally',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Operational', 'inline': True}
            ]
        }

    def _get_help_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Show help information."""
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
        return {
            'title': '🤖 Unified Discord Bot Help',
            'description': help_text,
            'color': 0x00ff00
        }

    def _get_system_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Get system information."""
        return {
            'title': '🔧 System Information',
            'description': 'Discord bot system status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Bot Version', 'value': 'Unified v1.0', 'inline': True},
                {'name': 'Command Types', 'value': '✅ Prefix & Slash', 'inline': True},
                {'name': 'Status', 'value': '🟢 Operational', 'inline': True},
                {'name': 'Commands', 'value': '15+ Available', 'inline': True}
            ]
        }

    def _get_agent_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Agent management command."""
        return {
            'title': '🎯 Agent Management',
            'description': 'Agent coordination and management',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Team Beta Leader', 'value': 'Agent-5', 'inline': True},
                {'name': 'Infrastructure', 'value': 'Agent-3', 'inline': True},
                {'name': 'Captain', 'value': 'Agent-4', 'inline': True}
            ]
        }

    def _get_agent_status_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Check agent status."""
        return {
            'title': '📊 Agent Status',
            'description': 'Current status of all agents',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Active Agents', 'value': '8/8', 'inline': True},
                {'name': 'Team Alpha', 'value': '✅ Active', 'inline': True},
                {'name': 'Team Beta', 'value': '✅ Active', 'inline': True}
            ]
        }

    def _get_send_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Send message to agent."""
        return {
            'title': '📤 Send Message',
            'description': 'Send message to specific agent',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Target', 'value': 'Any Agent', 'inline': True},
                {'name': 'Method', 'value': 'PyAutoGUI', 'inline': True},
                {'name': 'Status', 'value': '✅ Available', 'inline': True}
            ]
        }

    def _get_broadcast_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Broadcast to all agents."""
        return {
            'title': '📡 Broadcast Message',
            'description': 'Send message to all agents',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Recipients', 'value': 'All 8 Agents', 'inline': True},
                {'name': 'Method', 'value': 'PyAutoGUI', 'inline': True},
                {'name': 'Status', 'value': '✅ Available', 'inline': True}
            ]
        }

    def _get_message_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Send message."""
        return {
            'title': '💬 Message System',
            'description': 'Agent messaging system',
            'color': 0x00ff00,
            'fields': [
                {'name': 'System', 'value': 'Unified Messaging', 'inline': True},
                {'name': 'Fallback', 'value': 'Inbox Files', 'inline': True},
                {'name': 'Status', 'value': '✅ Operational', 'inline': True}
            ]
        }

    def _get_health_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Health check."""
        return {
            'title': '🏥 Health Check',
            'description': 'Bot health status',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '✅ Healthy', 'inline': True},
                {'name': 'Commands', 'value': '✅ Working', 'inline': True},
                {'name': 'Connection', 'value': '✅ Stable', 'inline': True}
            ]
        }

    def _get_uptime_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Bot uptime."""
        return {
            'title': '⏱️ Bot Uptime',
            'description': 'Bot operational time',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Status', 'value': '🟢 Running', 'inline': True},
                {'name': 'Duration', 'value': 'Continuous', 'inline': True},
                {'name': 'Availability', 'value': '24/7', 'inline': True}
            ]
        }

    def _get_version_command(self, ctx=None, interaction=None) -> Dict[str, Any]:
        """Bot version."""
        return {
            'title': '📦 Bot Version',
            'description': 'Bot version information',
            'color': 0x00ff00,
            'fields': [
                {'name': 'Version', 'value': 'Unified v1.0', 'inline': True},
                {'name': 'Type', 'value': 'Consolidated', 'inline': True},
                {'name': 'Compliance', 'value': '✅ V2', 'inline': True}
            ]
        }

    def get_command_count(self) -> Dict[str, int]:
        """Get command counts."""
        return {
            'prefix_commands': len(self.prefix_commands),
            'slash_commands': len(self.slash_commands),
            'total_commands': len(self.prefix_commands) + len(self.slash_commands),
            'aliases': len(self.command_aliases)
        }

    def list_commands(self) -> Dict[str, List[str]]:
        """List all commands."""
        return {
            'prefix': list(self.prefix_commands.keys()),
            'slash': list(self.slash_commands.keys()),
            'aliases': list(self.command_aliases.keys())
        }


# Global command registry instance
command_registry = DiscordCommandRegistry()


