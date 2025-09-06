#!/usr/bin/env python3
"""
Embedding Service - Agent Cellphone V2
=====================================

Service for generating text embeddings using various models.
Supports sentence transformers, OpenAI embeddings, and custom models.

V2 Compliance: < 300 lines, single responsibility, embedding generation.

Author: Agent-7 - Web Development Specialist
License: MIT
"""


# Import dependencies with fallbacks for testing
try:
    import openai
except ImportError:
    openai = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

import logging
from ..services.models.vector_models import EmbeddingModel
from typing import List, Optional


class EmbeddingService:
    """Service for generating text embeddings.

    Supports multiple embedding models with fallback mechanisms.
    """

    def __init__(self, model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMERS):
        """Initialize embedding service.

        Args:
            model: Default embedding model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self._sentence_transformer = None
        self._openai_client = None

    def _get_sentence_transformer(self):
        """Lazy load sentence transformer model."""
        if self._sentence_transformer is None:
            if SentenceTransformer is None:
                raise ImportError("❌ sentence-transformers not installed")
            try:
                self._sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
                self.get_logger(__name__).info("✅ Sentence transformer model loaded")
            except Exception as e:
                self.get_logger(__name__).error(
                    f"❌ Failed to load sentence transformer: {e}"
                )
                raise
        return self._sentence_transformer

    def _get_openai_client(self):
        """Lazy load OpenAI client."""
        if self._openai_client is None:
            if openai is None:
                raise ImportError("❌ OpenAI not installed")
            try:
                self._openai_client = openai.OpenAI()
                self.get_logger(__name__).info("✅ OpenAI client initialized")
            except Exception as e:
                self.get_logger(__name__).error(
                    f"❌ Failed to initialize OpenAI client: {e}"
                )
                raise
        return self._openai_client

    def generate_embedding(
        self, text: str, model: Optional[EmbeddingModel] = None
    ) -> List[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed
            model: Model to use (defaults to service model)

        Returns:
            List of embedding values
        """
        model = model or self.model
        start_time = time.time()

        try:
            if model == EmbeddingModel.SENTENCE_TRANSFORMERS:
                embedding = self._generate_sentence_transformer_embedding(text)
            elif get_unified_validator().validate_type(
                model, EmbeddingModel
            ) and model.value.startswith("openai"):
                embedding = self._generate_openai_embedding(text, model)
            elif get_unified_validator().validate_type(model, str) and model.startswith(
                "openai"
            ):
                # Handle string model names
                embedding_model = (
                    EmbeddingModel(model)
                    if model in [e.value for e in EmbeddingModel]
                    else EmbeddingModel.OPENAI
                )
                embedding = self._generate_openai_embedding(text, embedding_model)
            else:
                get_unified_validator().raise_validation_error(
                    f"Unsupported model: {model}"
                )

            processing_time = time.time() - start_time
            self.get_logger(__name__).debug(
                f"Generated embedding in {processing_time:.3f}s"
            )

            return embedding

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error generating embedding: {e}")
            raise

    def generate_embeddings_batch(
        self,
        texts: List[str],
        model: Optional[EmbeddingModel] = None,
        batch_size: int = 32,
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            model: Model to use
            batch_size: Batch size for processing

        Returns:
            List of embedding vectors
        """
        model = model or self.model
        start_time = time.time()

        try:
            if model == EmbeddingModel.SENTENCE_TRANSFORMERS:
                embeddings = self._generate_sentence_transformer_batch(
                    texts, batch_size
                )
            elif model.value.startswith("openai"):
                embeddings = self._generate_openai_batch(texts, model)
            else:
                get_unified_validator().raise_validation_error(
                    f"Unsupported model: {model}"
                )

            processing_time = time.time() - start_time
            self.get_logger(__name__).info(
                f"Generated {len(embeddings)} embeddings in {processing_time:.3f}s"
            )

            return embeddings

        except Exception as e:
            self.get_logger(__name__).error(
                f"❌ Error generating batch embeddings: {e}"
            )
            raise

    def _generate_sentence_transformer_embedding(self, text: str) -> List[float]:
        """Generate embedding using sentence transformers."""
        model = self._get_sentence_transformer()
        embedding = model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def _generate_sentence_transformer_batch(
        self, texts: List[str], batch_size: int
    ) -> List[List[float]]:
        """Generate batch embeddings using sentence transformers."""
        model = self._get_sentence_transformer()
        embeddings = model.encode(texts, batch_size=batch_size, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]

    def _generate_openai_embedding(
        self, text: str, model: EmbeddingModel
    ) -> List[float]:
        """Generate embedding using OpenAI API."""
        client = self._get_openai_client()

        # Map model enum to OpenAI model name
        model_mapping = {
            EmbeddingModel.OPENAI_ADA: "text-embedding-ada-002",
            EmbeddingModel.OPENAI_3_SMALL: "text-embedding-3-small",
            EmbeddingModel.OPENAI_3_LARGE: "text-embedding-3-large",
        }

        openai_model = model_mapping.get(model, "text-embedding-ada-002")

        response = client.embeddings.create(input=text, model=openai_model)

        return response.data[0].embedding

    def _generate_openai_batch(
        self, texts: List[str], model: EmbeddingModel
    ) -> List[List[float]]:
        """Generate batch embeddings using OpenAI API."""
        client = self._get_openai_client()

        # Map model enum to OpenAI model name
        model_mapping = {
            EmbeddingModel.OPENAI_ADA: "text-embedding-ada-002",
            EmbeddingModel.OPENAI_3_SMALL: "text-embedding-3-small",
            EmbeddingModel.OPENAI_3_LARGE: "text-embedding-3-large",
        }

        openai_model = model_mapping.get(model, "text-embedding-ada-002")

        response = client.embeddings.create(input=texts, model=openai_model)

        return [data.embedding for data in response.data]

    def get_embedding_dimension(self, model: Optional[EmbeddingModel] = None) -> int:
        """Get the dimension of embeddings for a model.

        Args:
            model: Model to check (defaults to service model)

        Returns:
            Embedding dimension
        """
        model = model or self.model

        if model == EmbeddingModel.SENTENCE_TRANSFORMERS:
            return 384  # all-MiniLM-L6-v2 dimension
        elif model == EmbeddingModel.OPENAI_ADA:
            return 1536
        elif model == EmbeddingModel.OPENAI_3_SMALL:
            return 1536
        elif model == EmbeddingModel.OPENAI_3_LARGE:
            return 3072
        else:
            get_unified_validator().raise_validation_error(
                f"Unknown model dimension: {model}"
            )

    def validate_text(self, text: str) -> bool:
        """Validate text for embedding generation.

        Args:
            text: Text to validate

        Returns:
            True if valid, False otherwise
        """
        if not text or not get_unified_validator().validate_type(text, str):
            return False

        # Check for reasonable length (OpenAI has token limits)
        if len(text) > 8000:  # Conservative limit
            self.get_logger(__name__).warning(
                f"Text length {len(text)} may exceed token limits"
            )
            return False

        return True

    def preprocess_text(self, text: str) -> str:
        """Preprocess text before embedding generation.

        Args:
            text: Raw text

        Returns:
            Preprocessed text
        """
        # Basic preprocessing
        text = text.strip()

        # Remove excessive whitespace

        text = re.sub(r"\s+", " ", text)

        return text
