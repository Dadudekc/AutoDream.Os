"""
SQLite Connection Manager
=========================

Manages SQLite connections with automatic cleanup.

Author: Captain Agent-4
License: MIT
"""

import logging
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Optional

logger = logging.getLogger(__name__)


class SQLiteConnectionManager:
    """Manage SQLite connections with proper cleanup."""
    
    def __init__(self):
        """Initialize SQLite connection manager."""
        self.active_connections: Dict[str, sqlite3.Connection] = {}
        self._lock = threading.Lock()
    
    @contextmanager
    def connection(
        self,
        db_path: str | Path,
        timeout: float = 5.0,
        check_same_thread: bool = False
    ) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager for SQLite connections.
        
        Usage:
            with manager.connection("db.sqlite") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        db_path = str(db_path)
        conn_id = f"{db_path}_{threading.get_ident()}"
        
        try:
            with sqlite3.connect(
                db_path,
                timeout=timeout,
                check_same_thread=check_same_thread
            ) as conn:
                conn.row_factory = sqlite3.Row
            
            with self._lock:
                self.active_connections[conn_id] = conn
            
            yield conn
            conn.commit()
            
        except Exception as e:
            logger.error(f"SQLite error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
            with self._lock:
                self.active_connections.pop(conn_id, None)
    
    def close_all(self) -> int:
        """Close all active connections."""
        closed = 0
        with self._lock:
            for conn in list(self.active_connections.values()):
                try:
                    conn.close()
                    closed += 1
                except Exception as e:
                    logger.warning(f"Close error: {e}")
            self.active_connections.clear()
        return closed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        with self._lock:
            return {
                "active_connections": len(self.active_connections),
                "connection_ids": list(self.active_connections.keys())
            }


# Global SQLite manager
_global_sqlite_manager = SQLiteConnectionManager()


def get_sqlite_manager() -> SQLiteConnectionManager:
    """Get global SQLite connection manager."""
    return _global_sqlite_manager

