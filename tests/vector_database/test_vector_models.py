#!/usr/bin/env python3
"""
Vector Models Tests - Agent Cellphone V2
======================================

Unit tests for vector database models and schemas.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

    VectorDocument, SearchQuery, SearchResult, CollectionConfig,
    VectorDatabaseStats, DocumentType, EmbeddingModel, SearchType
)


class TestVectorDocument:
    """Test VectorDocument model."""

    def test_vector_document_creation(self):
        """Test basic document creation."""
        doc = VectorDocument(
            content="Test content",
            document_type=DocumentType.MESSAGE,
            agent_id="Agent-1"
        )

        assert doc.content == "Test content"
        assert doc.document_type == DocumentType.MESSAGE
        assert doc.agent_id == "Agent-1"
        assert doc.id is not None
        assert get_unified_validator().validate_type(doc.timestamp, datetime)

    def test_vector_document_to_dict(self):
        """Test document serialization."""
        doc = VectorDocument(
            content="Test content",
            document_type=DocumentType.MESSAGE,
            agent_id="Agent-1",
            tags=["test", "message"]
        )

        data = doc.to_dict()

        assert data["content"] == "Test content"
        assert data["document_type"] == "message"
        assert data["agent_id"] == "Agent-1"
        assert data["tags"] == ["test", "message"]
        assert "id" in data
        assert "timestamp" in data

    def test_vector_document_from_dict(self):
        """Test document deserialization."""
        data = {
            "id": "test-id",
            "content": "Test content",
            "document_type": "message",
            "agent_id": "Agent-1",
            "timestamp": "2024-01-01T12:00:00",
            "tags": ["test", "message"]
        }

        doc = VectorDocument.from_dict(data)

        assert doc.id == "test-id"
        assert doc.content == "Test content"
        assert doc.document_type == DocumentType.MESSAGE
        assert doc.agent_id == "Agent-1"
        assert doc.tags == ["test", "message"]


class TestSearchQuery:
    """Test SearchQuery model."""

    def test_search_query_creation(self):
        """Test basic search query creation."""
        query = SearchQuery(
            query_text="test query",
            search_type=SearchType.SIMILARITY,
            limit=10
        )

        assert query.query_text == "test query"
        assert query.search_type == SearchType.SIMILARITY
        assert query.limit == 10
        assert query.similarity_threshold == 0.7  # Default threshold value

    def test_search_query_with_filters(self):
        """Test search query with filters."""
        query = SearchQuery(
            query_text="test query",
            agent_id="Agent-1",
            document_type=DocumentType.MESSAGE,
            tags=["urgent"]
        )

        assert query.agent_id == "Agent-1"
        assert query.document_type == DocumentType.MESSAGE
        assert query.tags == ["urgent"]

    def test_search_query_to_dict(self):
        """Test search query serialization."""
        query = SearchQuery(
            query_text="test query",
            search_type=SearchType.SIMILARITY,
            limit=5,
            agent_id="Agent-1"
        )

        data = query.to_dict()

        assert data["query_text"] == "test query"
        assert data["search_type"] == "similarity"
        assert data["limit"] == 5
        assert data["agent_id"] == "Agent-1"


class TestSearchResult:
    """Test SearchResult model."""

    def test_search_result_creation(self):
        """Test search result creation."""
        doc = VectorDocument(
            content="Test content",
            document_type=DocumentType.MESSAGE,
            agent_id="Agent-1"
        )
        result = SearchResult(
            document=doc,
            similarity_score=0.85,
            rank=1
        )

        assert result.document == doc
        assert result.similarity_score == 0.85
        assert result.rank == 1

    def test_search_result_to_dict(self):
        """Test search result serialization."""
        doc = VectorDocument(
            content="Test content",
            document_type=DocumentType.MESSAGE,
            agent_id="Agent-1"
        )
        result = SearchResult(
            document=doc,
            similarity_score=0.85,
            rank=1
        )

        data = result.to_dict()

        assert data["similarity_score"] == 0.85
        assert data["rank"] == 1
        assert "document" in data


class TestCollectionConfig:
    """Test CollectionConfig model."""

    def test_collection_config_creation(self):
        """Test collection config creation."""
        config = CollectionConfig(
            name="test_collection",
            description="Test collection",
            embedding_model=EmbeddingModel.SENTENCE_TRANSFORMERS
        )

        assert config.name == "test_collection"
        assert config.description == "Test collection"
        assert config.embedding_model == EmbeddingModel.SENTENCE_TRANSFORMERS
        assert config.distance_metric == "cosine"

    def test_collection_config_to_dict(self):
        """Test collection config serialization."""
        config = CollectionConfig(
            name="test_collection",
            description="Test collection"
        )

        data = config.to_dict()

        assert data["name"] == "test_collection"
        assert data["description"] == "Test collection"
        assert data["embedding_model"] == "sentence-transformers"


class TestVectorDatabaseStats:
    """Test VectorDatabaseStats model."""

    def test_stats_creation(self):
        """Test stats creation."""
        stats = VectorDatabaseStats(
            total_documents=100,
            total_collections=5,
            storage_size=10485760  # 10MB in bytes
        )

        assert stats.total_documents == 100
        assert stats.total_collections == 5
        assert stats.storage_size == 10485760
        assert get_unified_validator().validate_type(stats.last_updated, datetime)

    def test_stats_to_dict(self):
        """Test stats serialization."""
        stats = VectorDatabaseStats(
            total_documents=50,
            total_collections=3,
            collections=["default", "messages", "config"]
        )

        data = stats.to_dict()

        assert data["total_documents"] == 50
        assert data["total_collections"] == 3
        # Collections dict will have equal distribution
        assert "default" in data["collections"]
        assert "messages" in data["collections"]
        assert "config" in data["collections"]


class TestEnums:
    """Test enum types."""

    def test_document_type_enum(self):
        """Test DocumentType enum."""
        assert DocumentType.MESSAGE.value == "message"
        assert DocumentType.DEVLOG.value == "devlog"
        assert DocumentType.CONTRACT.value == "contract"

    def test_embedding_model_enum(self):
        """Test EmbeddingModel enum."""
        assert EmbeddingModel.SENTENCE_TRANSFORMERS.value == "sentence-transformers"
        assert EmbeddingModel.OPENAI_ADA.value == "openai-ada-002"

    def test_search_type_enum(self):
        """Test SearchType enum."""
        assert SearchType.SIMILARITY.value == "similarity"
        assert SearchType.MAX_MARGINAL_RELEVANCE.value == "mmr"
        assert SearchType.FILTERED.value == "filtered"


if __name__ == "__main__":
    pytest.main([__file__])
