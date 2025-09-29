"""
Swarm Brain Embeddings
======================

Embedding backends for semantic search and similarity.
Supports multiple backends: numpy (fallback), FAISS, Chroma, OpenAI.
"""

from .base import EmbeddingsBackend
from .numpy_backend import NumpyBackend

# Try to import optional backends
try:
    from .faiss_backend import FaissBackend
except ImportError:
    FaissBackend = None

try:
    from .openai_backend import OpenAIBackend
except ImportError:
    OpenAIBackend = None

try:
    from .chroma_backend import ChromaBackend
except ImportError:
    ChromaBackend = None

__all__ = ["EmbeddingsBackend", "NumpyBackend", "FaissBackend", "OpenAIBackend", "ChromaBackend"]
