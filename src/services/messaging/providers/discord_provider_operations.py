#!/usr/bin/env python3
"""
Discord Provider Operations - Operations Module
===============================================

Operations and utilities for Discord messaging provider.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: discord_provider.py (432 lines) - Operations module
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import discord
from discord.ext import commands

from src.services.messaging.providers.discord_provider_core import DiscordMessagingProvider

logger = logging.getLogger(__name__)


class DiscordChannelManager:
    """Manages Discord channels for agents"""
    
    def __init__(self):
        """Initialize channel manager"""
        self.channel_mappings: Dict[str, int] = {}
        self.agent_permissions: Dict[str, List[str]] = {}
    
    def manage_channels(self, action: str, **kwargs) -> Any:
        """Consolidated channel management"""
        if action == "register":
            self.channel_mappings[kwargs["agent_id"]] = kwargs["channel_id"]
            return True
        elif action == "unregister":
            if kwargs["agent_id"] in self.channel_mappings:
                del self.channel_mappings[kwargs["agent_id"]]
                return True
            return False
        elif action == "get_channel":
            return self.channel_mappings.get(kwargs["agent_id"])
        elif action == "list_channels":
            return dict(self.channel_mappings)
        elif action == "set_permissions":
            self.agent_permissions[kwargs["agent_id"]] = kwargs["permissions"]
            return True
        elif action == "get_permissions":
            return self.agent_permissions.get(kwargs["agent_id"], [])
        return None


class DiscordMessageLogger:
    """Logs Discord messages for audit and analysis"""
    
    def __init__(self):
        """Initialize message logger"""
        self.message_log: List[Dict[str, Any]] = []
        self.max_log_size = 1000
    
    def manage_logging(self, action: str, **kwargs) -> Any:
        """Consolidated logging management"""
        if action == "log_message":
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "from_agent": kwargs["from_agent"],
                "to_agent": kwargs.get("to_agent"),
                "channel_id": kwargs.get("channel_id"),
                "message": kwargs["message"],
                "message_type": kwargs.get("message_type", "direct"),
                "success": kwargs.get("success", True)
            }
            
            self.message_log.append(log_entry)
            
            # Keep log size manageable
            if len(self.message_log) > self.max_log_size:
                self.message_log = self.message_log[-self.max_log_size:]
            
            return True
        
        elif action == "get_logs":
            agent_id = kwargs.get("agent_id")
            if agent_id:
                return [
                    log for log in self.message_log
                    if log.get("from_agent") == agent_id or log.get("to_agent") == agent_id
                ]
            return self.message_log
        
        elif action == "get_stats":
            total_messages = len(self.message_log)
            successful_messages = sum(1 for log in self.message_log if log.get("success", True))
            
            return {
                "total_messages": total_messages,
                "successful_messages": successful_messages,
                "failed_messages": total_messages - successful_messages,
                "success_rate": (successful_messages / total_messages * 100) if total_messages > 0 else 0
            }
        
        return None


class DiscordProviderService:
    """Main service for Discord provider operations"""
    
    def __init__(self, bot: commands.Bot):
        """Initialize Discord provider service"""
        self.core = DiscordMessagingProvider(bot)
        self.channel_manager = DiscordChannelManager()
        self.message_logger = DiscordMessageLogger()
    
    def manage_provider_operations(self, action: str, **kwargs) -> Any:
        """Consolidated provider operations"""
        if action == "send_message":
            result = self.core.manage_messaging(
                "send_to_agent",
                agent_id=kwargs["agent_id"],
                message=kwargs["message"],
                from_agent=kwargs.get("from_agent")
            )
            
            # Log the message
            self.message_logger.manage_logging(
                "log_message",
                from_agent=kwargs.get("from_agent", "system"),
                to_agent=kwargs["agent_id"],
                message=kwargs["message"],
                message_type="direct",
                success=result
            )
            
            return result
        
        elif action == "send_broadcast":
            result = self.core.manage_messaging(
                "send_broadcast",
                message=kwargs["message"],
                from_agent=kwargs.get("from_agent"),
                exclude_agents=kwargs.get("exclude_agents", [])
            )
            
            # Log the broadcast
            self.message_logger.manage_logging(
                "log_message",
                from_agent=kwargs.get("from_agent", "system"),
                message=kwargs["message"],
                message_type="broadcast",
                success=result > 0
            )
            
            return result
        
        elif action == "register_agent_channel":
            success = self.channel_manager.manage_channels(
                "register",
                agent_id=kwargs["agent_id"],
                channel_id=kwargs["channel_id"]
            )
            
            if success:
                # Also register with core provider
                self.core.manage_messaging(
                    "register_channel",
                    agent_id=kwargs["agent_id"],
                    channel=kwargs.get("channel")
                )
            
            return success
        
        elif action == "get_provider_status":
            core_status = self.core.get_provider_status()
            channel_status = self.channel_manager.manage_channels("list_channels")
            log_stats = self.message_logger.manage_logging("get_stats")
            
            return {
                **core_status,
                "channel_mappings": channel_status,
                "message_stats": log_stats
            }
        
        return None
    
    def cleanup_old_logs(self, days: int = 7) -> int:
        """Cleanup old log entries and return count removed"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        initial_count = len(self.message_logger.message_log)
        
        self.message_logger.message_log = [
            log for log in self.message_logger.message_log
            if datetime.fromisoformat(log["timestamp"]).timestamp() > cutoff_date
        ]
        
        removed_count = initial_count - len(self.message_logger.message_log)
        
        logger.info(f"Cleaned up {removed_count} old log entries")
        return removed_count
