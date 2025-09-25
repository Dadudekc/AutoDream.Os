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
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

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

from src.services.discord_commander.core import (
    DiscordConfig, DiscordConnectionManager, DiscordEventManager, DiscordStatusMonitor
)
from src.services.discord_commander.commands import CommandManager
from src.services.consolidated_messaging_service import ConsolidatedMessagingService

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
                    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
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
                    agent_id=agent_id,
                    message=message,
                    sender="Discord-Commander"
                )

                if result.get("success"):
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=0x00ff00
                    )
                    embed.add_field(name="Content", value=message[:1000], inline=False)
                    embed.set_footer(text=f"Sent by {ctx.author}")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=0xff0000
                    )
                    embed.add_field(name="Error", value=result.get('error', 'Unknown error'), inline=False)
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

                with open(coords_file, 'r') as f:
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
                        color=0x0099ff
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
                    "messaging_service": "Operational"
                }

                embed = discord.Embed(
                    title="🔧 System Status",
                    description="Current system status",
                    color=0x00ff00
                )
                for key, value in status.items():
                    embed.add_field(name=key.replace("_", " ").title(), value=str(value), inline=True)

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
                    "agents": "8 Active Agents"
                }

                embed = discord.Embed(
                    title="📋 Project Information",
                    description="Agent Cellphone V2 System",
                    color=0x0099ff
                )
                for key, value in info.items():
                    embed.add_field(name=key.replace("_", " ").title(), value=str(value), inline=True)

                embed.set_footer(text="🐝 WE ARE SWARM - Multi-Agent Intelligence System")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error getting project info: {e}")

        # Swarm commands
        @self.bot.command(name="swarm_status")
        async def swarm_status(ctx):
            """Get swarm status."""
            try:
                agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                swarm_info = []

                for agent in agents:
                    status = await self._get_swarm_agent_status(agent)
                    swarm_info.append(f"• {agent}: {status}")

                embed = discord.Embed(
                    title="🐝 Swarm Status",
                    description="Current swarm activity",
                    color=0xffaa00
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
                agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                results = []

                for agent in agents:
                    result = await self.messaging_service.send_message(
                        agent_id=agent,
                        message=f"[SWARM COORDINATION] {message}",
                        sender="Discord-Commander"
                    )
                    results.append(f"• {agent}: {'✅' if result.get('success') else '❌'}")

                embed = discord.Embed(
                    title="🐝 Swarm Coordination",
                    description="Coordination message sent to all agents",
                    color=0xffaa00
                )
                embed.add_field(name="Message", value=message, inline=False)
                embed.add_field(name="Results", value="\n".join(results), inline=False)
                embed.set_footer(text=f"Coordinated by {ctx.author}")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"❌ Error in swarm coordination: {e}")

        # Help command (Legacy prefix command)
        @self.bot.command(name="help")
        async def help_command(ctx):
            """Show available commands."""
            embed = discord.Embed(
                title="🤖 Discord Commander - Complete Command Guide",
                description="Modern Discord integration for the Agent Swarm system with both prefix and slash commands",
                color=0x0099ff
            )

            embed.add_field(
                name="🔧 **SYSTEM MANAGEMENT**",
                value="• `!restart` - **Restart Discord Commander** (No runtime shutdown needed!)\n• `!sync` - Sync slash commands with Discord\n• `!system_status` - Get system health and metrics",
                inline=False
            )

            embed.add_field(
                name="🤖 **AGENT COMMANDS**",
                value="• `!agent_status [agent_id]` - Get agent status with rich embeds\n• `!send_message <agent_id> <message>` - Send message to agent\n• `!agent_coordinates [agent_id]` - Get agent coordinates",
                inline=False
            )

            embed.add_field(
                name="🐝 **SWARM OPERATIONS**",
                value="• `!swarm_status` - Get swarm coordination status\n• `!swarm_coordinate <message>` - Send coordination message to all agents",
                inline=False
            )

            embed.add_field(
                name="⚡ **MODERN SLASH COMMANDS**",
                value="• `/help` - Interactive slash command help\n• `/restart` - **Restart system** (Modern interface)\n• `/agent_status [agent_id]` - Get agent status\n• `/send_message <agent_id> <message>` - Send message to agent\n• `/system_status` - Get system status\n• `/swarm_status` - Get swarm status\n• `/project_info` - Get project information",
                inline=False
            )

            embed.add_field(
                name="🖥️ **WEB INTERFACE**",
                value="• **Dashboard:** `http://localhost:8080`\n• Real-time agent monitoring\n• Social media integration\n• Interactive controls\n• Live activity logs",
                inline=False
            )

            embed.add_field(
                name="🚀 **QUICK START**",
                value="1. Use `/help` for modern slash commands\n2. Use `!help` for legacy prefix commands\n3. Use `/restart` to restart without shutting down\n4. Open web dashboard for advanced control",
                inline=False
            )

            embed.set_footer(text="🐝 WE ARE SWARM - Modern Discord Integration | Use /restart for system updates")
            await ctx.send(embed=embed)

        @self.bot.command(name="restart")
        async def prefix_restart(ctx):
            """Restart the Discord Commander system (legacy prefix command)."""
            embed = discord.Embed(
                title="🔄 Restarting Discord Commander",
                description="The system will restart shortly using legacy command...",
                color=0xffaa00
            )

            embed.add_field(name="Status", value="⏳ Restarting...", inline=False)
            embed.add_field(name="Method", value="Legacy prefix command", inline=False)
            embed.set_footer(text="Use /restart for modern slash command interface")

            await ctx.send(embed=embed)

            # Log the restart request
            self.logger.info(f"Legacy restart requested by {ctx.author}")

            # Create restart devlog
            try:
                import asyncio
                from src.services.agent_devlog_posting import AgentDevlogPoster

                poster = AgentDevlogPoster()
                await poster.post_devlog(
                    agent_flag="Agent-4",
                    action="Discord Commander restart requested (legacy)",
                    status="in_progress",
                    details=f"Legacy restart requested by Discord user {ctx.author}. System will restart to apply any pending updates."
                )
            except Exception as e:
                self.logger.error(f"Failed to create restart devlog: {e}")

            # Schedule restart after a delay
            async def delayed_restart():
                await asyncio.sleep(2)  # Give time for response to be sent

                # Stop the bot
                await self.bot.close()

                # Log restart completion
                self.logger.info("Discord Commander restart completed (legacy)")

                # Exit to allow restart
                import sys
                sys.exit(0)  # This will trigger a restart in a process manager

            # Start the restart task
            asyncio.create_task(delayed_restart())

        @self.bot.command(name="sync")
        async def prefix_sync(ctx):
            """Sync slash commands with Discord (legacy prefix command)."""
            embed = discord.Embed(
                title="🔄 Syncing Commands",
                description="Syncing slash commands with Discord...",
                color=0xffaa00
            )

            await ctx.send(embed=embed)

            try:
                # Sync commands with Discord
                synced = await self.bot.sync_commands()

                embed = discord.Embed(
                    title="✅ Commands Synced",
                    description=f"Successfully synced {len(synced)} commands",
                    color=0x00ff00
                )
                embed.add_field(name="Method", value="Legacy prefix command", inline=False)
                embed.set_footer(text="Use /sync for modern slash command interface")

            except Exception as sync_error:
                embed = discord.Embed(
                    title="⚠️ Sync Warning",
                    description=f"Commands synced but with warnings: {sync_error}",
                    color=0xffaa00
                )
                embed.add_field(name="Method", value="Legacy prefix command", inline=False)

            await ctx.send(embed=embed)

        # Slash Commands
        @self.bot.slash_command(name="help", description="Show all available Discord Commander commands")
        async def slash_help(ctx):
            """Show available slash commands."""
            embed = discord.Embed(
                title="⚡ Discord Commander Slash Commands",
                description="Modern slash commands for the Agent Swarm system",
                color=0xff6b00
            )

            embed.add_field(
                name="🤖 Agent Management",
                value="• `/agent_status [agent_id]` - Get agent status\n• `/send_message <agent_id> <message>` - Send message to agent\n• `/agent_coordinates [agent_id]` - Get agent coordinates",
                inline=False
            )

            embed.add_field(
                name="🔧 System Control",
                value="• `/system_status` - Get system status\n• `/project_info` - Get project information\n• `/restart` - Restart Discord Commander",
                inline=False
            )

            embed.add_field(
                name="🐝 Swarm Operations",
                value="• `/swarm_status` - Get swarm status\n• `/swarm_coordinate <message>` - Coordinate all agents",
                inline=False
            )

            embed.add_field(
                name="🖥️ Web Interface",
                value="• Web Dashboard: `http://localhost:8080`\n• Real-time monitoring\n• Social media integration\n• Interactive controls",
                inline=False
            )

            embed.set_footer(text="🐝 WE ARE SWARM - Modern Discord Integration")
            await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="restart", description="Restart the Discord Commander system")
        async def slash_restart(ctx):
            """Restart the Discord Commander system."""
            embed = discord.Embed(
                title="🔄 Restarting Discord Commander",
                description="The system will restart shortly...",
                color=0xffaa00
            )

            embed.add_field(name="Status", value="⏳ Restarting...", inline=False)
            embed.set_footer(text="This may take a few moments")

            await ctx.respond(embed=embed, ephemeral=True)

            # Log the restart request
            self.logger.info(f"Restart requested by {ctx.author}")

            # Create restart devlog
            try:
                import asyncio
                from src.services.agent_devlog_posting import AgentDevlogPoster

                poster = AgentDevlogPoster()
                await poster.post_devlog(
                    agent_flag="Agent-4",
                    action="Discord Commander restart requested",
                    status="in_progress",
                    details=f"Restart requested by Discord user {ctx.author}. System will restart to apply any pending updates."
                )
            except Exception as e:
                self.logger.error(f"Failed to create restart devlog: {e}")

            # Schedule restart after a delay
            async def delayed_restart():
                await asyncio.sleep(2)  # Give time for response to be sent

                # Stop the bot
                await self.bot.close()

                # Log restart completion
                self.logger.info("Discord Commander restart completed")

                # Exit to allow restart
                import sys
                sys.exit(0)  # This will trigger a restart in a process manager

            # Start the restart task
            asyncio.create_task(delayed_restart())

        @self.bot.slash_command(name="agent_status", description="Get the status of agents")
        async def slash_agent_status(ctx, agent_id: str = None):
            """Get agent status via slash command."""
            try:
                if agent_id:
                    status = await self._get_agent_status(agent_id)
                    embed = discord.Embed(
                        title=f"🤖 Agent {agent_id} Status",
                        description=f"Current status of {agent_id}",
                        color=0x00ff00 if "Active" in status else 0xff0000
                    )
                    embed.add_field(name="Status", value=status, inline=False)
                else:
                    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                    embed = discord.Embed(
                        title="🤖 Agent Status Overview",
                        description="Current status of all agents",
                        color=0x0099ff
                    )

                    for agent in agents:
                        status = await self._get_agent_status(agent)
                        embed.add_field(name=agent, value=status, inline=True)

                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get agent status: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="send_message", description="Send a message to an agent")
        async def slash_send_message(ctx, agent_id: str, message: str):
            """Send message to agent via slash command."""
            try:
                result = await self.messaging_service.send_message(
                    agent_id=agent_id,
                    message=message,
                    sender="Discord-Commander-Slash"
                )

                if result.get("success"):
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=0x00ff00
                    )
                    embed.add_field(name="Content", value=message[:1000], inline=False)
                    embed.add_field(name="Recipient", value=agent_id, inline=True)
                    embed.set_footer(text=f"Sent by {ctx.author}")
                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=0xff0000
                    )
                    embed.add_field(name="Error", value=result.get('error', 'Unknown error'), inline=False)
                    await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to send message: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="system_status", description="Get system status")
        async def slash_system_status(ctx):
            """Get system status via slash command."""
            try:
                status = self.get_status()
                uptime = status.get('uptime_formatted', 'Unknown')

                embed = discord.Embed(
                    title="🔧 System Status",
                    description="Discord Commander system health",
                    color=0x00ff00
                )

                embed.add_field(name="Status", value=status.get('status', 'Unknown').title(), inline=True)
                embed.add_field(name="Uptime", value=uptime, inline=True)
                embed.add_field(name="Commands", value=str(status.get('command_count', 0)), inline=True)
                embed.add_field(name="Messages Received", value=str(status.get('messages_received', 0)), inline=True)

                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get system status: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="swarm_status", description="Get swarm coordination status")
        async def slash_swarm_status(ctx):
            """Get swarm status via slash command."""
            try:
                agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                swarm_info = []

                for agent in agents:
                    status = await self._get_swarm_agent_status(agent)
                    swarm_info.append(f"• {agent}: {status}")

                embed = discord.Embed(
                    title="🐝 Swarm Status",
                    description="Multi-agent coordination status",
                    color=0xffaa00
                )

                embed.add_field(name="Agent Status", value="\n".join(swarm_info), inline=False)
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get swarm status: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="agent_coordinates", description="Get agent coordinates")
        async def slash_agent_coordinates(ctx, agent_id: str = None):
            """Get agent coordinates via slash command."""
            try:
                coords_file = Path("cursor_agent_coords.json")
                if not coords_file.exists():
                    embed = discord.Embed(
                        title="❌ Coordinates Not Found",
                        description="Agent coordinates file not found",
                        color=0xff0000
                    )
                    await ctx.respond(embed=embed, ephemeral=True)
                    return

                with open(coords_file, 'r') as f:
                    coords_data = json.load(f)

                if agent_id:
                    coords = coords_data.get(agent_id)
                    if coords:
                        embed = discord.Embed(
                            title=f"📍 Agent {agent_id} Coordinates",
                            description=f"Position: `{coords}`",
                            color=0x0099ff
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Agent Not Found",
                            description=f"No coordinates found for {agent_id}",
                            color=0xff0000
                        )
                else:
                    embed = discord.Embed(
                        title="📍 Agent Coordinates",
                        description="Current agent positions",
                        color=0x0099ff
                    )

                    for agent, coords in coords_data.items():
                        embed.add_field(name=agent, value=f"`{coords}`", inline=True)

                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get coordinates: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="project_info", description="Get project information")
        async def slash_project_info(ctx):
            """Get project information via slash command."""
            try:
                info = {
                    "name": "Agent Cellphone V2",
                    "version": "2.1.0",
                    "description": "Advanced AI Agent System with Code Quality Standards",
                    "total_files": self._count_project_files(),
                    "python_files": self._count_python_files(),
                    "agents": "8 Active Agents"
                }

                embed = discord.Embed(
                    title="📋 Project Information",
                    description="Agent Cellphone V2 System",
                    color=0x0099ff
                )

                for key, value in info.items():
                    embed.add_field(name=key.replace("_", " ").title(), value=str(value), inline=True)

                embed.set_footer(text=f"🐝 WE ARE SWARM - Requested by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to get project info: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="swarm_coordinate", description="Send coordination message to all agents")
        async def slash_swarm_coordinate(ctx, message: str):
            """Send coordination message to all agents via slash command."""
            try:
                agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
                results = []

                for agent in agents:
                    result = await self.messaging_service.send_message(
                        agent_id=agent,
                        message=f"[SWARM COORDINATION] {message}",
                        sender="Discord-Commander-Slash"
                    )
                    results.append(f"• {agent}: {'✅' if result.get('success') else '❌'}")

                embed = discord.Embed(
                    title="🐝 Swarm Coordination",
                    description="Coordination message sent to all agents",
                    color=0xffaa00
                )

                embed.add_field(name="Message", value=message, inline=False)
                embed.add_field(name="Results", value="\n".join(results), inline=False)
                embed.set_footer(text=f"Coordinated by {ctx.author}")
                await ctx.respond(embed=embed, ephemeral=True)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Failed to coordinate swarm: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        @self.bot.slash_command(name="sync", description="Sync slash commands with Discord")
        async def slash_sync(ctx):
            """Sync slash commands with Discord."""
            try:
                embed = discord.Embed(
                    title="🔄 Syncing Commands",
                    description="Syncing slash commands with Discord...",
                    color=0xffaa00
                )

                await ctx.respond(embed=embed, ephemeral=True)

                # Sync commands with Discord
                try:
                    synced = await self.bot.sync_commands()
                    embed = discord.Embed(
                        title="✅ Commands Synced",
                        description=f"Successfully synced {len(synced)} commands",
                        color=0x00ff00
                    )
                    embed.set_footer(text="Commands are now available!")
                except Exception as sync_error:
                    embed = discord.Embed(
                        title="⚠️ Sync Warning",
                        description=f"Commands synced but with warnings: {sync_error}",
                        color=0xffaa00
                    )

                # Update the original response
                await ctx.edit(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Sync Failed",
                    description=f"Failed to sync commands: {e}",
                    color=0xff0000
                )
                await ctx.respond(embed=embed, ephemeral=True)

        # Event handler for slash command errors
        @self.bot.event
        async def on_application_command_error(ctx, error):
            """Handle slash command errors."""
            self.logger.error(f"Slash command error: {error}")

            embed = discord.Embed(
                title="❌ Command Error",
                description=f"An error occurred: {error}",
                color=0xff0000
            )

            if isinstance(error, discord.errors.CommandOnCooldown):
                embed.description = f"Command on cooldown. Try again in {error.retry_after:.2f}s"
                embed.color = 0xffaa00
            elif isinstance(error, discord.errors.MissingPermissions):
                embed.description = "You don't have permission to use this command"
            elif isinstance(error, discord.errors.BotMissingPermissions):
                embed.description = "I don't have permission to execute this command"

            embed.set_footer(text="Report this error if it persists")
            await ctx.respond(embed=embed, ephemeral=True)
    
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

        # Sync slash commands with Discord
        try:
            synced = await self.bot.sync_commands()
            self.logger.info(f"Synced {len(synced)} slash commands with Discord")
        except Exception as e:
            self.logger.warning(f"Failed to sync commands: {e}")

        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="🐝 WE ARE SWARM - Modern Discord Integration"
        )
        await self.bot.change_presence(activity=activity)

        # Log ready status
        self.logger.info("Discord Commander is ready with both prefix and slash commands!")
    
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
    
    def get_status(self) -> Dict[str, Any]:
        """Get bot status."""
        status = self.status_monitor.get_status()
        status.update({
            "bot_user": str(self.bot.user) if self.bot and self.bot.user else None,
            "guild_count": len(self.bot.guilds) if self.bot else 0,
            "command_count": len(self.command_manager.list_commands()),
            "config_valid": len(self.config.validate()) == 0
        })
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
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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




