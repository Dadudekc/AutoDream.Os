#!/usr/bin/env python3
"""
Vector Database Orchestrator
============================

Orchestrates vector database operations and provides service interface.
V2 Compliance: < 300 lines, single responsibility.

Author: V2 Implementation Team
License: MIT
"""

import logging
from typing import Any

from .vector_database_engine import VectorDatabaseEngine
from .vector_database_models import (
    CollectionConfig,
    DocumentType,
    SearchQuery,
    SearchResult,
    VectorDatabaseConfig,
    VectorDatabaseResult,
    VectorDatabaseStats,
    VectorDocument,
)


class VectorDatabaseService:
    """Service interface for vector database operations."""

    def __init__(self, config: VectorDatabaseConfig | None = None):
        """Initialize vector database service."""
        self.logger = logging.getLogger(__name__)
        self.engine = VectorDatabaseEngine(config)
        self.config = config or VectorDatabaseConfig()
        self.logger.info("VectorDatabaseService initialized")

    def add_document(
        self, document: VectorDocument, collection_name: str = "default"
    ) -> VectorDatabaseResult:
        """Add a document to the vector database."""
        return self.engine.add_document(document, collection_name)

    def search_documents(
        self,
        query: str,
        collection_name: str = "default",
        limit: int = 10,
        document_types: list[DocumentType] | None = None,
    ) -> list[SearchResult]:
        """Search documents in the vector database."""
        search_query = SearchQuery(
            query=query, collection_name=collection_name, limit=limit, document_types=document_types
        )
        return self.engine.search_documents(search_query)

    def get_document(
        self, document_id: str, collection_name: str = "default"
    ) -> VectorDocument | None:
        """Retrieve a document by ID."""
        return self.engine.get_document(document_id, collection_name)

    def delete_document(
        self, document_id: str, collection_name: str = "default"
    ) -> VectorDatabaseResult:
        """Delete a document by ID."""
        return self.engine.delete_document(document_id, collection_name)

    def create_collection(self, config: CollectionConfig) -> VectorDatabaseResult:
        """Create a new collection."""
        return self.engine.create_collection(config)

    def get_stats(self) -> VectorDatabaseStats:
        """Get database statistics."""
        return self.engine.get_stats()

    def get_status(self) -> dict[str, Any]:
        """Get service status."""
        return {
            "service": "vector_database",
            "engine_status": self.engine.get_status(),
            "config": {
                "max_collections": self.config.max_collections,
                "max_documents_per_collection": self.config.max_documents_per_collection,
                "enable_persistence": self.config.enable_persistence,
            },
        }


# Global service instance
_service_instance: VectorDatabaseService | None = None


def get_vector_database_service() -> VectorDatabaseService:
    """Get the global vector database service instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = VectorDatabaseService()
    return _service_instance


def add_document_to_vector_db(
    document: VectorDocument, collection_name: str = "default"
) -> VectorDatabaseResult:
    """Add a document to the vector database."""
    service = get_vector_database_service()
    return service.add_document(document, collection_name)


def search_vector_database(
    query: str,
    collection_name: str = "default",
    limit: int = 10,
    document_types: list[DocumentType] | None = None,
) -> list[SearchResult]:
    """Search the vector database."""
    service = get_vector_database_service()
    return service.search_documents(query, collection_name, limit, document_types)


def get_vector_database_stats() -> VectorDatabaseStats:
    """Get vector database statistics."""
    service = get_vector_database_service()
    return service.get_stats()


__all__ = [
    "VectorDatabaseService",
    "get_vector_database_service",
    "add_document_to_vector_db",
    "search_vector_database",
    "get_vector_database_stats",
]
