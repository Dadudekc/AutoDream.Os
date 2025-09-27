#!/usr/bin/env python3
"""
Discord Command Router
======================

Advanced command routing system for Discord bot with webhook integration.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class CommandCategory(Enum):
    """Command categories for routing."""
    BASIC = "basic"
    AGENT = "agent"
    DEVLOG = "devlog"
    MESSAGING = "messaging"
    SYSTEM = "system"
    ADMIN = "admin"


@dataclass
class CommandContext:
    """Command execution context."""
    interaction: discord.Interaction
    user: discord.User
    channel: discord.TextChannel
    guild: Optional[discord.Guild]
    category: CommandCategory
    metadata: Dict[str, Any]


class CommandRouter:
    """Advanced command routing system."""
    
    def __init__(self, bot):
        """Initialize command router."""
        self.bot = bot
        self.command_handlers: Dict[str, callable] = {}
        self.category_handlers: Dict[CommandCategory, callable] = {}
        self.webhook_endpoints: Dict[str, str] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.command_stats: Dict[str, Dict[str, Any]] = {}
        
        # Load webhook configuration
        self._load_webhook_config()
        
        # Initialize rate limiting
        self._init_rate_limits()
    
    def _load_webhook_config(self):
        """Load webhook configuration from environment."""
        webhook_base = os.getenv("DISCORD_WEBHOOK_BASE_URL", "")
        if webhook_base:
            self.webhook_endpoints = {
                "agent_communication": f"{webhook_base}/agent-comm",
                "devlog_posting": f"{webhook_base}/devlog",
                "system_monitoring": f"{webhook_base}/monitoring",
                "command_analytics": f"{webhook_base}/analytics"
            }
            logger.info(f"[SUCCESS] Webhook endpoints configured: {len(self.webhook_endpoints)}")
        else:
            logger.warning("[WARNING] No webhook base URL configured")
    
    def _init_rate_limits(self):
        """Initialize rate limiting configuration."""
        self.rate_limits = {
            "global": {"requests": 100, "window": 60, "users": {}},
            "per_user": {"requests": 10, "window": 60, "users": {}},
            "per_command": {"requests": 5, "window": 60, "commands": {}}
        }
        logger.info("[SUCCESS] Rate limiting initialized")
    
    def register_command_handler(self, command_name: str, handler: callable, category: CommandCategory):
        """Register a command handler."""
        self.command_handlers[command_name] = {
            "handler": handler,
            "category": category,
            "stats": {"calls": 0, "errors": 0, "last_used": None}
        }
        logger.info(f"[SUCCESS] Registered command handler: {command_name} ({category.value})")
    
    def register_category_handler(self, category: CommandCategory, handler: callable):
        """Register a category handler."""
        self.category_handlers[category] = handler
        logger.info(f"[SUCCESS] Registered category handler: {category.value}")
    
    async def route_command(self, interaction: discord.Interaction, command_name: str) -> bool:
        """Route a command to appropriate handler."""
        try:
            # Check rate limits
            if not await self._check_rate_limits(interaction, command_name):
                await interaction.response.send_message(
                    "⏰ Rate limit exceeded. Please wait before using this command again.",
                    ephemeral=True
                )
                return False
            
            # Create command context
            context = CommandContext(
                interaction=interaction,
                user=interaction.user,
                channel=interaction.channel,
                guild=interaction.guild,
                category=self._get_command_category(command_name),
                metadata={"timestamp": interaction.created_at, "command": command_name}
            )
            
            # Route to specific command handler
            if command_name in self.command_handlers:
                handler_info = self.command_handlers[command_name]
                handler = handler_info["handler"]
                
                # Update stats
                handler_info["stats"]["calls"] += 1
                handler_info["stats"]["last_used"] = interaction.created_at
                
                # Execute handler
                await handler(context)
                
                # Send webhook notification
                await self._send_webhook_notification("command_executed", {
                    "command": command_name,
                    "user": str(interaction.user),
                    "channel": str(interaction.channel),
                    "guild": str(interaction.guild) if interaction.guild else None
                })
                
                return True
            
            # Route to category handler
            elif context.category in self.category_handlers:
                handler = self.category_handlers[context.category]
                await handler(context)
                return True
            
            else:
                logger.warning(f"[WARNING] No handler found for command: {command_name}")
                await interaction.response.send_message(
                    "❌ Command not found or not implemented.",
                    ephemeral=True
                )
                return False
                
        except Exception as e:
            logger.error(f"[ERROR] Error routing command {command_name}: {e}")
            
            # Update error stats
            if command_name in self.command_handlers:
                self.command_handlers[command_name]["stats"]["errors"] += 1
            
            try:
                await interaction.response.send_message(
                    "❌ An error occurred while processing your command.",
                    ephemeral=True
                )
            except:
                pass
            
            return False
    
    def _get_command_category(self, command_name: str) -> CommandCategory:
        """Get command category based on name."""
        category_map = {
            "ping": CommandCategory.BASIC,
            "commands": CommandCategory.BASIC,
            "swarm-help": CommandCategory.BASIC,
            "status": CommandCategory.SYSTEM,
            "info": CommandCategory.SYSTEM,
            "agents": CommandCategory.AGENT,
            "agent-channels": CommandCategory.AGENT,
            "swarm": CommandCategory.AGENT,
            "send": CommandCategory.MESSAGING,
            "msg-status": CommandCategory.MESSAGING,
            "devlog": CommandCategory.DEVLOG,
            "agent-devlog": CommandCategory.DEVLOG,
            "test-devlog": CommandCategory.DEVLOG
        }
        return category_map.get(command_name, CommandCategory.BASIC)
    
    async def _check_rate_limits(self, interaction: discord.Interaction, command_name: str) -> bool:
        """Check if command is within rate limits."""
        user_id = str(interaction.user.id)
        current_time = interaction.created_at.timestamp()
        
        # Check global rate limit
        global_limits = self.rate_limits["global"]
        if user_id not in global_limits["users"]:
            global_limits["users"][user_id] = {"count": 0, "window_start": current_time}
        
        user_global = global_limits["users"][user_id]
        if current_time - user_global["window_start"] > global_limits["window"]:
            user_global["count"] = 0
            user_global["window_start"] = current_time
        
        if user_global["count"] >= global_limits["requests"]:
            return False
        
        user_global["count"] += 1
        
        # Check per-user rate limit
        per_user_limits = self.rate_limits["per_user"]
        if user_id not in per_user_limits["users"]:
            per_user_limits["users"][user_id] = {"count": 0, "window_start": current_time}
        
        user_per_user = per_user_limits["users"][user_id]
        if current_time - user_per_user["window_start"] > per_user_limits["window"]:
            user_per_user["count"] = 0
            user_per_user["window_start"] = current_time
        
        if user_per_user["count"] >= per_user_limits["requests"]:
            return False
        
        user_per_user["count"] += 1
        
        # Check per-command rate limit
        per_command_limits = self.rate_limits["per_command"]
        if command_name not in per_command_limits["commands"]:
            per_command_limits["commands"][command_name] = {"count": 0, "window_start": current_time}
        
        command_limits = per_command_limits["commands"][command_name]
        if current_time - command_limits["window_start"] > per_command_limits["window"]:
            command_limits["count"] = 0
            command_limits["window_start"] = current_time
        
        if command_limits["count"] >= per_command_limits["requests"]:
            return False
        
        command_limits["count"] += 1
        
        return True
    
    async def _send_webhook_notification(self, event_type: str, data: Dict[str, Any]):
        """Send webhook notification."""
        if not self.webhook_endpoints:
            return
        
        try:
            # This would integrate with actual webhook service
            logger.info(f"📡 Webhook notification: {event_type} - {data}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to send webhook notification: {e}")
    
    def get_command_stats(self) -> Dict[str, Any]:
        """Get command usage statistics."""
        stats = {
            "total_commands": len(self.command_handlers),
            "total_calls": sum(h["stats"]["calls"] for h in self.command_handlers.values()),
            "total_errors": sum(h["stats"]["errors"] for h in self.command_handlers.values()),
            "commands": {}
        }
        
        for name, info in self.command_handlers.items():
            stats["commands"][name] = {
                "calls": info["stats"]["calls"],
                "errors": info["stats"]["errors"],
                "last_used": info["stats"]["last_used"]
            }
        
        return stats
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status."""
        return {
            "global_limits": self.rate_limits["global"],
            "per_user_limits": self.rate_limits["per_user"],
            "per_command_limits": self.rate_limits["per_command"]
        }
