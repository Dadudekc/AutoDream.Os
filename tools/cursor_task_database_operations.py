#!/usr/bin/env python3
"""
Cursor Task Database Integration - Operations
=============================================

Database operations for cursor task integration system.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- Database initialization
- CRUD operations
- Task queries
- Data conversion utilities

Extracted from main integration module for V2 compliance.
"""

import json
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from .cursor_task_database_models import CursorTask, TaskPriority, TaskStatus


class CursorTaskDatabaseOperations:
    """Database operations for cursor task integration."""

    def __init__(self, db_path: str | None = None):
        """Initialize database operations."""
        if db_path is None:
            db_path = "unified.db"

        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                # prefer JSON1; won't crash if absent but json_set will be no-op otherwise
                cur.execute("PRAGMA journal_mode=WAL;")
                cur.execute("PRAGMA foreign_keys=ON;")

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cursor_tasks_integrated (
                        task_id TEXT PRIMARY KEY,
                        agent_id TEXT NOT NULL,
                        description TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'CREATED',
                        priority TEXT NOT NULL DEFAULT 'NORMAL',
                        created_at TEXT DEFAULT (datetime('now')),
                        updated_at TEXT DEFAULT (datetime('now')),
                        metadata TEXT DEFAULT '{}',
                        cursor_session_id TEXT,
                        source_file TEXT,
                        scan_context TEXT DEFAULT '{}',
                        fsm_state TEXT,
                        state_transitions TEXT DEFAULT '[]',
                        dependencies TEXT DEFAULT '[]',
                        assigned_by TEXT
                    )
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS scanner_tasks (
                        task_id TEXT PRIMARY KEY,
                        scan_id TEXT,
                        file_path TEXT,
                        complexity_score INTEGER,
                        created_at TEXT DEFAULT (datetime('now')),
                        FOREIGN KEY (task_id) REFERENCES cursor_tasks_integrated(task_id)
                    )
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS fsm_task_tracking (
                        task_id TEXT PRIMARY KEY,
                        current_state TEXT,
                        state_history TEXT DEFAULT '[]',
                        last_transition TEXT,
                        FOREIGN KEY (task_id) REFERENCES cursor_tasks_integrated(task_id)
                    )
                    """
                )

                # Create indexes for performance
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cursor_tasks_agent ON cursor_tasks_integrated(agent_id)"
                )
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cursor_tasks_status ON cursor_tasks_integrated(status)"
                )
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cursor_tasks_priority ON cursor_tasks_integrated(priority)"
                )

                conn.commit()

        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            raise

    def _ensure_json(self, value: str | None) -> dict:
        """Ensure value is valid JSON dict."""
        if not value:
            return {}
        try:
            return json.loads(value) if isinstance(value, str) else value
        except json.JSONDecodeError:
            return {}

    def _row_to_task(self, row: tuple) -> CursorTask:
        """Convert database row to CursorTask object."""
        return CursorTask(
            task_id=row[0],
            agent_id=row[1],
            description=row[2],
            status=TaskStatus(row[3]),
            priority=TaskPriority(row[4]),
            created_at=datetime.fromisoformat(row[5]),
            updated_at=datetime.fromisoformat(row[6]),
            metadata=self._ensure_json(row[7]),
            cursor_session_id=row[8],
            source_file=row[9],
            scan_context=self._ensure_json(row[10]),
            fsm_state=row[11],
            state_transitions=self._ensure_json(row[12]) or [],
            dependencies=self._ensure_json(row[13]) or [],
            assigned_by=row[14],
        )

    def get_task(self, task_id: str) -> CursorTask | None:
        """Get a task by ID."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM cursor_tasks_integrated WHERE task_id = ?", (task_id,))
            row = cur.fetchone()
            return self._row_to_task(row) if row else None

    def list_tasks(self, status: TaskStatus | None = None) -> list[CursorTask]:
        """List tasks, optionally filtered by status."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            if status:
                cur.execute(
                    "SELECT * FROM cursor_tasks_integrated WHERE status = ?", (status.value,)
                )
            else:
                cur.execute("SELECT * FROM cursor_tasks_integrated")
            return [self._row_to_task(r) for r in cur.fetchall()]

    def _insert_cursor_task(self, task: CursorTask) -> None:
        """Insert a new task into the database."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO cursor_tasks_integrated
                (task_id, agent_id, description, status, priority, created_at, updated_at,
                 metadata, cursor_session_id, source_file, scan_context, fsm_state,
                 state_transitions, dependencies, assigned_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.agent_id,
                    task.description,
                    task.status.value,
                    task.priority.value,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                    json.dumps(task.metadata),
                    task.cursor_session_id,
                    task.source_file,
                    json.dumps(task.scan_context),
                    task.fsm_state,
                    json.dumps(task.state_transitions),
                    json.dumps(task.dependencies),
                    task.assigned_by,
                ),
            )
            conn.commit()

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    "UPDATE cursor_tasks_integrated SET status = ?, updated_at = datetime('now') WHERE task_id = ?",
                    (status.value, task_id),
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"❌ Failed to update task status: {e}")
            return False

    def update_task_metadata(self, task_id: str, metadata: dict) -> bool:
        """Update task metadata using JSON1 functions."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                # Use JSON1 functions for safe updates
                cur.execute(
                    """
                    UPDATE cursor_tasks_integrated 
                    SET metadata = json_patch(COALESCE(metadata, '{}'), ?),
                        updated_at = datetime('now')
                    WHERE task_id = ?
                    """,
                    (json.dumps(metadata), task_id),
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"❌ Failed to update task metadata: {e}")
            return False

    def update_task_fsm_state(self, task_id: str, new_state: str, transition_reason: str = "") -> bool:
        """Update task FSM state and log transition."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                # Get current state
                cur.execute("SELECT fsm_state, state_transitions FROM cursor_tasks_integrated WHERE task_id = ?", (task_id,))
                row = cur.fetchone()
                
                if not row:
                    return False
                
                current_state = row[0]
                transitions = self._ensure_json(row[1]) or []
                
                # Add new transition
                transitions.append({
                    "from_state": current_state,
                    "to_state": new_state,
                    "reason": transition_reason,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update task
                cur.execute(
                    """
                    UPDATE cursor_tasks_integrated 
                    SET fsm_state = ?, 
                        state_transitions = ?,
                        updated_at = datetime('now')
                    WHERE task_id = ?
                    """,
                    (new_state, json.dumps(transitions), task_id),
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"❌ Failed to update FSM state: {e}")
            return False

    def assign_task(self, task_id: str, agent_id: str, assigned_by: str = "system") -> bool:
        """Assign a task to an agent."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute(
                    """
                    UPDATE cursor_tasks_integrated 
                    SET agent_id = ?, 
                        assigned_by = ?,
                        status = 'ASSIGNED',
                        updated_at = datetime('now')
                    WHERE task_id = ?
                    """,
                    (agent_id, assigned_by, task_id),
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"❌ Failed to assign task: {e}")
            return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        try:
            with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
                cur.execute("DELETE FROM cursor_tasks_integrated WHERE task_id = ?", (task_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"❌ Failed to delete task: {e}")
            return False

    def get_tasks_by_agent(self, agent_id: str) -> list[CursorTask]:
        """Get all tasks assigned to an agent."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM cursor_tasks_integrated WHERE agent_id = ? ORDER BY created_at DESC",
                (agent_id,)
            )
            return [self._row_to_task(r) for r in cur.fetchall()]

    def get_tasks_by_status(self, status: TaskStatus) -> list[CursorTask]:
        """Get all tasks with a specific status."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM cursor_tasks_integrated WHERE status = ? ORDER BY created_at DESC",
                (status.value,)
            )
            return [self._row_to_task(r) for r in cur.fetchall()]

    def get_task_statistics(self) -> dict:
        """Get task statistics."""
        with sqlite3.connect(self.db_path) as conn, closing(conn.cursor()) as cur:
            stats = {}
            
            # Total tasks
            cur.execute("SELECT COUNT(*) FROM cursor_tasks_integrated")
            stats["total_tasks"] = cur.fetchone()[0]
            
            # Tasks by status
            cur.execute("SELECT status, COUNT(*) FROM cursor_tasks_integrated GROUP BY status")
            stats["by_status"] = dict(cur.fetchall())
            
            # Tasks by priority
            cur.execute("SELECT priority, COUNT(*) FROM cursor_tasks_integrated GROUP BY priority")
            stats["by_priority"] = dict(cur.fetchall())
            
            # Tasks by agent
            cur.execute("SELECT agent_id, COUNT(*) FROM cursor_tasks_integrated GROUP BY agent_id")
            stats["by_agent"] = dict(cur.fetchall())
            
            return stats

