#!/usr/bin/env python3
"""
Unified Vector Service - V2 Compliant Module
Consolidates vector database operations using Repository pattern
V2 Compliance: < 400 lines, single responsibility for all vector operations.
Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class EmbeddingModel(Enum):
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"


class DocumentType(Enum):
    MESSAGE = "message"
    STATUS = "status"
    CONTRACT = "contract"
    COORDINATE = "coordinate"
    GENERAL = "general"


@dataclass
class VectorDocument:
    id: str
    content: str
    document_type: DocumentType
    metadata: dict[str, Any]
    embedding: list[float] | None = None
    created_at: float | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


@dataclass
class SearchQuery:
    query: str
    collection_name: str = "default"
    limit: int = 10
    similarity_threshold: float = 0.7
    document_type: DocumentType | None = None


@dataclass
class SearchResult:
    document: VectorDocument
    similarity_score: float
    rank: int


@dataclass
class VectorDatabaseStats:
    total_documents: int
    total_collections: int
    total_embeddings: int
    last_updated: float


class VectorRepository(ABC):
    @abstractmethod
    def store_document(self, document: VectorDocument) -> bool:
        pass

    @abstractmethod
    def search_documents(self, query: SearchQuery) -> list[SearchResult]:
        pass

    @abstractmethod
    def get_document(self, document_id: str) -> VectorDocument | None:
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> bool:
        pass

    @abstractmethod
    def get_stats(self) -> VectorDatabaseStats:
        pass


class EmbeddingService:
    def __init__(self, model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS):
        self.model = model
        self.logger = logging.getLogger(__name__)
        self._sentence_transformer = None
        self._openai_client = None
        self.embedding_count = 0

    def generate_embedding(self, text: str) -> list[float]:
        try:
            self.embedding_count += 1
            if self.model == EmbeddingModel.SENTENCE_TRANSFORMERS:
                return self._generate_sentence_transformer_embedding(text)
            elif self.model == EmbeddingModel.OPENAI:
                return self._generate_openai_embedding(text)
            else:
                return self._generate_simple_embedding(text)
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return self._generate_simple_embedding(text)

    def _generate_sentence_transformer_embedding(self, text: str) -> list[float]:
        try:
            if self._sentence_transformer is None:
                try:
                    from sentence_transformers import SentenceTransformer

                    self._sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
                except ImportError:
                    self.logger.warning("Sentence transformers not available, using fallback")
                    return self._generate_simple_embedding(text)
            embedding = self._sentence_transformer.encode(text)
            return embedding.tolist()
        except Exception as e:
            self.logger.error(f"Error with sentence transformer: {e}")
            return self._generate_simple_embedding(text)

    def _generate_openai_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI."""
        try:
            if self._openai_client is None:
                # Lazy loading for V2 compliance
                try:
                    import openai

                    self._openai_client = openai.OpenAI()
                except ImportError:
                    self.logger.warning("OpenAI not available, using fallback")
                    return self._generate_simple_embedding(text)

            response = self._openai_client.embeddings.create(
                model="text-embedding-ada-002", input=text
            )
            return response.data[0].embedding

        except Exception as e:
            self.logger.error(f"Error with OpenAI: {e}")
            return self._generate_simple_embedding(text)

    def _generate_simple_embedding(self, text: str) -> list[float]:
        """Generate simple hash-based embedding as fallback."""
        # Simple hash-based embedding for V2 compliance
        import hashlib

        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert to float vector
        embedding = []
        for i in range(0, len(hash_bytes), 4):
            chunk = hash_bytes[i : i + 4]
            if len(chunk) == 4:
                value = int.from_bytes(chunk, byteorder="big")
                embedding.append(value / (2**32))  # Normalize to [0, 1]

        # Pad or truncate to 384 dimensions
        while len(embedding) < 384:
            embedding.append(0.0)
        embedding = embedding[:384]

        return embedding


