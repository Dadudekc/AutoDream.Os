#!/usr/bin/env python3
"""
EMERGENCY UNIT TESTS - Consolidated Vector Service
==================================================

CRITICAL UNIT TESTING for Agent-1 Emergency Pytest Assignment:
- Vector database operations (233 lines)
- Embedding generation and validation
- Document storage and retrieval
- Search functionality testing

Target: 95%+ unit test coverage for vector service
Execution: IMMEDIATE - PYTEST_MODE_ACTIVE

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: EMERGENCY PYTEST COVERAGE - UNIT TESTING EXECUTION
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

try:
    from services.consolidated_vector_service import ConsolidatedVectorService
    from services.models.vector_models import (
        EmbeddingModel,
        VectorDocument,
        VectorDatabaseConfig,
        VectorDatabaseResult,
        SearchQuery,
        SearchResult
    )
    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False


@pytest.mark.unit
class TestConsolidatedVectorServiceUnit:
    """Unit tests for ConsolidatedVectorService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedVectorService(agent_id="test-agent")
        self.sample_texts = ["Test document one", "Test document two"]
        self.sample_doc = VectorDocument(
            id="test-doc-1",
            content="Test document content",
            metadata={"type": "test", "version": "1.0"}
        )

    @pytest.mark.unit
    def test_service_initialization_unit(self):
        """UNIT TEST: Test vector service initialization."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedVectorService()
        assert service.agent_id == "default"
        assert service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS
        assert service.config is not None

        # Test custom initialization
        custom_config = VectorDatabaseConfig(collection_name="test_collection")
        service_custom = ConsolidatedVectorService(
            agent_id="custom-agent",
            config=custom_config
        )
        assert service_custom.agent_id == "custom-agent"
        assert service_custom.config.collection_name == "test_collection"

    @pytest.mark.unit
    def test_embedding_generation_sentence_transformers(self):
        """UNIT TEST: Test embedding generation with sentence transformers."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_encoder = Mock()
        mock_encoder.encode.return_value = np.array([
            [0.1, 0.2, 0.3, 0.4, 0.5],
            [0.6, 0.7, 0.8, 0.9, 1.0]
        ])

        with patch('services.consolidated_vector_service.SentenceTransformer', return_value=mock_encoder):
            embeddings = self.service.generate_embeddings(self.sample_texts)

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 5
            assert all(isinstance(val, float) for val in embeddings[0])
            mock_encoder.encode.assert_called_once_with(self.sample_texts)

    @pytest.mark.unit
    def test_embedding_generation_openai(self):
        """UNIT TEST: Test embedding generation with OpenAI."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1, 0.2, 0.3, 0.4, 0.5]),
            Mock(embedding=[0.6, 0.7, 0.8, 0.9, 1.0])
        ]
        mock_client.embeddings.create.return_value = mock_response

        with patch('services.consolidated_vector_service.openai.OpenAI', return_value=mock_client):
            self.service.embedding_model = EmbeddingModel.OPENAI
            embeddings = self.service.generate_embeddings(self.sample_texts)

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 5
            mock_client.embeddings.create.assert_called_once()

    @pytest.mark.unit
    def test_embedding_model_switching(self):
        """UNIT TEST: Test switching between embedding models."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Start with sentence transformers
        assert self.service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS

        # Switch to OpenAI and test
        with patch('services.consolidated_vector_service.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
            mock_client.embeddings.create.return_value = mock_response
            mock_openai.return_value = mock_client

            embeddings = self.service.generate_embeddings(["test"], EmbeddingModel.OPENAI)
            assert self.service.embedding_model == EmbeddingModel.OPENAI
            assert len(embeddings) == 1

    @pytest.mark.unit
    def test_embedding_generation_unsupported_model(self):
        """UNIT TEST: Test error handling for unsupported embedding models."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with pytest.raises(ValueError, match="Unsupported model"):
            self.service.generate_embeddings(["test"], "unsupported_model")

    @pytest.mark.unit
    def test_embedding_generation_missing_dependencies(self):
        """UNIT TEST: Test error handling when dependencies are missing."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test missing sentence transformers
        with patch.dict('sys.modules', {'sentence_transformers': None}):
            with pytest.raises(ImportError, match="sentence-transformers not installed"):
                self.service._encode_sentence_transformers(["test"])

        # Test missing OpenAI
        with patch.dict('sys.modules', {'openai': None}):
            with pytest.raises(ImportError):
                self.service._encode_openai(["test"])

    @pytest.mark.unit
    def test_store_document_success(self):
        """UNIT TEST: Test successful document storage."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True, message="Stored successfully")

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            with patch.object(self.service, '_engine', mock_engine):
                result = self.service.store_document(self.sample_doc)

                assert result.success is True
                assert result.message == "Stored successfully"
                mock_encoder.encode.assert_called_once()
                mock_engine.store.assert_called_once()

    @pytest.mark.unit
    def test_store_document_failure(self):
        """UNIT TEST: Test document storage failure."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=False, message="Storage failed")

        with patch.object(self.service, '_engine', mock_engine):
            result = self.service.store_document(self.sample_doc)

            assert result.success is False
            assert result.message == "Storage failed"

    @pytest.mark.unit
    def test_search_documents_unit(self):
        """UNIT TEST: Test document search functionality."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_search_result = SearchResult(
            documents=[
                VectorDocument(id="doc-1", content="Found document 1"),
                VectorDocument(id="doc-2", content="Found document 2")
            ],
            scores=[0.95, 0.89],
            total_found=2
        )
        mock_engine.search.return_value = mock_search_result

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_transformer.return_value = mock_encoder

            with patch.object(self.service, '_engine', mock_engine):
                query = SearchQuery(query="test search", limit=10)
                results = self.service.search_documents(query)

                assert len(results.documents) == 2
                assert results.scores[0] == 0.95
                assert results.total_found == 2
                mock_encoder.encode.assert_called_once()
                mock_engine.search.assert_called_once()

    @pytest.mark.unit
    def test_delete_document_unit(self):
        """UNIT TEST: Test document deletion."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_engine.delete.return_value = VectorDatabaseResult(success=True, message="Deleted successfully")

        with patch.object(self.service, '_engine', mock_engine):
            result = self.service.delete_document("test-doc-1")

            assert result.success is True
            assert result.message == "Deleted successfully"
            mock_engine.delete.assert_called_once_with("test-doc-1")

    @pytest.mark.unit
    def test_get_document_unit(self):
        """UNIT TEST: Test document retrieval."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        expected_doc = VectorDocument(id="test-doc-1", content="Retrieved content")
        mock_engine = Mock()
        mock_engine.get.return_value = expected_doc

        with patch.object(self.service, '_engine', mock_engine):
            result = self.service.get_document("test-doc-1")

            assert result.id == "test-doc-1"
            assert result.content == "Retrieved content"
            mock_engine.get.assert_called_once_with("test-doc-1")

    @pytest.mark.unit
    def test_get_stats_unit(self):
        """UNIT TEST: Test database statistics retrieval."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_stats = Mock()
        mock_stats.total_documents = 100
        mock_stats.total_collections = 5
        mock_stats.index_size_mb = 50.5

        mock_engine = Mock()
        mock_engine.get_stats.return_value = mock_stats

        with patch.object(self.service, '_engine', mock_engine):
            stats = self.service.get_stats()

            assert stats.total_documents == 100
            assert stats.total_collections == 5
            assert stats.index_size_mb == 50.5
            mock_engine.get_stats.assert_called_once()

    @pytest.mark.unit
    def test_collection_management_unit(self):
        """UNIT TEST: Test collection creation and management."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_engine.create_collection.return_value = VectorDatabaseResult(success=True)
        mock_engine.list_collections.return_value = ["collection1", "collection2"]

        with patch.object(self.service, '_engine', mock_engine):
            # Test collection creation
            config = Mock()
            config.name = "test_collection"
            result = self.service.create_collection(config)
            assert result.success is True
            mock_engine.create_collection.assert_called_once()

            # Test collection listing
            collections = self.service.list_collections()
            assert collections == ["collection1", "collection2"]
            mock_engine.list_collections.assert_called_once()

    @pytest.mark.unit
    def test_engine_initialization_failure(self):
        """UNIT TEST: Test service behavior when engine initialization fails."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_vector_service.VectorDatabaseEngine', side_effect=ImportError("Engine not available")):
            service = ConsolidatedVectorService()
            assert service._engine is None

            # Test that operations handle missing engine gracefully
            result = service.store_document(self.sample_doc)
            assert result.success is False

    @pytest.mark.unit
    def test_empty_text_embedding_unit(self):
        """UNIT TEST: Test embedding generation with empty text."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([[]])
            mock_transformer.return_value = mock_encoder

            embeddings = self.service.generate_embeddings([""])
            assert len(embeddings) == 1
            assert len(embeddings[0]) == 0

    @pytest.mark.unit
    def test_multiple_text_embedding_unit(self):
        """UNIT TEST: Test embedding generation with multiple texts."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.array([
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
                [0.7, 0.8, 0.9]
            ])
            mock_transformer.return_value = mock_encoder

            embeddings = self.service.generate_embeddings(["text1", "text2", "text3"])
            assert len(embeddings) == 3
            assert all(len(emb) == 3 for emb in embeddings)

    @pytest.mark.unit
    def test_document_validation_unit(self):
        """UNIT TEST: Test VectorDocument validation."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test valid document
        doc = VectorDocument(
            id="test-doc",
            content="Test content",
            metadata={"type": "test"}
        )
        assert doc.id == "test-doc"
        assert doc.content == "Test content"
        assert doc.metadata["type"] == "test"

        # Test document with empty content
        empty_doc = VectorDocument(id="empty-doc", content="")
        assert empty_doc.content == ""

    @pytest.mark.unit
    def test_search_query_validation_unit(self):
        """UNIT TEST: Test SearchQuery validation."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test basic query
        query = SearchQuery(query="test search", limit=5)
        assert query.query == "test search"
        assert query.limit == 5

        # Test query with filters
        query_with_filters = SearchQuery(
            query="filtered search",
            limit=10,
            filters={"type": "document"}
        )
        assert query_with_filters.filters["type"] == "document"

    @pytest.mark.unit
    def test_error_handling_engine_operations(self):
        """UNIT TEST: Test error handling for engine operations."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_engine = Mock()
        mock_engine.store.side_effect = Exception("Engine error")
        mock_engine.search.side_effect = Exception("Search error")
        mock_engine.delete.side_effect = Exception("Delete error")

        with patch.object(self.service, '_engine', mock_engine):
            # Test store error
            result = self.service.store_document(self.sample_doc)
            assert result.success is False

            # Test search error
            query = SearchQuery(query="test")
            with pytest.raises(Exception):
                self.service.search_documents(query)

            # Test delete error
            with pytest.raises(Exception):
                self.service.delete_document("test-id")

    @pytest.mark.unit
    def test_configuration_validation_unit(self):
        """UNIT TEST: Test configuration validation."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

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

    @pytest.mark.performance
    def test_embedding_generation_performance_unit(self):
        """UNIT TEST: Test embedding generation performance."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        import time

        large_texts = ["Test document " * 10] * 5

        with patch('services.consolidated_vector_service.SentenceTransformer') as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = np.random.rand(5, 384)
            mock_transformer.return_value = mock_encoder

            start_time = time.time()
            embeddings = self.service.generate_embeddings(large_texts)
            end_time = time.time()

            assert len(embeddings) == 5
            assert end_time - start_time < 2.0  # Should complete within 2 seconds

    @pytest.mark.unit
    def test_service_state_management_unit(self):
        """UNIT TEST: Test service state management."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test initial state
        assert self.service.agent_id == "test-agent"
        assert self.service.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS

        # Test state changes
        self.service.embedding_model = EmbeddingModel.OPENAI
        assert self.service.embedding_model == EmbeddingModel.OPENAI

        # Test that service maintains state
        assert self.service.agent_id == "test-agent"


