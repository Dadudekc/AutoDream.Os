#!/usr/bin/env python3
"""
Search Query Engine - V2 Compliant
=================================

Handles all search operations for vector messaging integration.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant search functionality
"""

from typing import Optional, Dict, Any, List
import time
from ...core.unified_import_system import logging
from ..models.vector_models import SearchQuery, SearchType, SearchResult, DocumentType
from .vector_messaging_models import VectorDatabaseValidator, SearchResultSummary, VectorMessagingMetrics


class SearchQueryEngine:
    """Engine for performing search operations on vector database."""
    
    def __init__(self, vector_db_service, validator: VectorDatabaseValidator, 
                 default_collection: str, logger: logging.Logger = None):
        """Initialize search engine."""
        self.vector_db = vector_db_service
        self.validator = validator
        self.default_collection = default_collection
        self.logger = logger or logging.getLogger(__name__)
        self.metrics = VectorMessagingMetrics()
    
    def search_messages(self, query_text: str, agent_id: Optional[str] = None,
                       limit: int = 10, similarity_threshold: float = 0.0) -> List[SearchResult]:
        """
        Search for similar messages.

        Args:
            query_text: Search query
            agent_id: Filter by agent ID
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score

        Returns:
            List of search results
        """
        start_time = time.time()
        
        try:
            # Validate search parameters
            if not self.validator.validate_search_query(query_text, limit):
                self.logger.warning(f"Invalid search parameters: query='{query_text}', limit={limit}")
                return []

            # Create search query
            search_query = SearchQuery(
                query_text=query_text,
                search_type=SearchType.SIMILARITY,
                limit=limit,
                similarity_threshold=similarity_threshold,
                agent_id=agent_id,
                document_type=DocumentType.MESSAGE,
            )

            # Perform search
            results = self.vector_db.search(search_query, self.default_collection)
            
            # Record metrics
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)

            self.logger.info(f"✅ Found {len(results)} message results for query")
            return results

        except Exception as e:
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)
            self.logger.error(f"❌ Error searching messages: {e}")
            return []

    def search_devlogs(self, query_text: str, agent_id: Optional[str] = None,
                      category: Optional[str] = None, limit: int = 10, 
                      similarity_threshold: float = 0.0) -> List[SearchResult]:
        """
        Search for similar devlog entries.

        Args:
            query_text: Search query
            agent_id: Filter by agent ID
            category: Filter by category
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score

        Returns:
            List of search results
        """
        start_time = time.time()
        
        try:
            # Validate search parameters
            if not self.validator.validate_search_query(query_text, limit):
                self.logger.warning(f"Invalid search parameters: query='{query_text}', limit={limit}")
                return []

            # Prepare filters
            filters = {}
            if category:
                filters["category"] = category

            # Create search query
            search_query = SearchQuery(
                query_text=query_text,
                search_type=SearchType.SIMILARITY,
                limit=limit,
                similarity_threshold=similarity_threshold,
                agent_id=agent_id,
                document_type=DocumentType.DEVLOG,
                filters=filters,
            )

            # Perform search
            results = self.vector_db.search(search_query, self.default_collection)
            
            # Record metrics
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)

            self.logger.info(f"✅ Found {len(results)} devlog results for query")
            return results

        except Exception as e:
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)
            self.logger.error(f"❌ Error searching devlogs: {e}")
            return []

    def search_all(self, query_text: str, agent_id: Optional[str] = None,
                  limit: int = 10, similarity_threshold: float = 0.0) -> List[SearchResult]:
        """
        Search across all document types.

        Args:
            query_text: Search query
            agent_id: Filter by agent ID
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score

        Returns:
            List of search results
        """
        start_time = time.time()
        
        try:
            # Validate search parameters
            if not self.validator.validate_search_query(query_text, limit):
                self.logger.warning(f"Invalid search parameters: query='{query_text}', limit={limit}")
                return []

            # Create search query (no document type filter)
            search_query = SearchQuery(
                query_text=query_text,
                search_type=SearchType.SIMILARITY,
                limit=limit,
                similarity_threshold=similarity_threshold,
                agent_id=agent_id,
            )

            # Perform search
            results = self.vector_db.search(search_query, self.default_collection)
            
            # Record metrics
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)

            self.logger.info(f"✅ Found {len(results)} total results for query")
            return results

        except Exception as e:
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)
            self.logger.error(f"❌ Error searching all: {e}")
            return []

    def get_related_messages(self, message_id: str, limit: int = 5) -> List[SearchResult]:
        """
        Find messages related to a specific message.

        Args:
            message_id: ID of the reference message
            limit: Maximum number of related messages

        Returns:
            List of related messages
        """
        start_time = time.time()
        
        try:
            # Get the original message
            original_doc = self.vector_db.get_document(message_id, self.default_collection)
            if not original_doc:
                self.logger.warning(f"Message {message_id} not found")
                return []

            # Search for similar messages
            search_query = SearchQuery(
                query_text=original_doc.content,
                search_type=SearchType.SIMILARITY,
                limit=limit + 1,  # +1 to account for the original message
                similarity_threshold=0.3,
                document_type=DocumentType.MESSAGE,
            )

            results = self.vector_db.search(search_query, self.default_collection)

            # Filter out the original message
            related_results = [r for r in results if r.document.id != message_id]
            
            # Record metrics
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)

            self.logger.info(f"✅ Found {len(related_results)} related messages")
            return related_results[:limit]

        except Exception as e:
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)
            self.logger.error(f"❌ Error finding related messages: {e}")
            return []

    def search_by_metadata(self, metadata_filters: Dict[str, Any], 
                          limit: int = 10) -> List[SearchResult]:
        """
        Search documents by metadata filters.
        
        Args:
            metadata_filters: Dictionary of metadata key-value pairs to filter by
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        start_time = time.time()
        
        try:
            # Create search query with metadata filters
            search_query = SearchQuery(
                query_text="",  # Empty query for metadata-only search
                search_type=SearchType.METADATA,
                limit=limit,
                filters=metadata_filters,
            )

            # Perform search
            results = self.vector_db.search(search_query, self.default_collection)
            
            # Record metrics
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)

            self.logger.info(f"✅ Found {len(results)} results for metadata search")
            return results

        except Exception as e:
            search_time = (time.time() - start_time) * 1000
            self.metrics.record_search(search_time)
            self.logger.error(f"❌ Error searching by metadata: {e}")
            return []

    def get_search_summary(self, query_text: str, results: List[SearchResult], 
                          execution_time_ms: float, agent_filter: Optional[str] = None,
                          document_type_filter: Optional[str] = None) -> SearchResultSummary:
        """
        Create a summary of search results.
        
        Args:
            query_text: Original search query
            results: Search results
            execution_time_ms: Search execution time in milliseconds
            agent_filter: Agent filter applied (if any)
            document_type_filter: Document type filter applied (if any)
            
        Returns:
            SearchResultSummary object
        """
        return SearchResultSummary(
            total_results=len(results),
            query_text=query_text,
            collection_name=self.default_collection,
            execution_time_ms=execution_time_ms,
            agent_filter=agent_filter,
            document_type_filter=document_type_filter
        )

    def get_search_metrics(self) -> Dict[str, Any]:
        """Get search metrics."""
        return self.metrics.to_dict()
