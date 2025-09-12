"""
Semantic search package for agent coordination intelligence.
"""

from .status_index import StatusIndex
from .utils import json_to_text, flatten_json
from .embeddings import EmbeddingProvider, build_provider
from .vector_store import VectorStore
from .semantic_router import SemanticRouter
from .router_hooks import route_message, similar_status

__all__ = [
    "StatusIndex",
    "json_to_text",
    "flatten_json",
    "EmbeddingProvider",
    "build_provider",
    "VectorStore",
    "SemanticRouter",
    "route_message",
    "similar_status"
]
