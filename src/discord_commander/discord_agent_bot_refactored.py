#!/usr/bin/env python3
"""
Discord Agent Bot - V2 Compliant Refactored Module
==================================================

Refactored Discord Agent Bot for V2_SWARM with modular architecture.
V2 COMPLIANT: Main bot coordinator under 200 lines.

Features:
- Modular component integration
- Command processing delegation
- Security policy enforcement
- Rate limiting integration

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""

import asyncio
import os
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

from .discord_agent_bot_core import DiscordAgentBot
from .discord_command_handlers import DiscordCommandHandlers
from .discord_security_policies import DiscordSecurityManager
from .discord_rate_limiting import DiscordRateLimiter


class DiscordAgentBotRefactored(DiscordAgentBot):
    """Refactored Discord Agent Bot with modular architecture."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """Initialize refactored Discord agent bot."""
        super().__init__(command_prefix, intents)
        
        # Initialize modular components
        self.security_manager = DiscordSecurityManager(self)
        self.rate_limiter = DiscordRateLimiter(self)
        self.command_handlers = DiscordCommandHandlers(self)

    async def on_message(self, message):
        """Handle incoming messages with security and rate limiting."""
        # Don't respond to own messages
        if message.author == self.user:
            return

        # Check security policies
        if not self.security_manager.check_security_policies(message):
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
        if not await self.rate_limiter.acquire(message.author.id):
            return  # Rate limit exceeded, silently ignore

        # Process commands through command handlers
        await self.command_handlers.process_command(message)

    async def _send_startup_notification(self):
        """Send startup notification to Discord channel."""
        try:
            # Find the first available channel to send the notification
            target_channel = None

            # Check for configured allowed channels first
            if self.security_manager.allowed_channels:
                for guild in self.guilds:
                    for channel_id in self.security_manager.allowed_channels:
                        channel = guild.get_channel(channel_id)
                        if channel and channel.permissions_for(guild.me).send_messages:
                            target_channel = channel
                            break
                    if target_channel:
                        break

            # If no configured channel found, use the first text channel we can send to
            if not target_channel:
                for guild in self.guilds:
                    for channel in guild.text_channels:
                        if channel.permissions_for(guild.me).send_messages:
                            target_channel = channel
                            break
                    if target_channel:
                        break

            if target_channel:
                # Simple notification message
                notification_msg = (
                    "**DISCORD COMMANDER ONLINE**\n\n"
                    "V2_SWARM Discord Agent Bot is now connected and operational!\n\n"
                    "**Available Commands:**\n"
                    "- `!ping` - Test bot responsiveness\n"
                    "- `!help` - Show all commands\n"
                    "- `!agents` - List all agents\n"
                    "- `!summary1-4` - Request agent status summaries\n"
                    "- `!agentsummary` - Show summary command help\n\n"
                    "**System Status:**\n"
                    "- Bot: Online\n"
                    "- PyAutoGUI: Integrated\n"
                    "- Agents: 8 ready for coordination\n"
                    "- Security: Active\n"
                    "- Rate Limiting: Active\n\n"
                    "**Ready for swarm coordination!**\n"
                    "_V2_SWARM - We are swarm intelligence in action!_"
                )

                await target_channel.send(notification_msg)
                print(
                    f"✅ Startup notification sent to #{target_channel.name} in {target_channel.guild.name}"
                )
            else:
                print("⚠️  No suitable channel found to send startup notification")

        except Exception as e:
            print(f"⚠️  Failed to send startup notification: {e}")
            # Fallback: try to send a simple message
            try:
                if target_channel:
                    await target_channel.send(
                        "🐝 Discord Commander Online - V2_SWARM Bot Connected!"
                    )
            except:
                print("❌ Even fallback notification failed")

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status."""
        base_stats = self.get_command_stats()
        security_status = self.security_manager.get_security_status()
        rate_limit_status = self.rate_limiter.get_rate_limit_status()
        
        return {
            **base_stats,
            "security": security_status,
            "rate_limiting": rate_limit_status,
            "messaging_gateway": self.messaging_gateway is not None,
            "agent_coordinates": len(self.agent_coordinates)
        }


class DiscordAgentBotManager:
    """Manager for Discord Agent Bot operations."""

    def __init__(self):
        """Initialize bot manager."""
        self.bot = None
        self.config_path = Path("config/discord_bot_config.json")
        self.token = os.getenv("DISCORD_BOT_TOKEN")

    def create_bot(self, token: str = None) -> DiscordAgentBotRefactored:
        """Create and configure Discord agent bot."""
        if token:
            self.token = token

        if not self.token:
            raise ValueError(
                "Discord bot token not provided. Set DISCORD_BOT_TOKEN environment variable."
            )

        self.bot = DiscordAgentBotRefactored()
        return self.bot

    async def start_bot(self, token: str = None):
        """Start the Discord agent bot."""
        if not self.bot:
            self.create_bot(token)

        print("🐝 Starting V2_SWARM Discord Agent Bot (Refactored)...")
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
            token = os.getenv("DISCORD_BOT_TOKEN")

        if not token:
            print("❌ No Discord bot token provided.")
            print("💡 Set DISCORD_BOT_TOKEN environment variable or pass as argument")
            sys.exit(1)

        print("🧪 Testing Discord Agent Bot (Refactored)...")
        success = await test_discord_bot_connection(token)
        if success:
            print("✅ Bot connection test passed!")
            print("🚀 Starting bot...")
            await start_discord_agent_bot(token)
        else:
            print("❌ Bot connection test failed!")
            sys.exit(1)

    asyncio.run(main())

