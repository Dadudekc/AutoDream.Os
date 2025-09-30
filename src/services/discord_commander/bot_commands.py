#!/usr/bin/env python3
"""
Discord Commander Bot Commands - Command handling
===============================================

Command handling extracted from bot.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class DiscordBotCommands:
    """Discord bot command handling system."""

    def __init__(self, bot_core):
        """Initialize bot commands."""
        self.bot_core = bot_core
        self.commands: dict[str, dict[str, Any]] = {}
        self.command_aliases: dict[str, str] = {}
        self._register_default_commands()
        logger.info("Discord bot commands initialized")

    def _register_default_commands(self):
        """Register default bot commands."""
        self.register_command(
            "status", self.cmd_status, "Get bot status and system information", ["health", "info"]
        )

        self.register_command("ping", self.cmd_ping, "Check bot responsiveness", ["latency"])

        self.register_command("help", self.cmd_help, "Show available commands", ["commands", "?"])

        self.register_command("uptime", self.cmd_uptime, "Show bot uptime", ["time", "runtime"])

        self.register_command(
            "agents", self.cmd_agents, "Show agent status information", ["swarm", "team"]
        )

    def register_command(
        self, name: str, handler: Callable, description: str, aliases: list[str] = None
    ):
        """Register a new command."""
        self.commands[name] = {
            "handler": handler,
            "description": description,
            "aliases": aliases or [],
            "registered_at": datetime.now().isoformat(),
        }

        # Register aliases
        if aliases:
            for alias in aliases:
                self.command_aliases[alias] = name

        logger.info(f"Command '{name}' registered with {len(aliases or [])} aliases")

    def unregister_command(self, name: str):
        """Unregister a command."""
        if name in self.commands:
            # Remove aliases
            aliases = self.commands[name].get("aliases", [])
            for alias in aliases:
                if alias in self.command_aliases:
                    del self.command_aliases[alias]

            # Remove command
            del self.commands[name]
            logger.info(f"Command '{name}' unregistered")

    def get_command(self, name: str) -> dict[str, Any] | None:
        """Get command by name or alias."""
        # Check direct command name
        if name in self.commands:
            return self.commands[name]

        # Check aliases
        if name in self.command_aliases:
            actual_name = self.command_aliases[name]
            return self.commands.get(actual_name)

        return None

    def list_commands(self) -> list[dict[str, Any]]:
        """List all registered commands."""
        command_list = []
        for name, cmd_data in self.commands.items():
            command_list.append(
                {
                    "name": name,
                    "description": cmd_data["description"],
                    "aliases": cmd_data["aliases"],
                    "registered_at": cmd_data["registered_at"],
                }
            )
        return command_list

    async def execute_command(self, command_name: str, *args, **kwargs) -> dict[str, Any]:
        """Execute a command."""
        command = self.get_command(command_name)
        if not command:
            return {
                "success": False,
                "error": f"Command '{command_name}' not found",
                "available_commands": list(self.commands.keys()),
            }

        try:
            # Record command execution
            self.bot_core.record_command_execution()

            # Execute command
            result = await command["handler"](*args, **kwargs)

            return {"success": True, "result": result, "command": command_name}

        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}")
            self.bot_core.record_error()

            return {"success": False, "error": str(e), "command": command_name}

    # Default command implementations
    async def cmd_status(self, *args, **kwargs) -> dict[str, Any]:
        """Status command implementation."""
        bot_info = self.bot_core.get_bot_info()
        performance_stats = self.bot_core.get_performance_stats()
        health_status = self.bot_core.get_health_status()

        return {
            "bot_info": bot_info,
            "performance_stats": performance_stats,
            "health_status": health_status,
            "timestamp": datetime.now().isoformat(),
        }

    async def cmd_ping(self, *args, **kwargs) -> dict[str, Any]:
        """Ping command implementation."""
        start_time = datetime.now()

        # Simulate some processing
        await asyncio.sleep(0.1)

        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds() * 1000  # ms

        return {
            "pong": True,
            "latency_ms": round(latency, 2),
            "timestamp": datetime.now().isoformat(),
        }

    async def cmd_help(self, *args, **kwargs) -> dict[str, Any]:
        """Help command implementation."""
        commands = self.list_commands()

        help_text = "**Discord Commander Bot Commands:**\n\n"
        for cmd in commands:
            help_text += f"**{cmd['name']}** - {cmd['description']}\n"
            if cmd["aliases"]:
                help_text += f"  *Aliases: {', '.join(cmd['aliases'])}*\n"
            help_text += "\n"

        return {
            "help_text": help_text,
            "total_commands": len(commands),
            "timestamp": datetime.now().isoformat(),
        }

    async def cmd_uptime(self, *args, **kwargs) -> dict[str, Any]:
        """Uptime command implementation."""
        uptime_string = self.bot_core.get_uptime_string()
        bot_info = self.bot_core.get_bot_info()

        return {
            "uptime_string": uptime_string,
            "uptime_seconds": bot_info["uptime_seconds"],
            "start_time": bot_info["start_time"],
            "timestamp": datetime.now().isoformat(),
        }

    async def cmd_agents(self, *args, **kwargs) -> dict[str, Any]:
        """Agents command implementation."""
        # TODO: Implement actual agent status retrieval
        # For now, return mock data
        return {
            "agents": [
                {"agent_id": "Agent-1", "status": "ACTIVE", "role": "Integration Specialist"},
                {"agent_id": "Agent-4", "status": "ACTIVE", "role": "Captain"},
                {"agent_id": "Agent-7", "status": "ACTIVE", "role": "Web Development Specialist"},
            ],
            "total_agents": 8,
            "active_agents": 5,
            "timestamp": datetime.now().isoformat(),
        }

    def get_command_usage_stats(self) -> dict[str, Any]:
        """Get command usage statistics."""
        return {
            "total_commands": len(self.commands),
            "total_aliases": len(self.command_aliases),
            "most_used_command": "status",  # TODO: Implement actual tracking
            "commands_executed": self.bot_core.commands_executed,
            "timestamp": datetime.now().isoformat(),
        }

    def validate_command_syntax(self, command_text: str) -> dict[str, Any]:
        """Validate command syntax."""
        if not command_text.startswith(self.bot_core.command_prefix):
            return {
                "valid": False,
                "error": f"Command must start with '{self.bot_core.command_prefix}'",
            }

        parts = command_text[1:].split()
        if not parts:
            return {"valid": False, "error": "No command specified"}

        command_name = parts[0]
        command = self.get_command(command_name)

        if not command:
            return {
                "valid": False,
                "error": f"Unknown command: {command_name}",
                "suggestions": self._get_command_suggestions(command_name),
            }

        return {
            "valid": True,
            "command_name": command_name,
            "arguments": parts[1:],
            "command_info": command,
        }

    def _get_command_suggestions(self, partial_name: str) -> list[str]:
        """Get command suggestions for partial name."""
        suggestions = []
        partial_lower = partial_name.lower()

        for cmd_name in self.commands.keys():
            if partial_lower in cmd_name.lower():
                suggestions.append(cmd_name)

        # Check aliases
        for alias in self.command_aliases.keys():
            if partial_lower in alias.lower():
                suggestions.append(alias)

        return suggestions[:5]  # Return top 5 suggestions
