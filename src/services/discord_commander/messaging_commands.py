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

from .messaging_controller import (
    AgentMessagingView,
    DiscordMessagingController,
    QuickMessagingView,
    SwarmStatusView,
)

logger = logging.getLogger(__name__)


class MessagingCommands(commands.Cog):
    """Discord commands for agent messaging."""

    def __init__(self, bot, messaging_controller: DiscordMessagingController):
        """Initialize messaging commands."""
        self.bot = bot
        self.messaging_controller = messaging_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="test")
    async def test(self, ctx: commands.Context):
        """Test command to verify the bot is working."""
        embed = discord.Embed(
            title="✅ Bot Test Successful!",
            description="The Discord messaging bot is working correctly.",
            color=discord.Color.green(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="Status", value="✅ Online and responsive", inline=True)
        embed.add_field(name="Commands", value="✅ Command system working", inline=True)
        await ctx.send(embed=embed)

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

    @commands.command(name="agent_interact")
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

            # Create the view with actual agent data
            view = AgentMessagingView(self.messaging_controller.messaging_service)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error in agent_interact command: {e}")
            await ctx.send(f"Error creating interface: {str(e)}")

    @commands.command(name="swarm_status")
    async def swarm_status(self, ctx: commands.Context):
        """View current swarm status."""
        try:
            # Create the view directly
            view = SwarmStatusView(self.messaging_controller.messaging_service)
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

    @commands.command(name="broadcast")
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

    @commands.command(name="agent_list")
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

    @commands.command(name="quick_message")
    async def quick_message(self, ctx: commands.Context):
        """Quick messaging interface - no typing required."""
        try:
            embed = discord.Embed(
                title="⚡ Quick Agent Messaging",
                description="Click the button below to start messaging agents instantly!",
                color=discord.Color.green(),
                timestamp=datetime.now(),
            )

            # Create a simple button that opens the agent messaging interface
            view = QuickMessagingView(self.messaging_controller.messaging_service)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error in quick_message command: {e}")
            await ctx.send(f"Error creating quick interface: {str(e)}")

    @commands.command(name="help_messaging")
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
                ("`!quick_message`", "⚡ Quick messaging interface (no typing required)"),
                ("`!agent_interact`", "🤖 Interactive messaging interface with dropdowns"),
                ("`!swarm_status`", "📊 View current swarm status with refresh"),
                ("`!broadcast`", "📢 Broadcast message to all agents"),
                ("`!agent_list`", "📋 List all available agents with status"),
                ("`!message_agent`", "💬 Send message to specific agent (text command)"),
                ("`!help_messaging`", "❓ Show this help message"),
            ]

            for command, description in commands_help:
                embed.add_field(name=command, value=description, inline=False)

            embed.add_field(
                name="Priority Levels",
                value="• **NORMAL**: Standard priority\n• **HIGH**: High priority\n• **CRITICAL**: Critical priority",
                inline=False,
            )

            embed.add_field(
                name="💡 Pro Tips",
                value="• Use `!quick_message` for the easiest way to start messaging\n• Use `!agent_interact` for dropdown agent selection\n• Check `!swarm_status` before messaging agents\n• Use `!agent_list` to see all available agents",
                inline=False,
            )

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in help_messaging command: {e}")
            await ctx.send(f"Error showing help: {str(e)}")

    @commands.command(name="help")
    async def help_alias(self, ctx: commands.Context):
        """Alias to show messaging help (maps to !help_messaging)."""
        try:
            await self.help_messaging(ctx)
        except Exception as e:
            self.logger.error(f"Error in help alias: {e}")
            await ctx.send("Help is temporarily unavailable. Try `!help_messaging`.")


async def setup(bot):
    """Setup the messaging commands cog."""
    # Get messaging controller from bot
    messaging_controller = bot.messaging_controller
    await bot.add_cog(MessagingCommands(bot, messaging_controller))
