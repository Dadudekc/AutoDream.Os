#!/usr/bin/env python3
"""
Vector Database Service Tests - Agent Cellphone V2
===============================================

Unit tests for vector database service functionality.

Author: Agent-7 - Web Development Specialist
License: MIT
"""


    VectorDocument, SearchQuery, SearchResult, CollectionConfig,
    DocumentType, EmbeddingModel, SearchType
)


class TestVectorDatabaseService:
    """Test VectorDatabaseService functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.service = VectorDatabaseService(
            persist_directory=self.temp_dir,
            default_embedding_model=EmbeddingModel.SENTENCE_TRANSFORMERS
        )
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('src.services.vector_database_service.chromadb.PersistentClient')
    def test_get_client(self, mock_chromadb):
        """Test ChromaDB client initialization."""
        mock_client = Mock()
        mock_chromadb.return_value = mock_client
        
        result = self.service._get_client()
        
        assert result == mock_client
        mock_chromadb.assert_called_once_with(path=self.temp_dir)
    
    @patch('src.services.vector_database_service.chromadb.PersistentClient')
    def test_create_collection(self, mock_chromadb):
        """Test collection creation."""
        # Setup mocks
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.list_collections.return_value = []
        mock_client.create_collection.return_value = mock_collection
        mock_chromadb.return_value = mock_client
        
        config = CollectionConfig(
            name="test_collection",
            description="Test collection"
        )
        
        result = self.service.create_collection(config)
        
        assert result is True
        mock_client.create_collection.assert_called_once_with(
            name="test_collection",
            metadata={"description": "Test collection"}
        )
        assert "test_collection" in self.service._collections
    
    @patch('src.services.vector_database_service.chromadb.PersistentClient')
    def test_create_collection_already_exists(self, mock_chromadb):
        """Test collection creation when collection already exists."""
        # Setup mocks
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.name = "test_collection"
        mock_client.list_collections.return_value = [mock_collection]
        mock_chromadb.return_value = mock_client
        
        config = CollectionConfig(name="test_collection")
        
        result = self.service.create_collection(config)
        
        assert result is True
        mock_client.create_collection.assert_not_called()
    
    @patch('src.services.vector_database_service.chromadb.PersistentClient')
    def test_get_collection(self, mock_chromadb):
        """Test getting collection."""
        # Setup mocks
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.get_collection.return_value = mock_collection
        mock_chromadb.return_value = mock_client
        
        result = self.service.get_collection("test_collection")
        
        assert result == mock_collection
        mock_client.get_collection.assert_called_once_with("test_collection")
        assert "test_collection" in self.service._collections
    
    @patch.object(VectorDatabaseService, 'get_collection')
    @patch.object(VectorDatabaseService, '_get_client')
    def test_add_document(self, mock_get_client, mock_get_collection):
        """Test adding document to collection."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        # Mock embedding service
        with patch.object(self.service.embedding_service, 'generate_embedding') as mock_embedding:
            mock_embedding.return_value = [0.1, 0.2, 0.3]
            
            document = VectorDocument(
                id="test_id",
                content="Test content",
                document_type=DocumentType.MESSAGE,
                agent_id="Agent-1"
            )
            
            result = self.service.add_document(document, "test_collection")
            
            assert result is True
            mock_collection.add.assert_called_once()
            
            # Check the call arguments
            call_args = mock_collection.add.call_args
            assert call_args[1]['ids'] == ["test_id"]
            assert call_args[1]['documents'] == ["Test content"]
            assert call_args[1]['embeddings'] == [[0.1, 0.2, 0.3]]
    
    @patch.object(VectorDatabaseService, 'get_collection')
    def test_add_document_with_embedding(self, mock_get_collection):
        """Test adding document with existing embedding."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        document = VectorDocument(
            id="test_id",
            content="Test content",
            document_type=DocumentType.MESSAGE,
            agent_id="Agent-1",
            embedding=[0.1, 0.2, 0.3]
        )
        
        result = self.service.add_document(document, "test_collection")
        
        assert result is True
        mock_collection.add.assert_called_once()
        
        # Check that embedding service was not called
        with patch.object(self.service.embedding_service, 'generate_embedding') as mock_embedding:
            mock_embedding.assert_not_called()
    
    @patch.object(VectorDatabaseService, 'get_collection')
    def test_add_documents_batch(self, mock_get_collection):
        """Test adding multiple documents."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        # Mock embedding service
        with patch.object(self.service.embedding_service, 'generate_embedding') as mock_embedding:
            mock_embedding.return_value = [0.1, 0.2, 0.3]
            
            documents = [
                VectorDocument(
                    id="test_id_1",
                    content="Test content 1",
                    document_type=DocumentType.MESSAGE
                ),
                VectorDocument(
                    id="test_id_2",
                    content="Test content 2",
                    document_type=DocumentType.MESSAGE
                )
            ]
            
            result = self.service.add_documents_batch(documents, "test_collection")
            
            assert result is True
            mock_collection.add.assert_called_once()
            
            # Check the call arguments
            call_args = mock_collection.add.call_args
            assert len(call_args[1]['ids']) == 2
            assert len(call_args[1]['documents']) == 2
            assert len(call_args[1]['embeddings']) == 2
    
    @patch.object(VectorDatabaseService, 'get_collection')
    def test_search(self, mock_get_collection):
        """Test document search."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        # Mock search results
        mock_collection.query.return_value = {
            'documents': [['Test content 1', 'Test content 2']],
            'metadatas': [[
                {'document_type': 'message', 'agent_id': 'Agent-1'},
                {'document_type': 'message', 'agent_id': 'Agent-2'}
            ]],
            'distances': [[0.1, 0.2]],
            'ids': [['id1', 'id2']]
        }
        
        # Mock embedding service
        with patch.object(self.service.embedding_service, 'generate_embedding') as mock_embedding:
            mock_embedding.return_value = [0.1, 0.2, 0.3]
            
            query = SearchQuery(
                query_text="test query",
                search_type=SearchType.SIMILARITY,
                limit=10
            )
            
            results = self.service.search(query, "test_collection")
            
            assert len(results) == 2
            assert get_unified_validator().validate_type(results[0], SearchResult)
            assert results[0].similarity_score == 0.9  # 1 - 0.1
            assert results[1].similarity_score == 0.8  # 1 - 0.2
    
    @patch.object(VectorDatabaseService, 'get_collection')
    def test_get_document(self, mock_get_collection):
        """Test getting document by ID."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        mock_collection.get.return_value = {
            'documents': ['Test content'],
            'metadatas': [{'document_type': 'message', 'agent_id': 'Agent-1'}]
        }
        
        result = self.service.get_document("test_id", "test_collection")
        
        assert result is not None
        assert result.content == "Test content"
        assert result.document_type == DocumentType.MESSAGE
        assert result.agent_id == "Agent-1"
    
    @patch.object(VectorDatabaseService, 'get_collection')
    def test_delete_document(self, mock_get_collection):
        """Test deleting document."""
        # Setup mocks
        mock_collection = Mock()
        mock_get_collection.return_value = mock_collection
        
        result = self.service.delete_document("test_id", "test_collection")
        
        assert result is True
        mock_collection.delete.assert_called_once_with(ids=["test_id"])
    
    @patch.object(VectorDatabaseService, '_get_client')
    def test_get_stats(self, mock_get_client):
        """Test getting database statistics."""
        # Setup mocks
        mock_client = Mock()
        mock_collection1 = Mock()
        mock_collection1.name = "collection1"
        mock_collection1.count.return_value = 10
        mock_collection2 = Mock()
        mock_collection2.name = "collection2"
        mock_collection2.count.return_value = 20
        mock_client.list_collections.return_value = [mock_collection1, mock_collection2]
        mock_get_client.return_value = mock_client
        
        stats = self.service.get_stats()

        assert stats.total_documents == 30
        assert stats.total_collections == 2
        assert "collection1" in stats.collections
        assert "collection2" in stats.collections
        assert stats.storage_size == 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__])

