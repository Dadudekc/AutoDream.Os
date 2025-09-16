import logging

logger = logging.getLogger(__name__)
"""
Semantic Utilities - Consolidated Module
========================================

Consolidated utility functions for semantic operations and vector database utilities.
Merges functionality from src/web/vector_database/utils.py and src/core/semantic/utils.py.

V2 Compliance: < 400 lines, functions < 50 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist) - Consolidation Mission
License: MIT
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

# Import vector database utilities
try:
    from ...web.vector_database.analytics_utils import AnalyticsUtils
    from ...web.vector_database.collection_utils import CollectionUtils
    from ...web.vector_database.document_utils import DocumentUtils
    from ...web.vector_database.search_utils import SearchUtils
except ImportError:
    # Fallback for direct execution
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    from web.vector_database.analytics_utils import AnalyticsUtils
    from web.vector_database.collection_utils import CollectionUtils
    from web.vector_database.document_utils import DocumentUtils
    from web.vector_database.search_utils import SearchUtils


# ============================================================================
# SEMANTIC UTILITY FUNCTIONS
# ============================================================================


def flatten_json(obj: Any, prefix: str = "", keep: Iterable[str] | None = None) -> list[str]:
    """Turn nested JSON/dicts/lists into a list of 'key: value' strings."""
    keep_set = set(keep or [])
    out: list[str] = []

    def _walk(x: Any, path: list[str]):
        if isinstance(x, dict):
            for k, v in x.items():
                if keep_set and len(path) == 0 and k not in keep_set:
                    # at root, respect 'fields_keep'
                    continue
                _walk(v, path + [str(k)])
        elif isinstance(x, list):
            for i, v in enumerate(x):
                _walk(v, path + [str(i)])
        else:
            key = "/".join(path)
            val = str(x)
            out.append(f"{key}: {val}")

    _walk(obj, [prefix] if prefix else [])
    return out


def json_to_text(obj: Any, keep: Iterable[str] | None = None) -> str:
    """Convert JSON object to text format."""
    return "\n".join(flatten_json(obj, keep=keep))


# ============================================================================
# VECTOR DATABASE UTILITIES
# ============================================================================


class VectorDatabaseUtils:
    """Main utility orchestrator for vector database operations.

    V2 Compliance: < 100 lines, facade pattern, single responsibility.
    This class orchestrates all utility components.

    EXAMPLE USAGE:
    ==============

    # Basic usage example
    from src.core.semantic.utils import VectorDatabaseUtils

    # Initialize and use
    instance = VectorDatabaseUtils()
    result = instance.simulate_vector_search(request)
    logger.info(f"Execution result: {result}")

    # Advanced configuration
    config = {
        "option1": "value1",
        "option2": True
    }

    instance = VectorDatabaseUtils()
    advanced_result = instance.simulate_get_analytics("7d")
    logger.info(f"Advanced result: {advanced_result}")
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


# ============================================================================
# CONSOLIDATED UTILITIES INTERFACE
# ============================================================================


class ConsolidatedUtils:
    """Consolidated utilities interface providing both semantic and vector database functionality."""

    def __init__(self):
        """Initialize consolidated utilities."""
        self.vector_db = VectorDatabaseUtils()

    # Semantic utility functions
    def flatten_json(
        self, obj: Any, prefix: str = "", keep: Iterable[str] | None = None
    ) -> list[str]:
        """Turn nested JSON/dicts/lists into a list of 'key: value' strings."""
        return flatten_json(obj, prefix, keep)

    def json_to_text(self, obj: Any, keep: Iterable[str] | None = None) -> str:
        """Convert JSON object to text format."""
        return json_to_text(obj, keep)

    # Vector database utility methods
    def simulate_vector_search(self, request):
        """Simulate vector search operation."""
        return self.vector_db.simulate_vector_search(request)

    def simulate_get_documents(self, request):
        """Simulate get documents operation."""
        return self.vector_db.simulate_get_documents(request)

    def simulate_add_document(self, request):
        """Simulate add document operation."""
        return self.vector_db.simulate_add_document(request)

    def simulate_get_document(self, document_id: str):
        """Simulate get document operation."""
        return self.vector_db.simulate_get_document(document_id)

    def simulate_update_document(self, document_id: str, data):
        """Simulate update document operation."""
        return self.vector_db.simulate_update_document(document_id, data)

    def simulate_delete_document(self, document_id: str):
        """Simulate delete document operation."""
        return self.vector_db.simulate_delete_document(document_id)

    def simulate_get_analytics(self, time_range: str):
        """Simulate get analytics operation."""
        return self.vector_db.simulate_get_analytics(time_range)

    def simulate_get_collections(self):
        """Simulate get collections operation."""
        return self.vector_db.simulate_get_collections()

    def simulate_export_data(self, request):
        """Simulate export data operation."""
        return self.vector_db.simulate_export_data(request)


# ============================================================================
# EXPORTS
# ============================================================================

# Export semantic utility functions
__all__ = ["flatten_json", "json_to_text", "VectorDatabaseUtils", "ConsolidatedUtils"]
