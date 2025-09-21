#!/usr/bin/env python3
"""
Discord Bot Basic Commands
==========================

Basic command setup for the Discord bot.
Provides fundamental commands for bot interaction.

V2 Compliance: ≤400 lines, 1 class, 5 functions
"""

import discord
from discord.ext import commands
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def setup_basic_commands(bot: commands.Bot):
    """Setup basic Discord bot commands."""

    @bot.command(name="ping", help="Check bot responsiveness")
    async def ping(ctx):
        """Check bot ping/latency."""
        try:
            latency = round(bot.latency * 1000)
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"**Latency:** {latency}ms",
                color=0x00ff00
            )
            embed.set_footer(text="🐝 WE ARE SWARM - Discord Commander Active")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in ping command: {e}")
            await ctx.send("❌ Error processing ping command")

    @bot.command(name="status", help="Get Discord Commander status")
    async def status(ctx):
        """Get Discord Commander status."""
        try:
            embed = discord.Embed(
                title="🐝 Discord Commander Status",
                color=0x0099ff
            )

            embed.add_field(
                name="Commander",
                value="Active" if bot.is_ready else "Offline",
                inline=True
            )

            embed.add_field(
                name="Agent ID",
                value=getattr(bot, 'agent_id', 'Discord-Commander'),
                inline=True
            )

            embed.add_field(
                name="Guilds",
                value=len(bot.guilds),
                inline=True
            )

            embed.add_field(
                name="Latency",
                value=f"{round(bot.latency * 1000)}ms" if bot.latency else "Unknown",
                inline=True
            )

            embed.set_footer(text="WE ARE SWARM - Agent Coordination Active")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await ctx.send("❌ Error getting status")

    @bot.command(name="help", help="Show available commands")
    async def help_command(ctx):
        """Show available Discord bot commands."""
        try:
            embed = discord.Embed(
                title="🐝 Discord Commander Help",
                description="Available Commands:",
                color=0x0099ff
            )

            embed.add_field(
                name="!ping",
                value="Check bot responsiveness and latency",
                inline=False
            )

            embed.add_field(
                name="!status",
                value="Get Discord Commander status information",
                inline=False
            )

            embed.add_field(
                name="!help",
                value="Show this help message",
                inline=False
            )

            embed.add_field(
                name="!swarm",
                value="Get swarm coordination status",
                inline=False
            )

            embed.add_field(
                name="!agents",
                value="List connected agents",
                inline=False
            )

            embed.set_footer(text="🐝 WE ARE SWARM - Use @DiscordCommander to mention me!")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await ctx.send("❌ Error showing help")

    @bot.command(name="swarm", help="Get swarm coordination status")
    async def swarm_status(ctx):
        """Get swarm coordination status."""
        try:
            embed = discord.Embed(
                title="🐝 Swarm Coordination Status",
                color=0xffaa00
            )

            embed.add_field(
                name="Swarm Status",
                value="Active",
                inline=True
            )

            embed.add_field(
                name="Connected Agents",
                value=len(getattr(bot, 'connected_agents', set())),
                inline=True
            )

            embed.add_field(
                name="Active Tasks",
                value="Monitoring",
                inline=True
            )

            embed.add_field(
                name="Coordination Mode",
                value="Real-time",
                inline=True
            )

            embed.set_footer(text="WE ARE SWARM - Agent Intelligence Collective")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in swarm command: {e}")
            await ctx.send("❌ Error getting swarm status")

    @bot.command(name="agents", help="List connected agents")
    async def list_agents(ctx):
        """List connected agents."""
        try:
            connected_agents = getattr(bot, 'connected_agents', set())
            if not connected_agents:
                await ctx.send("🤖 **No agents currently connected**")
                return

            embed = discord.Embed(
                title="🤖 Connected Agents",
                description=f"Total: {len(connected_agents)} agents",
                color=0x00aa00
            )

            for i, agent in enumerate(connected_agents, 1):
                embed.add_field(
                    name=f"Agent {i}",
                    value=agent,
                    inline=True
                )

            embed.set_footer(text="🐝 WE ARE SWARM - Agent Network Active")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in agents command: {e}")
            await ctx.send("❌ Error listing agents")


class BasicCommandHandler:
    """Basic command handler for Discord bot."""

    def __init__(self, bot: commands.Bot):
        """Initialize basic command handler."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.BasicCommandHandler")

    def get_command_list(self) -> Dict[str, str]:
        """Get list of available commands."""
        return {
            "ping": "Check bot responsiveness",
            "status": "Get Discord Commander status",
            "help": "Show available commands",
            "swarm": "Get swarm coordination status",
            "agents": "List connected agents"
        }

    def get_command_help(self, command_name: str) -> str:
        """Get help for specific command."""
        commands = self.get_command_list()
        return commands.get(command_name, "Command not found")
