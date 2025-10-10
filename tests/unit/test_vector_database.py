#!/usr/bin/env python3
"""
Vector Database Unit Tests
==========================

Unit tests for the vector database components.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.services.vector_database.vector_database_models import (
    VectorDatabaseConfig,
    VectorDocument,
    VectorQuery,
    VectorSearchResult,
    VectorIndex,
    VectorDatabase
)


class TestVectorDatabaseConfig:
    """Test cases for VectorDatabaseConfig."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        config = VectorDatabaseConfig()
        
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.database == "vectordb"
        assert config.collection == "vectors"
        assert config.dimension == 768
        assert config.metric == "cosine"
    
    def test_initialization_custom(self):
        """Test custom initialization."""
        config = VectorDatabaseConfig(
            host="example.com",
            port=8080,
            database="testdb",
            collection="test_vectors",
            dimension=512,
            metric="euclidean"
        )
        
        assert config.host == "example.com"
        assert config.port == 8080
        assert config.database == "testdb"
        assert config.collection == "test_vectors"
        assert config.dimension == 512
        assert config.metric == "euclidean"
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        config = VectorDatabaseConfig(
            host="test.com",
            port=9000,
            database="testdb"
        )
        
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict["host"] == "test.com"
        assert config_dict["port"] == 9000
        assert config_dict["database"] == "testdb"
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        config_dict = {
            "host": "example.com",
            "port": 5432,
            "database": "vectordb",
            "collection": "vectors",
            "dimension": 768,
            "metric": "cosine"
        }
        
        config = VectorDatabaseConfig.from_dict(config_dict)
        
        assert config.host == "example.com"
        assert config.port == 5432
        assert config.database == "vectordb"
        assert config.collection == "vectors"
        assert config.dimension == 768
        assert config.metric == "cosine"


class TestVectorDocument:
    """Test cases for VectorDocument."""
    
    def test_initialization(self):
        """Test document initialization."""
        doc = VectorDocument(
            id="doc1",
            content="Test content",
            vector=[0.1, 0.2, 0.3],
            metadata={"type": "test"}
        )
        
        assert doc.id == "doc1"
        assert doc.content == "Test content"
        assert doc.vector == [0.1, 0.2, 0.3]
        assert doc.metadata == {"type": "test"}
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        doc = VectorDocument(
            id="doc1",
            content="Test content",
            vector=[0.1, 0.2, 0.3],
            metadata={"type": "test"}
        )
        
        doc_dict = doc.to_dict()
        
        assert isinstance(doc_dict, dict)
        assert doc_dict["id"] == "doc1"
        assert doc_dict["content"] == "Test content"
        assert doc_dict["vector"] == [0.1, 0.2, 0.3]
        assert doc_dict["metadata"] == {"type": "test"}
    
    def test_from_dict(self):
        """Test creating from dictionary."""
        doc_dict = {
            "id": "doc1",
            "content": "Test content",
            "vector": [0.1, 0.2, 0.3],
            "metadata": {"type": "test"}
        }
        
        doc = VectorDocument.from_dict(doc_dict)
        
        assert doc.id == "doc1"
        assert doc.content == "Test content"
        assert doc.vector == [0.1, 0.2, 0.3]
        assert doc.metadata == {"type": "test"}


class TestVectorQuery:
    """Test cases for VectorQuery."""
    
    def test_initialization(self):
        """Test query initialization."""
        query = VectorQuery(
            vector=[0.1, 0.2, 0.3],
            limit=10,
            threshold=0.8,
            filters={"type": "test"}
        )
        
        assert query.vector == [0.1, 0.2, 0.3]
        assert query.limit == 10
        assert query.threshold == 0.8
        assert query.filters == {"type": "test"}
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        query = VectorQuery(
            vector=[0.1, 0.2, 0.3],
            limit=5,
            threshold=0.9
        )
        
        query_dict = query.to_dict()
        
        assert isinstance(query_dict, dict)
        assert query_dict["vector"] == [0.1, 0.2, 0.3]
        assert query_dict["limit"] == 5
        assert query_dict["threshold"] == 0.9


