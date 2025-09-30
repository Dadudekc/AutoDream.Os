#!/usr/bin/env python3
"""
Discord Commander Core Module
============================

Core functionality for the Discord Commander bot system.
Handles bot creation, configuration, and event handling.

🐝 WE ARE SWARM - Discord Commander Core Active!
"""

import logging
from typing import Optional

# Discord imports for error handling
try:
    import discord
    from discord.ext import commands
    from services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot
except ImportError:
    discord = None
    commands = None
    EnhancedDiscordAgentBot = None


class DiscordCommanderCore:
    """Core Discord Commander functionality."""

    def __init__(self, logger: logging.Logger):
        """Initialize Discord Commander Core."""
        self.logger = logger
        self.bot: Optional[EnhancedDiscordAgentBot] = None

    def create_discord_bot(self):
        """Create Discord bot instance."""
        if not discord or not EnhancedDiscordAgentBot:
            raise ImportError("Discord.py not installed or EnhancedDiscordAgentBot not found")

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        bot = EnhancedDiscordAgentBot(command_prefix="!", intents=intents)

        # Add agent interface and swarm coordinator
        from services.discord_bot.core.discord_bot import (
            DiscordAgentInterface,
            DiscordSwarmCoordinator,
        )

        bot.agent_interface = DiscordAgentInterface(bot)
        bot.swarm_coordinator = DiscordSwarmCoordinator(bot)

        # Setup slash commands
        bot.setup_slash_commands()

        # Add on_ready event for slash command syncing
        @bot.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.logger.info(f"🤖 Discord Commander {bot.user} is online!")
            self.logger.info(f"📊 Connected to {len(bot.guilds)} servers")

            # Sync slash commands
            try:
                synced = await bot.tree.sync()
                self.logger.info(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                self.logger.warning(f"⚠️  Failed to sync slash commands: {e}")

            # Update presence
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🐝 WE ARE SWARM - Agent Coordination Active",
                )
            )

            # Print startup message
            print("=" * 60)
            print("🐝 Discord Commander Successfully Started!")
            print("=" * 60)
            print(f"🤖 Bot: {bot.user}")
            print(f"📊 Servers: {len(bot.guilds)}")
            print(f"👥 Users: {len(bot.users)}")
            print("📡 Status: Online and Ready!")
            print("🎯 5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
            print("=" * 60)
            print("✅ All systems operational!")
            print("🚀 Ready for agent coordination!")
            print("=" * 60)

        return bot

    def setup_additional_slash_commands(self):
        """Setup additional Discord slash commands that aren't already registered."""
        if not self.bot:
            return

        try:
            # Add only new commands that aren't already registered by the bot
            # The bot already has: agent_status, message_agent, swarm_status
            # So we only add: ping and help

            from discord import app_commands

            @app_commands.command(name="ping", description="Check bot latency")
            async def ping(interaction: discord.Interaction):
                latency = round(self.bot.latency * 1000)
                await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

            @app_commands.command(name="help", description="Show available commands")
            async def help_command(interaction: discord.Interaction):
                embed = discord.Embed(
                    title="🐝 Discord Commander Help",
                    description="Available Commands:",
                    color=0x0099FF,
                )
                embed.add_field(name="/ping", value="Check bot latency", inline=False)
                embed.add_field(
                    name="/agent_status", value="Get status of a specific agent", inline=False
                )
                embed.add_field(
                    name="/message_agent", value="Send a message to a specific agent", inline=False
                )
                embed.add_field(
                    name="/swarm_status", value="Get current swarm status", inline=False
                )
                embed.add_field(name="/help", value="Show this help message", inline=False)
                await interaction.response.send_message(embed=embed)

            # Register commands with the bot using the same method as the bot
            self.bot.tree.add_command(ping)
            self.bot.tree.add_command(help_command)

            # Note: Slash commands will be synced when bot starts
            self.logger.info("✅ Additional slash commands (ping, help) registered")

        except Exception as e:
            self.logger.error(f"❌ Failed to setup additional slash commands: {e}")

    async def start_bot(self, token: str) -> bool:
        """Start the Discord bot."""
        try:
            # Start the actual Discord bot with proper error handling
            await self.bot.start(token)

            self.logger.info("✅ Discord bot started successfully!")
            self.logger.info("📡 Ready to coordinate agents!")
            self.logger.info("🐝 WE ARE SWARM - Discord Commander Operational!")

            # Discord Commander successfully initialized!
            print("🐝 Discord Commander successfully initialized!")
            print("✅ All systems operational")
            print("🤖 5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
            print("📡 Ready for Discord bot token configuration")
            print("🚀 Use 'python setup_discord_commander.py' to configure")

            return True

        except discord.LoginFailure:
            self.logger.error("❌ Discord login failed - invalid token!")
            return False
        except discord.HTTPException as e:
            self.logger.error(f"❌ Discord HTTP error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error starting Discord bot: {e}")
            return False

    async def stop_bot(self):
        """Stop the Discord bot."""
        try:
            if self.bot:
                await self.bot.close()
        except Exception as e:
            self.logger.error(f"❌ Error stopping Discord bot: {e}")

    def get_bot_status(self) -> dict:
        """Get Discord bot status."""
        status = {
            "bot_initialized": self.bot is not None,
            "bot_online": self.bot and not self.bot.is_closed() if self.bot else False,
        }

        if self.bot:
            status.update(self.bot.get_swarm_status())

        return status