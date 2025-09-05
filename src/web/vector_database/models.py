"""
Vector Database Models
=====================

Data models and validation for vector database operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class SearchRequest:
    """Search request model."""
    query: str
    collection: str = 'all'
    search_type: str = 'semantic'
    limit: int = 25


@dataclass
class DocumentRequest:
    """Document request model."""
    title: str
    content: str
    collection: str
    tags: Optional[List[str]] = None


@dataclass
class PaginationRequest:
    """Pagination request model."""
    page: int = 1
    per_page: int = 25
    collection: str = 'all'
    sort_by: str = 'updated_at'
    sort_order: str = 'desc'


@dataclass
class SearchResult:
    """Search result model."""
    id: str
    title: str
    content: str
    collection: str
    relevance: float
    tags: List[str]
    created_at: str
    updated_at: str
    size: str


@dataclass
class Document:
    """Document model."""
    id: str
    title: str
    content: str
    collection: str
    tags: List[str]
    created_at: str
    updated_at: str
    size: str


@dataclass
class Collection:
    """Collection model."""
    id: str
    name: str
    description: str
    document_count: int
    last_updated: str


@dataclass
class AnalyticsData:
    """Analytics data model."""
    total_documents: int
    search_queries: int
    average_response_time: float
    success_rate: float
    top_searches: List[Dict[str, Any]]
    document_distribution: Dict[str, int]
    search_trends: List[Dict[str, Any]]


@dataclass
class ExportRequest:
    """Export request model."""
    format: str = 'json'
    collection: str = 'all'


@dataclass
class ExportData:
    """Export data model."""
    format: str
    collection: str
    data: str
    filename: str
    size: str


class VectorDatabaseModels:
    """Vector database models and validation."""
    
    @staticmethod
    def validate_search_request(data: Dict[str, Any]) -> Optional[str]:
        """Validate search request data."""
        if not data.get('query', '').strip():
            return 'Query is required'
        return None
    
    @staticmethod
    def validate_document_request(data: Dict[str, Any]) -> Optional[str]:
        """Validate document request data."""
        required_fields = ['title', 'content', 'collection']
        for field in required_fields:
            if not data.get(field):
                return f'{field} is required'
        return None
    
    @staticmethod
    def create_search_request(data: Dict[str, Any]) -> SearchRequest:
        """Create search request from data."""
        return SearchRequest(
            query=data.get('query', '').strip(),
            collection=data.get('collection', 'all'),
            search_type=data.get('search_type', 'semantic'),
            limit=int(data.get('limit', 25))
        )
    
    @staticmethod
    def create_document_request(data: Dict[str, Any]) -> DocumentRequest:
        """Create document request from data."""
        tags = data.get('tags', '')
        return DocumentRequest(
            title=data['title'],
            content=data['content'],
            collection=data['collection'],
            tags=tags.split(',') if tags else []
        )
    
    @staticmethod
    def create_pagination_request(args: Dict[str, Any]) -> PaginationRequest:
        """Create pagination request from args."""
        return PaginationRequest(
            page=int(args.get('page', 1)),
            per_page=int(args.get('per_page', 25)),
            collection=args.get('collection', 'all'),
            sort_by=args.get('sort_by', 'updated_at'),
            sort_order=args.get('sort_order', 'desc')
        )
    
    @staticmethod
    def create_export_request(data: Dict[str, Any]) -> ExportRequest:
        """Create export request from data."""
        return ExportRequest(
            format=data.get('format', 'json'),
            collection=data.get('collection', 'all')
        )
