"""
Embedding Service - V2 Compliance Module
=======================================

Text embedding service for vector operations.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from .models.vector_models import EmbeddingModel, EmbeddingResult


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self, model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS):

EXAMPLE USAGE:
==============

# Import the service
from src.services.embedding_service import Embedding_ServiceService

# Initialize service
service = Embedding_ServiceService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Embedding_ServiceService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Initialize embedding service."""
        self.model = model
        self._sentence_transformer = None
        self._openai_client = None

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts to embeddings."""
        if self.model == EmbeddingModel.SENTENCE_TRANSFORMERS:
            return self._encode_sentence_transformers(texts)
        elif self.model == EmbeddingModel.OPENAI:
            return self._encode_openai(texts)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def _encode_sentence_transformers(self, texts: list[str]) -> list[list[float]]:
        """Encode using sentence transformers."""
        try:
            if self._sentence_transformer is None:
                from sentence_transformers import SentenceTransformer

                self._sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

            embeddings = self._sentence_transformer.encode(texts)
            return embeddings.tolist()
        except ImportError:
            raise ImportError("sentence-transformers not installed")

    def _encode_openai(self, texts: list[str]) -> list[list[float]]:
        """Encode using OpenAI."""
        try:
            if self._openai_client is None:
                import openai

                self._openai_client = openai.OpenAI()

            embeddings = []
            for text in texts:
                response = self._openai_client.embeddings.create(
                    input=text, model="text-embedding-ada-002"
                )
                embeddings.append(response.data[0].embedding)

            return embeddings
        except ImportError:
            raise ImportError("openai not installed")

    def get_embedding_result(self, text: str) -> EmbeddingResult:
        """Get embedding result for text."""
        import time

        start_time = time.time()

        try:
            embedding = self.encode([text])[0]
            processing_time = time.time() - start_time

            return EmbeddingResult(
                document_id="test",
                embedding=embedding,
                model=self.model,
                tokens_used=len(text.split()),  # Approximate
                processing_time=processing_time,
                success=True,
            )
        except Exception as e:
            processing_time = time.time() - start_time
            return EmbeddingResult(
                document_id="test",
                embedding=[],
                model=self.model,
                tokens_used=0,
                processing_time=processing_time,
                success=False,
                error_message=str(e),
            )
