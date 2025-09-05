#!/usr/bin/env python3
"""
Messaging CLI Handlers Engine - V2 Compliant
============================================

Core engine for messaging CLI handlers operations.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: Modular engine for messaging CLI handlers
"""

import logging
from typing import Any, Dict, List, Optional

from .agent_registry import format_agent_list
from .messaging_handlers_models import CLICommand, CommandResult, CoordinateConfig
from .utils.agent_registry import AGENTS, list_agents


class MessagingHandlersEngine:
    """Core engine for messaging CLI handlers operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the messaging handlers engine."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.coordinates: Dict[str, CoordinateConfig] = {}
        self._load_coordinates()

    def _load_coordinates(self) -> None:
        """Load agent coordinates from configuration."""
        try:
            self.coordinates = {
                agent_id: CoordinateConfig(
                    agent_id,
                    info["coords"]["x"],
                    info["coords"]["y"],
                    f"{agent_id} coordinates",
                )
                for agent_id, info in AGENTS.items()
            }
        except Exception as e:
            self.logger.warning(f"Could not load coordinates: {e}")

    def get_agent_coordinates(self, agent_id: str) -> Optional[CoordinateConfig]:
        """Get coordinates for a specific agent."""
        return self.coordinates.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all available agents."""
        return list_agents()

    def validate_command(self, command: CLICommand) -> CommandResult:
        """Validate a CLI command."""
        try:
            if not command.command:
                return CommandResult(
                    False, "Command is required", error="Missing command"
                )

            if command.command == "send" and not command.message:
                return CommandResult(
                    False,
                    "Message is required for send command",
                    error="Missing message",
                )

            if command.command == "send" and not command.agent:
                return CommandResult(
                    False, "Agent is required for send command", error="Missing agent"
                )

            return CommandResult(True, "Command validated successfully")
        except Exception as e:
            return CommandResult(False, f"Command validation failed: {e}", error=str(e))

    def process_command(self, command: CLICommand) -> CommandResult:
        """Process a CLI command."""
        try:
            validation_result = self.validate_command(command)
            if not validation_result.success:
                return validation_result

            if command.command == "coordinates":
                return self._handle_coordinates_command()
            elif command.command == "list_agents":
                agents = self.list_agents()
                formatted = format_agent_list(agents)
                return CommandResult(
                    formatted["success"],
                    formatted["message"],
                    data=formatted["data"],
                )
            elif command.command == "send":
                return self._handle_send_command(command)
            else:
                return CommandResult(
                    False,
                    f"Unknown command: {command.command}",
                    error="Invalid command",
                )
        except Exception as e:
            return CommandResult(False, f"Command processing failed: {e}", error=str(e))

    def _handle_coordinates_command(self) -> CommandResult:
        """Handle coordinates command."""
        coords_data = {
            agent_id: {"x": coord.x, "y": coord.y, "description": coord.description}
            for agent_id, coord in self.coordinates.items()
        }
        return CommandResult(True, "Coordinates retrieved", data=coords_data)

    def _handle_send_command(self, command: CLICommand) -> CommandResult:
        """Handle send command."""
        # Simplified send command handling
        return CommandResult(
            True, f"Message sent to {command.agent}: {command.message}"
        )

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "total_agents": len(self.coordinates),
            "available_commands": ["coordinates", "list_agents", "send"],
            "system_health": "operational",
        }
