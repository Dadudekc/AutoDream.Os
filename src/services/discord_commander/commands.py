#!/usr/bin/env python3
"""
Discord Commander Commands
==========================

Command handlers for Discord Commander functionality.
V2 Compliance: ≤400 lines, focused command functionality.
"""

import json
import logging

# Add project root to path
import sys
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.consolidated_messaging_service import ConsolidatedMessagingService
from src.services.discord_commander.core import DiscordCommandRegistry

logger = logging.getLogger(__name__)


class AgentCommands:
    """Command handlers for agent-related operations."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(f"{__name__}.AgentCommands")

    async def agent_status(self, ctx, agent_id: str = None) -> str:
        """Get status of agents."""
        try:
            if agent_id:
                # Get specific agent status
                status = await self._get_agent_status(agent_id)
                return f"Agent {agent_id} status: {status}"
            else:
                # Get all agents status
                agents = [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "agent-5",
                    "agent-6",
                    "Agent-7",
                    "Agent-8",
                ]
                statuses = []
                for agent in agents:
                    status = await self._get_agent_status(agent)
                    statuses.append(f"{agent}: {status}")
                return "Agent Status:\n" + "\n".join(statuses)
        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return f"Error getting agent status: {e}"

    async def _get_agent_status(self, agent_id: str) -> str:
        """Get status of a specific agent."""
        try:
            # Check agent workspace
            agent_dir = Path(f"agent_workspaces/{agent_id}")
            if not agent_dir.exists():
                return "Not found"

            # Check for recent activity
            inbox_dir = agent_dir / "inbox"
            if inbox_dir.exists():
                messages = list(inbox_dir.glob("*.json"))
                if messages:
                    latest = max(messages, key=lambda x: x.stat().st_mtime)
                    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                    return f"Active (last message: {mtime.strftime('%H:%M:%S')})"

            return "Inactive"
        except Exception as e:
            return f"Error: {e}"

    async def send_message(self, ctx, agent_id: str, message: str) -> str:
        """Send a message to an agent."""
        try:
            result = await self.messaging_service.send_message(
                agent_id=agent_id, message=message, sender="Discord-Commander"
            )

            if result.get("success"):
                return f"Message sent to {agent_id}: {message}"
            else:
                return f"Failed to send message: {result.get('error', 'Unknown error')}"
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return f"Error sending message: {e}"

    async def agent_coordinates(self, ctx, agent_id: str = None) -> str:
        """Get agent coordinates."""
        try:
            if agent_id:
                coords = await self._get_agent_coordinates(agent_id)
                if coords:
                    return f"{agent_id} coordinates: {coords}"
                else:
                    return f"No coordinates found for {agent_id}"
            else:
                # Get all coordinates
                agents = [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "agent-5",
                    "agent-6",
                    "Agent-7",
                    "Agent-8",
                ]
                coords_list = []
                for agent in agents:
                    coords = await self._get_agent_coordinates(agent)
                    if coords:
                        coords_list.append(f"{agent}: {coords}")
                return "Agent Coordinates:\n" + "\n".join(coords_list)
        except Exception as e:
            self.logger.error(f"Error getting coordinates: {e}")
            return f"Error getting coordinates: {e}"

    async def _get_agent_coordinates(self, agent_id: str) -> str | None:
        """Get coordinates for a specific agent."""
        try:
            coords_file = Path("cursor_agent_coords.json")
            if coords_file.exists():
                with open(coords_file) as f:
                    coords_data = json.load(f)
                return coords_data.get(agent_id)
        except Exception as e:
            self.logger.error(f"Error reading coordinates: {e}")
        return None


class SystemCommands:
    """Command handlers for system-related operations."""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.SystemCommands")

    async def system_status(self, ctx) -> str:
        """Get system status."""
        try:
            status = {
                "timestamp": datetime.now().isoformat(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "discord_available": True,
                "messaging_service": "Available",
                "agent_workspaces": self._count_agent_workspaces(),
            }

            status_text = "System Status:\n"
            for key, value in status.items():
                status_text += f"{key}: {value}\n"

            return status_text
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return f"Error getting system status: {e}"

    def _count_agent_workspaces(self) -> int:
        """Count active agent workspaces."""
        try:
            agent_dir = Path("agent_workspaces")
            if agent_dir.exists():
                return len([d for d in agent_dir.iterdir() if d.is_dir()])
            return 0
        except Exception:
            return 0

    async def project_info(self, ctx) -> str:
        """Get project information."""
        try:
            info = {
                "project_name": "Agent Cellphone V2",
                "version": "2.1.0",
                "description": "Advanced AI Agent System with Code Quality Standards",
                "total_files": self._count_project_files(),
                "python_files": self._count_python_files(),
            }

            info_text = "Project Information:\n"
            for key, value in info.items():
                info_text += f"{key}: {value}\n"

            return info_text
        except Exception as e:
            self.logger.error(f"Error getting project info: {e}")
            return f"Error getting project info: {e}"

    def _count_project_files(self) -> int:
        """Count total project files."""
        try:
            count = 0
            for file_path in Path(".").rglob("*"):
                if file_path.is_file():
                    count += 1
            return count
        except Exception:
            return 0

    def _count_python_files(self) -> int:
        """Count Python files."""
        try:
            count = 0
            for file_path in Path(".").rglob("*.py"):
                if file_path.is_file():
                    count += 1
            return count
        except Exception:
            return 0


class SwarmCommands:
    """Command handlers for swarm-related operations."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(f"{__name__}.SwarmCommands")

    async def swarm_status(self, ctx) -> str:
        """Get swarm status."""
        try:
            agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "agent-5",
                "agent-6",
                "Agent-7",
                "Agent-8",
            ]
            swarm_info = []

            for agent in agents:
                status = await self._get_swarm_agent_status(agent)
                swarm_info.append(f"{agent}: {status}")

            return "Swarm Status:\n" + "\n".join(swarm_info)
        except Exception as e:
            self.logger.error(f"Error getting swarm status: {e}")
            return f"Error getting swarm status: {e}"

    async def _get_swarm_agent_status(self, agent_id: str) -> str:
        """Get swarm status for a specific agent."""
        try:
            agent_dir = Path(f"agent_workspaces/{agent_id}")
            if not agent_dir.exists():
                return "Not initialized"

            # Check for recent activity
            inbox_dir = agent_dir / "inbox"
            if inbox_dir.exists():
                messages = list(inbox_dir.glob("*.json"))
                if messages:
                    return "Active"

            return "Standby"
        except Exception:
            return "Unknown"

    async def swarm_coordinate(self, ctx, message: str) -> str:
        """Send coordination message to all agents."""
        try:
            agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "agent-5",
                "agent-6",
                "Agent-7",
                "Agent-8",
            ]
            results = []

            for agent in agents:
                result = await self.messaging_service.send_message(
                    agent_id=agent,
                    message=f"[SWARM COORDINATION] {message}",
                    sender="Discord-Commander",
                )
                results.append(f"{agent}: {'✓' if result.get('success') else '✗'}")

            return "Swarm Coordination Results:\n" + "\n".join(results)
        except Exception as e:
            self.logger.error(f"Error in swarm coordination: {e}")
            return f"Error in swarm coordination: {e}"


