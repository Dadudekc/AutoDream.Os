#!/usr/bin/env python3
"""
Embeddings Backend Base Class
=============================

Abstract base class for embedding backends.
V2 Compliance: ≤400 lines, focused interface definition.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np


class EmbeddingsBackend(ABC):
    """Abstract base class for embedding backends."""
    
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Embed a list of texts into vectors.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        pass
    
    @abstractmethod
    def add(self, ids: List[int], vectors: np.ndarray) -> None:
        """
        Add vectors to the index.
        
        Args:
            ids: List of document IDs
            vectors: numpy array of vectors to add
        """
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 10) -> List[Tuple[int, float]]:
        """
        Search for similar vectors.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (doc_id, similarity_score) tuples
        """
        pass
    
    @abstractmethod
    def persist(self) -> None:
        """Persist the index to disk."""
        pass
    
    @abstractmethod
    def get_stats(self) -> dict:
        """Get backend statistics."""
        pass




