from __future__ import annotations
import sqlite3
from typing import List

from .models import DataSource, DataSourceType, DataType, DataPriority


class DatabaseAdapter:
    """Simple SQLite adapter for storing data sources."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.connection = sqlite3.connect(self.path)
        self._initialize()

    def _initialize(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data_sources (
                id TEXT PRIMARY KEY,
                name TEXT,
                type TEXT,
                data_type TEXT,
                location TEXT,
                priority INTEGER,
                enabled INTEGER,
                metadata TEXT,
                original_service TEXT
            )
            """
        )
        self.connection.commit()

    def add_source(self, source: DataSource) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO data_sources (id, name, type, data_type, location, priority, enabled, metadata, original_service)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source.id,
                source.name,
                source.type.value,
                source.data_type.value,
                source.location,
                source.priority.value,
                int(source.enabled),
                str(source.metadata),
                source.original_service,
            ),
        )
        self.connection.commit()
        return True

    def list_sources(self) -> List[DataSource]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, name, type, data_type, location, priority, enabled, metadata, original_service FROM data_sources"
        )
        rows = cursor.fetchall()
        sources: List[DataSource] = []
        for row in rows:
            sources.append(
                DataSource(
                    id=row[0],
                    name=row[1],
                    type=DataSourceType(row[2]),
                    data_type=DataType(row[3]),
                    location=row[4],
                    priority=DataPriority(row[5]),
                    enabled=bool(row[6]),
                    metadata={},
                    original_service=row[8],
                )
            )
        return sources

    def remove_source(self, source_id: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM data_sources WHERE id = ?", (source_id,))
        self.connection.commit()
        return cursor.rowcount > 0
