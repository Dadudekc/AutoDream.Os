#!/usr/bin/env python3
"""
Command Logger
==============

Comprehensive logging and error handling for Discord commands.
"""

import asyncio
import logging
import time
import traceback
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import discord
from discord import app_commands

logger = logging.getLogger(__name__)


@dataclass
class CommandExecution:
    """Command execution record."""
    command_name: str
    user_id: int
    guild_id: Optional[int]
    channel_id: int
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class CommandLogger:
    """Enhanced command logging and error handling."""
    
    def __init__(self):
        """Initialize command logger."""
        self.execution_history: Dict[str, CommandExecution] = {}
        self.command_stats: Dict[str, Dict[str, Any]] = {}
        
    def log_command_start(self, interaction: discord.Interaction, command_name: str) -> str:
        """Log command start and return execution ID."""
        execution_id = f"{command_name}_{interaction.user.id}_{int(time.time() * 1000)}"
        
        execution = CommandExecution(
            command_name=command_name,
            user_id=interaction.user.id,
            guild_id=interaction.guild_id,
            channel_id=interaction.channel_id,
            start_time=time.time()
        )
        
        self.execution_history[execution_id] = execution
        
        logger.info(f"Command started: {command_name} by {interaction.user.name} ({interaction.user.id}) in channel {interaction.channel_id}")
        
        return execution_id
    
    def log_command_success(self, execution_id: str, response_message: str = ""):
        """Log successful command completion."""
        if execution_id in self.execution_history:
            execution = self.execution_history[execution_id]
            execution.end_time = time.time()
            execution.success = True
            execution.execution_time = execution.end_time - execution.start_time
            
            logger.info(f"Command completed: {execution.command_name} in {execution.execution_time:.2f}s")
            
            # Update stats
            self._update_command_stats(execution.command_name, execution.execution_time, True)
    
    def log_command_error(self, execution_id: str, error: Exception, error_message: str = ""):
        """Log command error."""
        if execution_id in self.execution_history:
            execution = self.execution_history[execution_id]
            execution.end_time = time.time()
            execution.success = False
            execution.error_message = str(error)
            execution.execution_time = execution.end_time - execution.start_time
            
            logger.error(f"Command failed: {execution.command_name} - {error}")
            logger.error(f"Error details: {traceback.format_exc()}")
            
            # Update stats
            self._update_command_stats(execution.command_name, execution.execution_time, False)
    
    def _update_command_stats(self, command_name: str, execution_time: float, success: bool):
        """Update command statistics."""
        if command_name not in self.command_stats:
            self.command_stats[command_name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_time": 0.0,
                "avg_execution_time": 0.0,
                "last_execution": None
            }
        
        stats = self.command_stats[command_name]
        stats["total_executions"] += 1
        stats["total_time"] += execution_time
        stats["avg_execution_time"] = stats["total_time"] / stats["total_executions"]
        stats["last_execution"] = datetime.now().isoformat()
        
        if success:
            stats["successful_executions"] += 1
        else:
            stats["failed_executions"] += 1
    
    def get_command_stats(self, command_name = None):
        """Get command statistics."""
        if command_name:
            return self.command_stats.get(command_name, {})
        return self.command_stats
    
    def get_execution_history(self, limit: int = 50) -> Dict[str, CommandExecution]:
        """Get recent command execution history."""
        sorted_executions = sorted(
            self.execution_history.items(),
            key=lambda x: x[1].start_time,
            reverse=True
        )
        return dict(sorted_executions[:limit])


def command_logger_decorator(logger_instance: CommandLogger):
    """Decorator for adding logging to Discord commands."""
    def decorator(func: Callable) -> Callable:
        async def wrapper(interaction):
            command_name = func.__name__
            execution_id = logger_instance.log_command_start(interaction, command_name)

            try:
                # Check if interaction is still valid
                if interaction.response.is_done():
                    logger.warning(f"Interaction already acknowledged for command: {command_name}")
                    return

                # Execute command with timeout
                result = await asyncio.wait_for(
                    func(interaction),
                    timeout=30.0  # 30 second timeout
                )

                logger_instance.log_command_success(execution_id)
                return result
                
            except asyncio.TimeoutError:
                error_msg = f"Command {command_name} timed out after 30 seconds"
                logger_instance.log_command_error(execution_id, Exception(error_msg), error_msg)
                
                # Send timeout message using safe response function
                try:
                    # Import here to avoid circular imports
                    from src.services.discord_bot.commands.basic_commands import send_discord_response
                    await send_discord_response(
                        interaction,
                        content="⏰ Command timed out. Please try again.",
                        ephemeral=True
                    )
                except Exception:
                    logger.error(f"Failed to send timeout message for {command_name}")
                
            except discord.NotFound:
                error_msg = f"Interaction not found for command {command_name}"
                logger_instance.log_command_error(execution_id, Exception(error_msg), error_msg)
                logger.warning(f"Interaction expired for command: {command_name}")
                
            except discord.InteractionResponded:
                error_msg = f"Interaction already responded for command {command_name}"
                logger_instance.log_command_error(execution_id, Exception(error_msg), error_msg)
                logger.warning(f"Interaction already responded for command: {command_name}")
                
            except Exception as e:
                error_msg = f"Unexpected error in command {command_name}: {str(e)}"
                logger_instance.log_command_error(execution_id, e, error_msg)
                
                # Send error message using safe response function
                try:
                    # Import here to avoid circular imports
                    from src.services.discord_bot.commands.basic_commands import send_discord_response
                    await send_discord_response(
                        interaction,
                        content="❌ An error occurred while executing the command. Please try again.",
                        ephemeral=True
                    )
                except Exception:
                    logger.error(f"Failed to send error message for {command_name}")
        
        return wrapper
    return decorator


# Global logger instance
command_logger = CommandLogger()
