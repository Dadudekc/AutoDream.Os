#!/usr/bin/env python3
"""
Discord Devlog Service
======================

Independent Discord devlog posting service that doesn't require Discord Commander.
V2 Compliant: ≤400 lines, focused Discord integration

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Any

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class DiscordDevlogService:
    """Independent Discord devlog posting service."""

    def __init__(self):
        """Initialize Discord devlog service."""
        self.bot: commands.Bot | None = None
        self.channel_id: int | None = None
        self.is_connected = False

        # Load Discord configuration
        self._load_config()

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        logger.info("DiscordDevlogService initialized - Independent Discord integration")

    def _load_config(self) -> None:
        """Load Discord configuration from environment variables."""
        try:
            # Get Discord webhook URL (preferred method)
            self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

            # Fallback to bot token if webhook not available
            self.bot_token = os.getenv("DISCORD_BOT_TOKEN")

            # Get Discord channel ID
            channel_id_str = os.getenv("DISCORD_CHANNEL_ID")
            if channel_id_str:
                self.channel_id = int(channel_id_str)

            # Get Discord guild ID
            guild_id_str = os.getenv("DISCORD_GUILD_ID")
            if guild_id_str:
                self.guild_id = int(guild_id_str)
            else:
                self.guild_id = None

            # Load agent-specific channels
            self.agent_channels = {}
            self.agent_webhooks = {}
            for i in range(1, 9):  # Agent-1 through Agent-8
                agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
                agent_channel = os.getenv(agent_key)
                if agent_channel:
                    self.agent_channels[f"Agent-{i}"] = int(agent_channel)

                # Load agent-specific webhook URLs
                webhook_key = f"DISCORD_WEBHOOK_AGENT_{i}"
                agent_webhook = os.getenv(webhook_key)
                if agent_webhook:
                    self.agent_webhooks[f"Agent-{i}"] = agent_webhook

            logger.info(
                f"Discord config loaded - Webhook: {'Yes' if self.webhook_url else 'No'}, Bot Token: {'Yes' if self.bot_token else 'No'}, Agent Channels: {len(self.agent_channels)}, Agent Webhooks: {len(self.agent_webhooks)}"
            )

        except Exception as e:
            logger.error(f"Failed to load Discord config: {e}")
            self.webhook_url = None
            self.bot_token = None
            self.channel_id = None
            self.guild_id = None
            self.agent_channels = {}
            self.agent_webhooks = {}

    async def _create_bot(self) -> commands.Bot:
        """Create Discord bot instance."""
        intents = discord.Intents.default()
        intents.message_content = True

        bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

        @bot.event
        async def on_ready():
            logger.info(f"Discord bot ready: {bot.user}")
            self.is_connected = True

        @bot.event
        async def on_error(event, *args, **kwargs):
            logger.error(f"Discord bot error in {event}: {args}, {kwargs}")

        return bot

    async def _connect_bot(self) -> bool:
        """Connect Discord bot."""
        try:
            if not self.bot_token:
                logger.warning("No Discord bot token provided")
                return False

            if not self.bot:
                self.bot = await self._create_bot()

            if not self.is_connected:
                # Start bot in background
                asyncio.create_task(self.bot.start(self.bot_token))

                # Wait for connection
                timeout = 10  # seconds
                start_time = datetime.now()
                while not self.is_connected and (datetime.now() - start_time).seconds < timeout:
                    await asyncio.sleep(0.1)

            return self.is_connected

        except Exception as e:
            logger.error(f"Failed to connect Discord bot: {e}")
            return False

    async def _get_channel(self, agent_id: str | None = None) -> discord.TextChannel | None:
        """Get Discord channel for posting."""
        try:
            if not self.bot or not self.is_connected:
                return None

            # Determine target channel ID
            target_channel_id = None
            if agent_id and agent_id in self.agent_channels:
                target_channel_id = self.agent_channels[agent_id]
                logger.info(f"Using agent-specific channel: {agent_id} -> {target_channel_id}")
            elif self.channel_id:
                target_channel_id = self.channel_id
                logger.info(f"Using default channel: {target_channel_id}")
            else:
                logger.warning("No Discord channel ID configured")
                return None

            channel = self.bot.get_channel(target_channel_id)
            if not channel:
                logger.error(f"Discord channel {target_channel_id} not found")
                return None

            return channel

        except Exception as e:
            logger.error(f"Failed to get Discord channel: {e}")
            return None

    async def post_devlog_to_discord(self, content: str, agent_id: str | None = None) -> bool:
        """Post devlog content to Discord."""
        try:
            # If agent-specific webhook is available, use it
            if agent_id and agent_id in self.agent_webhooks:
                logger.info(f"Using agent-specific webhook for: {agent_id}")
                return await self._post_to_agent_webhook(content, agent_id)

            # If agent-specific channel is needed, use bot method
            if agent_id and agent_id in self.agent_channels and self.bot_token:
                logger.info(f"Using bot method for agent-specific channel: {agent_id}")
                return await self._post_to_bot(content, agent_id)

            # Try default webhook
            if self.webhook_url:
                return await self._post_to_webhook(content, agent_id)

            # Fallback to bot method
            if self.bot_token:
                return await self._post_to_bot(content, agent_id)

            logger.warning("No Discord configuration available, skipping Discord posting")
            return False

        except Exception as e:
            logger.error(f"Failed to post devlog to Discord: {e}")
            return False

    async def _post_to_agent_webhook(self, content: str, agent_id: str) -> bool:
        """Post devlog content to Discord using agent-specific webhook."""
        try:
            import aiohttp

            webhook_url = self.agent_webhooks[agent_id]

            # Format message for Discord webhook
            discord_message = self._format_discord_message(content, agent_id)

            # Create webhook payload
            payload = {"content": discord_message, "username": f"{agent_id}"}

            logger.info(f"Posting to agent-specific webhook for {agent_id}")

            # Post to agent-specific webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:  # Discord webhook success
                        logger.info(f"Devlog posted to agent-specific webhook for {agent_id}")
                        return True
                    else:
                        logger.error(f"Agent webhook failed with status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to post to agent webhook: {e}")
            return False

    async def _post_to_webhook(self, content: str, agent_id: str | None = None) -> bool:
        """Post devlog content to Discord using webhook (default channel only)."""
        try:
            import aiohttp

            # Format message for Discord webhook
            discord_message = self._format_discord_message(content, agent_id)

            # Create webhook payload
            payload = {
                "content": discord_message,
                "username": f"{agent_id}" if agent_id else "Agent Devlog System",
            }

            # Note: Webhooks are tied to specific channels, cannot redirect
            logger.info(f"Posting to default webhook channel for {agent_id or 'unknown agent'}")

            # Post to webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:  # Discord webhook success
                        logger.info(
                            f"Devlog posted to Discord webhook for {agent_id or 'unknown agent'}"
                        )
                        return True
                    else:
                        logger.error(f"Discord webhook failed with status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to post to Discord webhook: {e}")
            return False

    async def _post_to_bot(self, content: str, agent_id: str | None = None) -> bool:
        """Post devlog content to Discord using bot."""
        try:
            # Connect bot if not connected
            if not await self._connect_bot():
                logger.warning("Discord bot not connected, skipping Discord posting")
                return False

            # Get channel (agent-specific or default)
            channel = await self._get_channel(agent_id)
            if not channel:
                logger.warning("Discord channel not available, skipping Discord posting")
                return False

            # Format message for Discord
            discord_message = self._format_discord_message(content, agent_id)

            # Post to Discord
            await channel.send(discord_message)

            channel_info = f" (channel: {channel.id})" if channel else ""
            logger.info(
                f"Devlog posted to Discord bot for {agent_id or 'unknown agent'}{channel_info}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to post to Discord bot: {e}")
            return False

    def _format_discord_message(self, content: str, agent_id: str | None = None) -> str:
        """Format devlog content for Discord."""
        # Extract key information from content
        lines = content.split("\n")

        # Find agent ID
        if not agent_id:
            for line in lines:
                if "Agent ID:" in line:
                    agent_id = line.split("Agent ID:")[-1].strip()
                    break

        # Find action
        action = "Unknown action"
        for line in lines:
            if "**Action:**" in line:
                action = line.split("**Action:**")[-1].strip()
                break

        # Find status
        status = "Unknown status"
        for line in lines:
            if "**Status:**" in line:
                status = line.split("**Status:**")[-1].strip()
                break

        # Create Discord-friendly message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        discord_message = f"""🤖 **Agent Devlog Update**

