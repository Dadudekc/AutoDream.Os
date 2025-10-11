"""
Vector Database Handlers
========================

Handler facade for vector database operations.
Maps handler classes from utility modules for clean imports.

V2 Compliance: < 100 lines, facade pattern.

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Created: 2025-10-11 (fixing missing import)
"""

from .analytics_utils import AnalyticsUtils as AnalyticsHandler
from .collection_utils import CollectionUtils as CollectionHandler
from .document_utils import DocumentUtils as DocumentHandler
from .search_utils import SearchUtils as SearchHandler
from .utils import VectorDatabaseUtils as ExportHandler

__all__ = [
    "AnalyticsHandler",
    "CollectionHandler",
    "DocumentHandler",
    "ExportHandler",
    "SearchHandler",
]
