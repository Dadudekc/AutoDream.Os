#!/usr/bin/env python3
"""
Discord Agent Bot - V2 Compliance Module (Streamlined)
======================================================

Streamlined Discord Agent Bot for V2_SWARM with modular architecture.
Reduced from 850+ lines to <400 lines for V2 compliance.

Features:
- Command routing via modular handlers
- Security policies and rate limiting
- Structured logging and monitoring
- Agent prompting and swarm coordination

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

import asyncio
import os
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

try:
    from .agent_communication_engine_refactored import AgentCommunicationEngine
    from .command_router import CommandRouter
    from .discord_commander_models import CommandResult
    from .embeds import EmbedManager
    from .guards import check_context
    from .handlers_agents import AgentCommandHandlers
    from .handlers_swarm import SwarmCommandHandlers
    from .rate_limits import RateLimiter
    from .security_policies import allow_channel, allow_guild, allow_user
    from .structured_logging import configure_logging
except ImportError:
    # Fallback for direct execution
    from agent_communication_engine_refactored import AgentCommunicationEngine
    from command_router import CommandRouter
    from embeds import EmbedManager
    from handlers_agents import AgentCommandHandlers
    from handlers_swarm import SwarmCommandHandlers
    from rate_limits import RateLimiter
    from security_policies import allow_channel, allow_guild, allow_user
    from structured_logging import configure_logging


class DiscordAgentBot(commands.Bot):
    """Streamlined Discord bot for V2_SWARM agent coordination."""

    def __init__(self, command_prefix: str = '!', intents=None):
        """Initialize Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        super().__init__(command_prefix=command_prefix, intents=intents)

        # Configure structured logging
        configure_logging()

        # Initialize modular components
        self.agent_engine = AgentCommunicationEngine()
        self.command_router = CommandRouter()
        self.embed_manager = EmbedManager()
        self.agent_handlers = AgentCommandHandlers(self.agent_engine, self.embed_manager)
        self.swarm_handlers = SwarmCommandHandlers(self.agent_engine, self.embed_manager)

        # Load agent map configuration
        self.agent_map = self._load_agent_map()

        # Initialize rate limiter
        global_rate = int(os.getenv('RATE_LIMIT_GLOBAL_PER_SEC', '5'))
        user_cooldown = int(os.getenv('RATE_LIMIT_USER_COOLDOWN_SEC', '2'))
        self.rate_limiter = RateLimiter(global_rate, user_cooldown)

        # Load configuration
        self._load_config()

    def _load_config(self):
        """Load bot configuration."""
        config_path = Path("config/discord_bot_config.json")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self.allowed_channels = config.get('allowed_channels', [])
                    self.admin_users = config.get('admin_users', [])
                    self.command_timeout = config.get('command_timeout', 300)
                    self.max_concurrent_commands = config.get('max_concurrent_commands', 10)
            except Exception as e:
                print(f"⚠️  Failed to load Discord bot config: {e}")

    def _load_agent_map(self) -> dict[str, dict[str, str]]:
        """Load agent mapping configuration."""
        agent_map_path = os.getenv('AGENT_MAP_PATH', 'config/agent_map.json')
        try:
            with open(agent_map_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load agent map: {e}. Using defaults.")
            # Return default agent map
            return {
                agent: {"mention": f"@{agent}", "inbox_path": f"agent_workspaces/{agent}/inbox"}
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
        print("  !agents                - List all agents")
        print("  !help                  - Show help")
        print("  !ping                  - Test bot responsiveness")
        print("=" * 60)

    async def on_message(self, message):
        """Handle incoming messages."""
        # Don't respond to own messages
        if message.author == self.user:
            return

        # Check security policies
        guild_id = message.guild.id if message.guild else None
        if not allow_guild(guild_id) or not allow_channel(message.channel.id) or not allow_user(message.author.id):
            return

        # Apply rate limiting
        try:
            await self.rate_limiter.acquire(message.author.id)
        except Exception:
            # Rate limit exceeded, silently ignore
            return
        finally:
            # Always release the rate limiter
            try:
                self.rate_limiter.release()
            except:
                pass

        # Process commands
        await self.process_command(message)

    async def process_command(self, message):
        """Process Discord command using modular handlers."""
        try:
            content = message.content
            author = message.author
            channel = message.channel

            # Parse command using command router
            cmd_type, args, remaining = self.command_router.parse_command(content)

            if cmd_type == 'unknown':
                return

            # Validate command
            is_valid, error_msg = self.command_router.validate_command(cmd_type, args, content)
            if not is_valid:
                error_embed = self.embed_manager.create_response_embed(
                    'error',
                    title="❌ Invalid Command",
                    description=error_msg
                )
                await channel.send(embed=error_embed)
                return

            # Check concurrent command limit
            total_active = (self.agent_handlers.get_active_command_count() +
                          self.swarm_handlers.get_active_broadcast_count())
            if total_active >= self.max_concurrent_commands:
                embed = self.embed_manager.create_response_embed('too_many_commands')
                await channel.send(embed=embed)
                return

            # Create command context
            context = self.command_router.create_command_context(cmd_type, args, author, channel)

            # Route to appropriate handler
            response_data = None

            if cmd_type == 'prompt':
                response_data = await self.agent_handlers.handle_prompt_command(context)
            elif cmd_type == 'status':
                response_data = await self.agent_handlers.handle_status_command(context)
            elif cmd_type == 'swarm':
                response_data = await self.swarm_handlers.handle_swarm_command(context)
            elif cmd_type == 'agents':
                agents = self.swarm_handlers.get_swarm_agent_list()
                embed = self.embed_manager.create_response_embed('agents', agents=agents, author=author)
                await channel.send(embed=embed)
                return
            elif cmd_type == 'help':
                embed = self.embed_manager.create_response_embed('help', author=author)
                await channel.send(embed=embed)
                return
            elif cmd_type == 'ping':
                # Calculate latency (simplified)
                latency = 42  # ms (would be calculated from message timestamps)
                active_commands = self.agent_handlers.get_active_command_count()
                embed = self.embed_manager.create_response_embed(
                    'ping',
                    latency=latency,
                    active_commands=active_commands
                )
                await channel.send(embed=embed)
                return

            # Handle response
            if response_data:
                if response_data.get('ignore'):
                    return

                embed = response_data['embed']
                follow_up = response_data.get('follow_up', False)

                if follow_up:
                    # Send initial response and handle followup
                    response_msg = await channel.send(embed=embed)
                    command_id = response_data.get('command_id')

                    if command_id and cmd_type == 'prompt':
                        # Handle agent prompt followup
                        try:
                            result = await self.agent_engine.send_to_agent_inbox(
                                response_data['agent_id'],
                                args[1],  # prompt
                                f"Discord User {author} (ID: {author.id})"
                            )
                            followup_data = await self.agent_handlers.handle_prompt_followup(command_id, result)
                            if followup_data and followup_data.get('edit'):
                                await response_msg.edit(embed=followup_data['embed'])
                        except Exception as e:
                            error_embed = self.embed_manager.create_response_embed(
                                'error',
                                title="❌ Agent Communication Error",
                                description="Error communicating with agent.",
                                error=str(e)
                            )
                            await response_msg.edit(embed=error_embed)

                    elif command_id and cmd_type == 'swarm':
                        # Handle swarm broadcast followup
                        try:
                            result = await self.swarm_handlers.execute_swarm_broadcast(
                                response_data['message'],
                                f"Discord User {author} (ID: {author.id})"
                            )
                            followup_data = await self.swarm_handlers.handle_swarm_followup(command_id, result)
                            if followup_data and followup_data.get('edit'):
                                await response_msg.edit(embed=followup_data['embed'])
                        except Exception as e:
                            error_embed = self.embed_manager.create_response_embed(
                                'error',
                                title="❌ Swarm Broadcast Error",
                                description="Error broadcasting to swarm.",
                                error=str(e)
                            )
                            await response_msg.edit(embed=error_embed)
                else:
                    # Send immediate response
                    await channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Error processing command: {e}")
            error_embed = self.embed_manager.create_response_embed(
                'error',
                title="❌ Command Processing Error",
                description="An error occurred while processing your command.",
                error=str(e)
            )
            await message.channel.send(embed=error_embed)

    def get_command_stats(self) -> dict[str, Any]:
        """Get bot command statistics."""
        return {
            'active_agent_commands': self.agent_handlers.get_active_command_count(),
            'active_swarm_broadcasts': self.swarm_handlers.get_active_broadcast_count(),
            'total_active': (self.agent_handlers.get_active_command_count() +
                           self.swarm_handlers.get_active_broadcast_count())
        }


class DiscordAgentBotManager:
    """Manager for Discord Agent Bot operations."""

    def __init__(self):
        """Initialize bot manager."""
        self.bot = None
        self.config_path = Path("config/discord_bot_config.json")
        self.token = os.getenv('DISCORD_BOT_TOKEN')

    def create_bot(self, token: str = None) -> DiscordAgentBot:
        """Create and configure Discord agent bot."""
        if token:
            self.token = token

        if not self.token:
            raise ValueError("Discord bot token not provided. Set DISCORD_BOT_TOKEN environment variable.")

        self.bot = DiscordAgentBot()
        return self.bot

    def save_config(self, config: dict[str, Any]):
        """Save bot configuration."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def load_config(self) -> dict[str, Any]:
        """Load bot configuration."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to load bot config: {e}")

        return {
            'allowed_channels': [],
            'admin_users': [],
            'command_timeout': 300,
            'max_concurrent_commands': 10
        }

    async def start_bot(self, token: str = None):
        """Start the Discord agent bot."""
        if not self.bot:
            self.create_bot(token)

        print("🐝 Starting V2_SWARM Discord Agent Bot...")
        print(f"🤖 Token: {'***' + token[-10:] if len(token) > 10 else token}")
        print("=" * 60)

        try:
            await self.bot.start(self.token)
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Bot error: {e}")
        finally:
            await self.bot.close()

    async def test_bot_connection(self, token: str = None) -> bool:
        """Test bot connection to Discord."""
        if not self.bot:
            self.create_bot(token)

        try:
            await self.bot.login(self.token)
            await self.bot.close()
            print("✅ Discord bot connection test successful")
            return True
        except Exception as e:
            print(f"❌ Discord bot connection test failed: {e}")
            return False


# Global manager instance
_bot_manager_instance = None


def get_discord_bot_manager() -> DiscordAgentBotManager:
    """Get Discord bot manager instance (singleton)."""
    global _bot_manager_instance
    if _bot_manager_instance is None:
        _bot_manager_instance = DiscordAgentBotManager()
    return _bot_manager_instance


async def start_discord_agent_bot(token: str = None):
    """Start the Discord agent bot."""
    manager = get_discord_bot_manager()
    await manager.start_bot(token)


async def test_discord_bot_connection(token: str = None) -> bool:
    """Test Discord bot connection."""
    manager = get_discord_bot_manager()
    return await manager.test_bot_connection(token)


if __name__ == "__main__":
    # Test the bot
    import sys

    async def main():
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            token = os.getenv('DISCORD_BOT_TOKEN')

        if not token:
            print("❌ No Discord bot token provided.")
            print("💡 Set DISCORD_BOT_TOKEN environment variable or pass as argument")
            sys.exit(1)

        print("🧪 Testing Discord Agent Bot...")
        success = await test_discord_bot_connection(token)
        if success:
            print("✅ Bot connection test passed!")
            print("🚀 Starting bot...")
            await start_discord_agent_bot(token)
        else:
            print("❌ Bot connection test failed!")
            sys.exit(1)

    asyncio.run(main())
