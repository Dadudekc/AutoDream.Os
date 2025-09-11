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
        """Simulate document retrieval with pagination."""
        # Mock documents
        all_documents = [
            Document(
                id=f"doc_{i}",
                title=f"Document {i}",
                content=f"Content for document {i}",
                collection=(
                    "agent_system"
                    if i % 4 == 0
                    else (
                        "project_docs"
                        if i % 4 == 1
                        else "development"
                        if i % 4 == 2
                        else "strategic_oversight"
                    )
                ),
                tags=[f"tag_{i % 3}"],
                size=f"{2 + (i % 5)}.{i % 10} KB",
                created_at=(datetime.now() - timedelta(days=i)).isoformat(),
                updated_at=(datetime.now() - timedelta(hours=i)).isoformat(),
            )
            for i in range(1, 101)  # 100 mock documents
        ]

        # Filter by collection
        if request.collection != "all":
            all_documents = [doc for doc in all_documents if doc.collection == request.collection]

        # Sort documents
        reverse = request.sort_order == "desc"
        all_documents.sort(key=lambda x: getattr(x, request.sort_by), reverse=reverse)

        # Paginate
        start = (request.page - 1) * request.per_page
        end = start + request.per_page
        documents = all_documents[start:end]

        total = len(all_documents)
        total_pages = (total + request.per_page - 1) // request.per_page

        return {
            "documents": [doc.__dict__ for doc in documents],
            "pagination": {
                "page": request.page,
                "per_page": request.per_page,
                "total": total,
                "total_pages": total_pages,
                "has_prev": request.page > 1,
                "has_next": request.page < total_pages,
            },
            "total": total,
        }

    def simulate_add_document(self, request: DocumentRequest) -> Document:
        """Simulate adding a document."""
        return Document(
            id=f"doc_{int(datetime.now().timestamp())}",
            title=request.title,
            content=request.content,
            collection=request.collection,
            tags=request.tags or [],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            size=f"{len(request.content) / 1000:.1f} KB",
        )

    def simulate_get_document(self, document_id: str) -> Document:
        """Simulate getting a specific document."""
        return Document(
            id=document_id,
            title="Sample Document",
            content="This is a sample document content.",
            collection="agent_system",
            tags=["sample", "test"],
            created_at="2025-01-27T10:00:00Z",
            updated_at="2025-01-27T10:00:00Z",
            size="1.2 KB",
        )

    def simulate_update_document(self, document_id: str, data: dict[str, Any]) -> Document:
        """Simulate updating a document."""
        return Document(
            id=document_id,
            title=data.get("title", "Updated Document"),
            content=data.get("content", "Updated content"),
            collection=data.get("collection", "agent_system"),
            tags=data.get("tags", []),
            created_at="2025-01-27T10:00:00Z",
            updated_at=datetime.now().isoformat(),
            size=f"{len(data.get('content', '')) / 1000:.1f} KB",
        )

    def simulate_delete_document(self, document_id: str) -> bool:
        """Simulate deleting a document."""
        return True
