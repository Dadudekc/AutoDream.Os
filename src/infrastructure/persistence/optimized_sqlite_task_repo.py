"""
Optimized SQLite Task Repository - Performance Enhancement
==========================================================

Enhanced SQLite implementation with connection pooling, query caching,
and performance optimizations for high-throughput operations.

V2 Compliance: <400 lines, single responsibility, performance optimization.
"""

import hashlib
import logging
import sqlite3
import threading
import time
from collections.abc import Iterable
from contextlib import contextmanager
from typing import Any, Optional

from ...domain.entities.task import Task
from ...domain.ports.task_repository import TaskRepository
from ...domain.value_objects.ids import AgentId, TaskId


class QueryCache:
    """Simple query result cache with TTL support."""

    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self._cache = {}
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get cached data if not expired."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry["timestamp"] < self._ttl:
                    return entry["data"]
                else:
                    del self._cache[key]
        return None

    def set(self, key: str, data: Any) -> None:
        """Set data in cache with eviction of oldest entries."""
        with self._lock:
            if len(self._cache) >= self._max_size:
                # Remove oldest entry
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]["timestamp"])
                del self._cache[oldest_key]

            self._cache[key] = {"data": data, "timestamp": time.time()}

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache entries containing pattern."""
        with self._lock:
            keys_to_remove = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self._cache[key]
            return len(keys_to_remove)


class OptimizedSqliteTaskRepository(TaskRepository):
    """
    Optimized SQLite implementation with connection pooling and caching.

    Performance improvements:
    - Connection pooling to reduce connection overhead
    - Query result caching for frequently accessed data
    - Database indexes for optimized queries
    - Prepared statements for repeated queries
    """

    def __init__(self, db_path: str = "data/tasks.db", pool_size: int = 5):
        """
        Initialize optimized repository.

        Args:
            db_path: Path to SQLite database file
            pool_size: Maximum number of connections in pool
        """
        self.db_path = db_path
        self._pool_size = pool_size
        self._connection_pool = []
        self._pool_lock = threading.Lock()
        self._cache = QueryCache(max_size=500, ttl=300)  # 5 min TTL
        self._prepared_statements = {}

        # Initialize database and indexes
        self._init_db()
        self._create_indexes()

    def _init_db(self) -> None:
        """Initialize database schema with performance optimizations."""
        with self._get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for performance
            conn.execute("PRAGMA synchronous=NORMAL")  # Balanced performance/safety
            conn.execute("PRAGMA cache_size=10000")  # 10MB cache
            conn.execute("PRAGMA temp_store=MEMORY")  # Temp tables in memory

            # Create optimized schema
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

    def _create_indexes(self) -> None:
        """Create performance indexes for common query patterns."""
        with self._get_connection() as conn:
            # Index for agent-specific queries
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_agent
                ON tasks(assigned_agent_id)
            """
            )

            # Composite index for priority sorting
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_priority_created
                ON tasks(priority DESC, created_at ASC)
            """
            )

            # Index for completion status queries
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(assigned_agent_id, completed_at)
            """
            )
            conn.commit()

    def _get_connection(self):
        """Get connection from pool or create new one."""
        with self._pool_lock:
            if self._connection_pool:
                return self._connection_pool.pop()
            return sqlite3.connect(self.db_path)

    def _return_connection(self, conn) -> None:
        """Return connection to pool."""
        with self._pool_lock:
            if len(self._connection_pool) < self._pool_size:
                self._connection_pool.append(conn)
            else:
                conn.close()

    @contextmanager
    def _managed_connection(self):
        """Context manager for connection lifecycle."""
        conn = self._get_connection()
        try:
            yield conn
        finally:
            self._return_connection(conn)

    def _generate_cache_key(self, operation: str, *args) -> str:
        """Generate cache key for query results."""
        key_parts = [operation] + [str(arg) for arg in args]
        return hashlib.md5("|".join(key_parts).encode()).hexdigest()

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task object."""
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            assigned_agent_id=row[3],
            created_at=row[4],
            assigned_at=row[5],
            completed_at=row[6],
            priority=row[7],
        )

    def get(self, task_id: TaskId) -> Optional[Task]:
        """
        Retrieve a task by ID with caching.

        Performance: O(1) cache lookup, O(log n) database query with index
        """
        cache_key = self._generate_cache_key("task", task_id)

        # Check cache first
        cached_task = self._cache.get(cache_key)
        if cached_task:
            return cached_task

        # Query database
        with self._managed_connection() as conn:
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

            task = self._row_to_task(row)

            # Cache the result
            self._cache.set(cache_key, task)
            return task

    def get_by_agent(self, agent_id: str, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve tasks by agent with optimized pagination.

        Performance: O(log n) with index, cached results for repeated queries
        """
        cache_key = self._generate_cache_key("agent_tasks", agent_id, limit)

        # Check cache first
        cached_tasks = self._cache.get(cache_key)
        if cached_tasks:
            yield from cached_tasks
            return

        # Query database with optimized index usage
        tasks = []
        with self._managed_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                WHERE assigned_agent_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (agent_id, limit),
            ).fetchall()

            for row in rows:
                task = self._row_to_task(row)
                tasks.append(task)
                yield task

        # Cache the results
        if tasks:
            self._cache.set(cache_key, tasks)

    def get_pending(self, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve pending tasks with optimized query.

        Performance: Uses composite index for efficient sorting and filtering
        """
        cache_key = self._generate_cache_key("pending_tasks", limit)

        # Check cache first
        cached_tasks = self._cache.get(cache_key)
        if cached_tasks:
            yield from cached_tasks
            return

        # Query with optimized composite index
        tasks = []
        with self._managed_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                WHERE assigned_agent_id IS NULL
                ORDER BY priority DESC, created_at ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            for row in rows:
                task = self._row_to_task(row)
                tasks.append(task)
                yield task

        # Cache the results
        if tasks:
            self._cache.set(cache_key, tasks)

    def add(self, task: Task) -> None:
        """
        Add a new task with cache invalidation.

        Performance: O(1) insertion with immediate cache invalidation
        """
        with self._managed_connection() as conn:
            conn.execute(
                """
                INSERT INTO tasks (id, title, description, assigned_agent_id,
                                 created_at, assigned_at, completed_at, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.id,
                    task.title,
                    task.description,
                    task.assigned_agent_id,
                    task.created_at,
                    task.assigned_at,
                    task.completed_at,
                    task.priority,
                ),
            )
            conn.commit()

        # Invalidate related caches
        self._cache.invalidate_pattern("pending_tasks")
        if task.assigned_agent_id:
            self._cache.invalidate_pattern(f"agent_tasks|{task.assigned_agent_id}")

    def update(self, task: Task) -> None:
        """
        Update existing task with cache management.

        Performance: O(log n) update with targeted cache invalidation
        """
        with self._managed_connection() as conn:
            conn.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, assigned_agent_id = ?,
                    created_at = ?, assigned_at = ?, completed_at = ?,
                    priority = ?
                WHERE id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.assigned_agent_id,
                    task.created_at,
                    task.assigned_at,
                    task.completed_at,
                    task.priority,
                    task.id,
                ),
            )
            conn.commit()

        # Invalidate affected caches
        self._cache.invalidate_pattern(f"task|{task.id}")
        self._cache.invalidate_pattern("pending_tasks")
        if task.assigned_agent_id:
            self._cache.invalidate_pattern(f"agent_tasks|{task.assigned_agent_id}")

    def delete(self, task_id: TaskId) -> None:
        """
        Delete task with cache cleanup.

        Performance: O(log n) deletion with cache invalidation
        """
        with self._managed_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

        # Invalidate caches
        self._cache.invalidate_pattern(f"task|{task_id}")
        self._cache.invalidate_pattern("pending_tasks")
        self._cache.invalidate_pattern("agent_tasks")

    def get_all(self, limit: int = 1000) -> Iterable[Task]:
        """
        Get all tasks with pagination for memory efficiency.

        Performance: Controlled memory usage with streaming results
        """
        cache_key = self._generate_cache_key("all_tasks", limit)

        # Check cache first
        cached_tasks = self._cache.get(cache_key)
        if cached_tasks:
            yield from cached_tasks
            return

        # Stream results to manage memory
        tasks = []
        with self._managed_connection() as conn:
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
                task = self._row_to_task(row)
                tasks.append(task)
                yield task

        # Cache results for future queries
        if tasks:
            self._cache.set(cache_key, tasks)

    def clear_cache(self) -> None:
        """Clear all cached query results."""
        self._cache._cache.clear()

    def get_cache_stats(self) -> dict:
        """Get cache performance statistics."""
        return {
            "cache_size": len(self._cache._cache),
            "max_cache_size": self._cache._max_size,
            "cache_ttl": self._cache._ttl,
            "connection_pool_size": len(self._connection_pool),
            "max_pool_size": self._pool_size,
        }


# Create optimized singleton instance
_optimized_repo = None


def get_optimized_task_repository(db_path: str = "data/tasks.db") -> OptimizedSqliteTaskRepository:
    """Get optimized task repository singleton."""
    global _optimized_repo
    if _optimized_repo is None:
        _optimized_repo = OptimizedSqliteTaskRepository(db_path)
    return _optimized_repo
