#!/usr/bin/env python3
"""
Vector Database Orchestrator - V2 Compliance Module
==================================================

Main coordination logic for vector database operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import List, Dict, Any, Optional, Union
from pathlib import Path

from .vector_database_models import (
    VectorDatabaseConfig,
    VectorDocument,
    SearchQuery,
    SearchResult,
    VectorDatabaseStats,
    VectorDatabaseResult,
    CollectionConfig,
    DocumentType,
    EmbeddingModel,
)
from .vector_database_engine import VectorDatabaseEngine


class VectorDatabaseService:
    """Main orchestrator for vector database operations."""

    def __init__(self, config: VectorDatabaseConfig = None):
        """Initialize vector database service."""
        self.config = config or VectorDatabaseConfig()
        self.engine = VectorDatabaseEngine(self.config)

    def create_collection(self, config: CollectionConfig) -> VectorDatabaseResult:
        """Create a new collection."""
        return self.engine.create_collection(config)

    def get_collection(self, name: str) -> Optional[Any]:
        """Get collection by name."""
        return self.engine.get_collection(name)

    def add_document(self, document: VectorDocument, collection_name: str = "default") -> VectorDatabaseResult:
        """Add document to collection."""
        return self.engine.add_document(document, collection_name)

    def search_documents(self, query: SearchQuery) -> List[SearchResult]:
        """Search documents in collection."""
        return self.engine.search_documents(query)

    def get_document(self, document_id: str, collection_name: str = "default") -> Optional[VectorDocument]:
        """Get document by ID."""
        return self.engine.get_document(document_id, collection_name)

    def delete_document(self, document_id: str, collection_name: str = "default") -> VectorDatabaseResult:
        """Delete document by ID."""
        return self.engine.delete_document(document_id, collection_name)

    def clear_collection(self, collection_name: str = "default") -> VectorDatabaseResult:
        """Clear all documents from collection."""
        return self.engine.clear_collection(collection_name)

    def get_stats(self) -> VectorDatabaseStats:
        """Get database statistics."""
        return self.engine.get_stats()

    # ================================
    # CONVENIENCE METHODS
    # ================================
    
    def add_text_document(
        self, 
        content: str, 
        document_id: str, 
        collection_name: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> VectorDatabaseResult:
        """Add text document with convenience method."""
        document = VectorDocument(
            id=document_id,
            content=content,
            document_type=DocumentType.TEXT,
            metadata=metadata,
            tags=tags
        )
        return self.add_document(document, collection_name)
    
    def add_code_document(
        self, 
        content: str, 
        document_id: str, 
        collection_name: str = "default",
        source_file: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> VectorDatabaseResult:
        """Add code document with convenience method."""
        document = VectorDocument(
            id=document_id,
            content=content,
            document_type=DocumentType.CODE,
            source_file=source_file,
            metadata=metadata,
            tags=tags
        )
        return self.add_document(document, collection_name)
    
    def search_by_content(
        self, 
        query_text: str, 
        collection_name: str = "default",
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[SearchResult]:
        """Search by content with convenience method."""
        query = SearchQuery(
            query=query_text,
            collection_name=collection_name,
            limit=limit,
            similarity_threshold=similarity_threshold
        )
        return self.search_documents(query)
    
    def search_by_agent(
        self, 
        agent_id: str, 
        collection_name: str = "default",
        limit: int = 10
    ) -> List[SearchResult]:
        """Search documents by agent ID."""
        query = SearchQuery(
            query="",  # Empty query for metadata filtering
            collection_name=collection_name,
            limit=limit,
            filter_metadata={"agent_id": agent_id}
        )
        return self.search_documents(query)
    
    def search_by_tags(
        self, 
        tags: List[str], 
        collection_name: str = "default",
        limit: int = 10
    ) -> List[SearchResult]:
        """Search documents by tags."""
        # This would require more complex filtering in a real implementation
        # For now, we'll use a simple text search
        query_text = " ".join(tags)
        return self.search_by_content(query_text, collection_name, limit)


# ================================
# GLOBAL INSTANCE
# ================================

_global_vector_service = None

def get_vector_database_service() -> VectorDatabaseService:
    """Get global vector database service instance."""
    global _global_vector_service
    
    if _global_vector_service is None:
        _global_vector_service = VectorDatabaseService()
    
    return _global_vector_service


# ================================
# CONVENIENCE FUNCTIONS
# ================================

def add_document_to_vector_db(
    content: str, 
    document_id: str, 
    collection_name: str = "default",
    document_type: DocumentType = DocumentType.TEXT,
    metadata: Optional[Dict[str, Any]] = None
) -> VectorDatabaseResult:
    """Convenience function to add document to vector database."""
    service = get_vector_database_service()
    document = VectorDocument(
        id=document_id,
        content=content,
        document_type=document_type,
        metadata=metadata
    )
    return service.add_document(document, collection_name)

def search_vector_database(
    query_text: str, 
    collection_name: str = "default",
    limit: int = 10
) -> List[SearchResult]:
    """Convenience function to search vector database."""
    service = get_vector_database_service()
    return service.search_by_content(query_text, collection_name, limit)

def get_vector_database_stats() -> VectorDatabaseStats:
    """Convenience function to get vector database statistics."""
    service = get_vector_database_service()
    return service.get_stats()
