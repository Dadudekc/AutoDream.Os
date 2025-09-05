"""
Vector Messaging Orchestrator Services
======================================

Service functionality for vector messaging operations.
V2 Compliance: < 300 lines, single responsibility, service logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Optional, Dict, Any, List
import logging
from ..models.messaging_models import UnifiedMessage
from ..models.vector_models import SearchResult, CollectionInfo
from .vector_messaging_models import VectorDatabaseConfig
from .orchestrator_core import VectorMessagingOrchestratorCore


class VectorMessagingOrchestratorServices:
    """Service functionality for vector messaging operations."""
    
    def __init__(self, orchestrator_core: VectorMessagingOrchestratorCore):
        """Initialize vector messaging orchestrator services."""
        self.orchestrator_core = orchestrator_core
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the orchestrator services."""
        try:
            if not self.orchestrator_core.is_initialized:
                raise Exception("Orchestrator core not initialized")
            
            self.is_initialized = True
            self.logger.info("Vector Messaging Orchestrator Services initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Messaging Orchestrator Services: {e}")
            return False
    
    def index_message(self, message: UnifiedMessage, collection_name: str = "messages") -> bool:
        """Index a message in the vector database."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.document_indexer:
                return False
            
            return self.orchestrator_core.document_indexer.index_message(message, collection_name)
            
        except Exception as e:
            self.logger.error(f"Error indexing message: {e}")
            return False
    
    def search_messages(self, query: str, collection_name: str = "messages", 
                       limit: int = 10) -> List[SearchResult]:
        """Search for messages in the vector database."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.search_engine:
                return []
            
            return self.orchestrator_core.search_engine.search_messages(query, collection_name, limit)
            
        except Exception as e:
            self.logger.error(f"Error searching messages: {e}")
            return []
    
    def enhance_agent_with_context(self, agent_id: str, context_data: Dict[str, Any]) -> bool:
        """Enhance agent with context data."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.agent_enhancer:
                return False
            
            return self.orchestrator_core.agent_enhancer.enhance_agent(agent_id, context_data)
            
        except Exception as e:
            self.logger.error(f"Error enhancing agent: {e}")
            return False
    
    def get_agent_context(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent context data."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.agent_enhancer:
                return None
            
            return self.orchestrator_core.agent_enhancer.get_agent_context(agent_id)
            
        except Exception as e:
            self.logger.error(f"Error getting agent context: {e}")
            return None
    
    def index_document(self, document_id: str, content: str, metadata: Dict[str, Any], 
                      collection_name: str = "documents") -> bool:
        """Index a document in the vector database."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.document_indexer:
                return False
            
            return self.orchestrator_core.document_indexer.index_document(
                document_id, content, metadata, collection_name
            )
            
        except Exception as e:
            self.logger.error(f"Error indexing document: {e}")
            return False
    
    def search_documents(self, query: str, collection_name: str = "documents", 
                        limit: int = 10) -> List[SearchResult]:
        """Search for documents in the vector database."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.search_engine:
                return []
            
            return self.orchestrator_core.search_engine.search_documents(query, collection_name, limit)
            
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            return []
    
    def get_vector_analytics(self) -> Dict[str, Any]:
        """Get vector database analytics."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator services not initialized")
            
            if not self.orchestrator_core.vector_db_service:
                return {'error': 'Vector database service not available'}
            
            # Get basic analytics
            collections = self.orchestrator_core.list_collections()
            
            analytics = {
                'total_collections': len(collections),
                'collections': collections,
                'vector_db_status': self.orchestrator_core.vector_db_service.get_status()
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting vector analytics: {e}")
            return {'error': str(e)}
    
    def get_services_status(self) -> Dict[str, Any]:
        """Get services status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'orchestrator_core_initialized': self.orchestrator_core.is_initialized,
            'services_type': 'vector_messaging'
        }
    
    def shutdown(self):
        """Shutdown orchestrator services."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Vector Messaging Orchestrator Services")
        self.is_initialized = False
