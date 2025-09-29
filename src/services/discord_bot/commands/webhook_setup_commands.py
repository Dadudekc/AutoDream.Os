"""
Webhook Setup Commands
======================
Admin-only slash commands for managing agent webhooks.
"""

import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.services.discord_bot.tools.webhook_provisioner import DiscordWebhookProvisioner
from src.services.secret_store import SecretStore

logger = logging.getLogger(__name__)

# Admin role name (adjust as needed)
ADMIN_ROLE = "SwarmAdmin"


def setup_webhook_setup_commands(bot: commands.Bot):
    """Setup webhook management commands."""
    provisioner = DiscordWebhookProvisioner(bot)

    def is_admin(interaction: discord.Interaction) -> bool:
        """Check if user has admin permissions."""
        # Check for administrator permission
        if interaction.user.guild_permissions.administrator:
            return True
        
        # Check for admin role
        if hasattr(interaction.user, "roles"):
            roles = [r.name for r in interaction.user.roles]
            return ADMIN_ROLE in roles
            
        return False

    @bot.tree.command(
        name="provision-webhook", 
        description="Create per-agent webhook in a channel"
    )
    @app_commands.describe(
        agent="Agent identifier (Agent-1 to Agent-8)",
        channel="Target channel for events"
    )
    async def provision_webhook(
        interaction: discord.Interaction, 
        agent: str, 
        channel: discord.TextChannel
    ):
        """Create a webhook for an agent."""
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Administrator permission required.", 
                ephemeral=True
            )
            
        await interaction.response.defer(ephemeral=True)
        
        # Validate agent ID format
        if not agent.startswith("Agent-") or agent not in [f"Agent-{i}" for i in range(1, 9)]:
            return await interaction.followup.send(
                "❌ Invalid agent ID. Use Agent-1 through Agent-8.", 
                ephemeral=True
            )
        
        # Check if webhook already exists
        existing = SecretStore.get_webhook(agent)
        if existing:
            return await interaction.followup.send(
                f"⚠️ Webhook already exists for **{agent}**. Use `/rotate-webhook` to recreate.", 
                ephemeral=True
            )
        
        # Create webhook
        webhook_url = await provisioner.create(agent, channel)
        if not webhook_url:
            return await interaction.followup.send(
                "❌ Failed to create webhook. Check bot permissions in the channel.", 
                ephemeral=True
            )
        
        # Mask the token for security
        masked_token = webhook_url.split("/")[-1][:6] + "..."
        
        await interaction.followup.send(
            f"✅ Webhook created for **{agent}** in {channel.mention}\n"
            f"🔐 Token: `{masked_token}`\n"
            f"💾 Stored securely outside repository", 
            ephemeral=True
        )

    @bot.tree.command(
        name="rotate-webhook", 
        description="Rotate (recreate) an agent's webhook"
    )
    @app_commands.describe(agent="Agent identifier (Agent-1 to Agent-8)")
    async def rotate_webhook(interaction: discord.Interaction, agent: str):
        """Rotate an existing webhook."""
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Administrator permission required.", 
                ephemeral=True
            )
            
        await interaction.response.defer(ephemeral=True)
        
        # Validate agent ID format
        if not agent.startswith("Agent-") or agent not in [f"Agent-{i}" for i in range(1, 9)]:
            return await interaction.followup.send(
                "❌ Invalid agent ID. Use Agent-1 through Agent-8.", 
                ephemeral=True
            )
        
        # Rotate webhook
        webhook_url = await provisioner.rotate(agent)
        if not webhook_url:
            return await interaction.followup.send(
                f"❌ No existing webhook to rotate for **{agent}** or permission issue.", 
                ephemeral=True
            )
        
        # Mask the token for security
        masked_token = webhook_url.split("/")[-1][:6] + "..."
        
        await interaction.followup.send(
            f"🔁 Rotated webhook for **{agent}**\n"
            f"🔐 New token: `{masked_token}`\n"
            f"💾 Updated secure storage", 
            ephemeral=True
        )

    @bot.tree.command(
        name="revoke-webhook", 
        description="Delete an agent's webhook"
    )
    @app_commands.describe(agent="Agent identifier (Agent-1 to Agent-8)")
    async def revoke_webhook(interaction: discord.Interaction, agent: str):
        """Revoke (delete) a webhook."""
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Administrator permission required.", 
                ephemeral=True
            )
            
        await interaction.response.defer(ephemeral=True)
        
        # Validate agent ID format
        if not agent.startswith("Agent-") or agent not in [f"Agent-{i}" for i in range(1, 9)]:
            return await interaction.followup.send(
                "❌ Invalid agent ID. Use Agent-1 through Agent-8.", 
                ephemeral=True
            )
        
        # Revoke webhook
        success = await provisioner.revoke(agent)
        if success:
            await interaction.followup.send(
                f"🧨 Webhook revoked and removed from storage for **{agent}**", 
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"⚠️ No webhook found to revoke for **{agent}**", 
                ephemeral=True
            )

    @bot.tree.command(
        name="test-webhook", 
        description="Send a test event through the stored webhook"
    )
    @app_commands.describe(agent="Agent identifier (Agent-1 to Agent-8)")
    async def test_webhook(interaction: discord.Interaction, agent: str):
        """Test webhook functionality."""
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Administrator permission required.", 
                ephemeral=True
            )
            
        await interaction.response.defer(ephemeral=True)
        
        # Validate agent ID format
        if not agent.startswith("Agent-") or agent not in [f"Agent-{i}" for i in range(1, 9)]:
            return await interaction.followup.send(
                "❌ Invalid agent ID. Use Agent-1 through Agent-8.", 
                ephemeral=True
            )
        
        # Test webhook
        success = await provisioner.test(agent)
        if success:
            await interaction.followup.send(
                f"✅ Test message delivered to **{agent}** webhook", 
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ Test failed for **{agent}** (no webhook or network issue)", 
                ephemeral=True
            )

    @bot.tree.command(
        name="list-webhooks", 
        description="List all configured webhooks"
    )
    async def list_webhooks(interaction: discord.Interaction):
        """List all configured webhooks."""
        if not is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Administrator permission required.", 
                ephemeral=True
            )
            
        await interaction.response.defer(ephemeral=True)
        
        webhooks = SecretStore.list_webhooks()
        if not webhooks:
            return await interaction.followup.send(
                "📝 No webhooks configured", 
                ephemeral=True
            )
        
        # Build status list
        status_lines = []
        for agent_id, webhook_data in webhooks.items():
            try:
                channel = bot.get_channel(webhook_data["channel_id"])
                channel_name = channel.name if channel else "Unknown"
                status_lines.append(f"• **{agent_id}**: #{channel_name}")
            except Exception:
                status_lines.append(f"• **{agent_id}**: Unknown channel")
        
        await interaction.followup.send(
            f"📋 **Configured Webhooks:**\n" + "\n".join(status_lines), 
            ephemeral=True
        )
