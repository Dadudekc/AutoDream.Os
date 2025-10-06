#!/usr/bin/env python3
"""
Discord Devlog Service - Main Interface
======================================

Main interface for Discord devlog service.
V2 Compliant: ≤100 lines, imports from modular components.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import asyncio
import logging
from typing import Optional

from .discord_devlog_config import DiscordDevlogConfig, create_discord_config
from .discord_bot_manager import DiscordBotManager, create_discord_bot_manager
from .discord_message_formatter import DiscordMessageFormatter, create_message_formatter
from .discord_webhook_manager import DiscordWebhookManager, create_webhook_manager

logger = logging.getLogger(__name__)


class DiscordDevlogService:
    """Main Discord devlog service combining all components."""

    def __init__(self):
        """Initialize Discord devlog service."""
        # Initialize components
        self.config = create_discord_config()
        self.bot_manager = create_discord_bot_manager(self.config)
        self.formatter = create_message_formatter()
        self.webhook_manager = create_webhook_manager(self.config, self.formatter)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        logger.info("DiscordDevlogService initialized - Independent Discord integration")

    async def post_devlog_to_discord(self, content: str, agent_id: Optional[str] = None) -> bool:
        """Post devlog content to Discord with spam prevention."""
        try:
            # SPECIAL HANDLING: Agent-4 (Captain) and captain flag should ALWAYS use bot method
            if agent_id and agent_id in ["Agent-4", "agent4", "captain"] and self.config.bot_token:
                normalized_agent_id = "Agent-4" if agent_id == "captain" else agent_id
                logger.info(f"FORCING {normalized_agent_id} to use bot method")
                result = await self.bot_manager.post_message(content, normalized_agent_id)
                if result:
                    return result
                else:
                    logger.error(f"{normalized_agent_id} bot method failed")
                    return False

            # FORCE BOT METHOD: Prefer bot method for agent-specific channels
            if agent_id and agent_id in self.config.agent_channels and self.config.bot_token:
                logger.info(f"Using bot method for agent-specific channel: {agent_id}")
                result = await self.bot_manager.post_message(content, agent_id)
                if result:
                    return result
                else:
                    logger.warning(f"Bot method failed for {agent_id}, trying alternatives...")

            # If agent-specific webhook is available, use it
            if agent_id and agent_id in self.config.agent_webhooks:
                logger.info(f"Using agent-specific webhook for: {agent_id}")
                return await self.webhook_manager.post_to_agent_webhook(content, agent_id)

            # Fallback to bot method (try again if not already attempted)
            if self.config.bot_token and not (agent_id and agent_id in self.config.agent_channels):
                logger.info(f"Using bot method as fallback for: {agent_id}")
                return await self.bot_manager.post_message(content, agent_id)

            # Last resort: Try default webhook
            if self.config.webhook_url:
                logger.info(f"Using default webhook as last resort for: {agent_id}")
                return await self.webhook_manager.post_to_webhook(content, agent_id)

            logger.warning("No Discord configuration available, skipping Discord posting")
            return False

        except Exception as e:
            logger.error(f"Failed to post devlog to Discord: {e}")
            return False

    async def test_connection(self) -> dict:
        """Test Discord connection."""
        try:
            # Test webhook first (preferred method)
            if self.config.webhook_url:
                webhook_result = await self.webhook_manager.test_webhook()
                if webhook_result["webhook_accessible"]:
                    return webhook_result

            # Fallback to bot testing
            return await self.bot_manager.test_connection()

        except Exception as e:
            return {
                "webhook_url_configured": bool(self.config.webhook_url),
                "bot_token_configured": bool(self.config.bot_token),
                "channel_id_configured": bool(self.config.channel_id),
                "webhook_accessible": False,
                "bot_connected": False,
                "channel_accessible": False,
                "error": str(e),
            }

    async def disconnect(self) -> None:
        """Disconnect Discord bot."""
        await self.bot_manager.disconnect()

    def get_status(self) -> dict:
        """Get service status."""
        return {
            "config": self.config.get_config_summary(),
            "bot": self.bot_manager.get_status(),
            "webhook": self.webhook_manager.get_webhook_summary(),
            "is_configured": self.config.is_configured()
        }


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