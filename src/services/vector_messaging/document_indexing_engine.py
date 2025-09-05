#!/usr/bin/env python3
"""
Document Indexing Engine - V2 Compliant
=======================================

Handles indexing of messages, devlogs, and other documents into vector database.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant document indexing functionality
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
    """Engine for indexing various document types into vector database."""
    
    def __init__(self, vector_db_service, validator: VectorDatabaseValidator, 
                 default_collection: str, logger: logging.Logger = None):
        """Initialize indexing engine."""
        self.vector_db = vector_db_service
        self.validator = validator
        self.default_collection = default_collection
        self.logger = logger or logging.getLogger(__name__)
        self.metrics = VectorMessagingMetrics()
    
    def index_message(self, message: UnifiedMessage, 
                     collection_name: Optional[str] = None) -> IndexingResult:
        """
        Index a message in the vector database.

        Args:
            message: Message to index
            collection_name: Collection to index in (defaults to default)

        Returns:
            IndexingResult with operation details
        """
        start_time = time.time()
        collection_name = collection_name or self.default_collection
        
        try:
            # Validate message content
            if not self.validator.validate_document_content(message.content):
                error_msg = "Invalid message content"
                self.logger.warning(f"Message validation failed: {error_msg}")
                self.metrics.record_indexing(False, (time.time() - start_time) * 1000)
                return IndexingResult(
                    success=False,
                    document_id=message.message_id,
                    error_message=error_msg,
                    collection_name=collection_name
                )

            # Create vector document
            vector_doc = VectorDocument(
                id=message.message_id,
                content=message.content,
                document_type=DocumentType.MESSAGE,
                agent_id=message.recipient,
                metadata={
                    "sender": message.sender,
                    "message_type": message.message_type.value,
                    "priority": message.priority.value,
                    "delivery_method": getattr(message, "delivery_method", "unknown"),
                    "timestamp": getattr(message, "timestamp", ""),
                },
                tags=[message.message_type.value, message.priority.value],
            )

            # Add to vector database
            success = self.vector_db.add_document(vector_doc, collection_name)
            processing_time = (time.time() - start_time) * 1000
            
            self.metrics.record_indexing(success, processing_time)
            
            if success:
                self.logger.info(f"✅ Indexed message {message.message_id}")
                return IndexingResult(
                    success=True,
                    document_id=message.message_id,
                    collection_name=collection_name,
                    document_size=len(message.content)
                )
            else:
                error_msg = "Vector database add operation failed"
                self.logger.error(f"❌ Failed to index message {message.message_id}: {error_msg}")
                return IndexingResult(
                    success=False,
                    document_id=message.message_id,
                    error_message=error_msg,
                    collection_name=collection_name
                )

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_indexing(False, processing_time)
            self.logger.error(f"❌ Error indexing message {message.message_id}: {e}")
            return IndexingResult(
                success=False,
                document_id=message.message_id,
                error_message=str(e),
                collection_name=collection_name
            )

    def index_devlog_entry(self, entry: Dict[str, Any], 
                          collection_name: Optional[str] = None) -> IndexingResult:
        """
        Index a devlog entry in the vector database.

        Args:
            entry: Devlog entry to index
            collection_name: Collection to index in

        Returns:
            IndexingResult with operation details
        """
        start_time = time.time()
        collection_name = collection_name or self.default_collection
        document_id = f"devlog_{entry.get('id', 'unknown')}"
        
        try:
            # Extract content from devlog entry
            content = f"{entry.get('title', '')} {entry.get('content', '')}"

            if not self.validator.validate_document_content(content):
                error_msg = "Invalid devlog content"
                self.logger.warning(f"Devlog validation failed: {error_msg}")
                self.metrics.record_indexing(False, (time.time() - start_time) * 1000)
                return IndexingResult(
                    success=False,
                    document_id=document_id,
                    error_message=error_msg,
                    collection_name=collection_name
                )

            # Create vector document
            vector_doc = VectorDocument(
                id=document_id,
                content=content,
                document_type=DocumentType.DEVLOG,
                agent_id=entry.get("agent_id"),
                metadata={
                    "title": entry.get("title", ""),
                    "category": entry.get("category", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "author": entry.get("author", ""),
                },
                tags=[entry.get("category", ""), "devlog"],
            )

            # Add to vector database
            success = self.vector_db.add_document(vector_doc, collection_name)
            processing_time = (time.time() - start_time) * 1000
            
            self.metrics.record_indexing(success, processing_time)

            if success:
                self.logger.info(f"✅ Indexed devlog entry {document_id}")
                return IndexingResult(
                    success=True,
                    document_id=document_id,
                    collection_name=collection_name,
                    document_size=len(content)
                )
            else:
                error_msg = "Vector database add operation failed"
                self.logger.error(f"❌ Failed to index devlog {document_id}: {error_msg}")
                return IndexingResult(
                    success=False,
                    document_id=document_id,
                    error_message=error_msg,
                    collection_name=collection_name
                )

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_indexing(False, processing_time)
            self.logger.error(f"❌ Error indexing devlog entry {document_id}: {e}")
            return IndexingResult(
                success=False,
                document_id=document_id,
                error_message=str(e),
                collection_name=collection_name
            )

    def index_inbox_files(self, agent_id: str, inbox_path: str) -> BatchIndexingResult:
        """
        Index all messages from an agent's inbox.

        Args:
            agent_id: Agent ID
            inbox_path: Path to agent's inbox directory

        Returns:
            BatchIndexingResult with batch operation details
        """
        start_time = time.time()
        
        try:
            # Validate agent ID
            if not self.validator.validate_agent_id(agent_id):
                error_msg = f"Invalid agent ID: {agent_id}"
                self.logger.error(error_msg)
                return BatchIndexingResult(
                    total_processed=0,
                    successful_indexes=0,
                    failed_indexes=0,
                    errors={"validation": error_msg},
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            inbox_dir = Path(inbox_path)
            if not inbox_dir.exists():
                error_msg = f"Inbox directory {inbox_path} does not exist"
                self.logger.warning(error_msg)
                return BatchIndexingResult(
                    total_processed=0,
                    successful_indexes=0,
                    failed_indexes=0,
                    errors={"path": error_msg},
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            successful_indexes = 0
            errors = {}
            total_processed = 0

            # Process all markdown files in inbox
            for file_path in inbox_dir.glob("*.md"):
                total_processed += 1
                file_doc_id = f"inbox_{agent_id}_{file_path.stem}"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if not self.validator.validate_document_content(content):
                        errors[file_doc_id] = "Invalid file content"
                        continue

                    # Create vector document
                    vector_doc = VectorDocument(
                        id=file_doc_id,
                        content=content,
                        document_type=DocumentType.MESSAGE,
                        agent_id=agent_id,
                        source_file=str(file_path),
                        metadata={
                            "file_name": file_path.name,
                            "file_size": file_path.stat().st_size,
                            "file_modified": file_path.stat().st_mtime,
                        },
                        tags=["inbox", "file"],
                    )

                    # Add to vector database
                    if self.vector_db.add_document(vector_doc, self.default_collection):
                        successful_indexes += 1
                        self.metrics.record_indexing(True, 0)  # Time tracked overall
                    else:
                        errors[file_doc_id] = "Vector database add operation failed"
                        self.metrics.record_indexing(False, 0)

                except Exception as e:
                    errors[file_doc_id] = str(e)
                    self.metrics.record_indexing(False, 0)

            processing_time = (time.time() - start_time) * 1000
            failed_indexes = total_processed - successful_indexes

            self.logger.info(
                f"✅ Indexed {successful_indexes}/{total_processed} files from {agent_id} inbox"
            )
            
            return BatchIndexingResult(
                total_processed=total_processed,
                successful_indexes=successful_indexes,
                failed_indexes=failed_indexes,
                errors=errors,
                processing_time_ms=processing_time
            )

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Error indexing inbox files: {e}")
            return BatchIndexingResult(
                total_processed=0,
                successful_indexes=0,
                failed_indexes=0,
                errors={"system": str(e)},
                processing_time_ms=processing_time
            )

    def get_indexing_metrics(self) -> Dict[str, Any]:
        """Get indexing metrics."""
        return self.metrics.to_dict()
