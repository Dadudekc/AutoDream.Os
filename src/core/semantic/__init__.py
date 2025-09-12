"""
Semantic search package for agent coordination intelligence.
"""

from .embeddings import EmbeddingProvider, build_provider
from .router_hooks import route_message, similar_status
from .semantic_router import SemanticRouter
from .status_index import StatusIndex
from .utils import flatten_json, json_to_text
from .vector_store import VectorStore

__all__ = [
    "StatusIndex",
    "json_to_text",
    "flatten_json",
    "EmbeddingProvider",
    "build_provider",
    "VectorStore",
    "SemanticRouter",
    "route_message",
    "similar_status",
]
