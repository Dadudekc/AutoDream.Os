#!/usr/bin/env python3
"""
Unified Persistence Service - V2 Compliance Module
==================================================

Consolidated data persistence system following SOLID principles.
Combines functionality from:
- sqlite_agent_repo.py (agent persistence)
- sqlite_task_repo.py (task persistence)
- __init__.py (module coordination)

SOLID Implementation:
- SRP: Each repository handles one entity type
- OCP: Extensible repository system
- DIP: Dependencies injected via constructor
- ISP: Separate interfaces for different persistence operations

Author: Agent-3 (DevOps Specialist)
License: MIT
"""

import json
import logging
import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

logger = logging.getLogger(__name__)

# Generic type for entities
T = TypeVar('T')


@dataclass
class PersistenceConfig:
    """Configuration for persistence operations."""
    db_path: str = "data/unified.db"
    auto_migrate: bool = True
    connection_timeout: float = 30.0
    enable_foreign_keys: bool = True
    enable_wal_mode: bool = True


class DatabaseConnection:
    """Manages database connections with proper cleanup and configuration."""

    def __init__(self, config: PersistenceConfig):
        """Initialize database connection manager."""
        self.config = config
        self.db_path = config.db_path

        # Ensure database directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Get a database connection with proper configuration and cleanup."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.config.connection_timeout
        )

        try:
            if self.config.enable_foreign_keys:
                conn.execute("PRAGMA foreign_keys = ON")

            if self.config.enable_wal_mode:
                conn.execute("PRAGMA journal_mode = WAL")

            yield conn

        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list[tuple]:
        """Execute a query and return results."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return affected rows."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def create_tables(self, schema_queries: list[str]) -> bool:
        """Create database tables from schema queries."""
        try:
            with self.get_connection() as conn:
                for query in schema_queries:
                    conn.execute(query)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            return False


class BaseRepository(ABC, Generic[T]):
    """Abstract base class for repositories."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize repository with database connection."""
        self.db = db_connection

    @abstractmethod
    def get(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        pass

    @abstractmethod
    def save(self, entity: T) -> None:
        """Save entity (create or update)."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    def list_all(self, limit: int = 1000) -> Iterable[T]:
        """List all entities."""
        pass


# Domain entity stubs (simplified for persistence layer)
@dataclass
class Agent:
    """Agent entity."""
    id: str
    name: str
    role: str
    capabilities: list[str]
    max_concurrent_tasks: int = 3
    is_active: bool = True
    created_at: datetime = None
    last_active_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Task:
    """Task entity."""
    id: str
    title: str
    description: str | None = None
    assigned_agent_id: str | None = None
    created_at: datetime = None
    assigned_at: datetime | None = None
    completed_at: datetime | None = None
    priority: int = 1

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


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
            capabilities TEXT,  -- JSON string of capabilities
            max_concurrent_tasks INTEGER DEFAULT 3,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT NOT NULL,
            last_active_at TEXT
        )
        """
        self.db.create_tables([schema])

    def get(self, agent_id: str) -> Agent | None:
        """Get agent by ID."""
        rows = self.db.execute_query(
            """
            SELECT id, name, role, capabilities, max_concurrent_tasks,
                   is_active, created_at, last_active_at
            FROM agents WHERE id = ?
            """,
            (agent_id,)
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
            (f"%{capability}%",)
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
            self._agent_to_row(agent)
        )

    def delete(self, agent_id: str) -> bool:
        """Delete agent by ID."""
        affected = self.db.execute_update(
            "DELETE FROM agents WHERE id = ?",
            (agent_id,)
        )
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
            (limit,)
        )

        for row in rows:
            yield self._row_to_agent(row)

    def _row_to_agent(self, row) -> Agent:
        """Convert database row to Agent entity."""
        (
            agent_id, name, role, capabilities_json,
            max_concurrent_tasks, is_active, created_at_str, last_active_at_str
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
        last_active_at = datetime.fromisoformat(last_active_at_str) if last_active_at_str else None

        return Agent(
            id=agent_id,
            name=name,
            role=role,
            capabilities=capabilities,
            max_concurrent_tasks=max_concurrent_tasks,
            is_active=bool(is_active),
            created_at=created_at,
            last_active_at=last_active_at
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


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entities."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize task repository."""
        super().__init__(db_connection)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Ensure task table schema exists."""
        schema = """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            assigned_agent_id TEXT,
            created_at TEXT NOT NULL,
            assigned_at TEXT,
            completed_at TEXT,
            priority INTEGER DEFAULT 1,
            FOREIGN KEY (assigned_agent_id) REFERENCES agents(id)
        )
        """
        self.db.create_tables([schema])

    def get(self, task_id: str) -> Task | None:
        """Get task by ID."""
        rows = self.db.execute_query(
            """
            SELECT id, title, description, assigned_agent_id,
                   created_at, assigned_at, completed_at, priority
            FROM tasks WHERE id = ?
            """,
            (task_id,)
        )

        if not rows:
            return None

        return self._row_to_task(rows[0])

    def get_by_agent(self, agent_id: str, limit: int = 100) -> Iterable[Task]:
        """Get tasks by agent ID."""
        rows = self.db.execute_query(
            """
            SELECT id, title, description, assigned_agent_id,
                   created_at, assigned_at, completed_at, priority
            FROM tasks
            WHERE assigned_agent_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (agent_id, limit)
        )

        for row in rows:
            yield self._row_to_task(row)

    def get_pending(self, limit: int = 100) -> Iterable[Task]:
        """Get pending (unassigned) tasks."""
        rows = self.db.execute_query(
            """
            SELECT id, title, description, assigned_agent_id,
                   created_at, assigned_at, completed_at, priority
            FROM tasks
            WHERE assigned_agent_id IS NULL
            ORDER BY priority DESC, created_at ASC
            LIMIT ?
            """,
            (limit,)
        )

        for row in rows:
            yield self._row_to_task(row)

    def save(self, task: Task) -> None:
        """Save task (create or update)."""
        self.db.execute_update(
            """
            INSERT OR REPLACE INTO tasks (
                id, title, description, assigned_agent_id,
                created_at, assigned_at, completed_at, priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            self._task_to_row(task)
        )

    def delete(self, task_id: str) -> bool:
        """Delete task by ID."""
        affected = self.db.execute_update(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        return affected > 0

    def list_all(self, limit: int = 1000) -> Iterable[Task]:
        """List all tasks."""
        rows = self.db.execute_query(
            """
            SELECT id, title, description, assigned_agent_id,
                   created_at, assigned_at, completed_at, priority
            FROM tasks
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,)
        )

        for row in rows:
            yield self._row_to_task(row)

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task entity."""
        (
            task_id, title, description, assigned_agent_id,
            created_at_str, assigned_at_str, completed_at_str, priority
        ) = row

        # Parse datetime strings
        created_at = datetime.fromisoformat(created_at_str)
        assigned_at = datetime.fromisoformat(assigned_at_str) if assigned_at_str else None
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

        return Task(
            id=task_id,
            title=title,
            description=description,
            assigned_agent_id=assigned_agent_id,
            created_at=created_at,
            assigned_at=assigned_at,
            completed_at=completed_at,
            priority=priority
        )

    def _task_to_row(self, task: Task) -> tuple:
        """Convert Task entity to database row tuple."""
        return (
            task.id,
            task.title,
            task.description,
            task.assigned_agent_id,
            task.created_at.isoformat(),
            task.assigned_at.isoformat() if task.assigned_at else None,
            task.completed_at.isoformat() if task.completed_at else None,
            task.priority
        )


class PersistenceStatistics:
    """Provides statistics about the persistence layer."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize statistics provider."""
        self.db = db_connection

    def get_database_stats(self) -> dict[str, Any]:
        """Get comprehensive database statistics."""
        stats = {
            'total_agents': 0,
            'active_agents': 0,
            'total_tasks': 0,
            'pending_tasks': 0,
            'completed_tasks': 0,
            'assigned_tasks': 0,
            'database_size': 0,
            'table_info': {}
        }

        try:
            # Agent statistics
            agent_rows = self.db.execute_query("SELECT COUNT(*) FROM agents")
            stats['total_agents'] = agent_rows[0][0] if agent_rows else 0

            active_rows = self.db.execute_query("SELECT COUNT(*) FROM agents WHERE is_active = 1")
            stats['active_agents'] = active_rows[0][0] if active_rows else 0

            # Task statistics
            task_rows = self.db.execute_query("SELECT COUNT(*) FROM tasks")
            stats['total_tasks'] = task_rows[0][0] if task_rows else 0

            pending_rows = self.db.execute_query("SELECT COUNT(*) FROM tasks WHERE assigned_agent_id IS NULL")
            stats['pending_tasks'] = pending_rows[0][0] if pending_rows else 0

            completed_rows = self.db.execute_query("SELECT COUNT(*) FROM tasks WHERE completed_at IS NOT NULL")
            stats['completed_tasks'] = completed_rows[0][0] if completed_rows else 0

            assigned_rows = self.db.execute_query("SELECT COUNT(*) FROM tasks WHERE assigned_agent_id IS NOT NULL AND completed_at IS NULL")
            stats['assigned_tasks'] = assigned_rows[0][0] if assigned_rows else 0

            # Database file size
            db_path = Path(self.db.db_path)
            if db_path.exists():
                stats['database_size'] = db_path.stat().st_size

            # Table information
            table_info_rows = self.db.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            for row in table_info_rows:
                table_name = row[0]
                count_rows = self.db.execute_query(f"SELECT COUNT(*) FROM {table_name}")
                stats['table_info'][table_name] = count_rows[0][0] if count_rows else 0

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")

        return stats


