#!/usr/bin/env python3
"""
Numpy Embeddings Backend
========================

Zero-dependency fallback embedding backend using deterministic hashing.
V2 Compliance: ≤400 lines, focused embedding functionality.
"""

import numpy as np
import hashlib
import json
import logging
from pathlib import Path
from typing import List, Tuple
from .base import EmbeddingsBackend

logger = logging.getLogger(__name__)


class NumpyBackend(EmbeddingsBackend):
    """
    Deterministic bag-of-character-ngrams hashing encoder.
    Not state-of-the-art, but zero-dependency and good for scaffolding.
    """
    
    def __init__(self, index_dir: Path, dim: int = 1536):
        """Initialize the numpy backend."""
        self.index_dir = index_dir
        self.dim = dim
        self.vecs_path = index_dir / "vectors.npy"
        self.ids_path = index_dir / "ids.npy"
        self.meta_path = index_dir / "metadata.json"
        
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing index if available
        if self.vecs_path.exists() and self.ids_path.exists():
            self.vectors = np.load(self.vecs_path)
            self.ids = np.load(self.ids_path)
            logger.info(f"Loaded existing index with {len(self.vectors)} vectors")
        else:
            self.vectors = np.zeros((0, dim), dtype=np.float32)
            self.ids = np.zeros((0,), dtype=np.int64)
            logger.info("Created new empty index")
    
    def _hash_embed(self, text: str) -> np.ndarray:
        """Create deterministic embedding via hashed character n-grams."""
        text = (text or "").lower()
        dim = self.dim
        vector = np.zeros(dim, dtype=np.float32)
        
        # Use 5-gram character hashing
        for i in range(len(text) - 4):
            ngram = text[i:i+5].encode("utf-8")
            hash_val = int(hashlib.blake2b(ngram, digest_size=8).hexdigest(), 16)
            vector[hash_val % dim] += 1.0
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm == 0:
            norm = 1.0
        
        return (vector / norm).astype(np.float32)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed a list of texts."""
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        
        embeddings = np.stack([self._hash_embed(text) for text in texts], axis=0)
        logger.debug(f"Embedded {len(texts)} texts into {embeddings.shape}")
        return embeddings
    
    def add(self, ids: List[int], vectors: np.ndarray) -> None:
        """Add vectors to the index."""
        if len(ids) != len(vectors):
            raise ValueError("Number of IDs must match number of vectors")
        
        if len(vectors) == 0:
            return
        
        # Ensure vectors have correct dimension
        if vectors.shape[1] != self.dim:
            raise ValueError(f"Vector dimension {vectors.shape[1]} doesn't match expected {self.dim}")
        
        # Add to existing index
        self.vectors = np.concatenate([self.vectors, vectors], axis=0)
        self.ids = np.concatenate([self.ids, np.array(ids, dtype=np.int64)], axis=0)
        
        logger.debug(f"Added {len(ids)} vectors to index. Total: {len(self.vectors)}")
    
    def search(self, query: str, k: int = 10) -> List[Tuple[int, float]]:
        """Search for similar vectors."""
        if len(self.vectors) == 0:
            return []
        
        # Embed query
        query_vector = self._hash_embed(query)
        
        # Compute cosine similarities
        similarities = self.vectors @ query_vector
        
        # Get top-k results
        k = min(k, len(similarities))
        top_indices = np.argpartition(-similarities, k-1)[:k]
        top_indices = top_indices[np.argsort(-similarities[top_indices])]
        
        results = [(int(self.ids[i]), float(similarities[i])) for i in top_indices]
        logger.debug(f"Found {len(results)} results for query")
        
        return results
    
    def persist(self) -> None:
        """Persist the index to disk."""
        try:
            np.save(self.vecs_path, self.vectors)
            np.save(self.ids_path, self.ids)
            
            # Save metadata
            metadata = {
                "dim": self.dim,
                "num_vectors": len(self.vectors),
                "backend": "numpy",
                "version": "1.0"
            }
            with open(self.meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Persisted index with {len(self.vectors)} vectors")
            
        except Exception as e:
            logger.error(f"Failed to persist index: {e}")
            raise
    
    def get_stats(self) -> dict:
        """Get backend statistics."""
        return {
            "backend": "numpy",
            "dimension": self.dim,
            "num_vectors": len(self.vectors),
            "index_size_mb": (self.vectors.nbytes + self.ids.nbytes) / (1024 * 1024),
            "index_path": str(self.index_dir)
        }




