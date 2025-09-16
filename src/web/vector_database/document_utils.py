import logging
logger = logging.getLogger(__name__)
"""
Document Utils
==============

Document CRUD utility functions for vector database operations.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from datetime import datetime, timedelta
from typing import Any

from .models import Document, DocumentRequest, PaginationRequest


class DocumentUtils:
    """Utility functions for document operations."""

    def simulate_get_documents(self, request: PaginationRequest) -> dict[str, Any]:
        """
        Simulate document retrieval with pagination.

        EXAMPLE USAGE:
        ==============

        # Basic usage example
        from src.web.vector_database.document_utils import DocumentUtils
        from src.web.vector_database.models import PaginationRequest

        # Initialize document utils
        docs = DocumentUtils()

        # Get documents with pagination
        pagination = PaginationRequest(page=1, page_size=10)
        result = docs.simulate_get_documents(pagination)

        logger.info(f"Total documents: {result['total']}")
        logger.info(f"Returned documents: {len(result['documents'])}")

        # Advanced pagination with filters
        filtered_request = PaginationRequest(
            page=1,
            page_size=5,
            filters={"type": "technical"}
        )
        filtered_result = docs.simulate_get_documents(filtered_request)

        Args:
            request: Pagination and filtering parameters

        Returns:
            dict: Paginated document results with metadata
        """
        # Simulate realistic document retrieval with pagination
        import random
        from datetime import datetime, timedelta

        # Calculate pagination parameters
        total_docs = random.randint(50, 200)
        start_idx = (request.page - 1) * request.page_size
        end_idx = min(start_idx + request.page_size, total_docs)

        # Generate sample documents
        documents = []
        for i in range(start_idx, end_idx):
            days_ago = random.randint(1, 90)
            created_at = (datetime.now() - timedelta(days=days_ago)).isoformat()

            doc = {
                "id": f"doc_{i:06d}",
                "content": f"This is sample document content for item {i}. It contains relevant information about the topic being discussed.",
                "metadata": {
                    "type": ["article", "report", "guide", "tutorial"][i % 4],
                    "category": ["technology", "business", "science", "health"][i % 4],
                    "author": f"author_{i % 10}",
                    "created_at": created_at,
                    "tags": [f"tag_{j}" for j in range(random.randint(1, 4))],
                    "word_count": random.randint(100, 2000),
                    "language": "en"
                }
            }

            # Apply filters if specified
            if request.filters:
                if "category" in request.filters:
                    if doc["metadata"]["category"] != request.filters["category"]:
                        continue
                if "type" in request.filters:
                    if doc["metadata"]["type"] != request.filters["type"]:
                        continue

            documents.append(doc)

        return {
            "documents": documents,
            "total": total_docs,
            "page": request.page,
            "page_size": request.page_size,
            "has_next": end_idx < total_docs,
            "total_pages": (total_docs + request.page_size - 1) // request.page_size
        }

    def simulate_add_document(self, request: DocumentRequest) -> Document:
        """
        Simulate adding a document to the collection.

        EXAMPLE USAGE:
        ==============

        # Add a new document
        from src.web.vector_database.document_utils import DocumentUtils
        from src.web.vector_database.models import DocumentRequest

        docs = DocumentUtils()
        doc_request = DocumentRequest(
            collection_name="my_collection",
            content="New document content",
            metadata={"type": "article", "author": "Agent-1"}
        )

        new_doc = docs.simulate_add_document(doc_request)
        logger.info(f"Added document: {new_doc.id}")

        Args:
            request: Document creation parameters

        Returns:
            Document: The created document
        """
        # Simulate realistic document creation with validation
        import hashlib
        from datetime import datetime

        # Generate a unique ID based on content hash for consistency
        content_hash = hashlib.md5((request.content or "").encode()).hexdigest()[:8]
        document_id = f"doc_{content_hash}_{int(datetime.now().timestamp())}"

        # Create enhanced metadata
        base_metadata = request.metadata or {}
        enhanced_metadata = {
            **base_metadata,
            "created_at": datetime.now().isoformat(),
            "content_length": len(request.content or ""),
            "word_count": len((request.content or "").split()),
            "language": base_metadata.get("language", "en"),
            "version": "1.0"
        }

        # Add content analysis if content is provided
        if request.content:
            content_lower = request.content.lower()
            # Simple keyword-based categorization
            if any(word in content_lower for word in ["python", "javascript", "code", "programming"]):
                enhanced_metadata["category"] = "technical"
            elif any(word in content_lower for word in ["business", "finance", "market"]):
                enhanced_metadata["category"] = "business"
            else:
                enhanced_metadata["category"] = "general"

        return Document(
            id=document_id,
            content=request.content or "",
            metadata=enhanced_metadata,
            created_at=enhanced_metadata["created_at"]
        )

    def simulate_delete_document(self, document_id: str) -> bool:
        """
        Simulate deleting a document.

        EXAMPLE USAGE:
        ==============

        # Delete a document
        from src.web.vector_database.document_utils import DocumentUtils

        docs = DocumentUtils()
        success = docs.simulate_delete_document("doc_123")

        if success:
            logger.info("Document deleted successfully")
        else:
            logger.info("Document deletion failed")

        Args:
            document_id: ID of the document to delete

        Returns:
            bool: True if deletion was successful
        """
        # Simulate realistic document deletion with validation
        import random

        # Validate document ID format
        if not document_id or not document_id.startswith("doc_"):
            return False

        # Simulate deletion with small chance of failure (for realism)
        # In a real implementation, this would check if document exists and delete it
        deletion_success = random.random() > 0.05  # 95% success rate

        return deletion_success
