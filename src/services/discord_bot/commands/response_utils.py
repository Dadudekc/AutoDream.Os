"""
Response Utilities Module
========================
Common utilities for handling Discord responses safely.
"""

import discord
import logging

logger = logging.getLogger(__name__)


async def send_discord_response(interaction, **kwargs):
    """Safely send Discord response, handling rate limits and double acknowledgment."""
    try:
        # Filter out None values to prevent Discord errors
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        if interaction.response.is_done():
            await interaction.followup.send(**filtered_kwargs)
        else:
            await interaction.response.send_message(**filtered_kwargs)
    except discord.HTTPException as e:
        logger.warning(f"Discord HTTP error: {e}")
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ Response error occurred", ephemeral=True)


def is_admin(interaction):
    """Check if user is administrator."""
    return interaction.user.guild_permissions.administrator


async def send_denial_message(interaction, message):
    """Send denial message."""
    embed = discord.Embed(title="❌ Access Denied", description=message, color=0xFF0000)
    await send_discord_response(interaction, embed=embed, ephemeral=True)
