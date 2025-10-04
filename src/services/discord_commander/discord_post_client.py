#!/usr/bin/env python3
"""
Discord Post Client (SSOT)
===========================

Single Source of Truth client for Discord devlog posting.
Routes all Discord posting through Discord Manager with fallbacks.

V2 Compliant: ≤400 lines, focused Discord posting interface.
"""

import asyncio
import logging
import os
from pathlib import Path

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class DiscordPostClient:
    """Single Source of Truth client for Discord devlog posting."""

    def __init__(self):
        """Initialize Discord post client."""
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.env_file = self.project_root / ".env"

        # Initialize attributes before loading config
        self.bot = None
        self.bot_token = None
        self.default_webhook_url = None
        self.agent_channels = {}
        self.agent_webhooks = {}

        # Load environment variables
        self._load_config()

    def _load_config(self):
        """Load Discord configuration with robust parsing."""
        try:
            from dotenv import load_dotenv

            env_path = self.project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
        except ImportError:
            pass

        # Load bot token
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")

        # Load default webhook
        self.default_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

        # Load agent channels and webhooks with safe parsing
        for i in range(1, 9):
            agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
            agent_channel = os.getenv(agent_key)
            if agent_channel and agent_channel.strip() and not agent_channel.startswith("your_"):
                try:
                    self.agent_channels[f"Agent-{i}"] = int(agent_channel)
                except ValueError:
                    logger.warning(f"Invalid channel ID for {agent_key}: {agent_channel}")

            webhook_key = f"DISCORD_WEBHOOK_AGENT_{i}"
            agent_webhook = os.getenv(webhook_key)
            if agent_webhook and agent_webhook.strip() and not agent_webhook.startswith("your_"):
                self.agent_webhooks[f"Agent-{i}"] = agent_webhook

        logger.info(
            f"SSOT Config loaded - Bot: {'Yes' if self.bot_token else 'No'}, "
            f"Default Webhook: {'Yes' if self.default_webhook_url else 'No'}, "
            f"Agent Channels: {len(self.agent_channels)}, "
            f"Agent Webhooks: {len(self.agent_webhooks)}"
        )

    def set_discord_bot(self, bot_instance):
        """Set Discord bot instance from Discord Manager."""
        self.bot = bot_instance
        logger.info("Discord bot instance set for SSOT client")

    async def post_devlog(self, agent_id: str, content: str) -> bool:
        """Post devlog content via Discord using SSOT routing.

        Routing priority:
        1. Agent-specific webhook (DISCORD_WEBHOOK_AGENT_X)
        2. Bot method to agent channel (if bot available)
        3. Default webhook (logged warning)

        Args:
            agent_id: Agent identifier (e.g., "Agent-7", "captain")
            content: Message content to post

        Returns:
            bool: True if posting successful, False otherwise
        """
        try:
            # Normalize agent ID
            normalized_agent_id = self._normalize_agent_id(agent_id)

            logger.info(f"SSOT posting devlog for {agent_id} (normalized: {normalized_agent_id})")

            # Route 1: Agent-specific webhook (highest priority)
            if normalized_agent_id in self.agent_webhooks:
                webhook_url = self.agent_webhooks[normalized_agent_id]
                logger.info(f"Routing via agent webhook: {webhook_url[:50]}...")
                result = await self._post_to_webhook(content, webhook_url, normalized_agent_id)
                if result:
                    logger.info(f"✅ Devlog posted via agent webhook for {normalized_agent_id}")
                    return True

            # Route 2: Bot method to agent channel (if bot available)
            if self.bot and normalized_agent_id in self.agent_channels:
                channel_id = self.agent_channels[normalized_agent_id]
                logger.info(f"Routing via bot to agent channel: {channel_id}")
                result = await self._post_via_bot(content, channel_id, normalized_agent_id)
                if result:
                    logger.info(f"✅ Devlog posted via bot for {normalized_agent_id}")
                    return True

            # Route 3: Default webhook (fallback with warning)
            if self.default_webhook_url:
                logger.warning(
                    f"⚠️ Routing via default webhook (inaccurate routing) for {agent_id}: {self.default_webhook_url[:50]}..."
                )
                result = await self._post_to_webhook(
                    content, self.default_webhook_url, normalized_agent_id
                )
                if result:
                    logger.warning(
                        f"⚠️ Devlog posted via default webhook for {agent_id} - check channel routing!"
                    )
                    return True

            logger.error(f"❌ No Discord posting method available for {agent_id}")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to post devlog for {agent_id}: {e}")
            return False

    def _normalize_agent_id(self, agent_id: str) -> str:
        """Normalize agent ID for consistent mapping."""
        if agent_id and isinstance(agent_id, str):
            # Handle captain flag
            if agent_id.lower() in ["captain", "agent4", "agent-4"]:
                return "Agent-4"
            # Handle agent-X format
            if agent_id.lower().startswith("agent") and not agent_id.startswith("Agent"):
                return f"Agent-{agent_id.split('agent')[-1]}"
        return agent_id

    async def _post_to_webhook(self, content: str, webhook_url: str, agent_id: str) -> bool:
        """Post content to Discord webhook."""
        try:
            import aiohttp

            payload = {"content": content, "username": f"{agent_id} (SSOT)"}

            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:  # Discord webhook success
                        return True
                    else:
                        logger.error(f"Webhook failed with status {response.status}")
                        return False
                        # await response.text()

        except Exception as e:
            logger.error(f"Webhook posting error: {e}")
            return False

    async def _post_via_bot(self, content: str, channel_id: int, agent_id: str) -> bool:
        """Post content via Discord bot to channel."""
        try:
            if not DISCORD_AVAILABLE or not self.bot:
                return False

            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Bot channel {channel_id} not found")
                return False

            await channel.send(f"**{agent_id} Devlog (SSOT):**\n{content}")
            return True

        except Exception as e:
            logger.error(f"Bot posting error: {e}")
            return False

    def get_routing_info(self) -> dict:
        """Get current routing configuration info."""
        return {
            "bot_available": self.bot is not None,
            "default_webhook": bool(self.default_webhook_url),
            "agent_channels": len(self.agent_channels),
            "agent_webhooks": len(self.agent_webhooks),
            "agents_with_channels": list(self.agent_channels.keys()),
            "agents_with_webhooks": list(self.agent_webhooks.keys()),
        }


# Global SSOT client instance
_ssot_client = None


def get_discord_post_client() -> DiscordPostClient:
    """Get global SSOT client instance."""
    global _ssot_client
    if _ssot_client is None:
        _ssot_client = DiscordPostClient()
    return _ssot_client


def set_discord_bot_for_ssot(bot_instance):
    """Set Discord bot instance for SSOT client."""
    client = get_discord_post_client()
    client.set_discord_bot(bot_instance)


async def post_devlog_via_ssot(agent_id: str, content: str) -> bool:
    """Convenience function to post devlog via SSOT."""
    client = get_discord_post_client()
    return await client.post_devlog(agent_id, content)


if __name__ == "__main__":
    # Simple test
    async def test_client():
        client = get_discord_post_client()
        info = client.get_routing_info()
        print("SSOT Client Routing Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")

        # Test posting (will likely fail without proper setup)
        result = await client.post_devlog("Agent-7", "Test message via SSOT")
        print(f"Test posting result: {result}")

    asyncio.run(test_client())
