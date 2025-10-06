#!/usr/bin/env python3
"""
Cursor Task Database Integration - Models
=========================================

Data models and enums for cursor task database integration.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- CursorTask dataclass
- Task enums (Priority, Status)
- Type definitions

Extracted from main integration module for V2 compliance.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"


class TaskStatus(Enum):
    """Task status states."""
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class CursorTask:
    """Enhanced cursor task with full system integration."""

    task_id: str
    agent_id: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    cursor_session_id: str | None = None

    # Project Scanner Integration
    source_file: str | None = None
    scan_context: dict[str, Any] = field(default_factory=dict)

    # FSM Integration
    fsm_state: str | None = None
    state_transitions: list[dict[str, Any]] = field(default_factory=list)

    # Agent Coordination
    dependencies: list[str] = field(default_factory=list)
    assigned_by: str | None = None

