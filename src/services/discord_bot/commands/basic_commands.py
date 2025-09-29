#!/usr/bin/env python3
"""
Discord Bot Basic Commands
==========================

Basic command setup for the Discord bot.
Provides fundamental commands for bot interaction.

V2 Compliance: ≤400 lines, 1 class, 5 functions
"""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


def setup_basic_commands(bot: commands.Bot):
    """Setup basic Discord bot commands."""

    @bot.command(name="ping", help="Check bot responsiveness")
    async def ping(ctx):
        """Check bot ping/latency."""
        try:
            latency = round(bot.latency * 1000)
            embed = discord.Embed(
                title="🏓 Pong!", description=f"**Latency:** {latency}ms", color=0x00FF00
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
            embed = discord.Embed(title="🐝 Discord Commander Status", color=0x0099FF)

            embed.add_field(
                name="Commander", value="Active" if bot.is_ready else "Offline", inline=True
            )

            embed.add_field(
                name="Agent ID", value=getattr(bot, "agent_id", "Discord-Commander"), inline=True
            )

            embed.add_field(name="Guilds", value=len(bot.guilds), inline=True)

            embed.add_field(
                name="Latency",
                value=f"{round(bot.latency * 1000)}ms" if bot.latency else "Unknown",
                inline=True,
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
                title="🐝 Discord Commander Help", description="Available Commands:", color=0x0099FF
            )

            embed.add_field(
                name="!ping", value="Check bot responsiveness and latency", inline=False
            )

            embed.add_field(
                name="!status", value="Get Discord Commander status information", inline=False
            )

            embed.add_field(name="!help", value="Show this help message", inline=False)

            embed.add_field(name="!swarm", value="Get swarm coordination status", inline=False)

            embed.add_field(name="!agents", value="List connected agents", inline=False)

            embed.add_field(
                name="!devlog_help",
                value="Show help for the agent devlog posting system",
                inline=False,
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
            embed = discord.Embed(title="🐝 Swarm Coordination Status", color=0xFFAA00)

            embed.add_field(name="Swarm Status", value="Active", inline=True)

            embed.add_field(
                name="Connected Agents",
                value=len(getattr(bot, "connected_agents", set())),
                inline=True,
            )

            embed.add_field(name="Active Tasks", value="Monitoring", inline=True)

            embed.add_field(name="Coordination Mode", value="Real-time", inline=True)

            embed.set_footer(text="WE ARE SWARM - Agent Intelligence Collective")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in swarm command: {e}")
            await ctx.send("❌ Error getting swarm status")

    @bot.command(name="agents", help="List connected agents")
    async def list_agents(ctx):
        """List connected agents."""
        try:
            connected_agents = getattr(bot, "connected_agents", set())
            if not connected_agents:
                await ctx.send("🤖 **No agents currently connected**")
                return

            embed = discord.Embed(
                title="🤖 Connected Agents",
                description=f"Total: {len(connected_agents)} agents",
                color=0x00AA00,
            )

            for i, agent in enumerate(connected_agents, 1):
                embed.add_field(name=f"Agent {i}", value=agent, inline=True)

            embed.set_footer(text="🐝 WE ARE SWARM - Agent Network Active")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in agents command: {e}")
            await ctx.send("❌ Error listing agents")

    @bot.command(name="devlog_help", help="Show devlog posting help")
    async def devlog_help(ctx):
        """Show help for the devlog posting system."""
        try:
            embed = discord.Embed(
                title="🤖 Agent Devlog System Help",
                description="Automated devlog posting for agents",
                color=0x0099FF,
            )

            embed.add_field(name="📝 Usage", value="Use the standalone Python script:", inline=False)

            embed.add_field(
                name="Command", value="`python src/services/agent_devlog_posting.py`", inline=False
            )

            embed.add_field(
                name="Parameters",
                value=(
                    "`--agent Agent-4` (Required: Agent-1 through Agent-8)\n"
                    '`--action "Task completed"` (Required: Action description)\n'
                    "`--status completed` (Optional: completed|in_progress|failed)\n"
                    '`--details "Details here"` (Optional: Additional details)\n'
                    "`--vectorize` (Optional: Add to vector database)\n"
                    "`--cleanup` (Optional: Delete file after vectorization)\n"
                    "`--dry-run` (Optional: Test mode - create file only, use -t)"
                ),
                inline=False,
            )

            embed.add_field(
                name="Examples",
                value=(
                    '`python src/services/agent_devlog_posting.py --agent Agent-4 --action "Discord integration completed"`\n'
                    '`python src/services/agent_devlog_posting.py --agent Agent-3 --action "Code review" --status in_progress --details "Reviewing pull request"`\n'
                    '`python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed" --vectorize --cleanup`\n'
                    '`python src/services/agent_devlog_posting.py --agent Agent-4 --action "Test" --dry-run`'
                ),
                inline=False,
            )

            embed.add_field(
                name="Features",
                value="✅ Agent flag validation\n✅ Automatic Discord channel routing\n✅ File storage in devlogs/ directory\n✅ Vector database integration\n✅ Automatic cleanup after vectorization\n✅ Proper formatting and timestamps",
                inline=False,
            )

            embed.set_footer(text="🐝 WE ARE SWARM - Use the Python script for devlog posting")
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in devlog_help command: {e}")
            await ctx.send("❌ Error showing devlog help")


class BasicCommandHandler:
    """Basic command handler for Discord bot."""

    def __init__(self, bot: commands.Bot):
        """Initialize basic command handler."""
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.BasicCommandHandler")

    def get_command_list(self) -> dict[str, str]:
        """Get list of available commands."""
        return {
            "ping": "Check bot responsiveness",
            "status": "Get Discord Commander status",
            "help": "Show available commands",
            "swarm": "Get swarm coordination status",
            "agents": "List connected agents",
            "devlog_help": "Show help for the agent devlog posting system",
        }

    def get_command_help(self, command_name: str) -> str:
        """Get help for specific command."""
        commands = self.get_command_list()
        return commands.get(command_name, "Command not found")
