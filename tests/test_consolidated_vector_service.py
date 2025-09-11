#!/usr/bin/env python3
"""
Test Suite for Consolidated Vector Database Service
=================================================

Comprehensive pytest coverage for:
- Embedding generation and validation
- Vector database operations (store, search, delete)
- Multiple embedding model support
- Document indexing and retrieval
- Error handling and edge cases
- Performance and scalability tests

Author: Agent-1 (Integration & Core Systems Specialist)
Coverage Target: 85%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from pathlib import Path
import sys
from typing import List, Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.consolidated_vector_service import ConsolidatedVectorService
from services.models.vector_models import (
    EmbeddingModel,
    EmbeddingResult,
    VectorDocument,
    VectorDatabaseConfig,
    VectorDatabaseResult,
    VectorDatabaseStats,
    SearchQuery,
    SearchResult,
    CollectionConfig,
    DocumentType
)


class TestConsolidatedVectorService:
    """Test suite for ConsolidatedVectorService class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedVectorService(agent_id="test-agent")
        self.sample_texts = [
            "This is a test document for vector embeddings.",
            "Another sample text for testing purposes.",
            "Machine learning and AI are transforming technology."
        ]

    def teardown_method(self):
        """Cleanup test fixtures."""
        pass

    @pytest.mark.unit
    def test_service_initialization(self):
        """Test service initialization with different configurations."""
        # Test default initialization
        service = ConsolidatedVectorService()
        assert service.agent_id == "default"
        assert service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS
        assert service.config is not None

        # Test custom initialization
        custom_config = VectorDatabaseConfig(
            host="localhost",
            port=8080,
            collection_name="test_collection"
        )
        service_custom = ConsolidatedVectorService(
            agent_id="custom-agent",
            config=custom_config
        )
        assert service_custom.agent_id == "custom-agent"
        assert service_custom.config.collection_name == "test_collection"

    @pytest.mark.unit
    def test_embedding_generation_sentence_transformers(self):
        """Test embedding generation using sentence transformers."""
        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            embeddings = service.generate_embeddings(self.sample_texts[:2])

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 3
            assert all(isinstance(val, float) for val in embeddings[0])
            mock_encoder.encode.assert_called_once_with(self.sample_texts[:2])

    @pytest.mark.unit
    def test_embedding_generation_openai(self):
        """Test embedding generation using OpenAI."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1, 0.2, 0.3]),
            Mock(embedding=[0.4, 0.5, 0.6])
        ]
        mock_client.embeddings.create.return_value = mock_response

        with patch('services.consolidated_vector_service.openai.OpenAI', return_value=mock_client):
            service = ConsolidatedVectorService()
            service.embedding_model = EmbeddingModel.OPENAI
            embeddings = service.generate_embeddings(self.sample_texts[:2])

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 3
            mock_client.embeddings.create.assert_called_once()

    @pytest.mark.unit
    def test_embedding_generation_model_switching(self):
        """Test switching between embedding models."""
        service = ConsolidatedVectorService()

        # Start with sentence transformers
        assert service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS

        # Switch to OpenAI
        with patch('services.consolidated_vector_service.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
            mock_client.embeddings.create.return_value = mock_response
            mock_openai.return_value = mock_client

            embeddings = service.generate_embeddings(["test"], EmbeddingModel.OPENAI)
            assert service.embedding_model == EmbeddingModel.OPENAI
            assert len(embeddings) == 1

    @pytest.mark.unit
    def test_embedding_generation_unsupported_model(self):
        """Test error handling for unsupported embedding models."""
        service = ConsolidatedVectorService()

        with pytest.raises(ValueError, match="Unsupported model"):
            service.generate_embeddings(["test"], "unsupported_model")

    @pytest.mark.unit
    def test_embedding_generation_missing_dependencies(self):
        """Test error handling when dependencies are missing."""
        service = ConsolidatedVectorService()

        # Test missing sentence transformers
        with patch.dict('sys.modules', {'sentence_transformers': None}):
            with pytest.raises(ImportError, match="sentence-transformers not installed"):
                service._encode_sentence_transformers(["test"])

        # Test missing OpenAI
        with patch.dict('sys.modules', {'openai': None}):
            with pytest.raises(ImportError):
                service._encode_openai(["test"])

    @pytest.mark.unit
    def test_vector_document_creation(self):
        """Test VectorDocument creation and validation."""
        # Test basic document creation
        doc = VectorDocument(
            id="test-doc-1",
            content="Test document content",
            metadata={"type": "test", "version": "1.0"},
            document_type=DocumentType.TEXT
        )

        assert doc.id == "test-doc-1"
        assert doc.content == "Test document content"
        assert doc.metadata["type"] == "test"
        assert doc.document_type == DocumentType.TEXT

    @pytest.mark.unit
    def test_store_document_with_embeddings(self):
        """Test document storage with embedding generation."""
        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True, message="Stored successfully")

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            service._engine = mock_engine

            doc = VectorDocument(
                id="test-doc-1",
                content="Test content",
                metadata={"type": "test"}
            )

            result = service.store_document(doc)

            assert result.success is True
            mock_encoder.encode.assert_called_once()
            mock_engine.store.assert_called_once()

    @pytest.mark.unit
    def test_store_document_engine_failure(self):
        """Test document storage when engine fails."""
        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=False, message="Storage failed")

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            service._engine = mock_engine

            doc = VectorDocument(id="test-doc-1", content="Test content")
            result = service.store_document(doc)

            assert result.success is False
            assert result.message == "Storage failed"

    @pytest.mark.unit
    def test_search_documents(self):
        """Test document search functionality."""
        mock_engine = Mock()
        mock_search_result = SearchResult(
            documents=[
                VectorDocument(id="doc-1", content="Matching document"),
                VectorDocument(id="doc-2", content="Another match")
            ],
            scores=[0.95, 0.89],
            total_found=2
        )
        mock_engine.search.return_value = mock_search_result

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            service._engine = mock_engine

            query = SearchQuery(query="test query", limit=10)
            results = service.search_documents(query)

            assert len(results.documents) == 2
            assert results.scores[0] == 0.95
            mock_encoder.encode.assert_called_once()
            mock_engine.search.assert_called_once()

    @pytest.mark.unit
    def test_delete_document(self):
        """Test document deletion."""
        mock_engine = Mock()
        mock_engine.delete.return_value = VectorDatabaseResult(success=True, message="Deleted successfully")

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        result = service.delete_document("test-doc-1")

        assert result.success is True
        assert result.message == "Deleted successfully"
        mock_engine.delete.assert_called_once_with("test-doc-1")

    @pytest.mark.unit
    def test_get_document(self):
        """Test document retrieval."""
        mock_doc = VectorDocument(id="test-doc-1", content="Retrieved content")
        mock_engine = Mock()
        mock_engine.get.return_value = mock_doc

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        result = service.get_document("test-doc-1")

        assert result.id == "test-doc-1"
        assert result.content == "Retrieved content"
        mock_engine.get.assert_called_once_with("test-doc-1")

    @pytest.mark.unit
    def test_get_stats(self):
        """Test database statistics retrieval."""
        mock_stats = VectorDatabaseStats(
            total_documents=100,
            total_collections=5,
            index_size_mb=50.5
        )
        mock_engine = Mock()
        mock_engine.get_stats.return_value = mock_stats

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        stats = service.get_stats()

        assert stats.total_documents == 100
        assert stats.total_collections == 5
        assert stats.index_size_mb == 50.5
        mock_engine.get_stats.assert_called_once()

    @pytest.mark.unit
    def test_collection_management(self):
        """Test collection creation and management."""
        mock_engine = Mock()
        mock_engine.create_collection.return_value = VectorDatabaseResult(success=True)
        mock_engine.list_collections.return_value = ["collection1", "collection2"]

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        # Test collection creation
        config = CollectionConfig(name="test_collection", dimension=384)
        result = service.create_collection(config)
        assert result.success is True
        mock_engine.create_collection.assert_called_once()

        # Test collection listing
        collections = service.list_collections()
        assert collections == ["collection1", "collection2"]
        mock_engine.list_collections.assert_called_once()

    @pytest.mark.unit
    def test_engine_initialization_failure(self):
        """Test service behavior when engine initialization fails."""
        with patch('services.consolidated_vector_service.VectorDatabaseEngine', side_effect=ImportError("Engine not available")):
            service = ConsolidatedVectorService()
            assert service._engine is None

            # Test that operations handle missing engine gracefully
            doc = VectorDocument(id="test", content="test")
            result = service.store_document(doc)
            assert result.success is False

    @pytest.mark.unit
    def test_empty_text_embedding(self):
        """Test embedding generation with empty text."""
        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            embeddings = service.generate_embeddings([""])

            assert len(embeddings) == 1
            assert len(embeddings[0]) == 0

    @pytest.mark.unit
    def test_multiple_text_embedding(self):
        """Test embedding generation with multiple texts."""
        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
                [0.7, 0.8, 0.9]
            ])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            embeddings = service.generate_embeddings(["text1", "text2", "text3"])

            assert len(embeddings) == 3
            assert all(len(emb) == 3 for emb in embeddings)
            mock_encoder.encode.assert_called_once()

    @pytest.mark.performance
    def test_embedding_generation_performance(self):
        """Test embedding generation performance."""
        import time

        large_texts = ["Test document " * 100] * 10

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.random.rand(10, 384)
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()

            start_time = time.time()
            embeddings = service.generate_embeddings(large_texts)
            end_time = time.time()

            assert len(embeddings) == 10
            assert end_time - start_time < 5.0  # Should complete within 5 seconds

    @pytest.mark.unit
    def test_search_query_validation(self):
        """Test search query validation and processing."""
        service = ConsolidatedVectorService()

        # Test basic query
        query = SearchQuery(query="test search", limit=5)
        assert query.query == "test search"
        assert query.limit == 5

        # Test query with filters
        query_with_filters = SearchQuery(
            query="filtered search",
            limit=10,
            filters={"type": "document", "category": "test"}
        )
        assert query_with_filters.filters["type"] == "document"

    @pytest.mark.unit
    def test_document_type_handling(self):
        """Test different document types."""
        service = ConsolidatedVectorService()

        doc_types = [DocumentType.TEXT, DocumentType.CODE, DocumentType.JSON]

        for doc_type in doc_types:
            doc = VectorDocument(
                id=f"test-{doc_type.value}",
                content="Test content",
                document_type=doc_type
            )
            assert doc.document_type == doc_type

    @pytest.mark.unit
    def test_error_handling_engine_operations(self):
        """Test error handling for engine operations."""
        mock_engine = Mock()
        mock_engine.store.side_effect = Exception("Engine error")
        mock_engine.search.side_effect = Exception("Search error")
        mock_engine.delete.side_effect = Exception("Delete error")

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        # Test store error
        doc = VectorDocument(id="test", content="test")
        result = service.store_document(doc)
        assert result.success is False

        # Test search error
        query = SearchQuery(query="test")
        with pytest.raises(Exception):
            service.search_documents(query)

        # Test delete error
        with pytest.raises(Exception):
            service.delete_document("test-id")

    @pytest.mark.unit
    def test_configuration_validation(self):
        """Test configuration validation and defaults."""
        # Test default configuration
        config = VectorDatabaseConfig()
        assert config.host == "localhost"
        assert config.port == 6333
        assert config.collection_name == "default_collection"

        # Test custom configuration
        custom_config = VectorDatabaseConfig(
            host="custom-host",
            port=8080,
            collection_name="custom_collection"
        )
        assert custom_config.host == "custom-host"
        assert custom_config.port == 8080
        assert custom_config.collection_name == "custom_collection"

    @pytest.mark.unit
    def test_service_state_management(self):
        """Test service state management and cleanup."""
        service = ConsolidatedVectorService()

        # Test initial state
        assert service.agent_id is not None
        assert service.config is not None

        # Test embedding model state
        assert service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS

        # Test that service can be reused
        embeddings1 = service.generate_embeddings(["test1"])
        embeddings2 = service.generate_embeddings(["test2"])

        # Both should succeed (implementation details may vary)
        assert isinstance(embeddings1, list)
        assert isinstance(embeddings2, list)


# Integration Tests
class TestVectorServiceIntegration:
    """Integration tests for vector service components."""

    @pytest.mark.integration
    def test_full_vector_workflow(self):
        """Test complete vector workflow from embedding to search."""
        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True)
        mock_engine.search.return_value = SearchResult(
            documents=[VectorDocument(id="test-doc", content="Found document")],
            scores=[0.95],
            total_found=1
        )

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            service = ConsolidatedVectorService()
            service._engine = mock_engine

            # Store document
            doc = VectorDocument(id="test-doc", content="Test document for integration")
            store_result = service.store_document(doc)
            assert store_result.success is True

            # Search for document
            query = SearchQuery(query="test search")
            search_results = service.search_documents(query)
            assert len(search_results.documents) == 1
            assert search_results.documents[0].id == "test-doc"

    @pytest.mark.integration
    def test_model_switching_workflow(self):
        """Test switching between embedding models in workflow."""
        service = ConsolidatedVectorService()

        # Test switching from sentence transformers to OpenAI
        with patch('services.consolidated_vector_service.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
            mock_client.embeddings.create.return_value = mock_response
            mock_openai.return_value = mock_client

            # Switch to OpenAI and generate embeddings
            embeddings = service.generate_embeddings(["test"], EmbeddingModel.OPENAI)
            assert len(embeddings) == 1
            assert service.embedding_model == EmbeddingModel.OPENAI

    @pytest.mark.integration
    def test_batch_operations(self):
        """Test batch document operations."""
        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True)
        mock_engine.delete.return_value = VectorDatabaseResult(success=True)

        service = ConsolidatedVectorService()
        service._engine = mock_engine

        # Create batch of documents
        docs = [
            VectorDocument(id=f"batch-doc-{i}", content=f"Content {i}")
            for i in range(5)
        ]

        # Store batch
        for doc in docs:
            result = service.store_document(doc)
            assert result.success is True

        # Delete batch
        for doc in docs:
            result = service.delete_document(doc.id)
            assert result.success is True

        # Verify engine was called correct number of times
        assert mock_engine.store.call_count == 5
        assert mock_engine.delete.call_count == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/services/consolidated_vector_service",
                "--cov-report=html", "--cov-report=term-missing"])