@pytest.mark.unit
class TestVectorServiceEdgeCases:
    """Unit tests for vector service edge cases."""

    @pytest.mark.unit
    def test_extreme_document_sizes(self):
        """UNIT TEST: Test handling of extreme document sizes."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedVectorService()

        # Test very large document
        large_content = "A" * 10000
        large_doc = VectorDocument(id="large-doc", content=large_content)

        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True)

        with patch.object(service, '_engine', mock_engine):
            result = service.store_document(large_doc)
            assert result.success is True

        # Test empty document
        empty_doc = VectorDocument(id="empty-doc", content="")
        with patch.object(service, '_engine', mock_engine):
            result = service.store_document(empty_doc)
            assert result.success is True

    @pytest.mark.unit
    def test_special_characters_in_documents(self):
        """UNIT TEST: Test handling of special characters in documents."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedVectorService()

        special_contents = [
            "Document with unicode: 🚀🐝💻",
            "Document with quotes: \"Hello World\"",
            "Document with newlines:\nLine 1\nLine 2",
            "Document with special chars: !@#$%^&*()",
        ]

        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True)

        for content in special_contents:
            doc = VectorDocument(id=f"special-doc-{len(content)}", content=content)
            with patch.object(service, '_engine', mock_engine):
                result = service.store_document(doc)
                assert result.success is True

    @pytest.mark.unit
    def test_concurrent_operations_simulation(self):
        """UNIT TEST: Test concurrent operations simulation."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedVectorService()

        # Simulate concurrent document operations
        docs = [
            VectorDocument(id=f"concurrent-doc-{i}", content=f"Content {i}")
            for i in range(5)
        ]

        mock_engine = Mock()
        mock_engine.store.return_value = VectorDatabaseResult(success=True)

        with patch.object(service, '_engine', mock_engine):
            results = []
            for doc in docs:
                result = service.store_document(doc)
                results.append(result)

            assert all(result.success for result in results)
            assert mock_engine.store.call_count == 5


if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--cov=src/services/consolidated_vector_service",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--tb=short"
    ])