**Agent:** {agent_id or 'Unknown'}
**Action:** {action}
**Status:** {status}
**Time:** {timestamp}

📝 **Details:**
```
{content[:1000]}{'...' if len(content) > 1000 else ''}
```

🐝 *Posted by Discord Devlog Service*"""

        return discord_message

    async def test_connection(self) -> dict[str, Any]:
        """Test Discord connection and configuration."""
        try:
            result = {
                "webhook_url_configured": bool(self.webhook_url),
                "bot_token_configured": bool(self.bot_token),
                "channel_id_configured": bool(self.channel_id),
                "guild_id_configured": bool(self.guild_id),
                "agent_channels_configured": len(self.agent_channels),
                "agent_channels": self.agent_channels,
                "agent_webhooks_configured": len(self.agent_webhooks),
                "agent_webhooks": self.agent_webhooks,
                "webhook_accessible": False,
                "bot_connected": False,
                "channel_accessible": False,
                "error": None,
            }

            # Test webhook first (preferred method)
            if self.webhook_url:
                try:
                    import aiohttp

                    async with aiohttp.ClientSession() as session:
                        async with session.get(self.webhook_url) as response:
                            if response.status == 200:
                                result["webhook_accessible"] = True
                                return result
                            else:
                                result[
                                    "error"
                                ] = f"Webhook test failed with status {response.status}"
                                return result
                except Exception as e:
                    result["error"] = f"Webhook test failed: {e}"
                    return result

            # Fallback to bot testing
            if not self.bot_token:
                result["error"] = "No Discord webhook URL or bot token configured"
                return result

            if not self.channel_id:
                result["error"] = "No Discord channel ID configured"
                return result

            # Test bot connection
            if await self._connect_bot():
                result["bot_connected"] = True

                # Test channel access
                channel = await self._get_channel()
                if channel:
                    result["channel_accessible"] = True
                else:
                    result["error"] = "Channel not accessible"
            else:
                result["error"] = "Failed to connect Discord bot"

            return result

        except Exception as e:
            return {
                "webhook_url_configured": bool(self.webhook_url),
                "bot_token_configured": bool(self.bot_token),
                "channel_id_configured": bool(self.channel_id),
                "guild_id_configured": bool(self.guild_id),
                "webhook_accessible": False,
                "bot_connected": False,
                "channel_accessible": False,
                "error": str(e),
            }

    async def disconnect(self) -> None:
        """Disconnect Discord bot."""
        try:
            if self.bot and self.is_connected:
                await self.bot.close()
                self.is_connected = False
                logger.info("Discord bot disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting Discord bot: {e}")


# CLI interface for testing
async def main():
    """CLI interface for testing Discord devlog service."""
    import argparse

    parser = argparse.ArgumentParser(description="Discord Devlog Service CLI")
    parser.add_argument("--test", action="store_true", help="Test Discord connection")
    parser.add_argument("--post", type=str, help="Post test devlog")
    parser.add_argument("--agent", type=str, default="Agent-7", help="Agent ID")

    args = parser.parse_args()

    service = DiscordDevlogService()

    if args.test:
        result = await service.test_connection()
        print("Discord Connection Test:")
        for key, value in result.items():
            print(f"  {key}: {value}")

    elif args.post:
        success = await service.post_devlog_to_discord(args.post, args.agent)
        print(f"Devlog posting {'successful' if success else 'failed'}")

    else:
        print("Use --test to test connection or --post 'message' to post devlog")

    await service.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
