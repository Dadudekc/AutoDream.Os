#!/usr/bin/env python3
"""
Discord Commander Models
========================

Data models and enums for the Discord commander system.
V2 COMPLIANT: Focused Discord commander models under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR DISCORD COMMANDER MODELS
@license MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class CommandStatus(Enum):
    """Command execution status."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(Enum):
    """Agent status levels."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    ERROR = "ERROR"
    MAINTENANCE = "MAINTENANCE"


@dataclass
class CommandResult:
    """Result of a command execution."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None
    agent: Optional[str] = None
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class SwarmStatus:
    """Swarm coordination status."""
    active_agents: List[str] = None
    total_agents: int = 8
    current_cycle: int = 1
    system_health: str = "OPERATIONAL"
    efficiency_rating: float = 1.0
    active_missions: List[str] = None
    pending_tasks: List[str] = None
    last_update: str = None
    
    def __post_init__(self):
        if self.active_agents is None:
            self.active_agents = [f"Agent-{i}" for i in range(1, 9)]
        if self.active_missions is None:
            self.active_missions = []
        if self.pending_tasks is None:
            self.pending_tasks = []
        if self.last_update is None:
            self.last_update = datetime.utcnow().isoformat()


@dataclass
class DiscordConfig:
    """Discord configuration data."""
    token: str
    guild_id: str
    command_channel: str = "swarm-commands"
    status_channel: str = "swarm-status"
    log_channel: str = "swarm-logs"
    admin_role: str = "Captain"
    agent_roles: List[str] = None
    
    def __post_init__(self):
        if self.agent_roles is None:
            self.agent_roles = [f"Agent-{i}" for i in range(1, 9)]


@dataclass
class AgentMessage:
    """Message to be sent to an agent."""
    agent: str
    content: str
    sender: str
    priority: str = "normal"
    message_type: str = "text"
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DiscordEmbed:
    """Discord embed data structure."""
    title: str
    description: str = None
    color: int = 0x3498db
    fields: List[Dict[str, Any]] = None
    footer: str = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.fields is None:
            self.fields = []
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


class DiscordCommanderState(Enum):
    """Discord commander state."""
    INITIALIZING = "initializing"
    CONNECTING = "connecting"
    READY = "ready"
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    SHUTTING_DOWN = "shutting_down"
    OFFLINE = "offline"


@dataclass
class CommandHistory:
    """Command execution history entry."""
    command_id: str
    agent: str
    command: str
    result: CommandResult
    timestamp: str
    user: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ChannelConfig:
    """Discord channel configuration."""
    name: str
    channel_type: str = "text"
    topic: str = None
    permissions: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = {}


# Factory functions for creating objects
def create_command_result(success: bool, message: str, **kwargs) -> CommandResult:
    """Create a command result."""
    return CommandResult(success=success, message=message, **kwargs)


def create_swarm_status(**kwargs) -> SwarmStatus:
    """Create swarm status."""
    return SwarmStatus(**kwargs)


def create_discord_config(token: str, guild_id: str, **kwargs) -> DiscordConfig:
    """Create Discord configuration."""
    return DiscordConfig(token=token, guild_id=guild_id, **kwargs)


def create_agent_message(agent: str, content: str, sender: str, **kwargs) -> AgentMessage:
    """Create agent message."""
    return AgentMessage(agent=agent, content=content, sender=sender, **kwargs)


def create_discord_embed(title: str, **kwargs) -> DiscordEmbed:
    """Create Discord embed."""
    return DiscordEmbed(title=title, **kwargs)


def create_command_history(command_id: str, agent: str, command: str, result: CommandResult, **kwargs) -> CommandHistory:
    """Create command history entry."""
    return CommandHistory(command_id=command_id, agent=agent, command=command, result=result, **kwargs)


# Export for DI
__all__ = [
    'CommandStatus',
    'AgentStatus',
    'CommandResult',
    'SwarmStatus',
    'DiscordConfig',
    'AgentMessage',
    'DiscordEmbed',
    'DiscordCommanderState',
    'CommandHistory',
    'ChannelConfig',
    'create_command_result',
    'create_swarm_status',
    'create_discord_config',
    'create_agent_message',
    'create_discord_embed',
    'create_command_history'
]
