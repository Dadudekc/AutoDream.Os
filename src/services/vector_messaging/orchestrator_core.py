"""
Vector Messaging Orchestrator Core
==================================

Core orchestration logic for vector messaging operations.
V2 Compliance: < 300 lines, single responsibility, core orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
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


class VectorMessagingOrchestratorCore:
    """Core orchestration logic for vector messaging operations."""
    
    def __init__(self, config: Optional[VectorDatabaseConfig] = None):
        """Initialize vector messaging orchestrator core."""
        self.config = config or VectorDatabaseConfig()
        self.validator = VectorDatabaseValidator()
        self.vector_db_service: Optional[VectorDatabaseService] = None
        self.agent_enhancer: Optional[AgentEnhancementIntegrator] = None
        self.document_indexer: Optional[DocumentIndexingEngine] = None
        self.search_engine: Optional[SearchQueryEngine] = None
        self.is_initialized = False
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> bool:
        """Initialize the orchestrator core."""
        try:
            # Validate configuration
            if not self.validator.validate_config(self.config):
                self.logger.error("Invalid vector database configuration")
                return False
            
            # Initialize vector database service
            self.vector_db_service = VectorDatabaseService()
            if not self.vector_db_service.initialize():
                self.logger.error("Failed to initialize vector database service")
                return False
            
            # Initialize agent enhancement integrator
            self.agent_enhancer = AgentEnhancementIntegrator(self.vector_db_service)
            if not self.agent_enhancer.initialize():
                self.logger.error("Failed to initialize agent enhancement integrator")
                return False
            
            # Initialize document indexing engine
            self.document_indexer = DocumentIndexingEngine(self.vector_db_service)
            if not self.document_indexer.initialize():
                self.logger.error("Failed to initialize document indexing engine")
                return False
            
            # Initialize search query engine
            self.search_engine = SearchQueryEngine(self.vector_db_service)
            if not self.search_engine.initialize():
                self.logger.error("Failed to initialize search query engine")
                return False
            
            self.is_initialized = True
            self.logger.info("Vector Messaging Orchestrator Core initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Messaging Orchestrator Core: {e}")
            return False
    
    def create_collection(self, collection_name: str, config: Optional[CollectionConfig] = None) -> bool:
        """Create a new vector collection."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        if not self.vector_db_service:
            return False
        
        return self.vector_db_service.create_collection(collection_name, config)
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a vector collection."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        if not self.vector_db_service:
            return False
        
        return self.vector_db_service.delete_collection(collection_name)
    
    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get collection information."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        if not self.vector_db_service:
            return None
        
        return self.vector_db_service.get_collection_info(collection_name)
    
    def list_collections(self) -> List[str]:
        """List all collections."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator core not initialized")
        
        if not self.vector_db_service:
            return []
        
        return self.vector_db_service.list_collections()
    
    def get_core_status(self) -> Dict[str, Any]:
        """Get orchestrator core status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'vector_db_initialized': self.vector_db_service.is_initialized if self.vector_db_service else False,
            'agent_enhancer_initialized': self.agent_enhancer.is_initialized if self.agent_enhancer else False,
            'document_indexer_initialized': self.document_indexer.is_initialized if self.document_indexer else False,
            'search_engine_initialized': self.search_engine.is_initialized if self.search_engine else False
        }
    
    def shutdown(self):
        """Shutdown orchestrator core."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Vector Messaging Orchestrator Core")
        
        if self.search_engine:
            self.search_engine.shutdown()
        if self.document_indexer:
            self.document_indexer.shutdown()
        if self.agent_enhancer:
            self.agent_enhancer.shutdown()
        if self.vector_db_service:
            self.vector_db_service.shutdown()
        
        self.is_initialized = False
