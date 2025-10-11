"""
Vector Database Models
======================

Data models for vector database operations.
V2 Compliance: < 200 lines, single responsibility.

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Created: 2025-10-11 (fixing missing import)
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalyticsData:
    """Analytics data model for vector database reporting."""

    total_documents: int
    search_queries: int
    average_response_time: float
    success_rate: float
    top_searches: list[dict[str, Any]] = field(default_factory=list)
    document_distribution: dict[str, int] = field(default_factory=dict)
    search_trends: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Collection:
    """Vector database collection model."""

    id: str
    name: str
    count: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExportData:
    """Export data model for vector database exports."""

    collection: str
    documents: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""


@dataclass
class ExportRequest:
    """Export request model."""

    collection: str
    format: str = "json"
    include_metadata: bool = True
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchRequest:
    """Search request model."""

    query: str
    collection: str = "default"
    limit: int = 10
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Search result model."""

    id: str
    score: float
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Document model for vector database."""

    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)


@dataclass
class DocumentRequest:
    """Document request model."""

    collection: str
    document_id: str
    include_embedding: bool = False


@dataclass
class PaginationRequest:
    """Pagination request model."""

    page: int = 1
    per_page: int = 25
    collection: str = "default"
