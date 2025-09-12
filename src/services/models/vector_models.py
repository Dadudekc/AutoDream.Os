"""
Vector Models - V2 Compliance Module
===================================

Data models for vector database operations.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class EmbeddingModel(Enum):
    """Supported embedding models."""

    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "openai-3-small"
    OPENAI_3_LARGE = "openai-3-large"


class DocumentType(Enum):

EXAMPLE USAGE:
==============

# Import the service
from src.services.models.vector_models import Vector_ModelsService

# Initialize service
service = Vector_ModelsService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Vector_ModelsService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

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


@dataclass
class VectorDocument:
    """Vector document representation."""

    id: str
    content: str
    embedding: list[float]
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VectorDocument":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            embedding=data["embedding"],
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class EmbeddingResult:
    """Result of embedding operation."""

    document_id: str
    embedding: list[float]
    model: EmbeddingModel
    tokens_used: int
    processing_time: float
    success: bool
    error_message: str | None = None


@dataclass
class SearchQuery:
    """Search query for vector database."""

    query_text: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    similarity_threshold: float = 0.0
    filters: dict[str, Any] | None = None


@dataclass
class SearchResult:
    """Result of vector database search."""

    document_id: str
    content: str
    similarity_score: float
    metadata: dict[str, Any]


@dataclass
class SimilaritySearchResult:
    """Result of similarity search."""

    query_embedding: list[float]
    results: list[dict[str, Any]]
    search_time: float
    total_candidates: int