class CommandManager:
    """Manages all Discord commands."""

    def __init__(self, messaging_service: ConsolidatedMessagingService):
        self.messaging_service = messaging_service
        self.command_registry = DiscordCommandRegistry()

        # Initialize command handlers
        self.agent_commands = AgentCommands(messaging_service)
        self.system_commands = SystemCommands()
        self.swarm_commands = SwarmCommands(messaging_service)

        # Register commands
        self._register_commands()

    def _register_commands(self):
        """Register all available commands."""
        # Agent commands
        self.command_registry.register_command(
            "agent_status", self.agent_commands.agent_status, "Get status of agents"
        )
        self.command_registry.register_command(
            "send_message", self.agent_commands.send_message, "Send message to an agent"
        )
        self.command_registry.register_command(
            "agent_coordinates", self.agent_commands.agent_coordinates, "Get agent coordinates"
        )

        # System commands
        self.command_registry.register_command(
            "system_status", self.system_commands.system_status, "Get system status"
        )
        self.command_registry.register_command(
            "project_info", self.system_commands.project_info, "Get project information"
        )

        # Swarm commands
        self.command_registry.register_command(
            "swarm_status", self.swarm_commands.swarm_status, "Get swarm status"
        )
        self.command_registry.register_command(
            "swarm_coordinate",
            self.swarm_commands.swarm_coordinate,
            "Send coordination message to all agents",
        )

    def get_command_handler(self, command_name: str):
        """Get command handler by name."""
        return self.command_registry.get_command(command_name)

    def list_commands(self) -> list[str]:
        """List all available commands."""
        return self.command_registry.list_commands()
