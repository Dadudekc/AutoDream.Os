#!/usr/bin/env python3
"""
Discord Webhook Management Commands
===================================

Bot commands for creating and managing Discord webhooks programmatically.
Enables agents to fully control Discord server webhook infrastructure.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class WebhookCommands(commands.Cog):
    """Discord bot commands for webhook management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)

    @commands.command(name="create_webhook")
    @commands.has_permissions(administrator=True)
    async def create_webhook(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        webhook_name: str = "Agent Webhook",
        *,
        reason: str = "Created by agent automation",
    ):
        """
        Create a webhook for a specific channel.

        Usage:
            !create_webhook #channel-name Webhook-Name
            !create_webhook 1234567890 Custom-Webhook

        Examples:
            !create_webhook #devlogs Agent-8-Devlog-Webhook
            !create_webhook #status Status-Update-Webhook
        """
        try:
            # Create webhook
            webhook = await channel.create_webhook(name=webhook_name, reason=reason)

            # Save to config
            config_file = self.config_dir / "discord_webhooks.json"
            webhooks_config = {}

            if config_file.exists():
                with open(config_file) as f:
                    webhooks_config = json.load(f)

            # Add new webhook
            webhook_key = f"{channel.name}_webhook"
            webhooks_config[webhook_key] = {
                "webhook_url": webhook.url,
                "webhook_id": str(webhook.id),
                "channel_id": str(channel.id),
                "channel_name": channel.name,
                "webhook_name": webhook_name,
                "created_by": str(ctx.author),
                "created_at": discord.utils.utcnow().isoformat(),
            }

            # Save config
            with open(config_file, "w") as f:
                json.dump(webhooks_config, f, indent=2)

            # Create success embed
            embed = discord.Embed(
                title="✅ Webhook Created Successfully!",
                description=f"Created webhook for {channel.mention}",
                color=discord.Color.green(),
            )

            embed.add_field(name="Webhook Name", value=webhook_name, inline=True)
            embed.add_field(name="Channel", value=channel.mention, inline=True)
            embed.add_field(name="Webhook ID", value=str(webhook.id), inline=False)
            embed.add_field(
                name="⚠️ Webhook URL",
                value="Saved to config/discord_webhooks.json (DO NOT share publicly!)",
                inline=False,
            )
            embed.add_field(name="Usage", value=f"Use config key: `{webhook_key}`", inline=False)

            await ctx.send(embed=embed)

            # Send webhook URL in DM for security
            try:
                dm_embed = discord.Embed(
                    title="🔐 Webhook URL (Private)",
                    description=f"Webhook URL for {channel.name}",
                    color=discord.Color.blue(),
                )
                dm_embed.add_field(name="URL", value=webhook.url, inline=False)
                dm_embed.add_field(
                    name="Security",
                    value="⚠️ Keep this URL private! Anyone with this URL can post to your channel.",
                    inline=False,
                )
                await ctx.author.send(embed=dm_embed)
            except discord.Forbidden:
                await ctx.send("⚠️ Couldn't DM you the webhook URL. Check config file.")

            logger.info(f"Created webhook '{webhook_name}' for {channel.name}")

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to create webhooks in that channel!")
        except Exception as e:
            logger.error(f"Failed to create webhook: {e}")
            await ctx.send(f"❌ Failed to create webhook: {str(e)}")

    @commands.command(name="list_webhooks")
    @commands.has_permissions(administrator=True)
    async def list_webhooks(
        self, ctx: commands.Context, channel: discord.TextChannel | None = None
    ):
        """
        List all webhooks in the server or specific channel.

        Usage:
            !list_webhooks              # List all server webhooks
            !list_webhooks #channel     # List webhooks for specific channel
        """
        try:
            if channel:
                # List webhooks for specific channel
                webhooks = await channel.webhooks()
                title = f"Webhooks in #{channel.name}"
            else:
                # List all server webhooks
                webhooks = await ctx.guild.webhooks()
                title = f"All Webhooks in {ctx.guild.name}"

            if not webhooks:
                await ctx.send("No webhooks found.")
                return

            embed = discord.Embed(
                title=title,
                description=f"Found {len(webhooks)} webhook(s)",
                color=discord.Color.blue(),
            )

            for webhook in webhooks[:25]:  # Discord embed limit
                channel_info = f"<#{webhook.channel_id}>" if webhook.channel_id else "Unknown"
                creator = webhook.user.mention if webhook.user else "Unknown"

                embed.add_field(
                    name=f"📌 {webhook.name}",
                    value=f"**Channel:** {channel_info}\n"
                    f"**Created by:** {creator}\n"
                    f"**ID:** `{webhook.id}`",
                    inline=False,
                )

            if len(webhooks) > 25:
                embed.set_footer(text=f"Showing first 25 of {len(webhooks)} webhooks")

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to view webhooks!")
        except Exception as e:
            logger.error(f"Failed to list webhooks: {e}")
            await ctx.send(f"❌ Failed to list webhooks: {str(e)}")

    @commands.command(name="delete_webhook")
    @commands.has_permissions(administrator=True)
    async def delete_webhook(self, ctx: commands.Context, webhook_id: str):
        """
        Delete a webhook by ID.

        Usage:
            !delete_webhook <webhook_id>

        Example:
            !delete_webhook 1234567890123456789
        """
        try:
            # Get webhook
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            # Confirm deletion
            confirm_embed = discord.Embed(
                title="⚠️ Confirm Webhook Deletion",
                description="Are you sure you want to delete this webhook?",
                color=discord.Color.orange(),
            )
            confirm_embed.add_field(name="Webhook Name", value=webhook.name, inline=True)
            confirm_embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            # Add confirmation buttons
            view = WebhookDeleteConfirmView(webhook, ctx.author)
            message = await ctx.send(embed=confirm_embed, view=view)

            # Wait for confirmation
            await view.wait()

            if view.confirmed:
                await webhook.delete(reason=f"Deleted by {ctx.author}")

                # Update config
                self._remove_from_config(webhook_id)

                success_embed = discord.Embed(
                    title="✅ Webhook Deleted",
                    description=f"Successfully deleted webhook '{webhook.name}'",
                    color=discord.Color.green(),
                )
                await message.edit(embed=success_embed, view=None)
                logger.info(f"Deleted webhook '{webhook.name}' (ID: {webhook_id})")
            else:
                await message.edit(content="❌ Webhook deletion cancelled.", embed=None, view=None)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete that webhook!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to delete webhook: {e}")
            await ctx.send(f"❌ Failed to delete webhook: {str(e)}")

    @commands.command(name="test_webhook")
    @commands.has_permissions(administrator=True)
    async def test_webhook(self, ctx: commands.Context, webhook_id: str):
        """
        Test a webhook by sending a test message.

        Usage:
            !test_webhook <webhook_id>
        """
        try:
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            # Send test message
            await webhook.send(
                content="✅ **Webhook Test Successful!**\n"
                f"This webhook is working correctly.\n"
                f"Tested by: {ctx.author.mention}",
                username="Webhook Test Bot",
            )

            embed = discord.Embed(
                title="✅ Webhook Test Sent",
                description=f"Test message sent to webhook '{webhook.name}'",
                color=discord.Color.green(),
            )
            embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            await ctx.send(embed=embed)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to use that webhook!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to test webhook: {e}")
            await ctx.send(f"❌ Failed to test webhook: {str(e)}")

    @commands.command(name="webhook_info")
    @commands.has_permissions(administrator=True)
    async def webhook_info(self, ctx: commands.Context, webhook_id: str):
        """
        Get detailed information about a webhook.

        Usage:
            !webhook_info <webhook_id>
        """
        try:
            webhook = await self.bot.fetch_webhook(int(webhook_id))

            embed = discord.Embed(
                title="📋 Webhook Information",
                description=f"Details for webhook '{webhook.name}'",
                color=discord.Color.blue(),
            )

            embed.add_field(name="Name", value=webhook.name, inline=True)
            embed.add_field(name="ID", value=str(webhook.id), inline=True)
            embed.add_field(name="Channel", value=f"<#{webhook.channel_id}>", inline=True)

            if webhook.user:
                embed.add_field(name="Created By", value=webhook.user.mention, inline=True)

            if webhook.avatar:
                embed.set_thumbnail(url=webhook.avatar.url)

            # Send webhook URL in DM
            try:
                dm_embed = discord.Embed(
                    title="🔐 Webhook URL (Private)",
                    description=f"URL for webhook '{webhook.name}'",
                    color=discord.Color.blue(),
                )
                dm_embed.add_field(name="URL", value=webhook.url, inline=False)
                await ctx.author.send(embed=dm_embed)

                embed.add_field(
                    name="Webhook URL", value="Sent to your DMs (keep it private!)", inline=False
                )
            except discord.Forbidden:
                embed.add_field(
                    name="Webhook URL", value="Enable DMs to receive the webhook URL", inline=False
                )

            await ctx.send(embed=embed)

        except discord.NotFound:
            await ctx.send(f"❌ Webhook with ID `{webhook_id}` not found!")
        except ValueError:
            await ctx.send(f"❌ Invalid webhook ID: `{webhook_id}`")
        except Exception as e:
            logger.error(f"Failed to get webhook info: {e}")
            await ctx.send(f"❌ Failed to get webhook info: {str(e)}")

    def _remove_from_config(self, webhook_id: str):
        """Remove webhook from config file."""
        config_file = self.config_dir / "discord_webhooks.json"

        if not config_file.exists():
            return

        try:
            with open(config_file) as f:
                config = json.load(f)

            # Find and remove webhook
            for key, value in list(config.items()):
                if isinstance(value, dict) and value.get("webhook_id") == webhook_id:
                    del config[key]

            # Save updated config
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to update config: {e}")


class WebhookDeleteConfirmView(discord.ui.View):
    """Confirmation view for webhook deletion."""

    def __init__(self, webhook: discord.Webhook, user: discord.User):
        super().__init__(timeout=30)
        self.webhook = webhook
        self.user = user
        self.confirmed = False

    @discord.ui.button(label="✅ Confirm Delete", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm deletion."""
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "❌ Only the command issuer can confirm this action.", ephemeral=True
            )
            return

        self.confirmed = True
        await interaction.response.send_message("✅ Confirmed", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel deletion."""
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "❌ Only the command issuer can cancel this action.", ephemeral=True
            )
            return

        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()


async def setup(bot: commands.Bot):
    """Setup function for loading as extension."""
    await bot.add_cog(WebhookCommands(bot))
