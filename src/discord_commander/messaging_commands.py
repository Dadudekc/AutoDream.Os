#!/usr/bin/env python3
"""
Discord Messaging Commands
===========================

Enhanced Discord commands for agent messaging using the messaging controller.
Provides easy-to-use slash commands with Discord views.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
from datetime import datetime

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from .messaging_controller import DiscordMessagingController

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
    """Discord commands for agent messaging."""

    def __init__(self, bot, messaging_controller: DiscordMessagingController):
        """Initialize messaging commands."""
        self.bot = bot
        self.messaging_controller = messaging_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="message_agent", description="Send a message to a specific agent")
    async def message_agent(
        self, ctx: commands.Context, agent_id: str, message: str, priority: str = "NORMAL"
    ):
        """Send message to specific agent."""
        try:
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "CRITICAL"]
            if priority not in valid_priorities:
                priority = "NORMAL"

            # Send message
            success = await self.messaging_controller.send_agent_message(
                agent_id=agent_id, message=message, priority=priority
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Message sent to **{agent_id}**",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)
                embed.add_field(name="From", value=ctx.user.display_name, inline=True)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Message Failed",
                    description=f"Failed to send message to **{agent_id}**",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in message_agent command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error sending message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="agent_interact", description="Interactive agent messaging interface")
    async def agent_interact(self, ctx: commands.Context):
        """Interactive agent messaging interface."""
        try:
            embed = discord.Embed(
                title="🤖 Agent Messaging Interface",
                description="Select an agent below to send a message",
                color=discord.Color.blue(),
                timestamp=datetime.now(),
            )
            embed.add_field(
                name="How to use",
                value="1. Select an agent from the dropdown\n2. Type your message in the modal\n3. Set priority if needed",
                inline=False,
            )

            view = self.messaging_controller.create_agent_messaging_view()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error in agent_interact command: {e}")
            await ctx.send(f"Error creating interface: {str(e)}")

    @commands.command(name="swarm_status", description="View current swarm status")
    async def swarm_status(self, ctx: commands.Context):
        """View current swarm status."""
        try:
            view = self.messaging_controller.create_swarm_status_view()
            embed = await view._create_status_embed()

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error in swarm_status command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error getting swarm status: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="broadcast", description="Broadcast message to all agents")
    async def broadcast(self, ctx: commands.Context, message: str, priority: str = "NORMAL"):
        """Broadcast message to all agents."""
        try:
            # Validate priority
            valid_priorities = ["NORMAL", "HIGH", "CRITICAL"]
            if priority not in valid_priorities:
                priority = "NORMAL"

            # Broadcast message
            success = await self.messaging_controller.broadcast_to_swarm(
                message=message, priority=priority
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Message broadcasted to all agents",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(name="Priority", value=priority, inline=True)
                embed.add_field(name="From", value=ctx.user.display_name, inline=True)

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Broadcast Failed",
                    description="Failed to broadcast message to agents",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in broadcast command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error broadcasting message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="agent_list", description="List all available agents")
    async def agent_list(self, ctx: commands.Context):
        """List all available agents."""
        try:
            agent_status = self.messaging_controller.get_agent_status()

            if not agent_status:
                embed = discord.Embed(
                    title="❌ No Agents Found",
                    description="No agents are currently available",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title="🤖 Available Agents",
                description="List of all agents in the swarm",
                color=discord.Color.blue(),
                timestamp=datetime.now(),
            )

            for agent_id, info in agent_status.items():
                status_emoji = "🟢" if info["active"] else "🔴"
                embed.add_field(
                    name=f"{status_emoji} {agent_id}",
                    value=f"Status: {'Active' if info['active'] else 'Inactive'}\nCoordinates: {info['coordinates']}",
                    inline=True,
                )

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in agent_list command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error listing agents: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="agent", description="Send message to agent (C-057)")
    async def agent_command(self, ctx: commands.Context, agent_name: str, *, message: str):
        """
        C-057: Send message to specific agent.

        Usage: !agent <agent-name> <message>
        Example: !agent Agent-1 Hello from Discord!
        """
        try:
            # Map agent names (handle with/without Agent- prefix)
            if not agent_name.startswith("Agent-"):
                agent_name = f"Agent-{agent_name}"

            # Send message via messaging controller
            success = await self.messaging_controller.send_agent_message(
                agent_id=agent_name, message=message, priority="NORMAL"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent (C-057)",
                    description=f"Message delivered to **{agent_name}**",
                    color=discord.Color.green(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="Message", value=message[:500], inline=False)
                embed.add_field(
                    name="From Discord User", value=ctx.author.display_name, inline=True
                )
                embed.set_footer(text="C-057 Discord View Controller")

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Message Failed",
                    description=f"Failed to send message to **{agent_name}**",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in agent command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error sending message: {str(e)}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="help_messaging", description="Get help with messaging commands")
    async def help_messaging(self, ctx: commands.Context):
        """Get help with messaging commands."""
        try:
            embed = discord.Embed(
                title="📖 Messaging Commands Help",
                description="Available commands for agent messaging",
                color=discord.Color.blue(),
                timestamp=datetime.now(),
            )

            commands_help = [
                ("`!agent <name> <msg>`", "Send message to agent (C-057)"),
                ("`/message_agent`", "Send message to specific agent"),
                ("`/agent_interact`", "Interactive messaging interface"),
                ("`/swarm_status`", "View current swarm status"),
                ("`/broadcast`", "Broadcast message to all agents"),
                ("`/agent_list`", "List all available agents"),
                ("`/help_messaging`", "Show this help message"),
            ]

            for command, description in commands_help:
                embed.add_field(name=command, value=description, inline=False)

            embed.add_field(
                name="Priority Levels",
                value="• **NORMAL**: Standard priority\n• **HIGH**: High priority\n• **CRITICAL**: Critical priority",
                inline=False,
            )

            embed.add_field(
                name="Tips",
                value="• Use `!agent Agent-1 Hello!` for quick messages\n• Use `/agent_interact` for easy agent selection\n• Check `/swarm_status` before messaging\n• Use `/agent_list` to see all available agents",
                inline=False,
            )

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in help_messaging command: {e}")
            await ctx.send(f"Error showing help: {str(e)}")


def setup(bot, messaging_controller: DiscordMessagingController):
    """Setup the messaging commands cog."""
    bot.add_cog(MessagingCommands(bot, messaging_controller))
