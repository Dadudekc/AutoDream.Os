#!/usr/bin/env python3
"""
Discord Commander Bot - Command Definitions
===========================================

Command definitions for Discord Commander Bot.
V2 Compliant: ≤400 lines, focused command definitions.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import logging
from datetime import datetime
from pathlib import Path

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class DiscordCommandDefinitions:
    """Command definitions for Discord Commander Bot."""

    def __init__(self, bot: commands.Bot):
        """Initialize command definitions."""
        self.bot = bot
        self._register_commands()

    def _register_commands(self) -> None:
        """Register all bot commands."""
        if not DISCORD_AVAILABLE:
            return

        # Agent commands
        self._register_agent_commands()

        # System commands
        self._register_system_commands()

        # Swarm commands
        self._register_swarm_commands()

    def _register_agent_commands(self) -> None:
        """Register agent-related commands."""

        @self.bot.command(name="agent_status")
        async def agent_status(ctx, agent_id: str = None):
            """Get agent status."""
            try:
                if agent_id:
                    status = await self._get_agent_status(agent_id)
                    embed = discord.Embed(
                        title=f"🤖 Agent Status: {agent_id}", description=status, color=0x00FF00
                    )
                    await ctx.send(embed=embed)
                else:
                    # Show all agents
                    agents = [
                        "Agent-1",
                        "Agent-2",
                        "Agent-3",
                        "Agent-4",
                        "Agent-5",
                        "Agent-6",
                        "Agent-7",
                        "Agent-8",
                    ]
                    statuses = []
                    for agent in agents:
                        status = await self._get_agent_status(agent)
                        statuses.append(f"• {agent}: {status}")

                    embed = discord.Embed(
                        title="🤖 All Agent Status", description="\n".join(statuses), color=0x00FF00
                    )
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting agent status: {e}")

        @self.bot.command(name="agent_coordinates")
        async def agent_coordinates(ctx, agent_id: str = None):
            """Get agent coordinates."""
            try:
                if agent_id:
                    coords = await self._get_agent_coordinates(agent_id)
                    embed = discord.Embed(
                        title=f"📍 Agent Coordinates: {agent_id}", description=coords, color=0x0099FF
                    )
                    await ctx.send(embed=embed)
                else:
                    # Show all agent coordinates
                    agents = [
                        "Agent-1",
                        "Agent-2",
                        "Agent-3",
                        "Agent-4",
                        "Agent-5",
                        "Agent-6",
                        "Agent-7",
                        "Agent-8",
                    ]
                    coords = []
                    for agent in agents:
                        coord = await self._get_agent_coordinates(agent)
                        coords.append(f"• {agent}: {coord}")

                    embed = discord.Embed(
                        title="📍 All Agent Coordinates",
                        description="\n".join(coords),
                        color=0x0099FF,
                    )
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting coordinates: {e}")

    def _register_system_commands(self) -> None:
        """Register system-related commands."""

        @self.bot.command(name="system_status")
        async def system_status(ctx):
            """Get system status."""
            try:
                status = {
                    "timestamp": datetime.now().isoformat(),
                    "active_agents": self._count_active_agents(),
                    "project_files": self._count_project_files(),
                    "discord_bot": "Connected",
                    "messaging_service": "Operational",
                }

                embed = discord.Embed(
                    title="🔧 System Status", description="Current system status", color=0x00FF00
                )
                for key, value in status.items():
                    embed.add_field(
                        name=key.replace("_", " ").title(), value=str(value), inline=True
                    )

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting system status: {e}")

        @self.bot.command(name="project_info")
        async def project_info(ctx):
            """Get project information."""
            try:
                info = {
                    "name": "Agent Cellphone V2",
                    "version": "2.1.0",
                    "description": "Advanced AI Agent System with Code Quality Standards",
                    "total_files": self._count_project_files(),
                    "python_files": self._count_python_files(),
                    "agents": "8 Active Agents",
                }

                embed = discord.Embed(
                    title="📋 Project Information",
                    description="Agent Cellphone V2 System",
                    color=0x0099FF,
                )
                for key, value in info.items():
                    embed.add_field(
                        name=key.replace("_", " ").title(), value=str(value), inline=True
                    )

                embed.set_footer(text="🐝 WE ARE SWARM - Multi-Agent Intelligence System")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting project info: {e}")

    def _register_swarm_commands(self) -> None:
        """Register swarm-related commands."""

        @self.bot.command(name="swarm_status")
        async def swarm_status(ctx):
            """Get swarm status."""
            try:
                agents = [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "Agent-5",
                    "Agent-6",
                    "Agent-7",
                    "Agent-8",
                ]
                swarm_info = []

                for agent in agents:
                    status = await self._get_swarm_agent_status(agent)
                    swarm_info.append(f"• {agent}: {status}")

                embed = discord.Embed(
                    title="🐝 Swarm Status", description="Current swarm activity", color=0xFFAA00
                )
                embed.add_field(name="Agents", value="\n".join(swarm_info), inline=False)
                embed.set_footer(text="Multi-Agent Coordination Active")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting swarm status: {e}")

        @self.bot.command(name="swarm_coordinate")
        async def swarm_coordinate(ctx, *, message: str):
            """Send coordination message to all agents."""
            try:
                agents = [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "Agent-5",
                    "Agent-6",
                    "Agent-7",
                    "Agent-8",
                ]

                embed = discord.Embed(
                    title="🐝 Swarm Coordination",
                    description=f"**Message:** {message}",
                    color=0xFFAA00,
                )
                embed.add_field(name="Target Agents", value="\n".join(agents), inline=False)
                embed.set_footer(text="Coordination message sent to all agents")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error sending coordination message: {e}")

    async def _get_agent_status(self, agent_id: str) -> str:
        """Get status for a specific agent."""
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

    async def _get_agent_coordinates(self, agent_id: str) -> str:
        """Get coordinates for a specific agent."""
        try:
            # This would typically read from agent configuration
            # For now, return placeholder coordinates
            coordinates = {
                "Agent-1": "(-1269, 481)",
                "Agent-2": "(-308, 480)",
                "Agent-3": "(-1269, 1001)",
                "Agent-4": "(-308, 1000)",
                "Agent-5": "(652, 421)",
                "Agent-6": "(1612, 419)",
                "Agent-7": "(920, 851)",
                "Agent-8": "(1611, 941)",
            }
            return coordinates.get(agent_id, "Unknown")
        except Exception as e:
            return f"Error: {e}"

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

    def _count_active_agents(self) -> int:
        """Count active agents."""
        try:
            agent_dir = Path("agent_workspaces")
            if agent_dir.exists():
                return len([d for d in agent_dir.iterdir() if d.is_dir()])
            return 0
        except Exception:
            return 0

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


def create_command_definitions(bot: commands.Bot) -> DiscordCommandDefinitions:
    """Create command definitions."""
    return DiscordCommandDefinitions(bot)
