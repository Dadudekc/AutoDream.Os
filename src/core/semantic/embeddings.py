"""
Simple embedding provider for semantic search.
Uses hash-based embeddings for demonstration - replace with real embeddings as needed.
"""

from __future__ import annotations

import hashlib

import numpy as np


class EmbeddingProvider:
    """Simple embedding provider using hash functions."""

    def __init__(self, dim: int = 128):
        self.dim = dim

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Convert texts to embeddings using hash functions."""
        embeddings = []
        for text in texts:
            # Simple hash-based embedding for demonstration
            hash_obj = hashlib.md5(text.encode(), usedforsecurity=False)
            hash_bytes = hash_obj.digest()

            # Convert to numpy array and normalize
            embedding = np.frombuffer(hash_bytes, dtype=np.uint8).astype(np.float32)
            # Pad or truncate to desired dimension
            if len(embedding) < self.dim:
                embedding = np.pad(embedding, (0, self.dim - len(embedding)))
            else:
                embedding = embedding[: self.dim]

            # Normalize to unit vector
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            embeddings.append(embedding)

        return np.array(embeddings)


def build_provider(cfg: dict) -> EmbeddingProvider:
    """Build embedding provider from config."""
    embedding_cfg = cfg.get("embedding", {})
    dim = embedding_cfg.get("dim", 128)
    return EmbeddingProvider(dim=dim)
