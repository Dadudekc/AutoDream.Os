"""
Task Repository Loader - Helper to load task repo without full infrastructure
==============================================================================

This helper loads only the task repository without triggering full infrastructure
imports that have browser dependencies.

Author: Agent-1
"""

import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import datetime

# Simple implementations to avoid importing from domain
TaskId = str
AgentId = str


class SimpleTask:
    """Lightweight task representation for CLI operations."""

    def __init__(
        self,
        id,
        title,
        description=None,
        assigned_agent_id=None,
        created_at=None,
        assigned_at=None,
        completed_at=None,
        priority=1,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_agent_id = assigned_agent_id
        self.created_at = created_at or datetime.utcnow()
        self.assigned_at = assigned_at
        self.completed_at = completed_at
        self.priority = priority

    @property
    def is_assigned(self) -> bool:
        return self.assigned_agent_id is not None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def is_pending(self) -> bool:
        return not self.is_assigned and not self.is_completed

    def assign_to(self, agent_id: str) -> None:
        if self.is_completed:
            raise ValueError("Cannot assign a completed task")
        self.assigned_agent_id = agent_id
        self.assigned_at = datetime.utcnow()

    def complete(self) -> None:
        if not self.is_assigned:
            raise ValueError("Cannot complete an unassigned task")
        if self.is_completed:
            return
        self.completed_at = datetime.utcnow()


class SimpleTaskRepository:
    """Lightweight SQLite task repository for CLI operations."""

    def __init__(self, db_path: str = "data/tasks.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    assigned_agent_id TEXT,
                    created_at TEXT NOT NULL,
                    assigned_at TEXT,
                    completed_at TEXT,
                    priority INTEGER DEFAULT 1
                )
            """
            )
            conn.commit()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def get(self, task_id: str) -> SimpleTask | None:
        with self._get_connection() as conn:
            row = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks WHERE id = ?
            """,
                (task_id,),
            ).fetchone()

            if not row:
                return None

            return self._row_to_task(row)

    def get_pending(self, limit: int = 100) -> Iterable[SimpleTask]:
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                WHERE assigned_agent_id IS NULL AND completed_at IS NULL
                ORDER BY priority DESC, created_at ASC
                LIMIT ?
            """,
                (limit,),
            ).fetchall()

            for row in rows:
                yield self._row_to_task(row)

    def save(self, task: SimpleTask) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO tasks (
                    id, title, description, assigned_agent_id,
                    created_at, assigned_at, completed_at, priority
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                self._task_to_row(task),
            )
            conn.commit()

    def list_all(self, limit: int = 1000) -> Iterable[SimpleTask]:
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            ).fetchall()

            for row in rows:
                yield self._row_to_task(row)

    def _row_to_task(self, row) -> SimpleTask:
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

        created_at = datetime.fromisoformat(created_at_str)
        assigned_at = datetime.fromisoformat(assigned_at_str) if assigned_at_str else None
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

        return SimpleTask(
            id=task_id,
            title=title,
            description=description,
            assigned_agent_id=assigned_agent_id,
            created_at=created_at,
            assigned_at=assigned_at,
            completed_at=completed_at,
            priority=priority,
        )

    def _task_to_row(self, task: SimpleTask):
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
