#!/usr/bin/env python3
"""
Embed Types and Enums
=====================

Discord embed type definitions and enums for UI components.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass

import discord


class EmbedType(Enum):
    """Types of embeds for different UI contexts."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    AGENT_STATUS = "agent_status"
    SYSTEM_STATUS = "system_status"
    DEVLOG = "devlog"
    HELP = "help"
    COMMAND_RESPONSE = "command_response"


class ButtonStyle(Enum):
    """Button style options."""
    PRIMARY = discord.ButtonStyle.primary
    SECONDARY = discord.ButtonStyle.secondary
    SUCCESS = discord.ButtonStyle.success
    DANGER = discord.ButtonStyle.danger
    LINK = discord.ButtonStyle.link


@dataclass
class EmbedConfig:
    """Configuration for embed creation."""
    title: str
    description: Optional[str] = None
    color: Optional[int] = None
    fields: Optional[Dict[str, Any]] = None
    footer: Optional[str] = None
    thumbnail: Optional[str] = None
    image: Optional[str] = None
    timestamp: Optional[bool] = False
    embed_type: EmbedType = EmbedType.INFO
