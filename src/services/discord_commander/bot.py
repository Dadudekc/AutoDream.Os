#!/usr/bin/env python3
"""
Discord Commander Bot
=====================

Main Discord bot implementation using modular components.
V2 Compliance: ≤400 lines, focused bot functionality.

Features:
- Rich Discord embeds for better user experience
- Comprehensive command system with error handling
- Real-time agent status monitoring
- Swarm coordination capabilities
- Interactive help system
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv

    dotenv_path = Path(__file__).parent.parent.parent.parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
except ImportError:
    pass

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
from src.services.messaging_service import ConsolidatedMessagingService
from src.services.discord_commander.commands import CommandManager
from src.services.discord_commander.core import (
    DiscordConfig,
    DiscordConnectionManager,
    DiscordEventManager,
    DiscordStatusMonitor,
)

logger = logging.getLogger(__name__)


class DiscordCommanderBot:
    """Main Discord Commander Bot implementation."""

    def __init__(self):
        """Initialize the Discord Commander Bot."""
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.config = DiscordConfig()
        self.connection_manager = DiscordConnectionManager(self.config)
        self.event_manager = DiscordEventManager()
        self.status_monitor = DiscordStatusMonitor()
        self.messaging_service = ConsolidatedMessagingService()
        self.command_manager = CommandManager(self.messaging_service)

        # Bot instance
        self.bot = None

        # Register event handlers
        self._register_event_handlers()

    def _register_event_handlers(self):
        """Register event handlers."""
        self.event_manager.register_event_handler("on_ready", self._on_ready)
        self.event_manager.register_event_handler("on_message", self._on_message)
        self.event_manager.register_event_handler("on_command", self._on_command)

    async def initialize(self) -> bool:
        """Initialize the bot."""
        self.logger.info("Initializing Discord Commander Bot...")

        # Validate configuration
        config_issues = self.config.validate()
        if config_issues:
            self.logger.error(f"Configuration issues: {config_issues}")
            return False

        # Create bot
        self.bot = await self.connection_manager.create_bot()
        if not self.bot:
            self.logger.error("Failed to create Discord bot")
            return False

        # Register commands
        await self._register_discord_commands()

        self.logger.info("Discord Commander Bot initialized successfully")
        return True

    async def _register_discord_commands(self):
        """Register Discord commands."""
        if not self.bot:
            return

        # Agent commands
        @self.bot.command(name="agent_status")
        async def agent_status(ctx, agent_id: str = None):
            """Get status of agents."""
            try:
                if agent_id:
                    # Get specific agent status
                    status = await self._get_agent_status(agent_id)
                    await ctx.send(f"🤖 Agent {agent_id} status: {status}")
                else:
                    # Get all agents status
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
                    status_text = "🤖 **Agent Status:**\n"
                    for agent in agents:
                        status = await self._get_agent_status(agent)
                        status_text += f"• {agent}: {status}\n"
                    await ctx.send(status_text)
            except Exception as e:
                await ctx.send(f"❌ Error getting agent status: {e}")

        @self.bot.command(name="send_message")
        async def send_message(ctx, agent_id: str, *, message: str):
            """Send a message to an agent."""
            try:
                result = await self.messaging_service.send_message(
                    agent_id=agent_id, message=message, sender="Discord-Commander"
                )

                if result.get("success"):
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=0x00FF00,
                    )
                    embed.add_field(name="Content", value=message[:1000], inline=False)
                    embed.set_footer(text=f"Sent by {ctx.author}")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=0xFF0000,
                    )
                    embed.add_field(
                        name="Error", value=result.get("error", "Unknown error"), inline=False
                    )
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error sending message: {e}")

        @self.bot.command(name="agent_coordinates")
        async def agent_coordinates(ctx, agent_id: str = None):
            """Get agent coordinates."""
            try:
                coords_file = Path("cursor_agent_coords.json")
                if not coords_file.exists():
                    await ctx.send("❌ Coordinates file not found")
                    return

                with open(coords_file) as f:
                    coords_data = json.load(f)

                if agent_id:
                    coords = coords_data.get(agent_id)
                    if coords:
                        await ctx.send(f"📍 **{agent_id}** coordinates: `{coords}`")
                    else:
                        await ctx.send(f"❌ No coordinates found for {agent_id}")
                else:
                    embed = discord.Embed(
                        title="📍 Agent Coordinates",
                        description="Current agent positions",
                        color=0x0099FF,
                    )
                    for agent, coords in coords_data.items():
                        embed.add_field(name=agent, value=f"`{coords}`", inline=True)
                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting coordinates: {e}")

        # System commands
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

        # Swarm commands
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
                results = []

                for agent in agents:
                    result = await self.messaging_service.send_message(
                        agent_id=agent,
                        message=f"[SWARM COORDINATION] {message}",
                        sender="Discord-Commander",
                    )
                    results.append(f"• {agent}: {'✅' if result.get('success') else '❌'}")

                embed = discord.Embed(
                    title="🐝 Swarm Coordination",
                    description="Coordination message sent to all agents",
                    color=0xFFAA00,
                )
                embed.add_field(name="Message", value=message, inline=False)
                embed.add_field(name="Results", value="\n".join(results), inline=False)
                embed.set_footer(text=f"Coordinated by {ctx.author}")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error in swarm coordination: {e}")

        # Help command
        @self.bot.command(name="help")
        async def help_command(ctx):
            """Show available commands."""
            embed = discord.Embed(
                title="🤖 Discord Commander Help",
                description="Available commands for the Agent Swarm system",
                color=0x0099FF,
            )

            embed.add_field(
                name="🤖 Agent Commands",
                value="• `!agent_status [agent_id]` - Get agent status\n• `!send_message <agent_id> <message>` - Send message to agent\n• `!agent_coordinates [agent_id]` - Get agent coordinates",
                inline=False,
            )

            embed.add_field(
                name="🔧 System Commands",
                value="• `!system_status` - Get system status\n• `!project_info` - Get project information",
                inline=False,
            )

            embed.add_field(
                name="🐝 Swarm Commands",
                value="• `!swarm_status` - Get swarm status\n• `!swarm_coordinate <message>` - Send coordination message to all agents",
                inline=False,
            )

            embed.set_footer(text="🐝 WE ARE SWARM - Use the web interface for advanced control")
            await ctx.send(embed=embed)

    async def start(self) -> bool:
        """Start the bot."""
        if not self.bot:
            self.logger.error("Bot not initialized")
            return False

        try:
            self.logger.info("Starting Discord Commander Bot...")
            await self.connection_manager.connect()
            return True
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            return False

    async def stop(self):
        """Stop the bot."""
        self.logger.info("Stopping Discord Commander Bot...")
        await self.connection_manager.disconnect()

    async def _on_ready(self):
        """Handle bot ready event."""
        self.logger.info(f"Discord Commander Bot ready: {self.bot.user}")
        self.status_monitor.record_heartbeat()

        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching, name="Agent Swarm Coordination"
        )
        await self.bot.change_presence(activity=activity)

    async def _on_message(self, message):
        """Handle message events."""
        if message.author == self.bot.user:
            return

        self.status_monitor.record_message()

        # Process commands
        if message.content.startswith(self.config.command_prefix):
            await self.bot.process_commands(message)

    async def _on_command(self, ctx):
        """Handle command events."""
        self.status_monitor.record_command()
        self.logger.info(f"Command executed: {ctx.command} by {ctx.author}")

    def get_status(self) -> dict[str, Any]:
        """Get bot status."""
        status = self.status_monitor.get_status()
        status.update(
            {
                "bot_user": str(self.bot.user) if self.bot and self.bot.user else None,
                "guild_count": len(self.bot.guilds) if self.bot else 0,
                "command_count": len(self.command_manager.list_commands()),
                "config_valid": len(self.config.validate()) == 0,
            }
        )
        return status

    def is_healthy(self) -> bool:
        """Check if bot is healthy."""
        return self.status_monitor.is_healthy()

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


async def main():
    """Main function to run the Discord Commander Bot."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not installed! Please install: pip install discord.py")
        return

    # Create and start bot
    bot = DiscordCommanderBot()

    try:
        if await bot.initialize():
            await bot.start()
        else:
            print("❌ Failed to initialize Discord Commander Bot")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Discord Commander Bot...")
    except Exception as e:
        print(f"❌ Error running Discord Commander Bot: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())


# Export for external use
__all__ = ["DiscordCommanderBot"]
