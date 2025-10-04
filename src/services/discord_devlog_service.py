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
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

# Load environment variables from .env file
# Environment will be loaded manually in _load_config

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
            # Load .env file manually like Discord Manager does
            env_file = Path(__file__).parent.parent.parent.parent / ".env"
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            value = value.strip('"\'')
                            os.environ[key] = value
            
            # Get Discord webhook URL (preferred method)
            self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
            logger.debug(f"Webhook URL loaded: {'Yes' if self.webhook_url else 'No'}")

            # Fallback to bot token if webhook not available
            self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
            logger.debug(f"Bot token loaded: {'Yes' if self.bot_token else 'No'}")

            # Get Discord channel ID
            channel_id_str = os.getenv("DISCORD_CHANNEL_ID")
            if channel_id_str:
                logger.debug(f"Channel ID string: {channel_id_str}")
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
                if agent_channel and agent_channel.strip() and not agent_channel.startswith('your_'):
                    try:
                        self.agent_channels[f"Agent-{i}"] = int(agent_channel)
                    except ValueError:
                        logger.warning(f"Invalid channel ID for {agent_key}: {agent_channel}")

                # Load agent-specific webhook URLs
                webhook_key = f"DISCORD_WEBHOOK_AGENT_{i}"
                agent_webhook = os.getenv(webhook_key)
                if agent_webhook and agent_webhook.strip() and not agent_webhook.startswith('your_'):
                    self.agent_webhooks[f"Agent-{i}"] = agent_webhook

            logger.info(
                f"Discord config loaded - Webhook: {'Yes' if self.webhook_url else 'No'}, Bot Token: {'Yes' if self.bot_token else 'No'}, Agent Channels: {len(self.agent_channels)}, Agent Webhooks: {len(self.agent_webhooks)}"
            )
            logger.info(f"Agent channels loaded: {list(self.agent_channels.keys())}")
            logger.info(f"Agent webhooks loaded: {list(self.agent_webhooks.keys())}")
            if self.webhook_url:
                logger.info(f"Default webhook URL: {self.webhook_url[:50]}...")

        except Exception as e:
            logger.error(f"Failed to load Discord config: {e}")
            # Fallback: Try to load basic webhook URL even if config parsing fails
            try:
                # Load .env file manually for fallback
                env_file = Path(__file__).parent.parent.parent.parent / ".env"
                if env_file.exists():
                    with open(env_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                value = value.strip('"\'')
                                os.environ[key] = value
                
                self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
                self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
                logger.info(f"Fallback config loaded - Webhook: {'Yes' if self.webhook_url else 'No'}, Bot: {'Yes' if self.bot_token else 'No'}")
                logger.info(f"Bot token length: {len(self.bot_token) if self.bot_token else 0}")
                
                # DEPRECATION WARNING
                logger.warning("⚠️ LEGACY DISCORD_DEVLOG_SERVICE: This service is deprecated. Use Discord Manager (discord_post_client) as SSOT.")
                logger.info("💡 Enable DEVLOG_POST_VIA_MANAGER=true to use new SSOT routing")
            except Exception as fallback_error:
                logger.error(f"Fallback config loading also failed: {fallback_error}")
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
        """Post devlog content to Discord with spam prevention."""
        try:
            # ANTI-SPAM: Check for spam patterns before processing
            formatted_message = self._format_discord_message(content, agent_id)
            if formatted_message is None:
                logger.info(f"Spam filter triggered for {agent_id}, content suppressed")
                return False  # Successfully suppressed spam
            
            # SPECIAL HANDLING: Agent-4 (Captain) and captain flag should ALWAYS use major channel
            if agent_id and agent_id in ["Agent-4", "agent4", "captain"] and self.bot_token:
                # Normalize captain flag to Agent-4
                normalized_agent_id = "Agent-4" if agent_id == "captain" else agent_id
                logger.info(f"FORCING {normalized_agent_id} to use major channel - NO webhook fallback")
                result = await self._post_to_bot(formatted_message, normalized_agent_id)
                if result:
                    return result
                else:
                    logger.error(f"{normalized_agent_id} bot method failed - NOT falling back to webhook")
                    return False

            # FORCE BOT METHOD: Prefer bot method for agent-specific channels
            if agent_id and agent_id in self.agent_channels and self.bot_token:
                logger.info(f"Using bot method for agent-specific channel: {agent_id}")
                result = await self._post_to_bot(formatted_message, agent_id)
                if result:
                    return result
                else:
                    logger.warning(f"Bot method failed for {agent_id}, trying alternatives...")

            # If agent-specific webhook is available, use it
            if agent_id and agent_id in self.agent_webhooks:
                logger.info(f"Using agent-specific webhook for: {agent_id}")
                return await self._post_to_agent_webhook(formatted_message, agent_id)

            # Fallback to bot method (try again if not already attempted)
            if self.bot_token and not (agent_id and agent_id in self.agent_channels):
                logger.info(f"Using bot method as fallback for: {agent_id}")
                return await self._post_to_bot(formatted_message, agent_id)

            # Last resort: Try default webhook for all agents including captain
            if self.webhook_url:
                logger.info(f"Using default webhook as last resort for: {agent_id}")
                logger.warning(f"⚠️  WARNING: Default webhook routes to 'dreamscape devlog' channel, not agent-specific channel!")
                return await self._post_to_webhook(formatted_message, agent_id)

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

            # CRITICAL FIX: Apply spam filtering to webhook posts
            discord_message = self._format_discord_message(content, agent_id)
            if discord_message is None:
                logger.info(f"Spam filter triggered for webhook, content suppressed for {agent_id}")
                return False  # Successfully suppressed spam

            # Create webhook payload
            payload = {
                "content": discord_message,
                "username": f"{agent_id}" if agent_id else "Agent Devlog System",
            }

            # Note: Webhooks are tied to specific channels, cannot redirect
            logger.info(f"Posting to default webhook channel for {agent_id or 'unknown agent'} (spam filtered)")

            # Post to webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:  # Discord webhook success
                        logger.info(
                            f"Devlog posted to Discord webhook for {agent_id or 'unknown agent'} (filtered)"
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
        """Format devlog content for Discord with minimal spam prevention."""
        # MINIMAL SPAM FILTER: Only block extreme spam patterns
        # Block only the most obvious automated reminder spam loops
        if "📝 DISCORD DEVLOG REMINDER:" in content and "devlogs/ directory" in content and content.count("📝") > 2:
            return None  # Suppress only repeated automated Discord reminder spam
            
        # Block only extreme coordination theater patterns (very specific)
        if ("coordination status update confirmed" in content.lower() and 
            "acknowledgment acknowledged" in content.lower() and 
            "acknowledgment acknowledged" in content.lower()):
            return None  # Suppress only circular acknowledgment loops
            
        # Block only excessive "ultimate" spam (5+ occurrences)
        if content.count("ultimate") >= 5 and "coordination" in content.lower():
            return None  # Suppress only extreme ultimate coordination theater
            
        # Extract key information from content
        lines = content.split("\n")

        # Find agent ID
        if not agent_id:
            for line in lines:
                if "Agent ID:" in line:
                    agent_id = line.split("Agent ID:")[-1].strip()
                    break

        # Find action - improved extraction with fallback
        action = "Agent Communication"
        for line in lines:
            if "**Action:**" in line:
                action = line.split("**Action:**")[-1].strip()
                break
            elif "Action:" in line:
                action = line.split("Action:")
                if len(action) > 1:
                    action = action[-1].strip()
                break
        
        # Extract action from content if no structured format found
        if action == "Agent Communication":
            # Try to extract meaningful action from message content
            words = content.replace("\n", " ").split()
            if len(words) > 2:
                action = " ".join(words[:4])[:40] + ("..." if len(" ".join(words[:4])) > 40 else "")

        # Find status - improved extraction with fallback
        status = "Communication Active"
        for line in lines:
            if "**Status:**" in line:
                status = line.split("**Status:**")[-1].strip()
                break
            elif "- **Status:**" in line:
                status = line.split("- **Status:**")[-1].strip()
                break
            elif "Status:" in line:
                status = line.split("Status:")[-1].strip()
                break

        # MINIMAL ANTI-SPAM: Only block extreme coordination theater in action
        if ("acknowledgment" in action.lower() and "coordination" in action.lower() and 
            action.lower().count("acknowledgment") >= 3):
            return None  # Only block excessive acknowledgment spam
            
        # Create Discord-friendly message (condensed format)
        timestamp = datetime.now().strftime("%H:%M:%S")

        discord_message = f"""🤖 **{agent_id or 'Agent'}**: {action}
Status: {status} | {timestamp}

🐝 *Devlog Service*"""

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
