#!/usr/bin/env python3
"""
Vector Database Models - Agent Cellphone V2
==========================================

Data models for vector database operations including documents, searches, and configurations.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import uuid


class DocumentType(Enum):
    """Types of documents that can be stored in the vector database."""

    MESSAGE = "message"
    DEVLOG = "devlog"
    CONTRACT = "contract"
    STATUS = "status"
    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIG = "config"
    CODE_PATTERN = "code_pattern"


class SearchType(Enum):
    """Types of search operations."""

    SIMILARITY = "similarity"
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    MAX_MARGINAL_RELEVANCE = "mmr"
    FILTERED = "filtered"


class EmbeddingModel(Enum):
    """Supported embedding models."""

    SENTENCE_TRANSFORMERS = "sentence-transformers"
    OPENAI = "openai"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "text-embedding-3-small"
    OPENAI_3_LARGE = "text-embedding-3-large"
    HUGGINGFACE = "huggingface"


@dataclass
class VectorDocument:
    """Document model for vector database storage."""

    content: str
    document_type: DocumentType
    id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    timestamp: datetime = field(
        default_factory=datetime.now
    )  # Alias for created_at for backward compatibility
    source: Optional[str] = None
    agent_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    source_file: Optional[str] = None  # For file-based documents

    def __post_init__(self):
        """Initialize default values after object creation."""
        if not self.id:
            self.id = f"doc_{self.created_at.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VectorDocument":
        """Create VectorDocument from dictionary."""
        return cls(
            id=data.get("id", ""),
            content=data["content"],
            document_type=DocumentType(data["document_type"]),
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if get_unified_validator().validate_type(data.get("created_at"), str)
                else data.get("created_at", datetime.now())
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if get_unified_validator().validate_type(data.get("updated_at"), str)
                else data.get("updated_at", datetime.now())
            ),
            timestamp=(
                datetime.fromisoformat(data["timestamp"])
                if get_unified_validator().validate_type(data.get("timestamp"), str)
                else data.get("timestamp", datetime.now())
            ),
            source=data.get("source"),
            agent_id=data.get("agent_id"),
            tags=data.get("tags", []),
            source_file=data.get("source_file"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert VectorDocument to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "document_type": self.document_type.value,
            "metadata": self.metadata,
            "embedding": self.embedding,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source": self.source,
            "agent_id": self.agent_id,
            "tags": self.tags,
            "source_file": self.source_file,
        }


@dataclass
class SearchQuery:
    """Search query model for vector database operations."""

    query_text: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    threshold: float = 0.7
    filters: Dict[str, Any] = field(default_factory=dict)
    document_types: List[DocumentType] = field(default_factory=list)
    agent_ids: List[str] = field(default_factory=list)
    agent_id: Optional[str] = None  # Single agent filter for backward compatibility
    document_type: Optional[DocumentType] = (
        None  # Single document type filter for backward compatibility
    )
    tags: List[str] = field(default_factory=list)
    date_range: Optional[Dict[str, datetime]] = None
    similarity_threshold: float = 0.7  # Alias for threshold for backward compatibility

    def to_dict(self) -> Dict[str, Any]:
        """Convert SearchQuery to dictionary."""
        return {
            "query_text": self.query_text,
            "search_type": self.search_type.value,
            "limit": self.limit,
            "threshold": self.threshold,
            "filters": self.filters,
            "document_types": [dt.value for dt in self.document_types],
            "agent_ids": self.agent_ids,
            "agent_id": self.agent_id,
            "document_type": self.document_type.value if self.document_type else None,
            "tags": self.tags,
            "date_range": (
                {
                    k: v.isoformat() if v else None
                    for k, v in (self.date_range or {}).items()
                }
                if self.date_range
                else None
            ),
            "similarity_threshold": self.similarity_threshold,
        }


@dataclass
class SearchResult:
    """Search result model for vector database queries."""

    document: VectorDocument
    similarity_score: float
    rank: int
    matched_content: Optional[str] = None
    highlights: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert SearchResult to dictionary."""
        return {
            "document": self.document.to_dict(),
            "similarity_score": self.similarity_score,
            "rank": self.rank,
            "matched_content": self.matched_content,
            "highlights": self.highlights,
        }


@dataclass
class CollectionConfig:
    """Configuration for a vector database collection."""

    name: str
    description: str = ""
    embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS
    metadata: Dict[str, Any] = field(default_factory=dict)
    similarity_threshold: float = 0.7
    max_results: int = 50
    distance_metric: str = "cosine"  # Distance metric for similarity search

    def to_dict(self) -> Dict[str, Any]:
        """Convert CollectionConfig to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "embedding_model": self.embedding_model.value,
            "metadata": self.metadata,
            "similarity_threshold": self.similarity_threshold,
            "max_results": self.max_results,
            "distance_metric": self.distance_metric,
        }


@dataclass
class VectorDatabaseConfig:
    """Configuration model for vector database operations."""

    collection_name: str = "agent_documents"
    default_collection: str = "agent_documents"  # Alias for backward compatibility
    embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS
    embedding_model_name: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    persist_directory: str = "vector_db"
    similarity_threshold: float = 0.7
    max_results: int = 50
    auto_index: bool = True
    batch_size: int = 100

    # OpenAI specific settings
    openai_api_key: Optional[str] = None
    openai_model: str = "text-embedding-ada-002"

    # ChromaDB specific settings
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_ssl: bool = False


@dataclass
class IndexingStats:
    """Statistics for indexing operations."""

    total_documents: int = 0
    indexed_documents: int = 0
    failed_documents: int = 0
    processing_time: float = 0.0
    average_embedding_time: float = 0.0
    collection_size: int = 0
    last_indexed: Optional[datetime] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate of indexing."""
        if self.total_documents == 0:
            return 0.0
        return self.indexed_documents / self.total_documents


@dataclass
class VectorDatabaseStats:
    """Statistics for vector database operations."""

    total_collections: int = 0
    total_documents: int = 0
    total_embeddings: int = 0
    storage_size: int = 0
    last_updated: Optional[datetime] = field(default_factory=datetime.now)
    indexing_stats: IndexingStats = field(default_factory=IndexingStats)
    collections: List[str] = field(default_factory=list)  # List of collection names

    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary for serialization."""
        return {
            "total_collections": self.total_collections,
            "total_documents": self.total_documents,
            "total_embeddings": self.total_embeddings,
            "storage_size": self.storage_size,
            "last_updated": (
                self.last_updated.isoformat() if self.last_updated else None
            ),
            "collections": {
                name: count
                for name, count in zip(
                    self.collections,
                    [self.total_documents // max(1, len(self.collections))]
                    * len(self.collections),
                )
            },
            "indexing_stats": {
                "total_documents": self.indexing_stats.total_documents,
                "indexed_documents": self.indexing_stats.indexed_documents,
                "failed_documents": self.indexing_stats.failed_documents,
                "success_rate": self.indexing_stats.success_rate,
                "processing_time": self.indexing_stats.processing_time,
                "last_indexed": (
                    self.indexing_stats.last_indexed.isoformat()
                    if self.indexing_stats.last_indexed
                    else None
                ),
            },
        }


@dataclass
class EmbeddingRequest:
    """Request for generating embeddings."""

    texts: List[str]
    model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResponse:
    """Response containing generated embeddings."""

    embeddings: List[List[float]]
    model: EmbeddingModel
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

