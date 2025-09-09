"""
Vector Models - V2 Compliance Module
===================================

Data models for vector database operations.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EmbeddingModel(Enum):
    """Supported embedding models."""
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    OPENAI_ADA = "openai-ada-002"
    OPENAI_3_SMALL = "openai-3-small"
    OPENAI_3_LARGE = "openai-3-large"


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


@dataclass
class VectorDocument:
    """Vector document representation."""

    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorDocument':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            content=data['content'],
            embedding=data['embedding'],
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'content': self.content,
            'embedding': self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class EmbeddingResult:
    """Result of embedding operation."""

    document_id: str
    embedding: List[float]
    model: EmbeddingModel
    tokens_used: int
    processing_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class SearchQuery:
    """Search query for vector database."""
    
    query_text: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    similarity_threshold: float = 0.0
    filters: Optional[Dict[str, Any]] = None


@dataclass
class SearchResult:
    """Result of vector database search."""
    
    document_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]


@dataclass
class SimilaritySearchResult:
    """Result of similarity search."""

    query_embedding: List[float]
    results: List[Dict[str, Any]]
    search_time: float
    total_candidates: int
