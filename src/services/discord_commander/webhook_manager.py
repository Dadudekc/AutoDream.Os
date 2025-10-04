#!/usr/bin/env python3
"""
Discord Webhook Manager
=======================

Webhook provisioning and management for Discord Commander.
Handles creation, deletion, and configuration of Discord webhooks.

V2 Compliant: ≤400 lines, focused webhook management
"""

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


class WebhookManager:
    """Manages Discord webhooks for agent-specific channels."""

    def __init__(self, bot):
        """Initialize webhook manager."""
        self.bot = bot
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.env_file = self.project_root / ".env"

    async def create_webhook(self, channel_id: int, webhook_name: str = None) -> str | None:
        """Create a webhook for the specified channel."""
        try:
            if not DISCORD_AVAILABLE:
                logger.error("Discord library not available")
                return None

            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return None

            # Default webhook name
            if not webhook_name:
                webhook_name = f"Agent Webhook - {channel.name}"

            # Check if webhook already exists
            existing_webhooks = await channel.webhooks()
            for webhook in existing_webhooks:
                if webhook_name in webhook.name or "Agent" in webhook.name:
                    logger.info(f"Webhook already exists: {webhook.url}")
                    return webhook.url

            # Create new webhook
            webhook = await channel.create_webhook(name=webhook_name)
            logger.info(f"Created webhook: {webhook.url}")
            return webhook.url

        except Exception as e:
            logger.error(f"Failed to create webhook: {e}")
            return None

    async def delete_webhook(self, channel_id: int, webhook_name: str = None) -> bool:
        """Delete webhook from the specified channel."""
        try:
            if not DISCORD_AVAILABLE:
                return False

            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return False

            webhooks = await channel.webhooks()
            for webhook in webhooks:
                if not webhook_name or webhook_name in webhook.name:
                    await webhook.delete()
                    logger.info(f"Deleted webhook: {webhook.name}")
                    return True

            logger.warning("No matching webhook found to delete")
            return False

        except Exception as e:
            logger.error(f"Failed to delete webhook: {e}")
            return False

    async def list_webhooks(self, channel_id: int) -> list:
        """List all webhooks in the specified channel."""
        try:
            if not DISCORD_AVAILABLE:
                return []

            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return []

            webhooks = await channel.webhooks()
            return [{"name": w.name, "url": w.url} for w in webhooks]

        except Exception as e:
            logger.error(f"Failed to list webhooks: {e}")
            return []

    async def provision_agent_webhook(self, agent_id: str) -> str | None:
        """Provision webhook for specific agent."""
        try:
            # Get agent channel ID from environment
            channel_key = f"DISCORD_CHANNEL_AGENT_{agent_id.split('-')[1]}"
            channel_id_str = os.getenv(channel_key)

            if not channel_id_str:
                logger.error(f"Channel ID not found for {agent_id}")
                return None

            channel_id = int(channel_id_str)
            webhook_name = f"{agent_id} Devlog Webhook"

            webhook_url = await self.create_webhook(channel_id, webhook_name)
            if webhook_url:
                await self._update_env_file(channel_key.replace("CHANNEL", "WEBHOOK"), webhook_url)
                logger.info(f"Provisioned webhook for {agent_id}: {webhook_url[:50]}...")

            return webhook_url

        except Exception as e:
            logger.error(f"Failed to provision webhook for {agent_id}: {e}")
            return None

    async def _update_env_file(self, key: str, value: str) -> bool:
        """Update environment file with webhook URL."""
        try:
            if not self.env_file.exists():
                logger.warning(".env file not found")
                return False

            # Read current content
            with open(self.env_file) as f:
                lines = f.readlines()

            # Update or add the key-value pair
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    updated = True
                    break

            if not updated:
                lines.append(f"{key}={value}\n")

            # Write back to file
            with open(self.env_file, "w") as f:
                f.writelines(lines)

            logger.info(f"Updated .env file: {key}={value[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to update .env file: {e}")
            return False

    async def provision_all_agent_webhooks(self) -> dict[str, str | None]:
        """Provision webhooks for all configured agents."""
        results = {}

        for agent_num in range(1, 9):
            agent_id = f"Agent-{agent_num}"
            channel_key = f"DISCORD_CHANNEL_AGENT_{agent_num}"

            if os.getenv(channel_key):
                webhook_url = await self.provision_agent_webhook(agent_id)
                results[agent_id] = webhook_url
            else:
                logger.info(f"No channel configured for {agent_id}")
                results[agent_id] = None

        return results

    def get_command_handlers(self) -> dict[str, callable]:
        """Get command handlers for Discord bot."""
        return {
            "create_webhook": self._cmd_create_webhook,
            "delete_webhook": self._cmd_delete_webhook,
            "list_webhooks": self._cmd_list_webhooks,
            "provision_agent": self._cmd_provision_agent,
            "provision_all": self._cmd_provision_all,
        }

    async def _cmd_create_webhook(self, ctx, channel_id: int, webhook_name: str = None):
        """Command handler for creating webhook."""
        webhook_url = await self.create_webhook(channel_id, webhook_name)

        if webhook_url:
            await ctx.send(f"✅ Created webhook: {webhook_url[:50]}...")
        else:
            await ctx.send("❌ Failed to create webhook")

    async def _cmd_delete_webhook(self, ctx, channel_id: int, webhook_name: str = None):
        """Command handler for deleting webhook."""
        success = await self.delete_webhook(channel_id, webhook_name)

        if success:
            await ctx.send("✅ Webhook deleted successfully")
        else:
            await ctx.send("❌ Failed to delete webhook")

    async def _cmd_list_webhooks(self, ctx, channel_id: int):
        """Command handler for listing webhooks."""
        webhooks = await self.list_webhooks(channel_id)

        if webhooks:
            webhook_list = "\n".join([f"- {w['name']}" for w in webhooks])
            await ctx.send(f"📋 **Webhooks in channel {channel_id}:**\n{webhook_list}")
        else:
            await ctx.send(f"📋 No webhooks found in channel {channel_id}")

    async def _cmd_provision_agent(self, ctx, agent_id: str):
        """Command handler for provisioning agent webhook."""
        webhook_url = await self.provision_agent_webhook(agent_id)

        if webhook_url:
            await ctx.send(f"✅ Provisions webhook for {agent_id}: {webhook_url[:50]}...")
        else:
            await ctx.send(f"❌ Failed to provision webhook for {agent_id}")

    async def _cmd_provision_all(self, ctx):
        """Command handler for provisioning all agent webhooks."""
        await ctx.send("🔄 Provisioning webhooks for all agents...")

        results = await self.provision_all_agent_webhooks()

        success_count = sum(1 for url in results.values() if url)
        await ctx.send(f"✅ Provisioned {success_count}/8 agent webhooks")

        # Show detailed results
        for agent_id, webhook_url in results.items():
            if webhook_url:
                await ctx.send(f"✅ {agent_id}: {webhook_url[:30]}...")
            else:
                await ctx.send(f"❌ {agent_id}: Failed")


