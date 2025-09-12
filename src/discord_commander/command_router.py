#!/usr/bin/env python3
"""
Command Router - V2 Compliance Module
=====================================

Command parsing and routing logic for Discord Agent Bot.
Handles command recognition, validation, and dispatching.

Features:
- Regex-based command parsing
- Command validation and sanitization
- Routing to appropriate handlers
- Command metadata extraction

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

import re
from datetime import datetime
from typing import Any


class CommandRouter:
    """Routes Discord commands to appropriate handlers."""

    def __init__(self):
        """Initialize command router."""
        self.command_patterns = {
            "prompt": r"^!prompt\s+@?(\w+[-\d]*)\s+(.+)$",
            "status": r"^!status\s*@?(\w+[-\d]*)$",
            "swarm": r"^!swarm\s+(.+)$",
            "urgent": r"^!urgent\s+(.+)$",
            "help": r"^!help$",
            "agents": r"^!agents$",
            "ping": r"^!ping$",
        }

        self.command_metadata = {
            "prompt": {
                "description": "Send prompt to specific agent",
                "syntax": "!prompt @agent message",
                "max_length": 2000,
                "cooldown": 2,
            },
            "status": {
                "description": "Check agent status and activity",
                "syntax": "!status @agent",
                "max_length": 100,
                "cooldown": 1,
            },
            "swarm": {
                "description": "Broadcast to all agents",
                "syntax": "!swarm message",
                "max_length": 1000,
                "cooldown": 5,
            },
            "urgent": {
                "description": "URGENT broadcast to all agents (high priority)",
                "syntax": "!urgent message",
                "max_length": 500,
                "cooldown": 10,
            },
            "help": {
                "description": "Show help information",
                "syntax": "!help",
                "max_length": 10,
                "cooldown": 0,
            },
            "agents": {
                "description": "List all available agents",
                "syntax": "!agents",
                "max_length": 10,
                "cooldown": 0,
            },
            "ping": {
                "description": "Test bot responsiveness",
                "syntax": "!ping",
                "max_length": 10,
                "cooldown": 0,
            },
        }

    def parse_command(self, message: str) -> tuple[str, list[str], str]:
        """
        Parse Discord command and return (command_type, args, remaining_text)

        Args:
            message: Raw Discord message content

        Returns:
            Tuple of (command_type, args_list, remaining_text)
        """
        if not message or not isinstance(message, str):
            return "unknown", [], message

        message = message.strip()

        for cmd_type, pattern in self.command_patterns.items():
            match = re.match(pattern, message, re.IGNORECASE)
            if match:
                if cmd_type == "prompt":
                    return cmd_type, [match.group(1), match.group(2)], ""
                elif cmd_type == "status":
                    return cmd_type, [match.group(1)], ""
                elif cmd_type == "swarm":
                    return cmd_type, [match.group(1)], ""
                elif cmd_type == "urgent":
                    return cmd_type, [match.group(1)], ""
                else:
                    return cmd_type, [], ""

        return "unknown", [], message

    def validate_command(self, cmd_type: str, args: list[str], content: str) -> tuple[bool, str]:
        """
        Validate command parameters and content.

        Args:
            cmd_type: Type of command
            args: Command arguments
            content: Full message content

        Returns:
            Tuple of (is_valid, error_message)
        """
        if cmd_type not in self.command_metadata:
            return False, f"Unknown command type: {cmd_type}"

        metadata = self.command_metadata[cmd_type]

        # Check content length
        if len(content) > metadata["max_length"]:
            return False, f"Command too long (max {metadata['max_length']} characters)"

        # Validate specific command requirements
        if cmd_type == "prompt":
            if len(args) != 2:
                return False, "Prompt command requires agent and message"
            agent_id = args[0]
            if not self._is_valid_agent_format(agent_id):
                return False, f"Invalid agent format: {agent_id}"

        elif cmd_type == "status":
            if len(args) != 1:
                return False, "Status command requires agent"
            agent_id = args[0]
            if not self._is_valid_agent_format(agent_id):
                return False, f"Invalid agent format: {agent_id}"

        elif cmd_type == "swarm":
            if len(args) != 1:
                return False, "Swarm command requires message"
            if not args[0].strip():
                return False, "Swarm message cannot be empty"

        return True, ""

    def get_command_metadata(self, cmd_type: str) -> dict[str, Any]:
        """Get metadata for a command type."""
        return self.command_metadata.get(cmd_type, {})

    def get_all_commands(self) -> dict[str, dict[str, Any]]:
        """Get all available commands with metadata."""
        return self.command_metadata.copy()

    def generate_command_id(self, author_id: int) -> str:
        """Generate unique command ID."""
        timestamp = int(datetime.utcnow().timestamp())
        return f"{author_id}_{timestamp}"

    def _is_valid_agent_format(self, agent_id: str) -> bool:
        """Validate agent ID format."""
        if not agent_id or not isinstance(agent_id, str):
            return False

        # Allow Agent-1 through Agent-8
        if agent_id.startswith("Agent-"):
            try:
                agent_num = int(agent_id.split("-")[1])
                return 1 <= agent_num <= 8
            except (IndexError, ValueError):
                return False

        return False

    def sanitize_content(self, content: str) -> str:
        """Sanitize command content."""
        if not content:
            return ""

        # Remove excessive whitespace
        content = " ".join(content.split())

        # Limit length (extra safety)
        max_length = 4000  # Discord message limit
        if len(content) > max_length:
            content = content[: max_length - 3] + "..."

        return content.strip()

    def create_command_context(
        self, cmd_type: str, args: list[str], author, channel
    ) -> dict[str, Any]:
        """Create command execution context."""
        return {
            "command_type": cmd_type,
            "args": args,
            "author": author,
            "channel": channel,
            "timestamp": datetime.utcnow(),
            "command_id": self.generate_command_id(author.id if hasattr(author, "id") else 0),
            "metadata": self.get_command_metadata(cmd_type),
        }


# Factory function for dependency injection
def create_command_router() -> CommandRouter:
    """Factory function to create command router."""
    return CommandRouter()


# Export for DI
__all__ = ["CommandRouter", "create_command_router"]
