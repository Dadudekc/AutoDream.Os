"""
Persistence Models - Unified Persistence Service
=================================================

Data models for persistence layer.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class PersistenceConfig:
    """Configuration for persistence operations."""

    db_path: str = "data/unified.db"
    auto_migrate: bool = True
    connection_timeout: float = 30.0
    enable_foreign_keys: bool = True
    enable_wal_mode: bool = True


@dataclass
class Agent:
    """Agent entity."""

    id: str
    name: str
    role: str
    capabilities: List[str]
    max_concurrent_tasks: int = 3
    is_active: bool = True
    created_at: datetime = None
    last_active_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Task:
    """Task entity."""

    id: str
    title: str
    description: str
    assigned_agent_id: Optional[str] = None
    status: str = "pending"
    priority: int = 1
    created_at: datetime = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()




