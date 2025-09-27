#!/usr/bin/env python3
"""
Command Wrapper
===============

Universal wrapper for Discord commands with logging and error handling.
"""

import asyncio
import logging
import time
import traceback
from typing import Callable, Any, Optional
import discord
from discord import app_commands

logger = logging.getLogger(__name__)


def safe_command(func: Callable) -> Callable:
    """Safe command wrapper with comprehensive error handling."""
    async def wrapper(interaction: discord.Interaction, *args, **kwargs):
        command_name = func.__name__
        start_time = time.time()
        
        try:
            logger.info(f"🚀 Command started: {command_name} by {interaction.user.name} ({interaction.user.id})")
            
            # Check if interaction is still valid
            if interaction.response.is_done():
                logger.warning(f"[WARNING] Interaction already acknowledged for command: {command_name}")
                return
            
            # Execute command with timeout
            result = await asyncio.wait_for(
                func(interaction, *args, **kwargs),
                timeout=30.0  # 30 second timeout
            )
            
            execution_time = time.time() - start_time
            logger.info(f"[SUCCESS] Command completed: {command_name} in {execution_time:.2f}s")
            return result
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            error_msg = f"Command {command_name} timed out after 30 seconds"
            logger.error(f"⏰ {error_msg} (execution time: {execution_time:.2f}s)")
            
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message(
                        f"⏰ Command timed out. Please try again.",
                        ephemeral=True
                    )
                except Exception as e:
                    logger.error(f"Failed to send timeout message for {command_name}: {e}")
            
        except discord.NotFound:
            execution_time = time.time() - start_time
            error_msg = f"Interaction not found for command {command_name}"
            logger.error(f"[ERROR] {error_msg} (execution time: {execution_time:.2f}s)")
            logger.warning(f"[WARNING] Interaction expired for command: {command_name}")
            
        except discord.InteractionResponded:
            execution_time = time.time() - start_time
            error_msg = f"Interaction already responded for command {command_name}"
            logger.error(f"[ERROR] {error_msg} (execution time: {execution_time:.2f}s)")
            logger.warning(f"[WARNING] Interaction already responded for command: {command_name}")
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Unexpected error in command {command_name}: {str(e)}"
            logger.error(f"[ERROR] {error_msg} (execution time: {execution_time:.2f}s)")
            logger.error(f"[DETAILS] Error details: {traceback.format_exc()}")
            
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message(
                        f"❌ An error occurred while executing the command. Please try again.",
                        ephemeral=True
                    )
                except Exception as e:
                    logger.error(f"Failed to send error message for {command_name}: {e}")
    
    return wrapper


def log_command_execution(command_name: str, user_name: str, user_id: int, success: bool, execution_time: float, error_msg: Optional[str] = None):
    """Log command execution details."""
    status = "✅" if success else "❌"
    logger.info(f"{status} {command_name} | User: {user_name} ({user_id}) | Time: {execution_time:.2f}s")
    
    if error_msg:
        logger.error(f"   Error: {error_msg}")


def create_safe_response_handler(interaction: discord.Interaction, command_name: str):
    """Create a safe response handler for commands."""
    async def safe_send_message(content: str, ephemeral: bool = False, **kwargs):
        """Safely send a message response."""
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(content, ephemeral=ephemeral, **kwargs)
                logger.info(f"[SUCCESS] Response sent for {command_name}")
            else:
                logger.warning(f"[WARNING] Cannot send response for {command_name} - interaction already done")
        except Exception as e:
            logger.error(f"[ERROR] Failed to send response for {command_name}: {e}")
            raise
    
    return safe_send_message


# Example usage decorator
def with_logging(func: Callable) -> Callable:
    """Decorator that adds logging to any Discord command."""
    return safe_command(func)
