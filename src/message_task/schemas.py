#!/usr/bin/env python3
"""
Message-Task Schemas
====================

Pydantic models for message-task integration.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InboundMessage(BaseModel):
    """Inbound message from any channel (Discord, CLI, Agent Bus)."""

    id: str
    channel: str  # "discord", "cli", "agent_bus"
    author: str  # agent ID or user ID
    content: str
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True


class ParsedTask(BaseModel):
    """Parsed task from message content."""

    title: str
    description: str = ""
    priority: str = "P3"  # P0 (critical) to P3 (low)
    due_timestamp: float | None = None
    tags: list[str] = Field(default_factory=list)
    assignee: str | None = None
    parent_id: str | None = None
    source_msg_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for fingerprinting."""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "assignee": self.assignee,
            "parent_id": self.parent_id,
            "due_timestamp": self.due_timestamp,
            "tags": sorted(self.tags) if self.tags else [],
        }


class TaskStateTransition(BaseModel):
    """Task state transition event."""

    task_id: str
    from_state: str
    to_state: str
    event: str
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True


class TaskCompletionReport(BaseModel):
    """Task completion report for messaging."""

    task_id: str
    title: str
    agent_id: str
    status: str  # "completed", "failed", "blocked"
    summary: str
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def format_message(self) -> str:
        """Format as message content."""
        status_emoji = {
            "completed": "✅",
            "failed": "❌",
            "blocked": "🚧",
        }.get(self.status, "📋")

        return f"""{status_emoji} Task {self.status.upper()}: {self.title}

Agent: {self.agent_id}
Task ID: {self.task_id}
Summary: {self.summary}

Completed at: {datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')}
"""
