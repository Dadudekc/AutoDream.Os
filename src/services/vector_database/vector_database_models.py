import logging

logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Vector Database Models
======================

Data models for vector database operations.
V2 Compliance: < 200 lines, single responsibility.

Author: V2 Implementation Team
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DocumentType(Enum):
    """Types of documents stored in vector database."""

    AGENT_WORK = "agent_work"
    MESSAGE = "message"
    TASK = "task"
    STATUS = "status"
    RECOMMENDATION = "recommendation"
    CONFIG = "config"
    LOG = "log"


@dataclass
class VectorDocument:

EXAMPLE USAGE:
==============

# Import the service
from src.services.vector_database.vector_database_models import Vector_Database_ModelsService

# Initialize service
service = Vector_Database_ModelsService()

# Basic service operation
response = service.handle_request(request_data)
logger.info(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Vector_Database_ModelsService)

# Execute service method
result = service.execute_operation(input_data, context)
logger.info(f"Operation result: {result}")

    """Represents a document stored in the vector database."""

    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    document_type: DocumentType = DocumentType.AGENT_WORK
    embedding: list[float] | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def __post_init__(self):
        """Validate and set defaults."""
        if not self.id:
            raise ValueError("Document ID cannot be empty")
        if not self.content:
            raise ValueError("Document content cannot be empty")
        self.updated_at = datetime.now()


@dataclass
class CollectionConfig:
    """Configuration for a document collection."""

    name: str
    description: str | None = None
    max_documents: int | None = None
    document_types: list[DocumentType] = field(default_factory=lambda: [DocumentType.AGENT_WORK])
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class VectorDatabaseConfig:
    """Configuration for vector database engine."""

    max_collections: int = 100
    max_documents_per_collection: int = 10000
    enable_persistence: bool = False
    persistence_path: str | None = None
    default_collection: str = "default"
    similarity_threshold: float = 0.7
    max_search_results: int = 50


@dataclass
class SearchQuery:
    """Represents a search query against the vector database."""

    query: str
    collection_name: str = "default"
    limit: int = 10
    similarity_threshold: float = 0.7
    document_types: list[DocumentType] | None = None
    metadata_filters: dict[str, Any] | None = None


@dataclass
class SearchResult:
    """Result of a vector database search."""

    document: VectorDocument
    similarity_score: float
    rank: int
    collection_name: str
    highlights: list[str] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)


@dataclass
class VectorDatabaseResult:
    """Result of a vector database operation."""

    success: bool
    message: str = ""
    data: Any | None = None
    documents_affected: int = 0
    execution_time: float = 0.0
    error_details: str | None = None


@dataclass
class VectorDatabaseStats:
    """Statistics for vector database operations."""

    total_collections: int = 0
    total_documents: int = 0
    total_queries: int = 0
    average_similarity: float = 0.0
    cache_hit_rate: float = 0.0
    uptime_seconds: float = 0.0
    last_backup: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "total_collections": self.total_collections,
            "total_documents": self.total_documents,
            "total_queries": self.total_queries,
            "average_similarity": self.average_similarity,
            "cache_hit_rate": self.cache_hit_rate,
            "uptime_seconds": self.uptime_seconds,
            "last_backup": self.last_backup.isoformat() if self.last_backup else None,
        }


__all__ = [
    "DocumentType",
    "VectorDocument",
    "CollectionConfig",
    "VectorDatabaseConfig",
    "SearchQuery",
    "SearchResult",
    "VectorDatabaseResult",
    "VectorDatabaseStats",
]
