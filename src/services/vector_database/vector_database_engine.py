#!/usr/bin/env python3
"""
Vector Database Engine (SSOT)
============================

Single source of truth for vector database operations.
Provides a simple in-memory implementation used by coordinators and services.
Other modules must import this engine from
``src/services/vector_database/vector_database_engine.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .vector_database_models import (
    CollectionConfig,
    SearchQuery,
    SearchResult,
    VectorDatabaseConfig,
    VectorDatabaseResult,
    VectorDatabaseStats,
    VectorDocument,
)
from ...core.unified_logging_system import get_logger


@dataclass
class _Collection:
    """Internal representation of a document collection."""

    documents: Dict[str, VectorDocument]


class VectorDatabaseEngine:
    """In-memory engine for vector database operations.

    This module is the authoritative implementation and should be treated as SSOT.
    """

    def __init__(self, config: Optional[VectorDatabaseConfig] = None):
        """Initialize engine with configuration."""
        self.logger = get_logger(__name__)
        self.config = config or VectorDatabaseConfig()
        self.collections: Dict[str, _Collection] = {}
        self.stats = VectorDatabaseStats()
        self.logger.info("VectorDatabaseEngine initialized")

    # ------------------------------------------------------------------
    # Core collection operations
    # ------------------------------------------------------------------

    def create_collection(self, config: CollectionConfig) -> VectorDatabaseResult:
        """Create a new collection."""
        if config.name in self.collections:
            msg = f"Collection {config.name} already exists"
            self.logger.warning(msg)
            return VectorDatabaseResult(False, msg)
        self.collections[config.name] = _Collection(documents={})
        self.stats.total_collections = len(self.collections)
        self.logger.info("Created collection %s", config.name)
        return VectorDatabaseResult(True, f"Collection {config.name} created")

    def get_collection(self, name: str) -> Optional[Dict[str, VectorDocument]]:
        """Get collection by name."""
        collection = self.collections.get(name)
        return collection.documents if collection else None

    def add_document(
        self, document: VectorDocument, collection_name: str = "default"
    ) -> VectorDatabaseResult:
        """Add a document to a collection."""
        collection = self.collections.setdefault(collection_name, _Collection(documents={}))
        collection.documents[document.id] = document
        self.stats.total_documents = sum(len(c.documents) for c in self.collections.values())
        self.logger.debug("Added document %s to %s", document.id, collection_name)
        return VectorDatabaseResult(True, "Document added", data=document.id, documents_affected=1)

    def search_documents(self, query: SearchQuery) -> List[SearchResult]:
        """Search documents using simple substring matching."""
        collection = self.collections.get(query.collection_name, _Collection(documents={}))
        results: List[SearchResult] = []
        rank = 1
        for doc in collection.documents.values():
            if query.query.lower() in doc.content.lower():
                results.append(
                    SearchResult(
                        document=doc,
                        similarity_score=1.0,
                        rank=rank,
                        collection_name=query.collection_name,
                    )
                )
                rank += 1
        self.stats.total_queries += 1
        if results:
            new_avg = (
                self.stats.average_similarity * (self.stats.total_queries - 1) + 1.0
            ) / self.stats.total_queries
            self.stats.average_similarity = new_avg
        self.logger.debug(
            "Search in %s for '%s' returned %d results",
            query.collection_name,
            query.query,
            len(results),
        )
        return results[: query.limit]

    def get_document(
        self,
        document_id: str,
        collection_name: str = "default",
    ) -> Optional[VectorDocument]:
        """Retrieve a document by ID."""
        collection = self.collections.get(collection_name, _Collection(documents={}))
        return collection.documents.get(document_id)

    def delete_document(
        self,
        document_id: str,
        collection_name: str = "default",
    ) -> VectorDatabaseResult:
        """Delete a document by ID."""
        collection = self.collections.get(collection_name)
        if not collection or document_id not in collection.documents:
            msg = f"Document {document_id} not found in {collection_name}"
            self.logger.warning(msg)
            return VectorDatabaseResult(False, msg)
        del collection.documents[document_id]
        self.stats.total_documents = sum(len(c.documents) for c in self.collections.values())
        self.logger.debug("Deleted document %s from %s", document_id, collection_name)
        return VectorDatabaseResult(True, "Document deleted", documents_affected=1)

    def clear_collection(self, collection_name: str = "default") -> VectorDatabaseResult:
        """Remove all documents from a collection."""
        collection = self.collections.get(collection_name)
        if not collection:
            msg = f"Collection {collection_name} does not exist"
            self.logger.warning(msg)
            return VectorDatabaseResult(False, msg)
        removed = len(collection.documents)
        collection.documents.clear()
        self.stats.total_documents = sum(len(c.documents) for c in self.collections.values())
        self.logger.info("Cleared %d documents from %s", removed, collection_name)
        return VectorDatabaseResult(True, "Collection cleared", documents_affected=removed)

    def get_stats(self) -> VectorDatabaseStats:
        """Return current statistics."""
        return self.stats

    # ------------------------------------------------------------------
    # Integration engine compatibility
    # ------------------------------------------------------------------

    def get_performance_report(self) -> Dict[str, Any]:
        """Return performance metrics for integration coordinators."""
        return self.stats.to_dict()

    def optimize(self, **kwargs: Any) -> bool:
        """Placeholder optimization hook."""
        self.logger.info("Optimization called with %s", kwargs)
        return True

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status."""
        return {
            "engine_type": "vector_database",
            "collections": len(self.collections),
            "total_documents": self.stats.total_documents,
        }


__all__ = ["VectorDatabaseEngine"]
