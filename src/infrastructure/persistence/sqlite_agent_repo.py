"""
SQLite Agent Repository - Infrastructure Adapter
===============================================

Concrete implementation of AgentRepository using SQLite.
"""

import json
import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager

from ...domain.entities.agent import Agent
from ...domain.ports.agent_repository import AgentRepository
from ...domain.value_objects.ids import AgentId


class SqliteAgentRepository(AgentRepository):
    """
    SQLite implementation of the AgentRepository port.

    This adapter provides persistence for agents using SQLite database.
    """

    def __init__(self, db_path: str = "data/agents.db"):
        """
        Initialize the SQLite repository.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with self._get_connection() as conn:
            conn.execute(

EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.persistence.sqlite_agent_repo import Sqlite_Agent_Repo

# Initialize and use
instance = Sqlite_Agent_Repo()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Sqlite_Agent_Repo(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

                """
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    capabilities TEXT,  -- JSON string of capabilities
                    max_concurrent_tasks INTEGER DEFAULT 3,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT NOT NULL,
                    last_active_at TEXT
                )
            """
            )
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper cleanup."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def get(self, agent_id: AgentId) -> Agent | None:
        """
        Retrieve an agent by its identifier.

        Args:
            agent_id: The unique identifier of the agent

        Returns:
            The agent if found, None otherwise
        """
        with self._get_connection() as conn:
            row = conn.execute(
                """
                SELECT id, name, role, capabilities, max_concurrent_tasks,
                       is_active, created_at, last_active_at
                FROM agents WHERE id = ?
            """,
                (agent_id,),
            ).fetchone()

            if not row:
                return None

            return self._row_to_agent(row)

    def get_by_capability(self, capability: str) -> Iterable[Agent]:
        """
        Retrieve agents that have a specific capability.

        Args:
            capability: The capability to search for

        Returns:
            Iterable of agents with the specified capability
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, name, role, capabilities, max_concurrent_tasks,
                       is_active, created_at, last_active_at
                FROM agents
                WHERE capabilities LIKE ?
            """,
                (f"%{capability}%",),
            ).fetchall()

            for row in rows:
                yield self._row_to_agent(row)

    def get_active(self) -> Iterable[Agent]:
        """
        Retrieve all active agents.

        Returns:
            Iterable of active agents
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, name, role, capabilities, max_concurrent_tasks,
                       is_active, created_at, last_active_at
                FROM agents
                WHERE is_active = 1
                ORDER BY last_active_at DESC
            """
            ).fetchall()

            for row in rows:
                yield self._row_to_agent(row)

    def get_available(self) -> Iterable[Agent]:
        """
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of available agents
        """
        with self._get_connection() as conn:
            rows = conn.execute(
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
            ).fetchall()

            for row in rows:
                agent = self._row_to_agent(row[:8])  # First 8 columns are agent data
                # Update current task count from the query
                agent._current_task_ids = []  # Reset to empty, will be populated by domain logic
                yield agent

    def add(self, agent: Agent) -> None:
        """
        Add a new agent to the repository.

        Args:
            agent: The agent to add

        Raises:
            ValueError: If agent with same ID already exists
        """
        with self._get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO agents (
                        id, name, role, capabilities, max_concurrent_tasks,
                        is_active, created_at, last_active_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    self._agent_to_row(agent),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Agent with ID {agent.id} already exists")

    def save(self, agent: Agent) -> None:
        """
        Save an existing agent (create or update).

        Args:
            agent: The agent to save
        """
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO agents (
                    id, name, role, capabilities, max_concurrent_tasks,
                    is_active, created_at, last_active_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                self._agent_to_row(agent),
            )
            conn.commit()

    def delete(self, agent_id: AgentId) -> bool:
        """
        Delete an agent from the repository.

        Args:
            agent_id: The identifier of the agent to delete

        Returns:
            True if agent was deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
            conn.commit()
            return cursor.rowcount > 0

    def list_all(self) -> Iterable[Agent]:
        """
        List all agents in the repository.

        Returns:
            Iterable of all agents
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, name, role, capabilities, max_concurrent_tasks,
                       is_active, created_at, last_active_at
                FROM agents
                ORDER BY created_at DESC
            """
            ).fetchall()

            for row in rows:
                yield self._row_to_agent(row)

    def _row_to_agent(self, row) -> Agent:
        """Convert database row to Agent entity."""
        from datetime import datetime

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
        capabilities = set()
        if capabilities_json:
            try:
                capabilities = set(json.loads(capabilities_json))
            except json.JSONDecodeError:
                capabilities = set()

        # Parse datetime strings
        created_at = datetime.fromisoformat(created_at_str)
        last_active_at = datetime.fromisoformat(last_active_at_str) if last_active_at_str else None

        return Agent(
            id=AgentId(agent_id),
            name=name,
            role=role,
            capabilities=capabilities,
            max_concurrent_tasks=max_concurrent_tasks,
            is_active=bool(is_active),
            created_at=created_at,
            last_active_at=last_active_at,
        )

    def _agent_to_row(self, agent: Agent):
        """Convert Agent entity to database row tuple."""
        return (
            agent.id,  # str (from AgentId)
            agent.name,
            agent.role,
            json.dumps(list(agent.capabilities)),
            agent.max_concurrent_tasks,
            1 if agent.is_active else 0,
            agent.created_at.isoformat(),
            agent.last_active_at.isoformat() if agent.last_active_at else None,
        )
