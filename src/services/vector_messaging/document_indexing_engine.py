#!/usr/bin/env python3
"""
Document Indexing Engine - KISS Simplified
==========================================

Simplified document indexing engine for vector database.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined document indexing.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Optional, Dict, Any, List
import time
from pathlib import Path
import logging
from ..models.vector_models import DocumentType, VectorDocument
from ..models.messaging_models import UnifiedMessage
from .vector_messaging_models import (
    VectorDatabaseValidator, IndexingResult, BatchIndexingResult, VectorMessagingMetrics
)


class DocumentIndexingEngine:
    """Simplified engine for indexing various document types into vector database."""
    
    def __init__(self, vector_db_service, validator: VectorDatabaseValidator, 
                 default_collection: str, logger: logging.Logger = None):
        """Initialize indexing engine - simplified."""
        self.vector_db = vector_db_service
        self.validator = validator
        self.default_collection = default_collection
        self.logger = logger or logging.getLogger(__name__)
        self.metrics = VectorMessagingMetrics()
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize engine - simplified."""
        try:
            self.is_initialized = True
            self.logger.info("Document Indexing Engine initialized (KISS)")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing engine: {e}")
            return False
    
    def index_message(self, message: UnifiedMessage, 
                     collection_name: Optional[str] = None) -> IndexingResult:
        """Index a message in the vector database - simplified."""
        start_time = time.time()
        collection_name = collection_name or self.default_collection
        
        try:
            if not self.is_initialized:
                return IndexingResult(success=False, error="Engine not initialized")
            
            # Create document from message
            document = VectorDocument(
                id=f"msg_{message.message_id}",
                content=message.content,
                metadata={
                    "type": "message",
                    "sender": message.sender_id,
                    "recipient": message.recipient_id,
                    "priority": message.priority.value,
                    "timestamp": message.timestamp.isoformat()
                },
                document_type=DocumentType.MESSAGE
            )
            
            # Validate document
            if not self.validator.validate_document(document):
                return IndexingResult(success=False, error="Document validation failed")
            
            # Index document
            result = self.vector_db.add_document(collection_name, document)
            
            if result:
                self.metrics.increment_indexed_documents()
                processing_time = time.time() - start_time
                self.logger.info(f"Message indexed successfully: {message.message_id}")
                return IndexingResult(
                    success=True,
                    document_id=document.id,
                    processing_time=processing_time
                )
            else:
                return IndexingResult(success=False, error="Vector DB indexing failed")
                
        except Exception as e:
            self.logger.error(f"Error indexing message: {e}")
            return IndexingResult(success=False, error=str(e))
    
    def index_devlog(self, devlog_path: Path, 
                    collection_name: Optional[str] = None) -> IndexingResult:
        """Index a devlog file - simplified."""
        start_time = time.time()
        collection_name = collection_name or self.default_collection
        
        try:
            if not self.is_initialized:
                return IndexingResult(success=False, error="Engine not initialized")
            
            # Read devlog content
            content = devlog_path.read_text(encoding='utf-8')
            
            # Create document from devlog
            document = VectorDocument(
                id=f"devlog_{devlog_path.stem}",
                content=content,
                metadata={
                    "type": "devlog",
                    "file_path": str(devlog_path),
                    "file_name": devlog_path.name,
                    "file_size": devlog_path.stat().st_size
                },
                document_type=DocumentType.DEVLOG
            )
            
            # Validate document
            if not self.validator.validate_document(document):
                return IndexingResult(success=False, error="Document validation failed")
            
            # Index document
            result = self.vector_db.add_document(collection_name, document)
            
            if result:
                self.metrics.increment_indexed_documents()
                processing_time = time.time() - start_time
                self.logger.info(f"Devlog indexed successfully: {devlog_path.name}")
                return IndexingResult(
                    success=True,
                    document_id=document.id,
                    processing_time=processing_time
                )
            else:
                return IndexingResult(success=False, error="Vector DB indexing failed")
                
        except Exception as e:
            self.logger.error(f"Error indexing devlog: {e}")
            return IndexingResult(success=False, error=str(e))
    
    def batch_index_documents(self, documents: List[VectorDocument], 
                            collection_name: Optional[str] = None) -> BatchIndexingResult:
        """Batch index multiple documents - simplified."""
        start_time = time.time()
        collection_name = collection_name or self.default_collection
        
        try:
            if not self.is_initialized:
                return BatchIndexingResult(success=False, error="Engine not initialized")
            
            successful_docs = []
            failed_docs = []
            
            for document in documents:
                # Validate document
                if not self.validator.validate_document(document):
                    failed_docs.append(document.id)
                    continue
                
                # Index document
                result = self.vector_db.add_document(collection_name, document)
                
                if result:
                    successful_docs.append(document.id)
                    self.metrics.increment_indexed_documents()
                else:
                    failed_docs.append(document.id)
            
            processing_time = time.time() - start_time
            success_rate = len(successful_docs) / len(documents) if documents else 0
            
            self.logger.info(f"Batch indexing completed: {len(successful_docs)}/{len(documents)} successful")
            
            return BatchIndexingResult(
                success=len(successful_docs) > 0,
                successful_documents=successful_docs,
                failed_documents=failed_docs,
                success_rate=success_rate,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in batch indexing: {e}")
            return BatchIndexingResult(success=False, error=str(e))
    
    def search_documents(self, query: str, collection_name: Optional[str] = None, 
                        limit: int = 10) -> List[VectorDocument]:
        """Search documents - simplified."""
        try:
            if not self.is_initialized:
                return []
            
            collection_name = collection_name or self.default_collection
            results = self.vector_db.search(collection_name, query, limit)
            return results or []
            
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            return []
    
    def get_document(self, document_id: str, collection_name: Optional[str] = None) -> Optional[VectorDocument]:
        """Get document by ID - simplified."""
        try:
            if not self.is_initialized:
                return None
            
            collection_name = collection_name or self.default_collection
            return self.vector_db.get_document(collection_name, document_id)
            
        except Exception as e:
            self.logger.error(f"Error getting document: {e}")
            return None
    
    def delete_document(self, document_id: str, collection_name: Optional[str] = None) -> bool:
        """Delete document - simplified."""
        try:
            if not self.is_initialized:
                return False
            
            collection_name = collection_name or self.default_collection
            result = self.vector_db.delete_document(collection_name, document_id)
            
            if result:
                self.metrics.increment_deleted_documents()
                self.logger.info(f"Document deleted: {document_id}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error deleting document: {e}")
            return False
    
    def get_indexing_stats(self) -> Dict[str, Any]:
        """Get indexing statistics - simplified."""
        return {
            "engine_type": "document_indexing",
            "initialized": self.is_initialized,
            "default_collection": self.default_collection,
            "metrics": self.metrics.get_metrics()
        }
    
    def cleanup_old_documents(self, days_old: int = 30) -> int:
        """Cleanup old documents - simplified."""
        try:
            if not self.is_initialized:
                return 0
            
            # Basic cleanup logic
            self.logger.info(f"Cleaning up documents older than {days_old} days")
            return 0  # Simplified - no actual cleanup
            
        except Exception as e:
            self.logger.error(f"Error cleaning up documents: {e}")
            return 0
    
    def shutdown(self) -> bool:
        """Shutdown engine - simplified."""
        try:
            self.is_initialized = False
            self.logger.info("Document Indexing Engine shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False