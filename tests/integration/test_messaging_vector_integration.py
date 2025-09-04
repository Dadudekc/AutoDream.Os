#!/usr/bin/env python3
"""
Messaging-Vector Database Integration Tests - Agent Cellphone V2
=================================================================

Comprehensive integration tests for messaging system and vector database interaction.
Tests end-to-end workflows, semantic search, and cross-system functionality.

V2 Compliance: Integration testing with proper isolation and mocking.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""


# Import messaging and vector components
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
)
    VectorDocument, SearchQuery, DocumentType, SearchType,
    SearchResult, VectorDatabaseConfig
)


@pytest.mark.integration
class TestMessagingVectorIntegration:
    """Integration tests for messaging and vector database interaction."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_vector_db = Mock()
        self.mock_config = Mock(spec=VectorDatabaseConfig)
        self.mock_config.persist_directory = self.temp_dir
        self.mock_config.default_collection = "test_messages"
        self.mock_config.default_embedding_model = "sentence-transformers"

    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_message_indexing_integration(self, mock_config_class, mock_vector_db_class):
        """Test complete message indexing workflow."""
        # Setup mocks
        mock_config = Mock()
        mock_config.persist_directory = self.temp_dir
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Create test message
        message = UnifiedMessage(
            content="Test message for vector indexing",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )

        # Test message indexing
        result = integration.index_message(message)

        # Verify interactions
        assert result is True
        mock_vector_db.add_document.assert_called_once()
        call_args = mock_vector_db.add_document.call_args

        # Verify document structure
        vector_doc = call_args[0][0]
        assert get_unified_validator().validate_type(vector_doc, VectorDocument)
        assert vector_doc.content == "Test message for vector indexing"
        assert vector_doc.document_type == DocumentType.MESSAGE
        assert vector_doc.agent_id == "Agent-2"
        assert "sender" in vector_doc.metadata
        assert "message_type" in vector_doc.metadata
        assert "priority" in vector_doc.metadata

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_message_search_integration(self, mock_config_class, mock_vector_db_class):
        """Test semantic search of messages."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock search results
        mock_result = Mock()
        mock_result.document.content = "Similar message content"
        mock_result.score = 0.85
        mock_vector_db.search.return_value = [mock_result]

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test message search
        results = integration.search_messages("test query", agent_id="Agent-1", limit=5)

        # Verify search was called correctly
        assert len(results) == 1
        mock_vector_db.search.assert_called_once()
        search_query = mock_vector_db.search.call_args[0][0]
        assert search_query.query_text == "test query"
        assert search_query.agent_id == "Agent-1"
        assert search_query.limit == 5
        assert search_query.document_type == DocumentType.MESSAGE

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_devlog_indexing_integration(self, mock_config_class, mock_vector_db_class):
        """Test devlog entry indexing in vector database."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Create test devlog entry
        devlog_entry = {
            "id": "devlog_001",
            "title": "Test Devlog Entry",
            "content": "This is a test devlog entry for vector indexing",
            "agent_id": "Agent-3",
            "category": "integration_test",
            "timestamp": "2024-01-01T12:00:00Z",
            "author": "Agent-3"
        }

        # Test devlog indexing
        result = integration.index_devlog_entry(devlog_entry)

        # Verify interactions
        assert result is True
        mock_vector_db.add_document.assert_called_once()
        call_args = mock_vector_db.add_document.call_args

        # Verify document structure
        vector_doc = call_args[0][0]
        assert get_unified_validator().validate_type(vector_doc, VectorDocument)
        assert "Test Devlog Entry" in vector_doc.content
        assert "This is a test devlog entry" in vector_doc.content
        assert vector_doc.document_type == DocumentType.DEVLOG
        assert vector_doc.agent_id == "Agent-3"
        assert vector_doc.metadata["title"] == "Test Devlog Entry"
        assert vector_doc.metadata["category"] == "integration_test"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_cross_agent_search_integration(self, mock_config_class, mock_vector_db_class):
        """Test searching across multiple agents."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock search results from different agents
        results = []
        for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
            mock_result = Mock()
            mock_result.document.content = f"Message from {agent_id}"
            mock_result.document.agent_id = agent_id
            mock_result.score = 0.8
            results.append(mock_result)

        mock_vector_db.search.return_value = results

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test cross-agent search
        search_results = integration.search_all("common query", limit=10)

        # Verify search results
        assert len(search_results) == 3
        agent_ids = [r.document.agent_id for r in search_results]
        assert "Agent-1" in agent_ids
        assert "Agent-2" in agent_ids
        assert "Agent-3" in agent_ids

        # Verify search was called without agent filter
        search_query = mock_vector_db.search.call_args[0][0]
        assert search_query.agent_id is None  # Should search across all agents

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_related_messages_integration(self, mock_config_class, mock_vector_db_class):
        """Test finding related messages functionality."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock original document
        original_doc = Mock()
        original_doc.content = "Original message content"
        mock_vector_db.get_document.return_value = original_doc

        # Mock related results
        related_results = []
        for i in range(3):
            mock_result = Mock()
            mock_result.document.id = f"related_{i}"
            mock_result.document.content = f"Related message {i}"
            related_results.append(mock_result)

        mock_vector_db.search.return_value = related_results

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test related messages
        related = integration.get_related_messages("original_msg_123", limit=5)

        # Verify interactions
        mock_vector_db.get_document.assert_called_once_with("original_msg_123", "test_messages")
        mock_vector_db.search.assert_called_once()

        # Verify search query used original content
        search_query = mock_vector_db.search.call_args[0][0]
        assert search_query.query_text == "Original message content"
        assert search_query.document_type == DocumentType.MESSAGE

        # Verify results (should exclude original)
        assert len(related) == 3
        for result in related:
            assert result.document.id.startswith("related_")

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_inbox_file_indexing_integration(self, mock_config_class, mock_vector_db_class):
        """Test indexing messages from agent inbox files."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Create temporary inbox with test files
        inbox_path = get_unified_utility().Path(self.temp_dir) / "inbox"
        inbox_path.mkdir()

        # Create test markdown files
        test_files = [
            ("message1.md", "# Message 1\n\nThis is the first test message."),
            ("message2.md", "# Message 2\n\nThis is the second test message."),
            ("message3.md", "# Message 3\n\nThis is the third test message.")
        ]

        for filename, content in test_files:
            file_path = inbox_path / filename
            with open(file_path, 'w') as f:
                f.write(content)

        # Test inbox indexing
        indexed_count = integration.index_inbox_files("Agent-1", str(inbox_path))

        # Verify results
        assert indexed_count == 3
        assert mock_vector_db.add_document.call_count == 3

        # Verify each document was created correctly
        calls = mock_vector_db.add_document.call_args_list
        for call in calls:
            vector_doc = call[0][0]
            assert get_unified_validator().validate_type(vector_doc, VectorDocument)
            assert vector_doc.agent_id == "Agent-1"
            assert vector_doc.document_type == DocumentType.MESSAGE
            assert "inbox" in vector_doc.tags
            assert "file" in vector_doc.tags
            assert "file_name" in vector_doc.metadata
            assert "file_size" in vector_doc.metadata

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_agent6_patterns_integration(self, mock_config_class, mock_vector_db_class):
        """Test Agent-6 communication enhancement patterns integration."""
        # Setup mocks
        mock_config = Mock()
        mock_config.persist_directory = self.temp_dir
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service (this should trigger Agent-6 pattern integration)
        integration = VectorMessagingIntegration(mock_config)

        # Verify Agent-6 patterns were added to vector database
        # The integration constructor calls _integrate_agent6_enhancements
        assert mock_vector_db.add_document.call_count > 0

        # Check that some expected patterns were added
        calls = mock_vector_db.add_document.call_args_list
        pattern_names = []
        for call in calls:
            doc = call[0][0]
            if "Agent-6 Communication Infrastructure Enhancement" in doc.content:
                # Extract pattern name from content
                content_lines = doc.content.split('\n')
                for line in content_lines:
                    if line.startswith("Pattern: "):
                        pattern_names.append(line.replace("Pattern: ", ""))

        # Verify some key Agent-6 patterns were indexed
        assert "enum_attribute_violations" in pattern_names
        assert "missing_method_violations" in pattern_names
        assert "performance_optimization_patterns" in pattern_names

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_agent6_pattern_search_integration(self, mock_config_class, mock_vector_db_class):
        """Test searching for Agent-6 enhancement patterns."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "communication_patterns"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock search results for Agent-6 patterns
        mock_results = []
        patterns = ["enum_attribute_violations", "missing_method_violations", "performance_optimization_patterns"]
        for pattern in patterns:
            mock_result = Mock()
            mock_result.document.content = f"Agent-6 pattern: {pattern}"
            mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test searching for patterns
        results = integration.search_agent6_patterns("enum violations", limit=3)

        # Verify search was configured correctly
        mock_vector_db.search.assert_called_once()
        search_query = mock_vector_db.search.call_args[0][0]

        assert search_query.query_text == "enum violations"
        assert search_query.search_type == SearchType.SEMANTIC
        assert search_query.limit == 3
        assert search_query.document_types == [DocumentType.CODE_PATTERN]
        assert search_query.agent_ids == ["Agent-6"]

        # Verify results
        assert len(results) == 3

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_database_stats_integration(self, mock_config_class, mock_vector_db_class):
        """Test vector database statistics integration."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock stats object
        mock_stats = Mock()
        mock_stats.to_dict.return_value = {
            "total_documents": 150,
            "total_collections": 5,
            "total_embeddings": 150,
            "collections": ["messages", "devlogs", "communication_patterns"]
        }
        mock_vector_db.get_stats.return_value = mock_stats

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test getting stats
        stats = integration.get_database_stats()

        # Verify stats structure
        assert stats["total_documents"] == 150
        assert stats["total_collections"] == 5
        assert stats["total_embeddings"] == 150
        assert "messages" in stats["collections"]
        assert "devlogs" in stats["collections"]
        assert "communication_patterns" in stats["collections"]

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_error_handling_integration(self, mock_config_class, mock_vector_db_class):
        """Test error handling in integration scenarios."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock vector DB to raise exception
        mock_vector_db.add_document.side_effect = Exception("Vector DB error")
        mock_vector_db.search.side_effect = Exception("Search error")

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test error handling in message indexing
        message = UnifiedMessage(
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )

        result = integration.index_message(message)
        assert result is False  # Should return False on error

        # Test error handling in search
        results = integration.search_messages("test query")
        assert results == []  # Should return empty list on error

        # Test error handling in devlog indexing
        devlog_entry = {"id": "test", "title": "Test", "content": "Test content"}
        result = integration.index_devlog_entry(devlog_entry)
        assert result is False  # Should return False on error

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_validation_integration(self, mock_config_class, mock_vector_db_class):
        """Test validation integration with vector database."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "test_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Test with empty content (should fail validation)
        message = UnifiedMessage(
            content="",  # Empty content
            sender="Agent-1",
            recipient="Agent-2"
        )

        result = integration.index_message(message)
        assert result is False  # Should fail validation
        mock_vector_db.add_document.assert_not_called()  # Should not attempt to add

        # Test with very long content (should pass validation)
        long_content = "A" * 10000
        message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2"
        )

        mock_vector_db.add_document.return_value = True
        result = integration.index_message(message)
        assert result is True  # Should pass validation
        mock_vector_db.add_document.assert_called_once()


@pytest.mark.integration
class TestMessagingVectorEndToEndWorkflows:
    """End-to-end workflow tests for messaging-vector integration."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = Mock(spec=VectorDatabaseConfig)
        self.mock_config.persist_directory = self.temp_dir
        self.mock_config.default_collection = "e2e_messages"

    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_complete_message_lifecycle(self, mock_config_class, mock_vector_db_class):
        """Test complete message lifecycle from creation to search."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "e2e_messages"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Step 1: Index multiple messages
        messages = [
            UnifiedMessage(
                content="First message about project architecture",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.TEXT
            ),
            UnifiedMessage(
                content="Second message about vector database integration",
                sender="Agent-2",
                recipient="Agent-3",
                message_type=UnifiedMessageType.TEXT
            ),
            UnifiedMessage(
                content="Third message about testing frameworks",
                sender="Agent-3",
                recipient="Agent-1",
                message_type=UnifiedMessageType.TEXT
            )
        ]

        # Index all messages
        for message in messages:
            result = integration.index_message(message)
            assert result is True

        # Verify all messages were indexed
        assert mock_vector_db.add_document.call_count == 3

        # Step 2: Search for messages
        mock_search_results = []
        for i, message in enumerate(messages):
            mock_result = Mock()
            mock_result.document.content = message.content
            mock_result.document.agent_id = message.recipient
            mock_result.score = 0.9 - (i * 0.1)  # Decreasing scores
            mock_search_results.append(mock_result)

        mock_vector_db.search.return_value = mock_search_results

        # Search for architecture-related messages
        results = integration.search_messages("architecture", limit=5)

        # Verify search results
        assert len(results) == 3
        assert "project architecture" in results[0].document.content

        # Step 3: Find related messages
        mock_vector_db.get_document.return_value = Mock(content=messages[0].content)
        related_results = integration.get_related_messages(messages[0].message_id, limit=2)

        # Verify related message search
        assert len(related_results) <= 2
        mock_vector_db.search.assert_called()

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_multi_agent_conversation_workflow(self, mock_config_class, mock_vector_db_class):
        """Test multi-agent conversation workflow with vector search."""
        # Setup mocks
        mock_config = Mock()
        mock_config.default_collection = "conversations"
        mock_config_class.return_value = mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(mock_config)

        # Simulate a multi-agent conversation
        conversation = [
            ("Agent-1", "Agent-2", "Let's discuss the new vector database integration"),
            ("Agent-2", "Agent-3", "I think we should use ChromaDB for persistence"),
            ("Agent-3", "Agent-1", "ChromaDB is a good choice for vector storage"),
            ("Agent-1", "Agent-4", "What about the embedding models?"),
            ("Agent-4", "Agent-1", "Sentence transformers work well for our use case"),
            ("Agent-1", "Agent-2", "Great, let's proceed with the implementation")
        ]

        # Index conversation messages
        for sender, recipient, content in conversation:
            message = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=UnifiedMessageType.TEXT
            )
            result = integration.index_message(message)
            assert result is True

        # Verify all messages indexed
        assert mock_vector_db.add_document.call_count == 6

        # Test searching within conversation context
        mock_results = []
        for sender, recipient, content in conversation:
            if "ChromaDB" in content or "vector" in content or "embedding" in content:
                mock_result = Mock()
                mock_result.document.content = content
                mock_result.document.agent_id = recipient
                mock_result.score = 0.85
                mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Search for vector-related discussions
        vector_discussions = integration.search_messages("vector database", limit=10)

        # Verify relevant messages were found
        assert len(vector_discussions) > 0
        for result in vector_discussions:
            content_lower = result.document.content.lower()
            assert any(keyword in content_lower for keyword in ["vector", "chromadb", "embedding", "database"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

