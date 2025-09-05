#!/usr/bin/env python3
"""
Vector Database Models - KISS Simplified
========================================

Simplified data models for vector database operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined vector models.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-7 - Web Development Specialist
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


class VectorDatabaseType(Enum):
    """Types of vector databases."""
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    SIMPLE = "simple"


@dataclass
class VectorDocument:
    """Simplified vector document model."""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    document_type: DocumentType = DocumentType.MESSAGE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    embedding: Optional[List[float]] = None
    vector_id: Optional[str] = None


@dataclass
class SearchQuery:
    """Simplified search query model."""
    query: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    filters: Dict[str, Any] = field(default_factory=dict)
    threshold: float = 0.0


@dataclass
class SearchResult:
    """Simplified search result model."""
    document: VectorDocument
    score: float
    distance: float = 0.0


@dataclass
class VectorDatabaseConfig:
    """Simplified vector database configuration."""
    db_type: VectorDatabaseType = VectorDatabaseType.CHROMA
    collection_name: str = "default"
    embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS
    persist_directory: str = "./vector_db"
    api_key: Optional[str] = None
    host: str = "localhost"
    port: int = 8000
    dimension: int = 384
    distance_metric: str = "cosine"


@dataclass
class VectorDatabaseMetrics:
    """Simplified vector database metrics."""
    total_documents: int = 0
    total_collections: int = 0
    total_searches: int = 0
    avg_search_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class CollectionInfo:
    """Simplified collection information."""
    name: str
    document_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingConfig:
    """Simplified embedding configuration."""
    model_name: str = "all-MiniLM-L6-v2"
    model_type: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS
    dimension: int = 384
    batch_size: int = 100
    max_length: int = 512


@dataclass
class VectorSearchConfig:
    """Simplified vector search configuration."""
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    threshold: float = 0.0
    filters: Dict[str, Any] = field(default_factory=dict)
    include_metadata: bool = True


@dataclass
class VectorDatabaseStatus:
    """Simplified vector database status."""
    is_connected: bool = False
    is_initialized: bool = False
    last_health_check: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None
    metrics: VectorDatabaseMetrics = field(default_factory=VectorDatabaseMetrics)


@dataclass
class DocumentBatch:
    """Simplified document batch for bulk operations."""
    documents: List[VectorDocument]
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"


@dataclass
class VectorDatabaseError:
    """Simplified vector database error."""
    error_code: str
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VectorDatabaseHealth:
    """Simplified vector database health check."""
    is_healthy: bool = False
    response_time: float = 0.0
    last_check: datetime = field(default_factory=datetime.now)
    issues: List[str] = field(default_factory=list)
    metrics: VectorDatabaseMetrics = field(default_factory=VectorDatabaseMetrics)


@dataclass
class VectorDatabaseBackup:
    """Simplified vector database backup."""
    backup_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    collection_name: str = "default"
    document_count: int = 0
    backup_path: str = ""
    status: str = "pending"


@dataclass
class VectorDatabaseRestore:
    """Simplified vector database restore."""
    restore_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    backup_id: str = ""
    collection_name: str = "default"
    status: str = "pending"


@dataclass
class VectorDatabaseMigration:
    """Simplified vector database migration."""
    migration_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    source_type: VectorDatabaseType = VectorDatabaseType.CHROMA
    target_type: VectorDatabaseType = VectorDatabaseType.CHROMA
    status: str = "pending"
    progress: float = 0.0


@dataclass
class VectorDatabaseSync:
    """Simplified vector database synchronization."""
    sync_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    source_collection: str = "default"
    target_collection: str = "default"
    status: str = "pending"
    last_sync: Optional[datetime] = None


@dataclass
class VectorDatabaseIndex:
    """Simplified vector database index."""
    index_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    collection_name: str = "default"
    index_type: str = "vector"
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)