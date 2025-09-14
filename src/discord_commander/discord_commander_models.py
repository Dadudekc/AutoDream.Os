#!/usr/bin/env python3
"""
Discord Commander Models - V2 Compliance Module
==============================================

Data models for Discord commander operations.

Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class CommandResult:
    """Result of a Discord commander command execution."""
    success: bool
    message: str
    data: dict[str, Any] | None = None
    agent: str | None = None
    execution_time: float | None = None
    timestamp: str | None = None
    error_code: str | None = None

    def __post_init__(self):
        """Set default timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


def create_command_result(
    success: bool,
    message: str,
    data: dict[str, Any] | None = None,
    agent: str | None = None,
    execution_time: float | None = None,
    error_code: str | None = None
) -> CommandResult:
    """Factory function to create CommandResult instances."""
    return CommandResult(
        success=success,
        message=message,
        data=data,
        agent=agent,
        execution_time=execution_time,
        error_code=error_code
    )


@dataclass
class DiscordMessage:
    """Discord message structure."""
    content: str
    author: str
    channel: str
    timestamp: str
    attachments: list | None = None
    embeds: list | None = None

    def __post_init__(self):
        """Set default timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class AgentCommand:
    """Agent command structure."""
    agent_id: str
    command: str
    parameters: dict[str, Any] | None = None
    priority: str = "NORMAL"
    timeout: int = 30

    def validate(self) -> bool:
        """Validate command structure."""
        if not self.agent_id or not self.command:
            return False
        return self.priority in ["LOW", "NORMAL", "HIGH", "URGENT"]


@dataclass
class CommunicationStats:
    """Communication statistics."""
    messages_sent: int = 0
    messages_received: int = 0
    commands_executed: int = 0
    errors_encountered: int = 0
    average_response_time: float = 0.0
    uptime_percentage: float = 100.0

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "commands_executed": self.commands_executed,
            "errors_encountered": self.errors_encountered,
            "average_response_time": self.average_response_time,
            "uptime_percentage": self.uptime_percentage
        }
