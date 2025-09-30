"""
Discord Bot Core Models
V2 Compliant data models for Discord bot
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class BotStatus(Enum):
    """Bot status enumeration"""
    OFFLINE = "offline"
    ONLINE = "online"
    IDLE = "idle"
    DND = "dnd"


class CommandType(Enum):
    """Command type enumeration"""
    SLASH = "slash"
    TEXT = "text"
    HYBRID = "hybrid"


@dataclass
class BotConfiguration:
    """Bot configuration structure"""
    command_prefix: str
    intents: Dict[str, bool]
    guild_id: Optional[int]
    log_level: str
    auto_sync: bool


@dataclass
class CommandContext:
    """Command context structure"""
    command_name: str
    user_id: int
    guild_id: Optional[int]
    channel_id: int
    timestamp: datetime
    parameters: Dict[str, Any]


@dataclass
class BotMetrics:
    """Bot performance metrics"""
    uptime: float
    commands_executed: int
    messages_sent: int
    errors_count: int
    guilds_count: int
    users_count: int
