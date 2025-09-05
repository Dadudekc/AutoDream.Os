#!/usr/bin/env python3
"""
Discord Commander Integration Engine
====================================

Discord integration engine for the Discord commander system.
Handles embeds, channel management, and Discord lifecycle.
V2 COMPLIANT: Focused Discord integration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR DISCORD INTEGRATION
@license MIT
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import discord

from .discord_commander_models import (
    SwarmStatus, DiscordConfig, DiscordEmbed, create_discord_embed
)


class DiscordIntegrationEngine:
    """Discord integration engine for Discord commander"""
    
    def __init__(self, config: DiscordConfig, swarm_status: SwarmStatus):
        """Initialize Discord integration engine"""
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.swarm_status = swarm_status
        self.guild: Optional[discord.Guild] = None
    
    async def initialize_channels(self, guild: discord.Guild) -> bool:
        """Initialize required Discord channels"""
        try:
            self.guild = guild
            
            if str(guild.id) != self.config.guild_id:
                self.logger.warning(f"Guild ID mismatch: expected {self.config.guild_id}, got {guild.id}")
                return False
            
            # Create channels if they don't exist
            channels_to_create = [
                self.config.command_channel,
                self.config.status_channel,
                self.config.log_channel
            ]
            
            for channel_name in channels_to_create:
                channel = discord.utils.get(guild.channels, name=channel_name)
                if channel is None:
                    try:
                        channel = await guild.create_text_channel(channel_name)
                        self.logger.info(f"Created channel: {channel_name}")
                    except Exception as e:
                        self.logger.error(f"Failed to create channel {channel_name}: {e}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize channels: {e}")
            return False
    
    async def send_startup_message(self) -> bool:
        """Send startup message to status channel"""
        try:
            if not self.guild:
                self.logger.error("Guild not initialized")
                return False
            
            status_channel = discord.utils.get(self.guild.channels, name=self.config.status_channel)
            if not status_channel:
                self.logger.error(f"Status channel '{self.config.status_channel}' not found")
                return False
            
            embed = create_discord_embed(
                title="🚀 Swarm Discord Commander Online",
                description="Discord integration activated for swarm coordination",
                color=0x00ff00
            )
            
            embed.fields = [
                {"name": "Status", "value": "✅ Operational", "inline": True},
                {"name": "Active Agents", "value": f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", "inline": True},
                {"name": "Current Cycle", "value": f"Cycle {self.swarm_status.current_cycle}", "inline": True},
                {"name": "System Health", "value": self.swarm_status.system_health, "inline": True},
                {"name": "Efficiency Rating", "value": f"{self.swarm_status.efficiency_rating}x", "inline": True}
            ]
            
            embed.footer = "WE. ARE. SWARM. ⚡️🔥"
            
            await status_channel.send(embed=embed)
            self.logger.info("Startup message sent to status channel")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send startup message: {e}")
            return False
    
    async def send_shutdown_message(self) -> bool:
        """Send shutdown message to status channel"""
        try:
            if not self.guild:
                return False
            
            status_channel = discord.utils.get(self.guild.channels, name=self.config.status_channel)
            if not status_channel:
                return False
            
            embed = create_discord_embed(
                title="🛑 Swarm Discord Commander Shutting Down",
                description="Discord integration deactivated",
                color=0xe74c3c
            )
            
            embed.footer = "WE. ARE. SWARM. ⚡️🔥"
            
            await status_channel.send(embed=embed)
            self.logger.info("Shutdown message sent to status channel")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send shutdown message: {e}")
            return False
    
    def create_status_embed(self) -> discord.Embed:
        """Create status embed"""
        embed = create_discord_embed(
            title="🤖 Swarm Status Report",
            description="Current swarm operational status",
            color=0x3498db
        )
        
        embed.fields = [
            {"name": "Active Agents", "value": f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", "inline": True},
            {"name": "Current Cycle", "value": f"Cycle {self.swarm_status.current_cycle}", "inline": True},
            {"name": "System Health", "value": self.swarm_status.system_health, "inline": True},
            {"name": "Efficiency Rating", "value": f"{self.swarm_status.efficiency_rating}x", "inline": True},
            {"name": "Active Missions", "value": str(len(self.swarm_status.active_missions)), "inline": True},
            {"name": "Pending Tasks", "value": str(len(self.swarm_status.pending_tasks)), "inline": True}
        ]
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def create_error_embed(self, title: str, error: str) -> discord.Embed:
        """Create error embed"""
        embed = create_discord_embed(
            title=f"❌ {title}",
            description=error[:2000],  # Discord embed limit
            color=0xe74c3c
        )
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def create_success_embed(self, title: str, message: str) -> discord.Embed:
        """Create success embed"""
        embed = create_discord_embed(
            title=f"✅ {title}",
            description=message[:2000],  # Discord embed limit
            color=0x27ae60
        )
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def create_warning_embed(self, title: str, message: str) -> discord.Embed:
        """Create warning embed"""
        embed = create_discord_embed(
            title=f"⚠️ {title}",
            description=message[:2000],  # Discord embed limit
            color=0xf1c40f
        )
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def create_info_embed(self, title: str, message: str) -> discord.Embed:
        """Create info embed"""
        embed = create_discord_embed(
            title=f"ℹ️ {title}",
            description=message[:2000],  # Discord embed limit
            color=0x3498db
        )
        
        embed.footer = "WE. ARE. SWARM. ⚡️🔥"
        return embed
    
    def get_channel_by_name(self, channel_name: str) -> Optional[discord.TextChannel]:
        """Get channel by name"""
        if not self.guild:
            return None
        
        return discord.utils.get(self.guild.channels, name=channel_name)
    
    def get_role_by_name(self, role_name: str) -> Optional[discord.Role]:
        """Get role by name"""
        if not self.guild:
            return None
        
        return discord.utils.get(self.guild.roles, name=role_name)
    
    def has_permission(self, member: discord.Member, permission: str) -> bool:
        """Check if member has permission"""
        if not self.guild:
            return False
        
        if permission == "admin":
            admin_role = self.get_role_by_name(self.config.admin_role)
            return admin_role in member.roles if admin_role else False
        
        if permission == "agent":
            agent_roles = [self.get_role_by_name(role) for role in self.config.agent_roles]
            return any(role in member.roles for role in agent_roles if role)
        
        return False
    
    def format_agent_list(self, agents: List[str]) -> str:
        """Format agent list for display"""
        if not agents:
            return "None"
        
        return ", ".join(agents)
    
    def format_timestamp(self, timestamp: str = None) -> str:
        """Format timestamp for display"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return timestamp


# Factory function for dependency injection
def create_discord_integration_engine(config: DiscordConfig, swarm_status: SwarmStatus) -> DiscordIntegrationEngine:
    """Factory function to create Discord integration engine"""
    return DiscordIntegrationEngine(config, swarm_status)


# Export for DI
__all__ = ['DiscordIntegrationEngine', 'create_discord_integration_engine']
