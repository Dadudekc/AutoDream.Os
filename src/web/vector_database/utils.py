"""
Vector Database Utilities
========================

Main utility orchestrator for vector database operations.
V2 Compliance: < 100 lines, facade pattern, single responsibility.

REFACTORED: Split into focused utility classes for V2 compliance
- SearchUtils: Search-related operations
- DocumentUtils: Document CRUD operations
- AnalyticsUtils: Analytics and reporting
- CollectionUtils: Collection management

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from .search_utils import SearchUtils
from .document_utils import DocumentUtils
from .analytics_utils import AnalyticsUtils
from .collection_utils import CollectionUtils


class VectorDatabaseUtils:
    """Main utility orchestrator for vector database operations.

    V2 Compliance: < 100 lines, facade pattern, single responsibility.
    This class orchestrates all utility components.
    """

    def __init__(self):
        """Initialize utility components."""
        self.search = SearchUtils()
        self.documents = DocumentUtils()
        self.analytics = AnalyticsUtils()
        self.collections = CollectionUtils()

    def simulate_vector_search(self, request):
        """Delegate to search utils."""
        return self.search.simulate_vector_search(request)

    def simulate_get_documents(self, request):
        """Delegate to document utils."""
        return self.documents.simulate_get_documents(request)

    def simulate_add_document(self, request):
        """Delegate to document utils."""
        return self.documents.simulate_add_document(request)

    def simulate_get_document(self, document_id: str):
        """Delegate to document utils."""
        return self.documents.simulate_get_document(document_id)

    def simulate_update_document(self, document_id: str, data):
        """Delegate to document utils."""
        return self.documents.simulate_update_document(document_id, data)

    def simulate_delete_document(self, document_id: str):
        """Delegate to document utils."""
        return self.documents.simulate_delete_document(document_id)

    def simulate_get_analytics(self, time_range: str):
        """Delegate to analytics utils."""
        return self.analytics.simulate_get_analytics(time_range)

    def simulate_get_collections(self):
        """Delegate to collection utils."""
        return self.collections.simulate_get_collections()

    def simulate_export_data(self, request):
        """Delegate to collection utils."""
        return self.collections.simulate_export_data(request)
