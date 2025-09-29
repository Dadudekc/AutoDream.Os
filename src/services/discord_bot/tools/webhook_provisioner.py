"""
Discord Webhook Provisioner
==========================
Manages Discord webhook creation, rotation, and revocation for agents.
"""

import logging
from typing import Any

import discord
from src.services.secret_store import SecretStore

logger = logging.getLogger(__name__)


class DiscordWebhookProvisioner:
    """Manages Discord webhooks for agent event posting."""

    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def create(self, agent_id: str, channel: discord.TextChannel) -> str | None:
        """
        Create a webhook for an agent in a specific channel.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            channel: Discord text channel

        Returns:
            Webhook URL if successful, None otherwise
        """
        # Check permissions
        perms = channel.permissions_for(channel.guild.me)
        if not (perms.view_channel and perms.manage_webhooks):
            logger.warning("Missing permissions in #%s", channel.name)
            return None

        try:
            # Create webhook with descriptive name
            name = f"{agent_id}-events"
            webhook = await channel.create_webhook(
                name=name, reason=f"Provision webhook for {agent_id}"
            )

            # Store securely
            SecretStore.set_webhook(agent_id, webhook.url, channel.id, webhook.id)

            logger.info(
                "Webhook created: agent=%s channel=%s id=%s", agent_id, channel.id, webhook.id
            )
            return webhook.url

        except Exception as e:
            logger.error("Failed to create webhook for %s: %s", agent_id, e)
            return None

    async def rotate(self, agent_id: str) -> str | None:
        """
        Rotate (recreate) an existing webhook.

        Args:
            agent_id: Agent identifier

        Returns:
            New webhook URL if successful, None otherwise
        """
        existing = SecretStore.get_webhook(agent_id)
        if not existing:
            logger.warning("No existing webhook to rotate for %s", agent_id)
            return None

        channel = self.bot.get_channel(existing["channel_id"])
        if not isinstance(channel, discord.TextChannel):
            logger.error("Channel not found for %s", agent_id)
            return None

        try:
            # Delete old webhook
            webhook = await channel.fetch_webhook(existing["webhook_id"])
            await webhook.delete(reason=f"Rotate webhook for {agent_id}")
            logger.info("Deleted old webhook for %s", agent_id)
        except Exception as e:
            logger.warning("Failed to delete old webhook for %s: %s", agent_id, e)

        # Create new webhook
        return await self.create(agent_id, channel)

    async def revoke(self, agent_id: str) -> bool:
        """
        Revoke (delete) a webhook and remove from storage.

        Args:
            agent_id: Agent identifier

        Returns:
            True if successful, False otherwise
        """
        existing = SecretStore.get_webhook(agent_id)
        if not existing:
            logger.warning("No webhook to revoke for %s", agent_id)
            return False

        success = False
        try:
            channel = self.bot.get_channel(existing["channel_id"])
            if isinstance(channel, discord.TextChannel):
                webhook = await channel.fetch_webhook(existing["webhook_id"])
                await webhook.delete(reason=f"Revoke webhook for {agent_id}")
                success = True
                logger.info("Deleted webhook for %s", agent_id)
        except Exception as e:
            logger.warning("Failed to delete webhook for %s: %s", agent_id, e)

        # Always remove from storage
        SecretStore.delete_webhook(agent_id)
        return success

    async def test(self, agent_id: str) -> bool:
        """
        Test webhook by sending a test message.

        Args:
            agent_id: Agent identifier

        Returns:
            True if test successful, False otherwise
        """
        existing = SecretStore.get_webhook(agent_id)
        if not existing:
            logger.warning("No webhook to test for %s", agent_id)
            return False

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": f"TEST_EVENT|{agent_id}|webhook_provisioner_test|ts={agent_id}"
                }
                async with session.post(existing["url"], json=payload) as response:
                    success = response.status in (200, 204)
                    if success:
                        logger.info("Test message sent successfully for %s", agent_id)
                    else:
                        logger.warning(
                            "Test message failed for %s: status %s", agent_id, response.status
                        )
                    return success
        except Exception as e:
            logger.error("Test message failed for %s: %s", agent_id, e)
            return False

    async def get_status(self, agent_id: str) -> dict[str, Any] | None:
        """
        Get webhook status information.

        Args:
            agent_id: Agent identifier

        Returns:
            Status dict or None if not found
        """
        webhook_data = SecretStore.get_webhook(agent_id)
        if not webhook_data:
            return None

        try:
            channel = self.bot.get_channel(webhook_data["channel_id"])
            if isinstance(channel, discord.TextChannel):
                webhook = await channel.fetch_webhook(webhook_data["webhook_id"])
                return {
                    "agent_id": agent_id,
                    "channel_name": channel.name,
                    "webhook_name": webhook.name,
                    "webhook_id": webhook.id,
                    "created_at": webhook.created_at.isoformat() if webhook.created_at else None,
                }
        except Exception as e:
            logger.warning("Failed to get status for %s: %s", agent_id, e)

        return webhook_data


def channel_from_id(bot: discord.Client, channel_id: int) -> discord.TextChannel | None:
    """
    Get text channel from ID.

    Args:
        bot: Discord bot instance
        channel_id: Channel ID

    Returns:
        TextChannel or None if not found/invalid
    """
    channel = bot.get_channel(channel_id)
    return channel if isinstance(channel, discord.TextChannel) else None
