"""
Task Repository - Unified Persistence Service
==============================================

Repository for Task entities.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

from collections.abc import Iterable
from datetime import datetime

from .base_repository import BaseRepository
from .database_connection import DatabaseConnection
from .persistence_models import Task


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
            (task_id,),
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
            (agent_id, limit),
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
            (limit,),
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
            self._task_to_row(task),
        )

    def delete(self, task_id: str) -> bool:
        """Delete task by ID."""
        affected = self.db.execute_update("DELETE FROM tasks WHERE id = ?", (task_id,))
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
            (limit,),
        )

        for row in rows:
            yield self._row_to_task(row)

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task entity."""
        (
            task_id,
            title,
            description,
            assigned_agent_id,
            created_at_str,
            assigned_at_str,
            completed_at_str,
            priority,
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
            priority=priority,
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
            task.priority,
        )