class TestVectorSearchResult:
    """Test cases for VectorSearchResult."""
    
    def test_initialization(self):
        """Test search result initialization."""
        result = VectorSearchResult(
            document_id="doc1",
            score=0.95,
            content="Test content"
        )
        
        assert result.document_id == "doc1"
        assert result.score == 0.95
        assert result.content == "Test content"
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        result = VectorSearchResult(
            document_id="doc1",
            score=0.95,
            content="Test content"
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["document_id"] == "doc1"
        assert result_dict["score"] == 0.95
        assert result_dict["content"] == "Test content"


class TestVectorIndex:
    """Test cases for VectorIndex."""
    
    def test_initialization(self):
        """Test index initialization."""
        index = VectorIndex(
            name="test_index",
            dimension=768,
            metric="cosine"
        )
        
        assert index.name == "test_index"
        assert index.dimension == 768
        assert index.metric == "cosine"
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        index = VectorIndex(
            name="test_index",
            dimension=512,
            metric="euclidean"
        )
        
        index_dict = index.to_dict()
        
        assert isinstance(index_dict, dict)
        assert index_dict["name"] == "test_index"
        assert index_dict["dimension"] == 512
        assert index_dict["metric"] == "euclidean"


class TestVectorDatabase:
    """Test cases for VectorDatabase."""
    
    def test_initialization(self):
        """Test database initialization."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        
        assert db.config == config
        assert db.is_connected is False
    
    def test_connect(self):
        """Test database connection."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        
        with patch.object(db, '_establish_connection', return_value=True):
            result = db.connect()
            
            assert result is True
            assert db.is_connected is True
    
    def test_disconnect(self):
        """Test database disconnection."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        with patch.object(db, '_close_connection', return_value=True):
            result = db.disconnect()
            
            assert result is True
            assert db.is_connected is False
    
    def test_insert_document(self):
        """Test document insertion."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        doc = VectorDocument(
            id="doc1",
            content="Test content",
            vector=[0.1, 0.2, 0.3]
        )
        
        with patch.object(db, '_insert_document_impl', return_value=True):
            result = db.insert_document(doc)
            
            assert result is True
    
    def test_search_similar(self):
        """Test similar document search."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        query = VectorQuery(
            vector=[0.1, 0.2, 0.3],
            limit=10
        )
        
        mock_results = [
            VectorSearchResult("doc1", 0.95, "Content 1"),
            VectorSearchResult("doc2", 0.90, "Content 2")
        ]
        
        with patch.object(db, '_search_similar_impl', return_value=mock_results):
            results = db.search_similar(query)
            
            assert len(results) == 2
            assert results[0].document_id == "doc1"
            assert results[1].document_id == "doc2"
    
    def test_delete_document(self):
        """Test document deletion."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        with patch.object(db, '_delete_document_impl', return_value=True):
            result = db.delete_document("doc1")
            
            assert result is True
    
    def test_get_document(self):
        """Test document retrieval."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        mock_doc = VectorDocument(
            id="doc1",
            content="Test content",
            vector=[0.1, 0.2, 0.3]
        )
        
        with patch.object(db, '_get_document_impl', return_value=mock_doc):
            doc = db.get_document("doc1")
            
            assert doc.id == "doc1"
            assert doc.content == "Test content"
    
    def test_create_index(self):
        """Test index creation."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        index = VectorIndex(
            name="test_index",
            dimension=768,
            metric="cosine"
        )
        
        with patch.object(db, '_create_index_impl', return_value=True):
            result = db.create_index(index)
            
            assert result is True
    
    def test_drop_index(self):
        """Test index deletion."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        with patch.object(db, '_drop_index_impl', return_value=True):
            result = db.drop_index("test_index")
            
            assert result is True
    
    def test_list_documents(self):
        """Test document listing."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        mock_docs = [
            VectorDocument("doc1", "Content 1", [0.1, 0.2, 0.3]),
            VectorDocument("doc2", "Content 2", [0.4, 0.5, 0.6])
        ]
        
        with patch.object(db, '_list_documents_impl', return_value=mock_docs):
            docs = db.list_documents()
            
            assert len(docs) == 2
            assert docs[0].id == "doc1"
            assert docs[1].id == "doc2"
    
    def test_get_stats(self):
        """Test database statistics retrieval."""
        config = VectorDatabaseConfig()
        db = VectorDatabase(config)
        db.is_connected = True
        
        mock_stats = {
            "total_documents": 100,
            "total_indexes": 5,
            "database_size": "1.2MB"
        }
        
        with patch.object(db, '_get_stats_impl', return_value=mock_stats):
            stats = db.get_stats()
            
            assert stats["total_documents"] == 100
            assert stats["total_indexes"] == 5
            assert stats["database_size"] == "1.2MB"