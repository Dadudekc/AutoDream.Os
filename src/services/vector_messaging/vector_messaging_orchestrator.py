#!/usr/bin/env python3
"""
Vector Messaging Orchestrator - V2 Compliant Redirect
=====================================================

V2 compliance redirect to modular vector messaging orchestrator.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular vector messaging orchestrator
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .orchestrator_core import VectorMessagingOrchestratorCore
from .orchestrator_services import VectorMessagingOrchestratorServices

# Backward compatibility - create main orchestrator class
class VectorMessagingOrchestrator:
    """Main vector messaging orchestrator - V2 compliant wrapper."""
    
    def __init__(self, config=None):
        """Initialize vector messaging orchestrator."""
        self.core = VectorMessagingOrchestratorCore(config)
        self.services = VectorMessagingOrchestratorServices(self.core)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            if not self.core.initialize():
                return False
            if not self.services.initialize():
                return False
            
            self.is_initialized = True
            return True
        except Exception as e:
            return False
    
    # Delegate core methods
    def create_collection(self, collection_name, config=None):
        return self.core.create_collection(collection_name, config)
    
    def delete_collection(self, collection_name):
        return self.core.delete_collection(collection_name)
    
    def get_collection_info(self, collection_name):
        return self.core.get_collection_info(collection_name)
    
    def list_collections(self):
        return self.core.list_collections()
    
    # Delegate service methods
    def index_message(self, message, collection_name="messages"):
        return self.services.index_message(message, collection_name)
    
    def search_messages(self, query, collection_name="messages", limit=10):
        return self.services.search_messages(query, collection_name, limit)
    
    def enhance_agent_with_context(self, agent_id, context_data):
        return self.services.enhance_agent_with_context(agent_id, context_data)
    
    def get_agent_context(self, agent_id):
        return self.services.get_agent_context(agent_id)
    
    def index_document(self, document_id, content, metadata, collection_name="documents"):
        return self.services.index_document(document_id, content, metadata, collection_name)
    
    def search_documents(self, query, collection_name="documents", limit=10):
        return self.services.search_documents(query, collection_name, limit)
    
    def get_vector_analytics(self):
        return self.services.get_vector_analytics()
    
    def get_orchestrator_status(self):
        return self.core.get_core_status()
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.services.shutdown()
        self.core.shutdown()
        self.is_initialized = False

# Re-export for backward compatibility
__all__ = [
    'VectorMessagingOrchestrator',
    'VectorMessagingOrchestratorCore',
    'VectorMessagingOrchestratorServices'
]