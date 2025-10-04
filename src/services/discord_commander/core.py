#!/usr/bin/env python3
"""
Discord Commander Core Components
=================================

Core components for Discord Commander functionality.
V2 Compliance: ≤400 lines, focused core functionality.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class DiscordConfig:
    """Discord bot configuration manager."""
    
    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.guild_id = os.getenv("DISCORD_GUILD_ID")
        self.command_prefix = os.getenv("DISCORD_COMMAND_PREFIX", "!")
        self.intents = self._get_intents()
        
    def _get_intents(self) -> Optional[discord.Intents]:
        """Get Discord intents configuration."""
        if not DISCORD_AVAILABLE:
            return None
            
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        return intents
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        if not self.token:
            issues.append("DISCORD_BOT_TOKEN not set")
        
        if not self.guild_id:
            issues.append("DISCORD_GUILD_ID not set")
        
        if not DISCORD_AVAILABLE:
            issues.append("discord.py not installed")
        
        return issues


class DiscordConnectionManager:
    """Manages Discord bot connection and reconnection."""
    
    def __init__(self, config: DiscordConfig):
        self.config = config
        self.bot = None
        self.logger = logging.getLogger(f"{__name__}.ConnectionManager")
        self.connection_attempts = 0
        self.max_retries = 5
        
    async def create_bot(self) -> Optional[commands.Bot]:
        """Create and configure Discord bot."""
        if not DISCORD_AVAILABLE:
            self.logger.error("Discord.py not available")
            return None
        
        try:
            bot = commands.Bot(
                command_prefix=self.config.command_prefix,
                intents=self.config.intents,
                help_command=None
            )
            
            # Add event handlers
            bot.add_listener(self._on_ready, 'on_ready')
            bot.add_listener(self._on_error, 'on_error')
            bot.add_listener(self._on_command_error, 'on_command_error')
            
            self.bot = bot
            return bot
            
        except Exception as e:
            self.logger.error(f"Error creating bot: {e}")
            return None
    
    async def connect(self) -> bool:
        """Connect to Discord."""
        if not self.bot:
            self.logger.error("Bot not created")
            return False
        
        try:
            self.connection_attempts += 1
            await self.bot.start(self.config.token)
            return True
            
        except discord.LoginFailure:
            self.logger.error("Invalid Discord token")
            return False
        except discord.ConnectionClosed:
            self.logger.warning("Discord connection closed")
            return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Discord."""
        if self.bot and not self.bot.is_closed():
            await self.bot.close()
    
    async def _on_ready(self):
        """Handle bot ready event."""
        self.logger.info(f"Discord bot ready: {self.bot.user}")
        self.connection_attempts = 0
    
    async def _on_error(self, event, *args, **kwargs):
        """Handle general errors."""
        self.logger.error(f"Discord error in event {event}: {args}")
    
    async def _on_command_error(self, ctx, error):
        """Handle command errors."""
        self.logger.error(f"Command error: {error}")


class DiscordCommandRegistry:
    """Registry for Discord commands and their handlers."""
    
    def __init__(self):
        self.commands: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.CommandRegistry")
    
    def register_command(self, name: str, handler: Any, description: str = ""):
        """Register a command handler."""
        self.commands[name] = {
            "handler": handler,
            "description": description,
            "registered_at": datetime.now()
        }
        self.logger.info(f"Registered command: {name}")
    
    def get_command(self, name: str) -> Optional[Any]:
        """Get a command handler by name."""
        return self.commands.get(name, {}).get("handler")
    
    def list_commands(self) -> List[str]:
        """List all registered commands."""
        return list(self.commands.keys())
    
    def unregister_command(self, name: str) -> bool:
        """Unregister a command."""
        if name in self.commands:
            del self.commands[name]
            self.logger.info(f"Unregistered command: {name}")
            return True
        return False


class DiscordEventManager:
    """Manages Discord events and their handlers."""
    
    def __init__(self):
        self.event_handlers: Dict[str, List[Any]] = {}
        self.logger = logging.getLogger(f"{__name__}.EventManager")
    
    def register_event_handler(self, event_name: str, handler: Any):
        """Register an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append(handler)
        self.logger.info(f"Registered handler for event: {event_name}")
    
    async def trigger_event(self, event_name: str, *args, **kwargs):
        """Trigger an event and call all registered handlers."""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(*args, **kwargs)
                    else:
                        handler(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {e}")
    
    def get_event_handlers(self, event_name: str) -> List[Any]:
        """Get all handlers for an event."""
        return self.event_handlers.get(event_name, [])


class DiscordStatusMonitor:
    """Monitors Discord bot status and health."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.StatusMonitor")
        self.start_time = datetime.now()
        self.last_heartbeat = None
        self.message_count = 0
        self.command_count = 0
        self.error_count = 0
    
    def record_heartbeat(self):
        """Record a heartbeat."""
        self.last_heartbeat = datetime.now()
    
    def record_message(self):
        """Record a message received."""
        self.message_count += 1
    
    def record_command(self):
        """Record a command executed."""
        self.command_count += 1
    
    def record_error(self):
        """Record an error."""
        self.error_count += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status."""
        uptime = datetime.now() - self.start_time
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "uptime_formatted": str(uptime).split('.')[0],
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "messages_received": self.message_count,
            "commands_executed": self.command_count,
            "errors": self.error_count,
            "status": "healthy" if self.error_count < 10 else "degraded"
        }
    
    def is_healthy(self) -> bool:
        """Check if bot is healthy."""
        if self.error_count > 50:
            return False
        
        if self.last_heartbeat:
            time_since_heartbeat = datetime.now() - self.last_heartbeat
            if time_since_heartbeat.total_seconds() > 300:  # 5 minutes
                return False
        
        return True




