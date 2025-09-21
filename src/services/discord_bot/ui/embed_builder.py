#!/usr/bin/env python3
"""
Embed Builder
=============

Discord embed builder with color schemes and formatting.
"""

import discord
from typing import Dict, Any, Optional, List
from .embed_types import EmbedType, EmbedConfig


class EmbedBuilder:
    """Builder for Discord embeds with predefined styles."""
    
    # Color scheme for different embed types
    COLORS = {
        EmbedType.SUCCESS: 0x00ff00,
        EmbedType.ERROR: 0xff0000,
        EmbedType.WARNING: 0xffff00,
        EmbedType.INFO: 0x0099ff,
        EmbedType.AGENT_STATUS: 0x9932cc,
        EmbedType.SYSTEM_STATUS: 0x00ced1,
        EmbedType.DEVLOG: 0xff8c00,
        EmbedType.HELP: 0x4169e1,
        EmbedType.COMMAND_RESPONSE: 0x32cd32,
    }
    
    @classmethod
    def create_embed(cls, config: EmbedConfig) -> discord.Embed:
        """Create a Discord embed from configuration."""
        embed = discord.Embed(
            title=config.title,
            description=config.description,
            color=config.color or cls.COLORS.get(config.embed_type, 0x0099ff),
            timestamp=discord.utils.utcnow() if config.timestamp else None
        )
        
        # Add fields if provided
        if config.fields:
            for name, value in config.fields.items():
                embed.add_field(name=name, value=str(value), inline=False)
        
        # Add footer if provided
        if config.footer:
            embed.set_footer(text=config.footer)
        
        # Add thumbnail if provided
        if config.thumbnail:
            embed.set_thumbnail(url=config.thumbnail)
        
        # Add image if provided
        if config.image:
            embed.set_image(url=config.image)
        
        return embed
    
    @classmethod
    def create_success_embed(cls, title: str, description: str, **kwargs) -> discord.Embed:
        """Create a success embed."""
        config = EmbedConfig(
            title=title,
            description=description,
            embed_type=EmbedType.SUCCESS,
            **kwargs
        )
        return cls.create_embed(config)
    
    @classmethod
    def create_error_embed(cls, title: str, description: str, **kwargs) -> discord.Embed:
        """Create an error embed."""
        config = EmbedConfig(
            title=title,
            description=description,
            embed_type=EmbedType.ERROR,
            **kwargs
        )
        return cls.create_embed(config)
    
    @classmethod
    def create_agent_status_embed(cls, agent_id: str, status: str, **kwargs) -> discord.Embed:
        """Create an agent status embed."""
        config = EmbedConfig(
            title=f"Agent Status: {agent_id}",
            description=f"**Status:** {status}",
            embed_type=EmbedType.AGENT_STATUS,
            **kwargs
        )
        return cls.create_embed(config)
