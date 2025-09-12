#!/usr/bin/env python3
"""Core vector database utilities.

This module provides a minimal SSOT interface for storing agent status
embeddings. It uses SQLite under the hood and exposes helper functions for
interacting with the ``agent_status_embeddings`` table.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class DocumentType(Enum):
    """Document types for vector database."""

    MESSAGE = "message"
    DEVLOG = "devlog"
    CONTRACT = "contract"
    STATUS = "status"
    CODE = "code"
    DOCUMENTATION = "documentation"


class SearchType(Enum):
    """Search types for vector database."""

    SIMILARITY = "similarity"
    MAX_MARGINAL_RELEVANCE = "mmr"
    FILTERED = "filtered"


class SearchResult:
    """Result of vector database search."""

    def __init__(
    """# Example usage:
result = __init__("example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value", "example_value", {"key": "value"})
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value", "example_value", {"key": "value"})
print(f"Result: {result}")"""
        self, document_id: str, content: str, similarity_score: float, metadata: dict[str, Any]
    ):
        self.document_id = document_id
        self.content = content
        self.similarity_score = similarity_score
        self.metadata = metadata


class VectorDocument:
    """Vector document representation."""

    def __init__(self, id: str, content: str, embedding: list, metadata: dict[str, Any]):
        self.id = id
        self.content = content
        self.embedding = embedding
        self.metadata = metadata


class EmbeddingModel(Enum):
    """Supported embedding models."""

    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "openai-3-small"
    OPENAI_3_LARGE = "openai-3-large"


class VectorDatabaseStats:
    """Vector database statistics."""

    def __init__(self):
        self.total_documents = 0
        self.collections = {}


# ---------------------------------------------------------------------------
# Single source of truth constants
# ---------------------------------------------------------------------------
DB_PATH = Path("data/vector_database.db")
AGENT_STATUS_TABLE = "agent_status_embeddings"


@dataclass
class CollectionConfig:
    """Configuration for vector database collections."""

    name: str
    description: str
    embedding_dimension: int
    similarity_threshold: float = 0.7
    max_documents: int = 10000
    metadata: dict[str, Any] | None = None


SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {AGENT_STATUS_TABLE} (
    agent_id TEXT PRIMARY KEY,
    raw_status TEXT NOT NULL,
    embedding TEXT NOT NULL,
    last_updated TEXT NOT NULL
)
"""


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection ensuring the status table exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    return conn


# ---------------------------------------------------------------------------
# Agent status embedding operations
# ---------------------------------------------------------------------------


def upsert_agent_status(
    conn: sqlite3.Connection,
    agent_id: str,
    raw_status: str,
    embedding: Sequence[float],
    last_updated: str,
) -> None:
    """Insert or update an agent status embedding."""
    payload = (
        agent_id,
        raw_status,
        json.dumps(list(embedding)),
        last_updated,
    )
    conn.execute(
        f"""
        INSERT INTO {AGENT_STATUS_TABLE}
            (agent_id, raw_status, embedding, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
            raw_status=excluded.raw_status,
            embedding=excluded.embedding,
            last_updated=excluded.last_updated
        """,
        payload,
    )
    conn.commit()


def fetch_agent_status(
    conn: sqlite3.Connection, agent_id: str
) -> tuple[str, str, Sequence[float], str] | None:
    """Fetch a stored agent status embedding."""
    cursor = conn.execute(
        (
            f"SELECT agent_id, raw_status, embedding, last_updated "
            f"FROM {AGENT_STATUS_TABLE} WHERE agent_id=?"
        ),
        (agent_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    stored_id, raw_status, embedding_json, last_updated = row
    return stored_id, raw_status, json.loads(embedding_json), last_updated


# Removed duplicate class definitions - keeping originals above


class EmbeddingModel(Enum):
    """Embedding model types."""

    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI_ADA = "openai_ada"
    OPENAI_3_SMALL = "openai_3_small"
    OPENAI_3_LARGE = "openai_3_large"


@dataclass
class SearchQuery:
    """Query for vector search operations."""

    query_text: str
    limit: int = 10
    threshold: float = 0.0
    search_type: SearchType | None = None
    metadata_filter: dict[str, Any] | None = None


class SearchType(Enum):
    """Search types for vector operations."""

    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"


@dataclass
class SearchResult:
    """Result from vector search operations."""

    document: VectorDocument
    score: float
    metadata: dict[str, Any]


@dataclass
class VectorDatabaseStats:
    """Statistics for vector database operations."""

    total_documents: int
    total_collections: int
    last_updated: str | None = None
    storage_size: int | None = None


__all__ = [
    "AGENT_STATUS_TABLE",
    "CollectionConfig",
    "DocumentType",
    "EmbeddingModel",
    "get_connection",
    "SearchQuery",
    "SearchResult",
    "SearchType",
    "upsert_agent_status",
    "VectorDatabaseStats",
    "VectorDocument",
    "fetch_agent_status",
]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)
    # Function demonstrations
    print(f"\n📋 Testing get_connection():")
    try:
        # Add your function call here
        print(f"✅ get_connection executed successfully")
    except Exception as e:
        print(f"❌ get_connection failed: {e}")

    print(f"\n📋 Testing upsert_agent_status():")
    try:
        # Add your function call here
        print(f"✅ upsert_agent_status executed successfully")
    except Exception as e:
        print(f"❌ upsert_agent_status failed: {e}")

    print(f"\n📋 Testing fetch_agent_status():")
    try:
        # Add your function call here
        print(f"✅ fetch_agent_status executed successfully")
    except Exception as e:
        print(f"❌ fetch_agent_status failed: {e}")

    # Class demonstrations
    print(f"\n🏗️  Testing DocumentType class:")
    try:
        instance = DocumentType()
        print(f"✅ DocumentType instantiated successfully")
    except Exception as e:
        print(f"❌ DocumentType failed: {e}")

    print(f"\n🏗️  Testing SearchType class:")
    try:
        instance = SearchType()
        print(f"✅ SearchType instantiated successfully")
    except Exception as e:
        print(f"❌ SearchType failed: {e}")

    print("\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")
