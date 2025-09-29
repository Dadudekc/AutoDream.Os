"""
Safe Response Utilities
=======================
Shared utilities for safe Discord interaction handling.
"""

import discord
import logging

logger = logging.getLogger(__name__)


async def safe_send(interaction: discord.Interaction, *, ephemeral: bool = False, **kwargs):
    """
    Send a response without risking 'already acknowledged' errors.
    
    This function handles race conditions where decorators or error handlers
    might have already responded to the interaction.
    
    Args:
        interaction: Discord interaction object
        ephemeral: Whether the response should be ephemeral
        **kwargs: Additional arguments for send_message/followup.send
    """
    try:
        if interaction.response.is_done():
            await interaction.followup.send(ephemeral=ephemeral, **kwargs)
        else:
            await interaction.response.send_message(ephemeral=ephemeral, **kwargs)
    except discord.errors.InteractionResponded:
        # If something else raced us, fall back to followup
        await interaction.followup.send(ephemeral=ephemeral, **kwargs)
    except Exception as e:
        logger.error("Failed to send response: %s", e)
        # Last resort: try followup if available
        try:
            await interaction.followup.send(ephemeral=ephemeral, **kwargs)
        except Exception:
            logger.error("Failed to send followup response: %s", e)


def safe_log_info(message: str, user_id: str = None, channel_id: str = None, **kwargs):
    """
    Log info message with safe formatting to avoid cp1252 console issues.
    
    Args:
        message: Base log message (ASCII-only recommended)
        user_id: User ID to include in log
        channel_id: Channel ID to include in log
        **kwargs: Additional key-value pairs to include in log
    """
    parts = [message]
    if user_id:
        parts.append(f"user_id={user_id}")
    if channel_id:
        parts.append(f"channel_id={channel_id}")
    
    # Add any additional kwargs
    for key, value in kwargs.items():
        parts.append(f"{key}={value}")
    
    logger.info(" ".join(parts))
