#!/usr/bin/env python3
"""
Unified Vector Integration Service - V2 Compliant Consolidation
===============================================================

Consolidated from multiple vector integration files into single service.
V2 Compliance: < 400 lines, SOLID principles, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Phase 2 Consolidation - Chunk SVC-02 (Vector Integration)
"""

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class VectorDocument:
    """Vector document structure."""

    id: str
    content: str
    embedding: list[float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class VectorSearchResult:
    """Vector search result structure."""

    document: VectorDocument
    score: float


@dataclass
class VectorIntegrationConfig:
    """Configuration for vector integration."""

    embedding_model: str = "sentence-transformers"
    vector_db_type: str = "chroma"
    collection_name: str = "agent_vectors"
    similarity_threshold: float = 0.7
    max_results: int = 10


class UnifiedVectorIntegration:
    """
    Consolidated vector database and embedding service integration.
    Single responsibility: unified vector operations with caching and search.
    """

    def __init__(self, config: VectorIntegrationConfig | None = None):
        self.config = config or VectorIntegrationConfig()
        self.logger = logging.getLogger(__name__)
        self._initialized = False
        self._document_cache: dict[str, VectorDocument] = {}
        self._embedding_cache: dict[str, list[float]] = {}

    async def initialize(self) -> bool:
        """Initialize the vector integration service."""
        try:
            self.logger.info("Initializing UnifiedVectorIntegration...")
            self._initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize: {e}")
            return False

    async def store_document(self, document: VectorDocument) -> str:
        """Store document with embedding in vector database."""
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        # Generate embedding if not provided
        if document.embedding is None:
            document.embedding = await self.generate_embedding(document.content)

        # Cache document
        self._document_cache[document.id] = document
        self._embedding_cache[document.id] = document.embedding

        # Simulate vector DB storage (would integrate with actual DB)
        self.logger.info(f"Stored document: {document.id}")
        return document.id

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using configured model."""
        # Check cache first
        cache_key = hash(text)
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]

        # Generate embedding based on model
        if self.config.embedding_model == "sentence-transformers":
            embedding = self._generate_sentence_transformer_embedding(text)
        elif self.config.embedding_model == "openai":
            embedding = await self._generate_openai_embedding(text)
        else:
            embedding = self._generate_fallback_embedding(text)

        # Cache result
        self._embedding_cache[cache_key] = embedding
        return embedding

    def _generate_sentence_transformer_embedding(self, text: str) -> list[float]:
        """Generate embedding using sentence transformers."""
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer("all-MiniLM-L6-v2")
            return model.encode(text).tolist()
        except ImportError:
            return self._generate_fallback_embedding(text)

    async def _generate_openai_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI."""
        try:
            import openai

            # Simplified OpenAI call - would need actual API key
            return [0.1] * 384  # Placeholder
        except ImportError:
            return self._generate_fallback_embedding(text)

    def _generate_fallback_embedding(self, text: str) -> list[float]:
        """Generate fallback hash-based embedding."""
        hash_obj = hashlib.md5(text.encode(), usedforsecurity=False)
        hash_bytes = hash_obj.digest()
        embedding = []
        for i in range(0, len(hash_bytes), 4):
            chunk = hash_bytes[i : i + 4]
            value = int.from_bytes(chunk, byteorder="big", signed=False)
            normalized = (value / 2**32) * 2 - 1
            embedding.append(normalized)
        return embedding[:384]

    async def search_similar(
        self, query: str, limit: int | None = None
    ) -> list[VectorSearchResult]:
        """Search for documents similar to query."""
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        limit = limit or self.config.max_results
        query_embedding = await self.generate_embedding(query)

        results = []
        # Simulate similarity search (would use actual vector DB)
        for doc_id, doc in self._document_cache.items():
            if doc.embedding:
                # Simple cosine similarity approximation
                similarity = sum(
                    a * b for a, b in zip(query_embedding[:10], doc.embedding[:10], strict=False)
                )
                if similarity >= self.config.similarity_threshold:
                    results.append(VectorSearchResult(document=doc, score=similarity))

        # Sort and limit results
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    async def get_agent_context(self, agent_id: str) -> dict[str, Any]:
        """Get vector-based context for agent."""
        query = f"agent {agent_id} context"
        similar_docs = await self.search_similar(query, limit=5)

        return {
            "agent_id": agent_id,
            "similar_documents": len(similar_docs),
            "context_documents": [
                {
                    "id": doc.document.id,
                    "content": doc.document.content[:200] + "...",
                    "score": doc.score,
                }
                for doc in similar_docs
            ],
        }

    async def update_agent_vectors(self, agent_id: str, data: dict[str, Any]) -> bool:
        """Update agent vector representations."""
        try:
            content = f"Agent {agent_id} data: {str(data)}"
            document = VectorDocument(
                id=f"agent_{agent_id}_{datetime.now().isoformat()}",
                content=content,
                metadata={"agent_id": agent_id, **data},
            )
            await self.store_document(document)
            return True
        except Exception as e:
            self.logger.error(f"Failed to update agent vectors: {e}")
            return False

    async def get_stats(self) -> dict[str, Any]:
        """Get service statistics."""
        return {
            "initialized": self._initialized,
            "cached_documents": len(self._document_cache),
            "cached_embeddings": len(self._embedding_cache),
            "embedding_model": self.config.embedding_model,
        }


# Factory function for V2 compliance
def create_unified_vector_integration(config: VectorIntegrationConfig | None = None):
    """Factory function for UnifiedVectorIntegration."""
    return UnifiedVectorIntegration(config)


# Legacy compatibility functions
async def store_embedding(data: dict) -> str:
    """Legacy compatibility - redirects to unified service."""
    import warnings

    warnings.warn("store_embedding deprecated, use UnifiedVectorIntegration", DeprecationWarning)

    service = UnifiedVectorIntegration()
    await service.initialize()
    doc = VectorDocument(id=str(hash(str(data))), content=str(data), metadata=data)
    return await service.store_document(doc)


__all__ = [
    "UnifiedVectorIntegration",
    "VectorDocument",
    "VectorSearchResult",
    "VectorIntegrationConfig",
    "create_unified_vector_integration",
    "store_embedding",
]
