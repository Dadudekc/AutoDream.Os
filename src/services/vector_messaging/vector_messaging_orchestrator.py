#!/usr/bin/env python3
"""
Vector Messaging Orchestrator - V2 Compliant
============================================

Main orchestrator for vector messaging integration system.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant vector messaging orchestration
"""

from typing import Optional, Dict, Any, List
import logging
from ..vector_database_service import VectorDatabaseService
from ..models.messaging_models import UnifiedMessage
from ..models.vector_models import SearchResult, CollectionConfig
from .vector_messaging_models import VectorDatabaseConfig, VectorDatabaseValidator
from .agent_enhancement_integrator import AgentEnhancementIntegrator
from .document_indexing_engine import DocumentIndexingEngine
from .search_query_engine import SearchQueryEngine


class VectorMessagingOrchestrator:
    """
    Main orchestrator for vector messaging integration.
    
    Coordinates vector database operations with messaging system through
    modular, V2-compliant architecture.
    """

    def __init__(self, config: Optional[VectorDatabaseConfig] = None):
        """
        Initialize vector messaging orchestrator.

        Args:
            config: Vector database configuration
        """
        self.logger = logging.getLogger(__name__)
        self.config = config or VectorDatabaseConfig()
        self.validator = VectorDatabaseValidator(self.config)

        # Initialize vector database service
        self.vector_db = VectorDatabaseService(
            persist_directory=self.config.persist_directory,
            default_embedding_model=self.config.default_embedding_model,
        )

        # Initialize modular components
        self.agent_integrator = AgentEnhancementIntegrator(self.vector_db, self.logger)
        self.indexing_engine = DocumentIndexingEngine(
            self.vector_db, self.validator, self.config.default_collection, self.logger
        )
        self.search_engine = SearchQueryEngine(
            self.vector_db, self.validator, self.config.default_collection, self.logger
        )

        # Setup system
        self._initialize_system()

    def _initialize_system(self):
        """Initialize the vector messaging system."""
        try:
            # Ensure default collection exists
            self._ensure_default_collection()
            
            # Integrate Agent-6 enhancement patterns
            self.agent_integrator.integrate_agent6_enhancements()
            
            self.logger.info("Vector messaging orchestrator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vector messaging system: {e}")

    def _ensure_default_collection(self):
        """Ensure default collection exists."""
        try:
            config = CollectionConfig(
                name=self.config.default_collection,
                description="Default collection for agent messages and communications",
            )
            self.vector_db.create_collection(config)
        except Exception as e:
            self.logger.error(f"❌ Error ensuring default collection: {e}")

    # Message Indexing Operations
    def index_message(self, message: UnifiedMessage, 
                     collection_name: Optional[str] = None) -> bool:
        """
        Index a message in the vector database.

        Args:
            message: Message to index
            collection_name: Collection to index in (defaults to default)

        Returns:
            True if successful, False otherwise
        """
        result = self.indexing_engine.index_message(message, collection_name)
        return result.success

    def index_devlog_entry(self, entry: Dict[str, Any], 
                          collection_name: Optional[str] = None) -> bool:
        """
        Index a devlog entry in the vector database.

        Args:
            entry: Devlog entry to index
            collection_name: Collection to index in

        Returns:
            True if successful, False otherwise
        """
        result = self.indexing_engine.index_devlog_entry(entry, collection_name)
        return result.success

    def index_inbox_files(self, agent_id: str, inbox_path: str) -> int:
        """
        Index all messages from an agent's inbox.

        Args:
            agent_id: Agent ID
            inbox_path: Path to agent's inbox directory

        Returns:
            Number of files indexed
        """
        result = self.indexing_engine.index_inbox_files(agent_id, inbox_path)
        return result.successful_indexes

    # Search Operations
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
        return self.search_engine.search_messages(
            query_text, agent_id, limit, similarity_threshold
        )

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
        return self.search_engine.search_devlogs(
            query_text, agent_id, category, limit, similarity_threshold
        )

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
        return self.search_engine.search_all(query_text, agent_id, limit, similarity_threshold)

    def get_related_messages(self, message_id: str, limit: int = 5) -> List[SearchResult]:
        """
        Find messages related to a specific message.

        Args:
            message_id: ID of the reference message
            limit: Maximum number of related messages

        Returns:
            List of related messages
        """
        return self.search_engine.get_related_messages(message_id, limit)

    # Agent Enhancement Operations
    def search_agent6_patterns(self, query: str, limit: int = 5) -> List[SearchResult]:
        """
        Search for Agent-6 communication enhancement patterns.

        Args:
            query: Search query for patterns
            limit: Maximum number of results to return

        Returns:
            List of search results containing pattern solutions
        """
        return self.agent_integrator.search_agent6_patterns(query, limit)

    # System Information
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get vector database statistics.

        Returns:
            Database statistics
        """
        try:
            stats = self.vector_db.get_stats()
            return stats.to_dict() if hasattr(stats, 'to_dict') else stats
        except Exception as e:
            self.logger.error(f"❌ Error getting database stats: {e}")
            return {}

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive system metrics.
        
        Returns:
            System metrics including indexing and search performance
        """
        try:
            indexing_metrics = self.indexing_engine.get_indexing_metrics()
            search_metrics = self.search_engine.get_search_metrics()
            pattern_stats = self.agent_integrator.get_pattern_statistics()
            database_stats = self.get_database_stats()
            
            return {
                "indexing": indexing_metrics,
                "search": search_metrics,
                "agent_patterns": pattern_stats,
                "database": database_stats,
                "config": {
                    "default_collection": self.config.default_collection,
                    "persist_directory": self.config.persist_directory,
                    "embedding_model": self.config.default_embedding_model
                }
            }
        except Exception as e:
            self.logger.error(f"❌ Error getting system metrics: {e}")
            return {"error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        """
        Perform system health check.
        
        Returns:
            Health status of all components
        """
        health_status = {
            "overall_status": "healthy",
            "components": {},
            "timestamp": self.logger.info("Performing health check")
        }
        
        try:
            # Check vector database
            try:
                stats = self.vector_db.get_stats()
                health_status["components"]["vector_database"] = "healthy"
            except Exception as e:
                health_status["components"]["vector_database"] = f"unhealthy: {e}"
                health_status["overall_status"] = "degraded"
            
            # Check default collection
            try:
                # Attempt a simple search to verify collection accessibility
                test_results = self.search_engine.search_all("test", limit=1)
                health_status["components"]["default_collection"] = "healthy"
            except Exception as e:
                health_status["components"]["default_collection"] = f"unhealthy: {e}"
                health_status["overall_status"] = "degraded"
            
            # Check agent enhancement patterns
            try:
                pattern_stats = self.agent_integrator.get_pattern_statistics()
                if pattern_stats.get("total_patterns", 0) > 0:
                    health_status["components"]["agent_patterns"] = "healthy"
                else:
                    health_status["components"]["agent_patterns"] = "warning: no patterns found"
                    if health_status["overall_status"] == "healthy":
                        health_status["overall_status"] = "warning"
            except Exception as e:
                health_status["components"]["agent_patterns"] = f"unhealthy: {e}"
                health_status["overall_status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"❌ Error during health check: {e}")
            return {
                "overall_status": "critical",
                "error": str(e),
                "components": {}
            }


# Global orchestrator instance
_orchestrator = None

def get_vector_messaging_orchestrator(config: Optional[VectorDatabaseConfig] = None) -> VectorMessagingOrchestrator:
    """Get global vector messaging orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = VectorMessagingOrchestrator(config)
    return _orchestrator
