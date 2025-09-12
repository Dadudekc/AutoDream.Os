#!/usr/bin/env python3
"""
Agent Command Handlers - V2 Compliance Module
==============================================

Agent-specific command handlers for Discord Agent Bot.
Handles prompt and status commands for individual agents.

Features:
- Agent prompt delivery to inboxes
- Agent status checking and reporting
- Command tracking and response handling
- Error handling and user feedback

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .discord_commander_models import CommandResult
    from .embeds import EmbedManager
except ImportError:
    from discord_commander_models import CommandResult
    from embeds import EmbedManager


class AgentCommandHandlers:
    """Handles agent-specific commands (prompt, status)."""

    def __init__(self, agent_engine, embed_manager: EmbedManager):
        """Initialize agent command handlers."""
        self.agent_engine = agent_engine
        self.embed_manager = embed_manager
        self.active_commands: dict[str, dict[str, Any]] = {}

    async def handle_prompt_command(self, context: dict[str, Any]) -> dict[str, Any] | None:
        """
        Handle agent prompt command.

        Args:
            context: Command context containing author, channel, args, etc.

        Returns:
            Response data or None if command should be ignored
        """
        author = context["author"]
        channel = context["channel"]
        agent_id = context["args"][0]
        prompt = context["args"][1]
        command_id = context["command_id"]

        print(f"🤖 Prompting agent {agent_id}: {prompt[:50]}...")

        # Validate agent
        if not self.agent_engine.is_valid_agent(agent_id):
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Invalid Agent",
                description=f"**{agent_id}** is not a valid agent.",
                error="Use `!agents` to see available agents.",
            )
            return {"embed": error_embed, "ignore": True}

        # Add to active commands
        self.active_commands[command_id] = {
            "type": "prompt",
            "agent": agent_id,
            "prompt": prompt,
            "author": str(author),
            "channel": channel.id if hasattr(channel, "id") else channel,
            "timestamp": datetime.utcnow(),
            "status": "sending",
        }

        # Create initial response embed
        prompt_embed = self.embed_manager.create_response_embed(
            "prompt", agent_id=agent_id, prompt=prompt, command_id=command_id, author=author
        )

        return {
            "embed": prompt_embed,
            "command_id": command_id,
            "agent_id": agent_id,
            "follow_up": True,
        }

    async def handle_prompt_followup(
        self, command_id: str, result: CommandResult
    ) -> dict[str, Any]:
        """
        Handle followup for prompt command after agent communication.

        Args:
            command_id: Unique command identifier
            result: Result from agent communication

        Returns:
            Updated embed data
        """
        if command_id not in self.active_commands:
            return {}

        command_data = self.active_commands[command_id]
        agent_id = command_data["agent"]

        # Update command status
        self.active_commands[command_id]["status"] = "sent" if result.success else "failed"
        self.active_commands[command_id]["result"] = result

        # Create updated embed
        if result.success:
            updated_embed = self.embed_manager.builder.update_prompt_embed_success(
                self.embed_manager.builder.create_base_embed("🤖 Agent Prompt Sent"), agent_id
            )
        else:
            updated_embed = self.embed_manager.builder.update_prompt_embed_error(
                self.embed_manager.builder.create_base_embed("🤖 Agent Prompt Sent"),
                agent_id,
                result.message,
            )

        # Clean up active command after delay
        await asyncio.sleep(10)
        self.active_commands.pop(command_id, None)

        return {"embed": updated_embed, "edit": True}

    async def handle_status_command(self, context: dict[str, Any]) -> dict[str, Any] | None:
        """
        Handle agent status command.

        Args:
            context: Command context

        Returns:
            Response data or None
        """
        author = context["author"]
        channel = context["channel"]
        agent_id = context["args"][0]

        print(f"📊 Checking status for agent {agent_id}")

        # Validate agent
        if not self.agent_engine.is_valid_agent(agent_id):
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Invalid Agent",
                description=f"**{agent_id}** is not a valid agent.",
                error="Use `!agents` to see available agents.",
            )
            return {"embed": error_embed, "ignore": True}

        # Create status embed
        status_embed = self.embed_manager.create_response_embed(
            "status", agent_id=agent_id, author=author
        )

        # Get agent status
        try:
            status_info = await self._get_agent_status(agent_id)
            updated_embed = self.embed_manager.builder.update_status_embed(
                status_embed, agent_id, status_info
            )
        except Exception as e:
            updated_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Status Check Failed",
                description=f"Could not retrieve status for **{agent_id}**.",
                error=str(e),
            )

        return {"embed": updated_embed}

    async def _get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """
        Get agent status information.

        Args:
            agent_id: Agent identifier

        Returns:
            Status information dictionary
        """
        # Check if agent workspace exists
        workspace_path = Path(f"agent_workspaces/{agent_id}")

        if workspace_path.exists():
            # Check inbox for recent messages
            inbox_path = workspace_path / "inbox"
            if inbox_path.exists():
                inbox_files = list(inbox_path.glob("*.md"))
                recent_files = [
                    f
                    for f in inbox_files
                    if (datetime.utcnow() - datetime.fromtimestamp(f.stat().st_mtime)).seconds
                    < 3600
                ]
                active_commands = len(recent_files)
            else:
                active_commands = 0

            return {
                "active": True,
                "last_activity": "Recently active",
                "active_commands": active_commands,
            }
        else:
            return {"active": False, "last_activity": "Workspace not found", "active_commands": 0}

    async def execute_agent_command(self, agent_id: str, command: str) -> CommandResult:
        """
        Execute command on specific agent (placeholder for future implementation).

        Args:
            agent_id: Target agent identifier
            command: Command to execute

        Returns:
            Command result
        """
        # This would be implemented based on specific agent communication protocols
        await asyncio.sleep(1)  # Simulate processing

        return CommandResult(
            success=True,
            message=f"Command executed successfully on {agent_id}",
            data={"agent_id": agent_id, "command": command},
        )

    def get_active_command_count(self) -> int:
        """Get count of active commands."""
        return len(self.active_commands)

    def get_agent_command_stats(self, agent_id: str) -> dict[str, Any]:
        """Get command statistics for specific agent."""
        agent_commands = [
            cmd for cmd in self.active_commands.values() if cmd.get("agent") == agent_id
        ]

        return {
            "agent_id": agent_id,
            "active_commands": len(agent_commands),
            "command_types": [cmd.get("type", "unknown") for cmd in agent_commands],
        }

    async def cleanup_old_commands(self, max_age_seconds: int = 300):
        """Clean up old active commands."""
        cutoff_time = datetime.utcnow().timestamp() - max_age_seconds
        to_remove = []

        for command_id, command_data in self.active_commands.items():
            if command_data.get("timestamp", datetime.min).timestamp() < cutoff_time:
                to_remove.append(command_id)

        for command_id in to_remove:
            self.active_commands.pop(command_id, None)

        if to_remove:
            print(f"🧹 Cleaned up {len(to_remove)} old commands")

    async def handle_direct_agent_command(
        self, agent_number: int, message: str, context: dict[str, Any]
    ) -> dict[str, Any] | None:
        """
        Handle direct agent commands like !agent1, !agent2, etc.

        Args:
            agent_number: Agent number (1-8)
            message: Message to send
            context: Command context

        Returns:
            Response data or None
        """
        author = context["author"]
        channel = context["channel"]
        agent_id = f"Agent-{agent_number}"

        print(f"🎯 Direct message to {agent_id}: {message[:50]}...")

        # Validate agent number
        if not (1 <= agent_number <= 8):
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Invalid Agent Number",
                description="Agent number must be between 1 and 8.",
                error="Use `!agents` to see all available agents.",
            )
            return {"embed": error_embed, "ignore": True}

        # Validate agent
        if not self.agent_engine.is_valid_agent(agent_id):
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Agent Not Available",
                description=f"**{agent_id}** is not currently available.",
                error="Use `!agents` to see available agents.",
            )
            return {"embed": error_embed, "ignore": True}

        # Generate command ID
        command_id = f"direct_{agent_id}_{datetime.utcnow().strftime('%H%M%S')}"

        # Add to active commands
        self.active_commands[command_id] = {
            "type": "direct_message",
            "agent": agent_id,
            "message": message,
            "author": str(author),
            "channel": channel.id if hasattr(channel, "id") else channel,
            "timestamp": datetime.utcnow(),
            "status": "sending",
        }

        # Create response embed
        direct_embed = self.embed_manager.create_response_embed(
            "direct_agent", agent_id=agent_id, message=message, command_id=command_id, author=author
        )

        return {
            "embed": direct_embed,
            "command_id": command_id,
            "agent_id": agent_id,
            "follow_up": True,
        }

    async def handle_direct_agent_followup(
        self, command_id: str, result: CommandResult
    ) -> dict[str, Any]:
        """
        Handle followup for direct agent command.

        Args:
            command_id: Unique command identifier
            result: Result from agent communication

        Returns:
            Updated embed data
        """
        if command_id not in self.active_commands:
            return {}

        command_data = self.active_commands[command_id]
        agent_id = command_data["agent"]

        # Update command status
        self.active_commands[command_id]["status"] = "sent" if result.success else "failed"
        self.active_commands[command_id]["result"] = result

        # Create updated embed
        if result.success:
            updated_embed = self.embed_manager.builder.update_direct_embed_success(
                self.embed_manager.builder.create_base_embed("✅ Message Sent to Agent"), agent_id
            )
        else:
            updated_embed = self.embed_manager.builder.update_direct_embed_error(
                self.embed_manager.builder.create_base_embed("❌ Message Failed"),
                agent_id,
                result.message,
            )

        # Clean up active command after delay
        await asyncio.sleep(10)
        self.active_commands.pop(command_id, None)

        return {"embed": updated_embed, "edit": True}


# Factory function for dependency injection
def create_agent_command_handlers(
    agent_engine, embed_manager: EmbedManager
) -> AgentCommandHandlers:
    """Factory function to create agent command handlers."""
    return AgentCommandHandlers(agent_engine, embed_manager)


# Export for DI
__all__ = ["AgentCommandHandlers", "create_agent_command_handlers"]
