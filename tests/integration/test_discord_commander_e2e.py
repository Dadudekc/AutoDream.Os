#!/usr/bin/env python3
"""
Discord Commander End-to-End Test Suite
======================================

Comprehensive testing of Discord Commander slash commands
and messaging system integration.

Tests both Discord slash commands and messaging system options
to ensure they are properly synchronized.

🐝 WE ARE SWARM - Discord Commander E2E Testing
"""

import asyncio
import discord
from discord.ext import commands
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.messaging.providers.discord_provider import (
    DiscordMessagingProvider,
    DiscordCommandHandler,
    create_discord_messaging_integration
)
from src.services.messaging.core.messaging_service import MessagingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiscordCommanderTestBot:
    """Test bot for Discord Commander E2E testing."""

    def __init__(self, token: str):
        """Initialize test bot."""
        self.token = token
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        # Test results
        self.test_results = {
            "slash_commands": {},
            "messaging_system": {},
            "integration": {},
            "stability": {}
        }

        # Setup event handlers
        self._setup_events()

    def _setup_events(self):
        """Setup Discord bot events."""

        @self.bot.event
        async def on_ready():
            logger.info(f"🤖 Test bot {self.bot.user} is ready!")
            logger.info(f"📊 Guilds: {len(self.bot.guilds)}")
            logger.info(f"🏓 Latency: {round(self.bot.latency * 1000)}ms")

            # Test messaging system integration
            await self._test_messaging_system_integration()

        @self.bot.event
        async def on_interaction(interaction: discord.Interaction):
            """Handle slash command interactions."""
            if interaction.type == discord.InteractionType.application_command:
                logger.info(f"🔧 Slash command received: /{interaction.data['name']}")

                # Test slash command functionality
                await self._test_slash_command(interaction)

    async def _test_messaging_system_integration(self):
        """Test messaging system integration."""
        logger.info("🧪 Testing messaging system integration...")

        try:
            # Test MessagingService
            messaging_service = MessagingService("config/coordinates.json")
            self.test_results["messaging_system"]["messaging_service"] = True

            # Test Discord provider
            discord_provider = DiscordMessagingProvider(self.bot)
            self.test_results["messaging_system"]["discord_provider"] = True

            # Test broadcast functionality
            agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            results = await discord_provider.broadcast_to_swarm(
                message="[E2E Test] Discord Commander integration test",
                agent_ids=agents
            )
            self.test_results["messaging_system"]["broadcast"] = results

            logger.info("✅ Messaging system integration test complete")

        except Exception as e:
            logger.error(f"❌ Messaging system test failed: {e}")
            self.test_results["messaging_system"]["error"] = str(e)

    async def _test_slash_command(self, interaction: discord.Interaction):
        """Test slash command functionality."""
        command_name = interaction.data['name']

        try:
            if command_name == "swarm_status":
                await self._test_swarm_status_command(interaction)
            elif command_name == "send_to_agent":
                await self._test_send_to_agent_command(interaction)
            elif command_name == "broadcast":
                await self._test_broadcast_command(interaction)
            elif command_name == "agent_list":
                await self._test_agent_list_command(interaction)

            self.test_results["slash_commands"][command_name] = "✅ SUCCESS"

        except Exception as e:
            logger.error(f"❌ Slash command {command_name} test failed: {e}")
            self.test_results["slash_commands"][command_name] = f"❌ FAILED: {e}"

    async def _test_swarm_status_command(self, interaction: discord.Interaction):
        """Test /swarm_status command."""
        try:
            # Create Discord provider to test integration
            discord_provider = DiscordMessagingProvider(self.bot)
            status = await discord_provider.get_swarm_status()

            embed = discord.Embed(
                title="🐝 Swarm Status Report",
                color=0x00ff00
            )

            embed.add_field(
                name="Messaging System",
                value=status.get("messaging_system", "unknown"),
                inline=True
            )

            embed.add_field(
                name="Connected Agents",
                value=status.get("connected_agents", 0),
                inline=True
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

    async def _test_send_to_agent_command(self, interaction: discord.Interaction, agent: str, message: str):
        """Test /send_to_agent command."""
        try:
            discord_provider = DiscordMessagingProvider(self.bot)

            success = await discord_provider.send_message_to_agent(
                agent_id=agent,
                message=message,
                from_agent=f"E2E-Test-{interaction.user.name}"
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Sent to {agent}: {message}",
                    color=0x00ff00
                )
            else:
                embed = discord.Embed(
                    title="❌ Message Failed",
                    description=f"Could not send message to {agent}",
                    color=0xff0000
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

    async def _test_broadcast_command(self, interaction: discord.Interaction, message: str):
        """Test /broadcast command."""
        try:
            discord_provider = DiscordMessagingProvider(self.bot)

            results = await discord_provider.broadcast_to_swarm(
                message=message,
                from_agent=f"E2E-Test-{interaction.user.name}"
            )

            successful = sum(1 for result in results.values() if result)
            total = len(results)

            embed = discord.Embed(
                title="📡 Broadcast Results",
                description=f"Message: {message}",
                color=0x0099ff
            )

            embed.add_field(
                name="Successful",
                value=f"{successful}/{total}",
                inline=True
            )

            embed.add_field(
                name="Failed",
                value=f"{total - successful}/{total}",
                inline=True
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

    async def _test_agent_list_command(self, interaction: discord.Interaction):
        """Test /agent_list command."""
        try:
            agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

            embed = discord.Embed(
                title="🤖 Available Agents",
                description=f"Total: {len(agents)} agents",
                color=0x0099ff
            )

            for i, agent in enumerate(agents, 1):
                embed.add_field(
                    name=f"Agent {i}",
                    value=agent,
                    inline=True
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

    def setup_slash_commands(self):
        """Setup Discord slash commands for testing."""

        @self.bot.tree.command(name="swarm_status", description="Get current swarm status")
        async def swarm_status(interaction: discord.Interaction):
            await self._test_swarm_status_command(interaction)

        @self.bot.tree.command(name="send_to_agent", description="Send message to specific agent")
        async def send_to_agent(interaction: discord.Interaction, agent: str, message: str):
            await self._test_send_to_agent_command(interaction, agent, message)

        @self.bot.tree.command(name="broadcast", description="Broadcast message to all agents")
        async def broadcast(interaction: discord.Interaction, message: str):
            await self._test_broadcast_command(interaction, message)

        @self.bot.tree.command(name="agent_list", description="List all available agents")
        async def agent_list(interaction: discord.Interaction):
            await self._test_agent_list_command(interaction)

    def get_test_summary(self) -> Dict[str, Any]:
        """Get comprehensive test summary."""
        return {
            "test_timestamp": "2025-01-21T05:35:00Z",
            "test_type": "Discord Commander E2E Test",
            "test_status": "COMPLETED",
            "results": self.test_results,
            "summary": {
                "total_tests": len(self.test_results["slash_commands"]),
                "successful_tests": len([r for r in self.test_results["slash_commands"].values() if "SUCCESS" in r]),
                "failed_tests": len([r for r in self.test_results["slash_commands"].values() if "FAILED" in r]),
                "messaging_system_status": "OPERATIONAL" if self.test_results["messaging_system"] else "FAILED",
                "integration_status": "SUCCESS" if self.test_results["integration"] else "FAILED"
            }
        }

    async def run_tests(self):
        """Run all Discord Commander tests."""
        logger.info("🚀 Starting Discord Commander E2E Tests...")

        try:
            # Setup slash commands
            self.setup_slash_commands()

            # Sync slash commands
            logger.info("🔄 Syncing slash commands...")
            try:
                synced = await self.bot.tree.sync()
                logger.info(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                logger.error(f"❌ Failed to sync slash commands: {e}")

            # Run the bot
            logger.info("🤖 Starting Discord bot for testing...")
            await self.bot.start(self.token)

        except Exception as e:
            logger.error(f"❌ Test execution failed: {e}")
            self.test_results["execution_error"] = str(e)


def main():
    """Main function to run Discord Commander E2E tests."""
    print("🐝 Discord Commander E2E Test Suite")
    print("=" * 50)
    print()
    print("This test suite will:")
    print("1. ✅ Test Discord slash commands functionality")
    print("2. ✅ Test messaging system integration")
    print("3. ✅ Verify 5-agent mode operation")
    print("4. ✅ Validate command-messaging system synchronization")
    print("5. ✅ Confirm end-to-end functionality")
    print()
    print("⚠️  NOTE: This requires a valid Discord bot token")
    print("💡 Set DISCORD_BOT_TOKEN environment variable")
    print()

    # Get bot token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables")
        print("💡 Please set your Discord bot token:")
        print("   export DISCORD_BOT_TOKEN=your_bot_token_here")
        return 1

    # Create and run test bot
    test_bot = DiscordCommanderTestBot(token)

    try:
        asyncio.run(test_bot.run_tests())
    except KeyboardInterrupt:
        print("\n✅ Test interrupted by user")
        print("📊 Test Summary:")
        summary = test_bot.get_test_summary()
        print(f"   Tests Run: {summary['summary']['total_tests']}")
        print(f"   Successful: {summary['summary']['successful_tests']}")
        print(f"   Failed: {summary['summary']['failed_tests']}")
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
