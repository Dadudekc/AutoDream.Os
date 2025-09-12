# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import (
    status_indexer,
    vector_database_engine,
    vector_database_models,
    vector_database_orchestrator,
)

# Import service functions
from .vector_database_orchestrator import VectorDatabaseService

# Create global service instance
_vector_db_service = VectorDatabaseService()


def get_vector_database_service() -> VectorDatabaseService:
    """Get the global vector database service instance."""
    return _vector_db_service


def search_vector_database(query) -> list:
    """Search the vector database with SearchQuery object or string."""
    if isinstance(query, str):
        # Simple string query
        return _vector_db_service.search_documents(query, "agent_work", 10)
    else:
        # SearchQuery object - call the service's search_documents method
        return _vector_db_service.search_documents(query.query, query.collection_name, query.limit)


def add_document_to_vector_db(content: str, doc_type: str, metadata: dict = None) -> bool:
    """Add a document to the vector database."""
    return _vector_db_service.add_document(content, doc_type, metadata)


__all__ = [
    "status_indexer",
    "vector_database_engine",
    "vector_database_models",
    "vector_database_orchestrator",
    "get_vector_database_service",
    "search_vector_database",
    "add_document_to_vector_db",
]
