"""
Vector Database Models
======================

Data models for vector database operations.
V2 Compliance: Simple data structures, type hints.

Author: Agent-1 - Integration Specialist
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class AnalyticsData:
    """Analytics data structure for vector database operations."""
    total_queries: int = 0
    avg_response_time: float = 0.0
    error_rate: float = 0.0
    time_range: str = "last_24h"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_queries": self.total_queries,
            "avg_response_time": self.avg_response_time,
            "error_rate": self.error_rate,
            "time_range": self.time_range
        }


@dataclass
class SearchResult:
    """Search result data structure."""
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "document_id": self.document_id,
            "content": self.content,
            "score": self.score,
            "metadata": self.metadata
        }


@dataclass
class CollectionInfo:
    """Collection information data structure."""
    name: str
    dimension: int
    document_count: int = 0
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "dimension": self.dimension,
            "document_count": self.document_count,
            "created_at": self.created_at
        }


@dataclass
class Collection:
    """Collection data structure."""
    name: str
    dimension: int
    document_count: int = 0
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "dimension": self.dimension,
            "document_count": self.document_count,
            "created_at": self.created_at
        }


@dataclass
class ExportRequest:
    """Export request data structure."""
    collection_name: str
    format: str = "json"
    include_vectors: bool = False
    filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "collection_name": self.collection_name,
            "format": self.format,
            "include_vectors": self.include_vectors,
            "filters": self.filters
        }


@dataclass
class ExportData:
    """Export data structure."""
    collection_name: str
    documents: List[Dict[str, Any]]
    exported_at: str
    format: str = "json"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "collection_name": self.collection_name,
            "documents": self.documents,
            "exported_at": self.exported_at,
            "format": self.format
        }


@dataclass
class Document:
    """Document data structure."""
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class DocumentRequest:
    """Document request data structure."""
    collection_name: str
    document_id: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "collection_name": self.collection_name,
            "document_id": self.document_id,
            "content": self.content,
            "metadata": self.metadata
        }


@dataclass
class PaginationRequest:
    """Pagination request data structure."""
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"
    filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "page": self.page,
            "page_size": self.page_size,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "filters": self.filters
        }


@dataclass
class APIResponse:
    """Standard API response structure."""
    success: bool
    data: Any = None
    message: str = ""
    error_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
            "error_code": self.error_code
        }
