"""
Agent Repository - Unified Persistence Service
===============================================

Repository for Agent entities.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import json
from datetime import datetime
from typing import Iterable, Optional

from .base_repository import BaseRepository
from .database_connection import DatabaseConnection
from .persistence_models import Agent


class AgentRepository(BaseRepository[Agent]):
    """Repository for Agent entities."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize agent repository."""
        super().__init__(db_connection)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Ensure agent table schema exists."""
        schema = """
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            capabilities TEXT,
            max_concurrent_tasks INTEGER DEFAULT 3,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT NOT NULL,
            last_active_at TEXT
        )
        """
        self.db.create_tables([schema])

    def get(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        rows = self.db.execute_query(
            """
            SELECT id, name, role, capabilities, max_concurrent_tasks,
                   is_active, created_at, last_active_at
            FROM agents WHERE id = ?
            """,
            (agent_id,),
        )

        if not rows:
            return None

        return self._row_to_agent(rows[0])

    def get_by_capability(self, capability: str) -> Iterable[Agent]:
        """Get agents by capability."""
        rows = self.db.execute_query(
            """
            SELECT id, name, role, capabilities, max_concurrent_tasks,
                   is_active, created_at, last_active_at
            FROM agents
            WHERE capabilities LIKE ?
            """,
            (f"%{capability}%",),
        )

        for row in rows:
            yield self._row_to_agent(row)

    def get_active(self) -> Iterable[Agent]:
        """Get all active agents."""
        rows = self.db.execute_query(
            """
            SELECT id, name, role, capabilities, max_concurrent_tasks,
                   is_active, created_at, last_active_at
            FROM agents
            WHERE is_active = 1
            ORDER BY last_active_at DESC
            """
        )

        for row in rows:
            yield self._row_to_agent(row)

    def get_available(self) -> Iterable[Agent]:
        """Get agents that can accept more tasks."""
        rows = self.db.execute_query(
            """
            SELECT a.id, a.name, a.role, a.capabilities, a.max_concurrent_tasks,
                   a.is_active, a.created_at, a.last_active_at,
                   COUNT(t.id) as current_tasks
            FROM agents a
            LEFT JOIN tasks t ON t.assigned_agent_id = a.id AND t.completed_at IS NULL
            WHERE a.is_active = 1
            GROUP BY a.id, a.name, a.role, a.capabilities, a.max_concurrent_tasks,
                     a.is_active, a.created_at, a.last_active_at
            HAVING COUNT(t.id) < a.max_concurrent_tasks
            ORDER BY (COUNT(t.id) * 1.0 / a.max_concurrent_tasks) ASC
            """
        )

        for row in rows:
            yield self._row_to_agent(row[:8])  # First 8 columns are agent data

    def save(self, agent: Agent) -> None:
        """Save agent (create or update)."""
        self.db.execute_update(
            """
            INSERT OR REPLACE INTO agents (
                id, name, role, capabilities, max_concurrent_tasks,
                is_active, created_at, last_active_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            self._agent_to_row(agent),
        )

    def delete(self, agent_id: str) -> bool:
        """Delete agent by ID."""
        affected = self.db.execute_update("DELETE FROM agents WHERE id = ?", (agent_id,))
        return affected > 0

    def list_all(self, limit: int = 1000) -> Iterable[Agent]:
        """List all agents."""
        rows = self.db.execute_query(
            """
            SELECT id, name, role, capabilities, max_concurrent_tasks,
                   is_active, created_at, last_active_at
            FROM agents
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

        for row in rows:
            yield self._row_to_agent(row)

    def _row_to_agent(self, row) -> Agent:
        """Convert database row to Agent entity."""
        (
            agent_id,
            name,
            role,
            capabilities_json,
            max_concurrent_tasks,
            is_active,
            created_at_str,
            last_active_at_str,
        ) = row

        # Parse capabilities from JSON
        capabilities = []
        if capabilities_json:
            try:
                capabilities = json.loads(capabilities_json)
            except json.JSONDecodeError:
                capabilities = []

        # Parse datetime strings
        created_at = datetime.fromisoformat(created_at_str)
        last_active_at = (
            datetime.fromisoformat(last_active_at_str) if last_active_at_str else None
        )

        return Agent(
            id=agent_id,
            name=name,
            role=role,
            capabilities=capabilities,
            max_concurrent_tasks=max_concurrent_tasks,
            is_active=bool(is_active),
            created_at=created_at,
            last_active_at=last_active_at,
        )

    def _agent_to_row(self, agent: Agent) -> tuple:
        """Convert Agent entity to database row tuple."""
        return (
            agent.id,
            agent.name,
            agent.role,
            json.dumps(agent.capabilities),
            agent.max_concurrent_tasks,
            1 if agent.is_active else 0,
            agent.created_at.isoformat(),
            agent.last_active_at.isoformat() if agent.last_active_at else None,
        )




