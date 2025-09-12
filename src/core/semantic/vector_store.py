"""
Simple vector store for semantic search.
Supports adding vectors and searching for nearest neighbors.
"""
from __future__ import annotations
from typing import Dict, List, Tuple, Any
import os
import json
import numpy as np
from pathlib import Path


class VectorStore:
    """Simple vector store with persistence."""

    def __init__(self, store_path: str, backend: str = "numpy", normalize: bool = True):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.backend = backend
        self.normalize = normalize

        # In-memory storage
        self.vectors: Dict[str, np.ndarray] = {}
        self.metadata: Dict[str, Dict] = {}

        # Load existing data
        self._load()

    def _load(self):
        """Load vectors and metadata from disk."""
        vectors_file = self.store_path / "vectors.npy"
        metadata_file = self.store_path / "metadata.json"

        if vectors_file.exists() and metadata_file.exists():
            try:
                # Load vectors
                vectors_dict = np.load(vectors_file, allow_pickle=True).item()
                self.vectors = vectors_dict

                # Load metadata
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)

            except Exception as e:
                print(f"Warning: Could not load vector store: {e}")

    def _save(self):
        """Save vectors and metadata to disk."""
        try:
            vectors_file = self.store_path / "vectors.npy"
            metadata_file = self.store_path / "metadata.json"

            # Save vectors
            np.save(vectors_file, self.vectors)

            # Save metadata
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Warning: Could not save vector store: {e}")

    def add(self, ids: List[str], vectors: np.ndarray, metadata: List[Dict] | None = None):
        """Add vectors to the store."""
        if metadata is None:
            metadata = [{}] * len(ids)

        for i, (id_val, vector, meta) in enumerate(zip(ids, vectors, metadata)):
            self.vectors[id_val] = vector.copy()
            self.metadata[id_val] = meta.copy()

        self._save()

    def search(self, query_vectors: np.ndarray, top_k: int = 3) -> List[List[Tuple[str, float, Dict]]]:
        """Search for nearest neighbors."""
        results = []

        for query_vector in query_vectors:
            similarities = []
            for id_val, vector in self.vectors.items():
                # Cosine similarity
                dot_product = np.dot(query_vector, vector)
                norm_q = np.linalg.norm(query_vector)
                norm_v = np.linalg.norm(vector)

                if norm_q > 0 and norm_v > 0:
                    similarity = dot_product / (norm_q * norm_v)
                else:
                    similarity = 0.0

                similarities.append((id_val, similarity, self.metadata.get(id_val, {})))

            # Sort by similarity (descending) and take top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            results.append(similarities[:top_k])

        return results
