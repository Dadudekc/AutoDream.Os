#!/usr/bin/env python3
"""
Unified Database Services - Consolidated Module
==============================================

Consolidated database services providing unified access to all database operations.
Combines cursor management, model operations, and data persistence.

V2 Compliance: Single consolidated module, clean architecture.
Consolidation: 5→1 files (80% reduction)

Author: Agent-8 - Operations & Support Specialist
Mission: Phase 2 Consolidation - Chunk SVC-08
License: MIT
"""

from __future__ import annotations

import logging
import sqlite3
import json
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from ..core.unified_config import UnifiedConfig


class DatabaseConnectionError(Exception):
    """Database connection error."""
    pass


class DatabaseOperationError(Exception):
    """Database operation error."""
    pass


class DatabaseValidationError(Exception):
    """Database validation error."""
    pass


@dataclass
class DatabaseConfig:
    """Database configuration."""
    database_path: str = ":memory:"
    connection_timeout: float = 30.0
    max_connections: int = 10
    enable_foreign_keys: bool = True
    enable_wal_mode: bool = True
    cache_size: int = -64000  # 64MB cache
    synchronous: str = "NORMAL"


@dataclass
class DatabaseStats:
    """Database statistics."""
    total_connections: int = 0
    active_connections: int = 0
    total_queries: int = 0
    failed_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    last_backup: Optional[datetime] = None
    database_size: int = 0


class DatabaseConnectionManager:
    """Database connection manager."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._connections: Dict[str, sqlite3.Connection] = {}
        self._stats = DatabaseStats()

    @contextmanager
    def get_connection(self, connection_id: Optional[str] = None):
        """Get a database connection."""
        if connection_id is None:
            connection_id = str(uuid4())

        try:
            if connection_id not in self._connections:
                self._create_connection(connection_id)

            connection = self._connections[connection_id]
            self._stats.active_connections += 1

            yield connection

        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise DatabaseConnectionError(f"Failed to get connection: {e}")
        finally:
            self._stats.active_connections = max(0, self._stats.active_connections - 1)

    def _create_connection(self, connection_id: str):
        """Create a new database connection."""
        try:
            connection = sqlite3.connect(
                self.config.database_path,
                timeout=self.config.connection_timeout
            )

            # Configure connection
            if self.config.enable_foreign_keys:
                connection.execute("PRAGMA foreign_keys = ON")

            if self.config.enable_wal_mode:
                connection.execute("PRAGMA journal_mode = WAL")

            connection.execute(f"PRAGMA cache_size = {self.config.cache_size}")
            connection.execute(f"PRAGMA synchronous = {self.config.synchronous}")

            # Enable row factory for dict-like access
            connection.row_factory = sqlite3.Row

            self._connections[connection_id] = connection
            self._stats.total_connections += 1

            self.logger.info(f"Created database connection: {connection_id}")

        except Exception as e:
            self.logger.error(f"Failed to create connection: {e}")
            raise DatabaseConnectionError(f"Connection creation failed: {e}")

    def close_connection(self, connection_id: str):
        """Close a database connection."""
        if connection_id in self._connections:
            try:
                self._connections[connection_id].close()
                del self._connections[connection_id]
                self.logger.info(f"Closed database connection: {connection_id}")
            except Exception as e:
                self.logger.error(f"Error closing connection {connection_id}: {e}")

    def close_all_connections(self):
        """Close all database connections."""
        for connection_id in list(self._connections.keys()):
            self.close_connection(connection_id)

    def get_stats(self) -> DatabaseStats:
        """Get database statistics."""
        try:
            # Update database size if it's a file
            if self.config.database_path != ":memory:":
                db_path = Path(self.config.database_path)
                if db_path.exists():
                    self._stats.database_size = db_path.stat().st_size
        except Exception:
            pass

        return self._stats


class DatabaseQueryBuilder:
    """SQL query builder."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def build_select(self, table: str, columns: List[str] = None,
                    where: Dict[str, Any] = None, order_by: List[str] = None,
                    limit: int = None, offset: int = None) -> str:
        """Build SELECT query."""
        columns_str = "*" if not columns else ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table}"

        if where:
            where_clauses = []
            for key, value in where.items():
                if isinstance(value, str):
                    where_clauses.append(f"{key} = '{value}'")
                else:
                    where_clauses.append(f"{key} = {value}")
            query += f" WHERE {' AND '.join(where_clauses)}"

        if order_by:
            query += f" ORDER BY {', '.join(order_by)}"

        if limit:
            query += f" LIMIT {limit}"

        if offset:
            query += f" OFFSET {offset}"

        return query

    def build_insert(self, table: str, data: Dict[str, Any]) -> tuple[str, list]:
        """Build INSERT query."""
        columns = list(data.keys())
        placeholders = ["?" for _ in columns]
        values = list(data.values())

        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        return query, values

    def build_update(self, table: str, data: Dict[str, Any],
                    where: Dict[str, Any]) -> tuple[str, list]:
        """Build UPDATE query."""
        set_clauses = []
        values = []

        for key, value in data.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)

        query = f"UPDATE {table} SET {', '.join(set_clauses)}"

        if where:
            where_clauses = []
            for key, value in where.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            query += f" WHERE {' AND '.join(where_clauses)}"

        return query, values

    def build_delete(self, table: str, where: Dict[str, Any]) -> tuple[str, list]:
        """Build DELETE query."""
        query = f"DELETE FROM {table}"

        if where:
            where_clauses = []
            values = []
            for key, value in where.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            query += f" WHERE {' AND '.join(where_clauses)}"
            return query, values

        return query, []