class UnifiedPersistenceService:
    """Main unified persistence service interface."""

    def __init__(self, config: PersistenceConfig | None = None):
        """Initialize unified persistence service."""
        self.config = config or PersistenceConfig()

        # Initialize components
        self.db_connection = DatabaseConnection(self.config)
        self.agent_repo = AgentRepository(self.db_connection)
        self.task_repo = TaskRepository(self.db_connection)
        self.stats = PersistenceStatistics(self.db_connection)

    # Agent operations
    def save_agent(self, agent: Agent) -> None:
        """Save an agent."""
        self.agent_repo.save(agent)

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID."""
        return self.agent_repo.get(agent_id)

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        return self.agent_repo.delete(agent_id)

    def list_agents(self, limit: int = 1000) -> list[Agent]:
        """List all agents."""
        return list(self.agent_repo.list_all(limit))

    def get_active_agents(self) -> list[Agent]:
        """Get all active agents."""
        return list(self.agent_repo.get_active())

    def get_available_agents(self) -> list[Agent]:
        """Get agents that can accept more tasks."""
        return list(self.agent_repo.get_available())

    def get_agents_by_capability(self, capability: str) -> list[Agent]:
        """Get agents by capability."""
        return list(self.agent_repo.get_by_capability(capability))

    # Task operations
    def save_task(self, task: Task) -> None:
        """Save a task."""
        self.task_repo.save(task)

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        return self.task_repo.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        return self.task_repo.delete(task_id)

    def list_tasks(self, limit: int = 1000) -> list[Task]:
        """List all tasks."""
        return list(self.task_repo.list_all(limit))

    def get_tasks_by_agent(self, agent_id: str, limit: int = 100) -> list[Task]:
        """Get tasks by agent ID."""
        return list(self.task_repo.get_by_agent(agent_id, limit))

    def get_pending_tasks(self, limit: int = 100) -> list[Task]:
        """Get pending tasks."""
        return list(self.task_repo.get_pending(limit))

    # Statistics and maintenance
    def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics."""
        return self.stats.get_database_stats()

    def optimize_database(self) -> bool:
        """Optimize database performance."""
        try:
            # Vacuum database to reclaim space
            self.db_connection.execute_update("VACUUM")

            # Rebuild indexes
            self.db_connection.execute_update("REINDEX")

            logger.info("✅ Database optimization completed")
            return True

        except Exception as e:
            logger.error(f"❌ Database optimization failed: {e}")
            return False

    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        try:
            import shutil

            # Ensure backup directory exists
            Path(backup_path).parent.mkdir(parents=True, exist_ok=True)

            # Copy database file
            shutil.copy2(self.config.db_path, backup_path)

            logger.info(f"✅ Database backup created: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Database backup failed: {e}")
            return False


def create_persistence_service(db_path: str = "data/unified.db") -> UnifiedPersistenceService:
    """Factory function to create persistence service."""
    config = PersistenceConfig(db_path=db_path)
    return UnifiedPersistenceService(config)


if __name__ == '__main__':
    # Example usage
    service = create_persistence_service()

    # Create sample agent
    agent = Agent(
        id="agent_001",
        name="Test Agent",
        role="Test Role",
        capabilities=["test", "debug"]
    )

    # Save agent
    service.save_agent(agent)
    print("✅ Agent saved")

    # Retrieve agent
    retrieved = service.get_agent("agent_001")
    if retrieved:
        print(f"✅ Agent retrieved: {retrieved.name}")

    # Create sample task
    task = Task(
        id="task_001",
        title="Test Task",
        description="A test task",
        priority=2
    )

    # Save task
    service.save_task(task)
    print("✅ Task saved")

    # Get stats
    stats = service.get_database_stats()
    print(f"📊 Database stats: {stats}")

    print("🎉 Unified persistence service test complete!")