class InMemoryVectorRepository(VectorRepository):
    """In-memory vector repository implementation."""

    def __init__(self):
        self.documents: dict[str, VectorDocument] = {}
        self.collections: dict[str, list[str]] = {"default": []}
        self.logger = logging.getLogger(__name__)
        self.embedding_service = EmbeddingService()

    def store_document(self, document: VectorDocument) -> bool:
        """Store a document in the vector database."""
        try:
            # Generate embedding if not provided
            if document.embedding is None:
                document.embedding = self.embedding_service.generate_embedding(document.content)

            # Store document
            self.documents[document.id] = document

            # Add to collection
            collection = self.collections.get(document.metadata.get("collection", "default"), [])
            if document.id not in collection:
                collection.append(document.id)
                self.collections[document.metadata.get("collection", "default")] = collection

            self.logger.info(f"Stored document {document.id}")
            return True

        except Exception as e:
            self.logger.error(f"Error storing document: {e}")
            return False

    def search_documents(self, query: SearchQuery) -> list[SearchResult]:
        """Search documents in the vector database."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(query.query)

            # Get documents from collection
            collection_docs = self.collections.get(query.collection_name, [])
            candidates = [
                self.documents[doc_id] for doc_id in collection_docs if doc_id in self.documents
            ]

            # Filter by document type if specified
            if query.document_type:
                candidates = [doc for doc in candidates if doc.document_type == query.document_type]

            # Calculate similarities
            results = []
            for doc in candidates:
                if doc.embedding:
                    similarity = self._calculate_similarity(query_embedding, doc.embedding)
                    if similarity >= query.similarity_threshold:
                        results.append(
                            SearchResult(
                                document=doc,
                                similarity_score=similarity,
                                rank=0,  # Will be set after sorting
                            )
                        )

            # Sort by similarity score
            results.sort(key=lambda x: x.similarity_score, reverse=True)

            # Set ranks and limit results
            for i, result in enumerate(results[: query.limit]):
                result.rank = i + 1

            self.logger.info(f"Found {len(results)} documents for query")
            return results[: query.limit]

        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            return []

    def get_document(self, document_id: str) -> VectorDocument | None:
        """Get a document by ID."""
        return self.documents.get(document_id)

    def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID."""
        try:
            if document_id in self.documents:
                document = self.documents[document_id]

                # Remove from collection
                collection_name = document.metadata.get("collection", "default")
                if collection_name in self.collections:
                    collection = self.collections[collection_name]
                    if document_id in collection:
                        collection.remove(document_id)

                # Remove document
                del self.documents[document_id]

                self.logger.info(f"Deleted document {document_id}")
                return True
            else:
                self.logger.warning(f"Document {document_id} not found")
                return False

        except Exception as e:
            self.logger.error(f"Error deleting document: {e}")
            return False

    def get_stats(self) -> VectorDatabaseStats:
        """Get database statistics."""
        total_embeddings = sum(1 for doc in self.documents.values() if doc.embedding)

        return VectorDatabaseStats(
            total_documents=len(self.documents),
            total_collections=len(self.collections),
            total_embeddings=total_embeddings,
            last_updated=time.time(),
        )

    def _calculate_similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        try:
            import math

            # Ensure same length
            min_len = min(len(embedding1), len(embedding2))
            embedding1 = embedding1[:min_len]
            embedding2 = embedding2[:min_len]

            # Calculate dot product
            dot_product = sum(a * b for a, b in zip(embedding1, embedding2, strict=False))

            # Calculate magnitudes
            magnitude1 = math.sqrt(sum(a * a for a in embedding1))
            magnitude2 = math.sqrt(sum(b * b for b in embedding2))

            # Calculate cosine similarity
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0

            similarity = dot_product / (magnitude1 * magnitude2)
            return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]

        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0


class UnifiedVectorService:
    """Unified vector service using Repository pattern."""

    def __init__(self, repository: VectorRepository | None = None):
        self.logger = logging.getLogger(__name__)
        self.repository = repository or InMemoryVectorRepository()
        self.embedding_service = EmbeddingService()
        self.operation_count = 0
        self.search_count = 0
        self.store_count = 0

    def store_message(
        self,
        content: str,
        agent_id: str,
        message_type: str = "message",
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Store a message in the vector database."""
        try:
            self.operation_count += 1
            self.store_count += 1

            document = VectorDocument(
                id=f"msg_{int(time.time() * 1000)}_{agent_id}",
                content=content,
                document_type=DocumentType.MESSAGE,
                metadata={
                    "agent_id": agent_id,
                    "message_type": message_type,
                    "collection": "agent_messages",
                    **(metadata or {}),
                },
            )

            success = self.repository.store_document(document)

            if success:
                self.logger.info(f"Stored message from {agent_id}")
            else:
                self.logger.error(f"Failed to store message from {agent_id}")

            return success

        except Exception as e:
            self.logger.error(f"Error storing message: {e}")
            return False

    def search_messages(
        self, query: str, agent_id: str | None = None, limit: int = 10
    ) -> list[SearchResult]:
        """Search messages in the vector database."""
        try:
            self.operation_count += 1
            self.search_count += 1

            search_query = SearchQuery(
                query=query,
                collection_name="agent_messages",
                limit=limit,
                document_type=DocumentType.MESSAGE,
            )

            results = self.repository.search_documents(search_query)

            # Filter by agent if specified
            if agent_id:
                results = [r for r in results if r.document.metadata.get("agent_id") == agent_id]

            self.logger.info(f"Found {len(results)} messages for query")
            return results

        except Exception as e:
            self.logger.error(f"Error searching messages: {e}")
            return []

    def get_service_statistics(self) -> dict[str, Any]:
        """Get service statistics."""
        db_stats = self.repository.get_stats()

        return {
            "operations": {
                "total_operations": self.operation_count,
                "store_operations": self.store_count,
                "search_operations": self.search_count,
            },
            "database": {
                "total_documents": db_stats.total_documents,
                "total_collections": db_stats.total_collections,
                "total_embeddings": db_stats.total_embeddings,
                "last_updated": db_stats.last_updated,
            },
            "embedding_service": {
                "model": self.embedding_service.model.value,
                "total_embeddings": self.embedding_service.embedding_count,
            },
        }


# Export main classes
__all__ = [
    "UnifiedVectorService",
    "VectorRepository",
    "InMemoryVectorRepository",
    "EmbeddingService",
    "VectorDocument",
    "SearchQuery",
    "SearchResult",
    "VectorDatabaseStats",
    "DocumentType",
    "EmbeddingModel",
]