class DatabaseModel(ABC):
    """Base database model."""

    table_name: str = ""
    primary_key: str = "id"

    @classmethod
    @abstractmethod
    def create_table_sql(cls) -> str:
        """Return SQL to create the table."""
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseModel':
        """Create instance from dictionary."""
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {key: getattr(self, key) for key in dir(self)
                if not key.startswith('_') and not callable(getattr(self, key))}


class DatabaseValidator:
    """Database data validator."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_data(self, model_class: type, data: Dict[str, Any]) -> bool:
        """Validate data against model requirements."""
        try:
            # Basic validation - check required fields
            instance = model_class()
            required_attrs = [attr for attr in dir(instance)
                            if not attr.startswith('_') and
                            not callable(getattr(instance, attr)) and
                            getattr(instance, attr) is None]

            for attr in required_attrs:
                if attr not in data:
                    raise DatabaseValidationError(f"Missing required field: {attr}")

            return True

        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False


class UnifiedDatabaseService:
    """Unified database service."""

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.connection_manager = DatabaseConnectionManager(self.config)
        self.query_builder = DatabaseQueryBuilder()
        self.validator = DatabaseValidator()

        # Model registry
        self._models: Dict[str, type] = {}

        self.logger.info("✅ Unified Database Service initialized")

    def register_model(self, model_class: type):
        """Register a database model."""
        if not hasattr(model_class, 'table_name') or not model_class.table_name:
            raise ValueError("Model must have a table_name attribute")

        self._models[model_class.table_name] = model_class
        self.logger.info(f"Registered model: {model_class.__name__} for table {model_class.table_name}")

    def create_tables(self):
        """Create all registered tables."""
        with self.connection_manager.get_connection() as conn:
            for model_class in self._models.values():
                try:
                    conn.execute(model_class.create_table_sql())
                    self.logger.info(f"Created table: {model_class.table_name}")
                except Exception as e:
                    self.logger.error(f"Failed to create table {model_class.table_name}: {e}")
                    raise DatabaseOperationError(f"Table creation failed: {e}")

            conn.commit()

    def insert(self, model_class: type, data: Dict[str, Any]) -> str:
        """Insert a record."""
        if not self.validator.validate_data(model_class, data):
            raise DatabaseValidationError("Invalid data")

        query, values = self.query_builder.build_insert(model_class.table_name, data)

        with self.connection_manager.get_connection() as conn:
            try:
                cursor = conn.execute(query, values)
                record_id = cursor.lastrowid
                conn.commit()

                self._stats.total_queries += 1
                self.logger.info(f"Inserted record into {model_class.table_name}: {record_id}")
                return str(record_id)

            except Exception as e:
                self._stats.failed_queries += 1
                self.logger.error(f"Insert failed: {e}")
                raise DatabaseOperationError(f"Insert failed: {e}")

    def select(self, model_class: type, where: Dict[str, Any] = None,
              order_by: List[str] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Select records."""
        query = self.query_builder.build_select(
            model_class.table_name,
            where=where,
            order_by=order_by,
            limit=limit
        )

        with self.connection_manager.get_connection() as conn:
            try:
                cursor = conn.execute(query)
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    results.append(dict(row))

                self._stats.total_queries += 1
                self.logger.info(f"Selected {len(results)} records from {model_class.table_name}")
                return results

            except Exception as e:
                self._stats.failed_queries += 1
                self.logger.error(f"Select failed: {e}")
                raise DatabaseOperationError(f"Select failed: {e}")

    def update(self, model_class: type, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Update records."""
        if not self.validator.validate_data(model_class, data):
            raise DatabaseValidationError("Invalid data")

        query, values = self.query_builder.build_update(model_class.table_name, data, where)

        with self.connection_manager.get_connection() as conn:
            try:
                cursor = conn.execute(query, values)
                updated_count = cursor.rowcount
                conn.commit()

                self._stats.total_queries += 1
                self.logger.info(f"Updated {updated_count} records in {model_class.table_name}")
                return updated_count

            except Exception as e:
                self._stats.failed_queries += 1
                self.logger.error(f"Update failed: {e}")
                raise DatabaseOperationError(f"Update failed: {e}")

    def delete(self, model_class: type, where: Dict[str, Any]) -> int:
        """Delete records."""
        query, values = self.query_builder.build_delete(model_class.table_name, where)

        with self.connection_manager.get_connection() as conn:
            try:
                cursor = conn.execute(query, values)
                deleted_count = cursor.rowcount
                conn.commit()

                self._stats.total_queries += 1
                self.logger.info(f"Deleted {deleted_count} records from {model_class.table_name}")
                return deleted_count

            except Exception as e:
                self._stats.failed_queries += 1
                self.logger.error(f"Delete failed: {e}")
                raise DatabaseOperationError(f"Delete failed: {e}")

    def execute_raw_query(self, query: str, parameters: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a raw SQL query."""
        with self.connection_manager.get_connection() as conn:
            try:
                cursor = conn.execute(query, parameters)
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    results.append(dict(row))

                self._stats.total_queries += 1
                self.logger.info(f"Executed raw query, returned {len(results)} rows")
                return results

            except Exception as e:
                self._stats.failed_queries += 1
                self.logger.error(f"Raw query failed: {e}")
                raise DatabaseOperationError(f"Raw query failed: {e}")

    def backup_database(self, backup_path: str):
        """Backup the database."""
        try:
            with self.connection_manager.get_connection() as conn:
                # Create backup
                backup_conn = sqlite3.connect(backup_path)
                conn.backup(backup_conn)
                backup_conn.close()

            self._stats.last_backup = datetime.now()
            self.logger.info(f"Database backed up to: {backup_path}")

        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            raise DatabaseOperationError(f"Backup failed: {e}")

    def get_stats(self) -> DatabaseStats:
        """Get database statistics."""
        stats = self.connection_manager.get_stats()
        # Update with our query stats
        stats.total_queries = self._stats.total_queries
        stats.failed_queries = self._stats.failed_queries
        return stats

    def cleanup(self):
        """Clean up resources."""
        self.connection_manager.close_all_connections()
        self.logger.info("🧹 Database service cleanup completed")


# Factory function for creating database service instances
def create_unified_database_service(config: Optional[DatabaseConfig] = None) -> UnifiedDatabaseService:
    """Factory function for UnifiedDatabaseService creation."""
    return UnifiedDatabaseService(config=config)


# Backward compatibility aliases
DatabaseService = UnifiedDatabaseService
DatabaseManager = UnifiedDatabaseService

# Export all classes
__all__ = [
    "UnifiedDatabaseService",
    "DatabaseService",
    "DatabaseManager",
    "DatabaseConfig",
    "DatabaseStats",
    "DatabaseConnectionManager",
    "DatabaseQueryBuilder",
    "DatabaseModel",
    "DatabaseValidator",
    "DatabaseConnectionError",
    "DatabaseOperationError",
    "DatabaseValidationError",
    "create_unified_database_service"
]
