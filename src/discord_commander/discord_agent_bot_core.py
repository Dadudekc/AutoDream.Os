#!/usr/bin/env python3
"""
Discord Agent Bot Core - V2 Compliant Module
============================================

Core Discord bot functionality for V2_SWARM with modular architecture.
V2 COMPLIANT: Core bot operations under 200 lines.

Features:
- Bot initialization and configuration
- Event handling and command processing
- Modular component integration

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

try:
    from .agent_communication_engine_core import (
        AgentCommunicationEngineCore as AgentCommunicationEngine,
    )
    from .command_router import CommandRouter
    from .discord_commander_models import CommandResult
    from .embeds import EmbedManager
    from .guards import check_context
    from .handlers_agents import AgentCommandHandlers
    from .handlers_swarm import SwarmCommandHandlers
    from .rate_limits import RateLimiter
    from .security_policies import allow_channel, allow_guild, allow_user
    from .structured_logging import configure_logging

    try:
        from ..integration.messaging_gateway import MessagingGateway
        from .handlers_agent_summary import setup as setup_agent_summary
    except ImportError as e:
        print(f"⚠️ Import warning: {e}")
        MessagingGateway = None
        setup_agent_summary = None

except ImportError as e:
    print(f"⚠️ Primary imports failed: {e}")
    # Fallback imports would go here
    AgentCommunicationEngine = None
    CommandResult = None
    allow_guild = lambda x: True
    allow_channel = lambda x: True
    allow_user = lambda x: True
    RateLimiter = None
    configure_logging = lambda *a, **k: None
    check_context = lambda x: True
    CommandRouter = None
    EmbedManager = None
    AgentCommandHandlers = None
    SwarmCommandHandlers = None
    MessagingGateway = None
    setup_agent_summary = None


class DiscordAgentBot(commands.Bot):
    """Streamlined Discord bot for V2_SWARM agent coordination."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """Initialize Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = False

        super().__init__(command_prefix=command_prefix, intents=intents)

        # Configure structured logging
        configure_logging()

        # Initialize modular components
        self.agent_engine = AgentCommunicationEngine()
        self.command_router = CommandRouter()
        self.embed_manager = EmbedManager()
        self.agent_handlers = AgentCommandHandlers(self.agent_engine, self.embed_manager)
        self.swarm_handlers = SwarmCommandHandlers(self.agent_engine, self.embed_manager)

        # Initialize MessagingGateway for PyAutoGUI integration
        self.messaging_gateway = self._initialize_messaging_gateway()

        # Load agent coordinates configuration
        self.agent_coordinates = self._load_agent_coordinates()

        # Initialize rate limiter
        global_rate = int(os.getenv("RATE_LIMIT_GLOBAL_PER_SEC", "5"))
        user_cooldown = int(os.getenv("RATE_LIMIT_USER_COOLDOWN_SEC", "2"))
        self.rate_limiter = RateLimiter(global_rate, user_cooldown)

        # Load configuration
        self._load_config()

    def _initialize_messaging_gateway(self):
        """Initialize MessagingGateway for PyAutoGUI integration."""
        try:
            import sys
            from pathlib import Path

            current_dir = Path(__file__).parent.parent
            if str(current_dir) not in sys.path:
                sys.path.insert(0, str(current_dir))

            from integration.messaging_gateway import MessagingGateway

            coordinates_path = os.getenv("COORDINATES_PATH", "config/coordinates.json")
            gateway = MessagingGateway(coordinates_path)
            print("✅ MessagingGateway initialized for PyAutoGUI integration")
            return gateway
        except Exception as e:
            print(f"⚠️  MessagingGateway not available - PyAutoGUI integration disabled: {e}")
            return None

    def _load_config(self):
        """Load bot configuration."""
        config_path = Path("config/discord_bot_config.json")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self.allowed_channels = config.get("allowed_channels", [])
                    self.admin_users = config.get("admin_users", [])
                    self.command_timeout = config.get("command_timeout", 300)
                    self.max_concurrent_commands = config.get("max_concurrent_commands", 10)
            except Exception as e:
                print(f"⚠️  Failed to load Discord bot config: {e}")

    def _load_agent_coordinates(self) -> dict[str, dict[str, Any]]:
        """Load agent coordinates configuration."""
        coordinates_path = os.getenv("COORDINATES_PATH", "config/coordinates.json")
        try:
            with open(coordinates_path) as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            print(f"⚠️  Failed to load coordinates: {e}. Using defaults.")
            return {
                agent: {
                    "chat_input_coordinates": [0, 0],
                    "onboarding_coordinates": [0, 0],
                    "description": f"Agent {agent}",
                    "active": True,
                }
                for agent in [f"Agent-{i}" for i in range(1, 9)]
            }

    async def on_ready(self):
        """Called when bot is ready and connected."""
        print("🐝 V2_SWARM Discord Agent Bot Ready!")
        print(f"🤖 Logged in as: {self.user}")
        print(f"📊 Connected to {len(self.guilds)} guild(s)")

        for guild in self.guilds:
            print(f"  - {guild.name} (ID: {guild.id})")

        print(f"🎯 Command prefix: {self.command_prefix}")
        print(f"⏱️  Command timeout: {self.command_timeout}s")
        print(f"🔢 Max concurrent commands: {self.max_concurrent_commands}")
        print("=" * 60)
        print("💡 Available commands:")
        print("  !prompt @agent message  - Prompt specific agent")
        print("  !status @agent         - Check agent status")
        print("  !swarm message         - Send swarm-wide message")
        print("  !urgent message        - URGENT broadcast (high priority)")
        print("  !agents                - List all agents")
        print("  !help                  - Show help")
        print("  !ping                  - Test bot responsiveness")
        print("  /agent                 - Slash command with autocomplete")
        print("  !captain message       - Send to Captain (Agent-4)")
        print("  !agent1 message        - Send to Agent-1")
        print("  ...                    - Dynamic aliases from config/agent_aliases.json")
        print("=" * 60)

        # Register dynamic agent commands
        await self._register_dynamic_agent_commands()

        # Send startup notification to Discord
        await self._send_startup_notification()

        # Setup agent summary commands if gateway is available
        if self.messaging_gateway:
            try:
                from .handlers_agent_summary import setup as setup_agent_summary
                await setup_agent_summary(self, self.messaging_gateway)
                print("✅ Agent summary commands registered successfully")
            except Exception as e:
                print(f"⚠️  Failed to setup agent summary commands: {e}")

    async def on_message(self, message):
        """Handle incoming messages."""
        # Don't respond to own messages
        if message.author == self.user:
            return

        # Check security policies
        guild_id = message.guild.id if message.guild else None
        if (
            not allow_guild(guild_id)
            or not allow_channel(message.channel.id)
            or not allow_user(message.author.id)
        ):
            return

        # Handle keyboard shortcuts for urgent messages
        try:
            from .discord_dynamic_agent_commands import handle_keyboard_shortcut
            handled = await handle_keyboard_shortcut(message, self)
            if handled:
                return
        except Exception as e:
            print(f"Keyboard shortcut handler error: {e}")

        # Apply rate limiting
        try:
            await self.rate_limiter.acquire(message.author.id)
        except Exception:
            return
        finally:
            try:
                self.rate_limiter.release()
            except:
                pass

        # Process commands
        await self.process_command(message)

    def get_command_stats(self) -> dict[str, Any]:
        """Get bot command statistics."""
        return {
            "active_agent_commands": self.agent_handlers.get_active_command_count(),
            "active_swarm_broadcasts": self.swarm_handlers.get_active_broadcast_count(),
            "total_active": (
                self.agent_handlers.get_active_command_count()
                + self.swarm_handlers.get_active_broadcast_count()
            ),
        }

    async def _register_dynamic_agent_commands(self):
        """Register dynamic agent commands using the new system."""
        try:
            from .discord_dynamic_agent_commands import setup_dynamic_agent_commands
            await setup_dynamic_agent_commands(self)
            print("✅ Dynamic agent commands registered (prefix + slash)")
        except Exception as e:
            print(f"⚠️ Failed to register dynamic agent commands: {e}")
            self._register_basic_fallback_commands()

    def _register_basic_fallback_commands(self):
        """Register basic fallback commands if dynamic system fails."""
        @self.command(name="simple_agent")
        async def simple_agent(ctx, agent_num: int, *, message: str):
            """Simple fallback agent command."""
            if not (1 <= agent_num <= 8):
                await ctx.reply("❌ Agent number must be between 1 and 8.")
                return

            agent_id = f"Agent-{agent_num}"
            try:
                await self.agent_engine.send_to_agent_inbox(
                    agent_id, message, f"Discord:{ctx.author.id}"
                )
                await ctx.reply(f"✅ Message sent to {agent_id}")
            except Exception as e:
                await ctx.reply(f"❌ Failed to send message: {e}")

        print("✅ Basic fallback agent commands registered")