# CLI interface for webhook management
class WebhookCLI:
    """Command-line interface for webhook management."""

    def __init__(self, bot):
        """Initialize CLI."""
        self.manager = WebhookManager(bot)

    async def create_webhook_cli(self, channel_id: int, webhook_name: str = None):
        """CLI command to create webhook."""
        webhook_url = await self.manager.create_webhook(channel_id, webhook_name)

        if webhook_url:
            print(f"✅ Created webhook: {webhook_url}")
            return True
        else:
            print("❌ Failed to create webhook")
            return False

    async def provision_agent_cli(self, agent_id: str):
        """CLI command to provision agent webhook."""
        webhook_url = await self.manager.provision_agent_webhook(agent_id)

        if webhook_url:
            print(f"✅ Provisions webhook for {agent_id}: {webhook_url}")
            return True
        else:
            print(f"❌ Failed to provision webhook for {agent_id}")
            return False

    async def provision_all_cli(self):
        """CLI command to provision all agent webhooks."""
        print("🔄 Provisioning webhooks for all agents...")

        results = await self.manager.provision_all_agent_webhooks()

        success_count = sum(1 for url in results.values() if url)
        print(f"✅ Provisioned {success_count}/8 agent webhooks")

        for agent_id, webhook_url in results.items():
            if webhook_url:
                print(f"✅ {agent_id}: {webhook_url[:50]}...")
            else:
                print(f"❌ {agent_id}: Failed")

        return success_count > 0


if __name__ == "__main__":
    print("Discord Webhook Manager - Use with Discord Commander bot")
    print("Commands available: create_webhook, provision_agent, provision_all")
