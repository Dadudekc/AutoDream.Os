#!/usr/bin/env python3
"""
Discord Devlog Service - Webhook Manager
========================================

Manages Discord webhook posting for devlogs.
V2 Compliant: ≤400 lines, focused webhook operations.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import asyncio
import logging
from typing import Optional

from .discord_devlog_config import DiscordDevlogConfig
from .discord_message_formatter import DiscordMessageFormatter

logger = logging.getLogger(__name__)


class DiscordWebhookManager:
    """Manages Discord webhook posting."""

    def __init__(self, config: DiscordDevlogConfig, formatter: DiscordMessageFormatter):
        """Initialize webhook manager."""
        self.config = config
        self.formatter = formatter

    async def post_to_webhook(self, content: str, agent_id: Optional[str] = None) -> bool:
        """Post content to Discord webhook."""
        try:
            if not self.config.webhook_url:
                logger.warning("No Discord webhook URL configured")
                return False

            import aiohttp

            # Format message
            formatted_message = self.formatter.format_message(content, agent_id)
            if formatted_message is None:
                logger.info(f"Message suppressed for {agent_id}")
                return False

            # Create webhook payload
            payload = {"content": formatted_message}
            if agent_id:
                payload["username"] = agent_id

            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"Message posted to webhook for {agent_id}")
                        return True
                    else:
                        logger.error(f"Webhook post failed with status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to post to webhook: {e}")
            return False

    async def post_to_agent_webhook(self, content: str, agent_id: str) -> bool:
        """Post content to agent-specific webhook."""
        try:
            if agent_id not in self.config.agent_webhooks:
                logger.warning(f"No webhook configured for agent {agent_id}")
                return False

            import aiohttp

            webhook_url = self.config.agent_webhooks[agent_id]

            # Format message
            formatted_message = self.formatter.format_message(content, agent_id)
            if formatted_message is None:
                logger.info(f"Message suppressed for {agent_id}")
                return False

            # Create webhook payload
            payload = {"content": formatted_message, "username": agent_id}

            logger.info(f"Posting to agent-specific webhook for {agent_id}")

            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"Message posted to agent webhook for {agent_id}")
                        return True
                    else:
                        logger.error(f"Agent webhook post failed with status {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Failed to post to agent webhook: {e}")
            return False

    async def test_webhook(self) -> dict:
        """Test webhook connectivity."""
        try:
            result = {
                "webhook_url_configured": bool(self.config.webhook_url),
                "webhook_accessible": False,
                "error": None,
            }

            if not self.config.webhook_url:
                result["error"] = "No Discord webhook URL configured"
                return result

            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(self.config.webhook_url) as response:
                    if response.status == 200:
                        result["webhook_accessible"] = True
                        return result
                    else:
                        result["error"] = f"Webhook test failed with status {response.status}"
                        return result

        except Exception as e:
            result = {
                "webhook_url_configured": bool(self.config.webhook_url),
                "webhook_accessible": False,
                "error": str(e),
            }
            return result

    async def test_agent_webhook(self, agent_id: str) -> dict:
        """Test agent-specific webhook."""
        try:
            result = {
                "agent_id": agent_id,
                "webhook_configured": agent_id in self.config.agent_webhooks,
                "webhook_accessible": False,
                "error": None,
            }

            if agent_id not in self.config.agent_webhooks:
                result["error"] = f"No webhook configured for agent {agent_id}"
                return result

            import aiohttp

            webhook_url = self.config.agent_webhooks[agent_id]

            async with aiohttp.ClientSession() as session:
                async with session.get(webhook_url) as response:
                    if response.status == 200:
                        result["webhook_accessible"] = True
                        return result
                    else:
                        result["error"] = f"Agent webhook test failed with status {response.status}"
                        return result

        except Exception as e:
            result = {
                "agent_id": agent_id,
                "webhook_configured": agent_id in self.config.agent_webhooks,
                "webhook_accessible": False,
                "error": str(e),
            }
            return result

    def get_webhook_summary(self) -> dict:
        """Get webhook configuration summary."""
        return {
            "default_webhook_configured": bool(self.config.webhook_url),
            "agent_webhooks_count": len(self.config.agent_webhooks),
            "agent_webhooks": list(self.config.agent_webhooks.keys()),
            "is_available": bool(self.config.webhook_url or self.config.agent_webhooks)
        }


def create_webhook_manager(config: DiscordDevlogConfig, formatter: DiscordMessageFormatter) -> DiscordWebhookManager:
    """Create webhook manager."""
    return DiscordWebhookManager(config, formatter)

