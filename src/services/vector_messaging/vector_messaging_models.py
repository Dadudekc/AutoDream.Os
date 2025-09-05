#!/usr/bin/env python3
"""
Vector Messaging Models - V2 Compliant
======================================

Configuration and validation models for vector messaging integration.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant vector messaging data models
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VectorDatabaseConfig:
    """Configuration for vector database integration."""
    persist_directory: str = "data/vector_db"
    default_collection: str = "messages"
    default_embedding_model: str = "sentence-transformers"
    max_document_size: int = 100000  # Max characters per document
    similarity_threshold: float = 0.3
    search_limit: int = 100


class VectorDatabaseValidator:
    """Validator for vector database operations."""
    
    def __init__(self, config: VectorDatabaseConfig):
        """Initialize validator with configuration."""
        self.config = config
    
    def validate_document_content(self, content: str) -> bool:
        """
        Validate document content.
        
        Args:
            content: Content to validate
            
        Returns:
            bool: True if valid
        """
        if not content or not isinstance(content, str):
            return False
        
        content = content.strip()
        if len(content) == 0:
            return False
        
        if len(content) > self.config.max_document_size:
            return False
        
        return True
    
    def validate_search_query(self, query: str, limit: int) -> bool:
        """
        Validate search query parameters.
        
        Args:
            query: Search query text
            limit: Result limit
            
        Returns:
            bool: True if valid
        """
        if not query or not isinstance(query, str):
            return False
        
        if len(query.strip()) == 0:
            return False
        
        if limit <= 0 or limit > self.config.search_limit:
            return False
        
        return True
    
    def validate_collection_name(self, collection_name: str) -> bool:
        """
        Validate collection name.
        
        Args:
            collection_name: Name to validate
            
        Returns:
            bool: True if valid
        """
        if not collection_name or not isinstance(collection_name, str):
            return False
        
        # Basic validation - alphanumeric and underscores only
        if not collection_name.replace('_', '').replace('-', '').isalnum():
            return False
        
        return True
    
    def validate_agent_id(self, agent_id: str) -> bool:
        """
        Validate agent ID format.
        
        Args:
            agent_id: Agent ID to validate
            
        Returns:
            bool: True if valid
        """
        if not agent_id or not isinstance(agent_id, str):
            return False
        
        # Expected format: Agent-1, Agent-2, etc.
        if not agent_id.startswith('Agent-'):
            return False
        
        try:
            int(agent_id.split('-')[1])
            return True
        except (IndexError, ValueError):
            return False


@dataclass
class IndexingResult:
    """Result of document indexing operation."""
    success: bool
    document_id: str
    error_message: Optional[str] = None
    collection_name: Optional[str] = None
    document_size: Optional[int] = None


@dataclass
class SearchResultSummary:
    """Summary of search operation results."""
    total_results: int
    query_text: str
    collection_name: str
    execution_time_ms: float
    agent_filter: Optional[str] = None
    document_type_filter: Optional[str] = None


@dataclass
class BatchIndexingResult:
    """Result of batch indexing operation."""
    total_processed: int
    successful_indexes: int
    failed_indexes: int
    errors: Dict[str, str]  # document_id -> error_message
    processing_time_ms: float


class VectorMessagingMetrics:
    """Metrics tracking for vector messaging operations."""
    
    def __init__(self):
        """Initialize metrics."""
        self.total_documents_indexed = 0
        self.total_searches_performed = 0
        self.total_errors = 0
        self.average_search_time_ms = 0.0
        self.average_indexing_time_ms = 0.0
    
    def record_indexing(self, success: bool, time_ms: float):
        """Record indexing operation."""
        if success:
            self.total_documents_indexed += 1
        else:
            self.total_errors += 1
        
        # Update average indexing time
        total_ops = self.total_documents_indexed + self.total_errors
        if total_ops > 0:
            self.average_indexing_time_ms = (
                (self.average_indexing_time_ms * (total_ops - 1) + time_ms) / total_ops
            )
    
    def record_search(self, time_ms: float):
        """Record search operation."""
        self.total_searches_performed += 1
        
        # Update average search time
        if self.total_searches_performed > 0:
            self.average_search_time_ms = (
                (self.average_search_time_ms * (self.total_searches_performed - 1) + time_ms) 
                / self.total_searches_performed
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_documents_indexed": self.total_documents_indexed,
            "total_searches_performed": self.total_searches_performed,
            "total_errors": self.total_errors,
            "average_search_time_ms": self.average_search_time_ms,
            "average_indexing_time_ms": self.average_indexing_time_ms
        }
