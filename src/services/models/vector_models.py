"""
Vector Models - V2 Compliance Module
===================================

Data models for vector database operations.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from dataclasses import dataclass, field
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
    """Types of documents in the vector database."""
    TEXT = "text"
    CODE = "code"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    PDF = "pdf"
    IMAGE = "image"


class VectorDocumentType(Enum):
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


@dataclass
class CollectionConfig:
    """Configuration for vector collection."""
    
    name: str
    dimensions: int
    distance_metric: str = "cosine"
    index_type: str = "hnsw"
    max_elements: int = 1000000
    ef_construction: int = 200
    m: int = 16


def create_vector_document(content: str, doc_type: DocumentType = DocumentType.TEXT) -> VectorDocument:
    """Create a new vector document."""
    now = datetime.now()
    return VectorDocument(
        id=f"doc_{now.timestamp()}",
        content=content,
        embedding=[],
        metadata={},
        created_at=now,
        updated_at=now
    )


if __name__ == "__main__":
    # Example usage
    doc = create_vector_document("Test content", DocumentType.TEXT)
    print(f"Created document: {doc}")