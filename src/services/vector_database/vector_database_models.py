#!/usr/bin/env python3
"""
Vector Database Models - V2 Compliance Module
============================================

Data models and enums for vector database operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class DocumentType(Enum):
    """Types of documents in vector database."""
    TEXT = "text"
    CODE = "code"
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"
    LOG = "log"


class EmbeddingModel(Enum):
    """Embedding models for vector generation."""
    DEFAULT = "default"
    OPENAI = "openai"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    CUSTOM = "custom"


@dataclass
class VectorDatabaseConfig:
    """Configuration for vector database operations."""
    
    database_path: Union[str, Path] = "vector_db"
    default_collection: str = "default"
    embedding_model: EmbeddingModel = EmbeddingModel.DEFAULT
    embedding_dimension: int = 384
    similarity_threshold: float = 0.7
    max_results: int = 10
    enable_persistence: bool = True
    enable_metadata: bool = True
    chunk_size: int = 1000
    chunk_overlap: int = 200


@dataclass
class VectorDocument:
    """Vector document representation."""
    
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None
    document_type: DocumentType = DocumentType.TEXT
    agent_id: Optional[str] = None
    source_file: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.tags is None:
            self.tags = []


@dataclass
class SearchQuery:
    """Search query for vector database."""
    
    query: str
    collection_name: str = "default"
    limit: int = 10
    similarity_threshold: float = 0.7
    include_metadata: bool = True
    filter_metadata: Optional[Dict[str, Any]] = None


@dataclass
class SearchResult:
    """Search result from vector database."""
    
    document: VectorDocument
    similarity_score: float
    rank: int
    collection_name: str = "default"


@dataclass
class VectorDatabaseStats:
    """Statistics for vector database operations."""
    
    total_documents: int = 0
    total_collections: int = 0
    total_queries: int = 0
    average_similarity: float = 0.0
    cache_hit_rate: float = 0.0
    last_updated: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "total_documents": self.total_documents,
            "total_collections": self.total_collections,
            "total_queries": self.total_queries,
            "average_similarity": self.average_similarity,
            "cache_hit_rate": self.cache_hit_rate,
            "last_updated": self.last_updated
        }


@dataclass
class VectorDatabaseResult:
    """Result of vector database operation."""
    
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    documents_affected: int = 0


@dataclass
class CollectionConfig:
    """Configuration for vector database collection."""
    
    name: str
    description: str = ""
    embedding_model: EmbeddingModel = EmbeddingModel.DEFAULT
    metadata_schema: Optional[Dict[str, Any]] = None
    similarity_threshold: float = 0.7
    max_documents: int = 10000
    enable_indexing: bool = True
