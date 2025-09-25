#!/usr/bin/env python3
"""
Discord Commander Bot
=====================

Main Discord bot implementation using modular components.
V2 Compliance: ≤400 lines, focused bot functionality.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

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
            handler = self.command_manager.get_command_handler("agent_status")
            if handler:
                result = await handler(ctx, agent_id)
                await ctx.send(result)
        
        @self.bot.command(name="send_message")
        async def send_message(ctx, agent_id: str, *, message: str):
            handler = self.command_manager.get_command_handler("send_message")
            if handler:
                result = await handler(ctx, agent_id, message)
                await ctx.send(result)
        
        @self.bot.command(name="agent_coordinates")
        async def agent_coordinates(ctx, agent_id: str = None):
            handler = self.command_manager.get_command_handler("agent_coordinates")
            if handler:
                result = await handler(ctx, agent_id)
                await ctx.send(result)
        
        # System commands
        @self.bot.command(name="system_status")
        async def system_status(ctx):
            handler = self.command_manager.get_command_handler("system_status")
            if handler:
                result = await handler(ctx)
                await ctx.send(result)
        
        @self.bot.command(name="project_info")
        async def project_info(ctx):
            handler = self.command_manager.get_command_handler("project_info")
            if handler:
                result = await handler(ctx)
                await ctx.send(result)
        
        # Swarm commands
        @self.bot.command(name="swarm_status")
        async def swarm_status(ctx):
            handler = self.command_manager.get_command_handler("swarm_status")
            if handler:
                result = await handler(ctx)
                await ctx.send(result)
        
        @self.bot.command(name="swarm_coordinate")
        async def swarm_coordinate(ctx, *, message: str):
            handler = self.command_manager.get_command_handler("swarm_coordinate")
            if handler:
                result = await handler(ctx, message)
                await ctx.send(result)
        
        # Help command
        @self.bot.command(name="help")
        async def help_command(ctx):
            commands = self.command_manager.list_commands()
            help_text = "Available Commands:\n"
            for cmd in commands:
                help_text += f"!{cmd}\n"
            await ctx.send(help_text)
    
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
            type=discord.ActivityType.watching,
            name="Agent Swarm Coordination"
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




