#!/usr/bin/env python3
"""
Messaging-Vector Database End-to-End Integration Tests - Agent Cellphone V2
===========================================================================

Complete end-to-end integration tests covering the full messaging-vector pipeline.
Tests real-world scenarios, error recovery, and system resilience.

V2 Compliance: End-to-end testing with comprehensive scenario coverage.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""


# Import integration components
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
)


@pytest.mark.e2e
class TestMessagingVectorEndToEndScenarios:
    """End-to-end scenarios for messaging-vector integration."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = Mock()
        self.mock_config.persist_directory = self.temp_dir
        self.mock_config.default_collection = "e2e_test"

    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_agent_collaboration_workflow(self, mock_config_class, mock_vector_db_class):
        """Test complete agent collaboration workflow with vector search."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Simulate a complex multi-agent collaboration scenario
        # Agent-1 starts a project discussion
        project_start = UnifiedMessage(
            content="Starting new project: Implement advanced vector search for agent communications. Need input from all agents.",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.BROADCAST
        )

        # Agent-2 provides technical architecture input
        tech_input = UnifiedMessage(
            content="For the vector search, I recommend using ChromaDB with sentence transformers. We can achieve semantic search with 85%+ accuracy.",
            sender="Agent-2",
            recipient="Agent-3",
            message_type=UnifiedMessageType.TEXT
        )

        # Agent-3 provides implementation details
        implementation_details = UnifiedMessage(
            content="Implementation plan: 1) Set up ChromaDB collection, 2) Implement embedding service, 3) Create search API, 4) Integrate with messaging core.",
            sender="Agent-3",
            recipient="Agent-4",
            message_type=UnifiedMessageType.TEXT
        )

        # Agent-4 asks clarifying questions
        clarification = UnifiedMessage(
            content="What about performance requirements? Should we optimize for real-time search or batch processing?",
            sender="Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT
        )

        # Agent-1 provides requirements
        requirements = UnifiedMessage(
            content="Performance requirements: Real-time search with <100ms response time for queries up to 1000 messages.",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )

        # Index all collaboration messages
        collaboration_messages = [
            project_start, tech_input, implementation_details,
            clarification, requirements
        ]

        for message in collaboration_messages:
            result = integration.index_message(message)
            assert result is True

        # Verify all messages were indexed
        assert mock_vector_db.add_document.call_count == len(collaboration_messages)

        # Test semantic search capabilities
        mock_results = []
        for i, message in enumerate(collaboration_messages):
            if any(keyword in message.content.lower() for keyword in ["vector", "search", "chromadb", "performance"]):
                mock_result = Mock()
                mock_result.document.content = message.content
                mock_result.document.agent_id = message.recipient
                mock_result.score = 0.9 - (i * 0.1)
                mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Search for vector-related discussions
        vector_discussions = integration.search_messages("vector search implementation", limit=10)

        # Verify relevant discussions were found
        assert len(vector_discussions) > 0
        found_technical = False
        found_implementation = False

        for result in vector_discussions:
            content = result.document.content.lower()
            if "chromadb" in content and "sentence transformers" in content:
                found_technical = True
            if "implementation plan" in content:
                found_implementation = True

        assert found_technical, "Technical architecture discussion not found"
        assert found_implementation, "Implementation details not found"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_error_recovery_and_resilience(self, mock_config_class, mock_vector_db_class):
        """Test system resilience and error recovery capabilities."""
        # Setup mocks with intermittent failures
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Simulate intermittent failures (every 3rd call fails)
        call_count = 0
        def intermittent_failure(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:
                raise Exception(f"Simulated failure on call {call_count}")
            return True

        mock_vector_db.add_document.side_effect = intermittent_failure

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test error recovery with multiple messages
        messages = []
        for i in range(10):
            message = UnifiedMessage(
                content=f"Error recovery test message {i}",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}"
            )
            messages.append(message)

        # Process messages (some will fail due to simulated errors)
        results = []
        for message in messages:
            result = integration.index_message(message)
            results.append(result)

        # Verify error recovery behavior
        successful_count = sum(1 for r in results if r is True)
        failed_count = sum(1 for r in results if r is False)

        # Should have some successes and some failures due to intermittent errors
        assert successful_count > 0, "No messages succeeded - error recovery not working"
        assert failed_count > 0, "No messages failed - error simulation not working"

        # Verify call count matches expectations
        assert mock_vector_db.add_document.call_count == len(messages)

        # Test that system continues to function after errors
        # Reset mock to always succeed
        mock_vector_db.add_document.return_value = True
        mock_vector_db.add_document.side_effect = None

        # Send recovery messages
        recovery_messages = []
        for i in range(5):
            message = UnifiedMessage(
                content=f"Recovery message {i}",
                sender="Agent-1",
                recipient="Agent-2"
            )
            recovery_messages.append(message)

        recovery_results = []
        for message in recovery_messages:
            result = integration.index_message(message)
            recovery_results.append(result)

        # All recovery messages should succeed
        assert all(recovery_results), "Recovery messages failed"
        assert mock_vector_db.add_document.call_count == len(messages) + len(recovery_messages)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_cross_component_data_flow(self, mock_config_class, mock_vector_db_class):
        """Test data flow across multiple components and services."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Simulate complex data flow scenario
        # 1. Agent communication messages
        comm_messages = []
        for i in range(5):
            message = UnifiedMessage(
                content=f"Communication {i}: Team coordination update",
                sender=f"Agent-{i + 1}",
                recipient=f"Agent-{(i + 1) % 5 + 1}",
                message_type=UnifiedMessageType.TEXT
            )
            comm_messages.append(message)

        # 2. System status messages
        status_messages = []
        for i in range(3):
            message = UnifiedMessage(
                content=f"System status {i}: Component health check passed",
                sender="System",
                recipient=f"Agent-{i + 1}",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT
            )
            status_messages.append(message)

        # 3. Devlog entries
        devlogs = []
        for i in range(3):
            devlog = {
                "id": f"devlog_{i}",
                "title": f"Development Update {i}",
                "content": f"Progress on vector integration feature {i}",
                "agent_id": f"Agent-{i + 2}",
                "category": "integration",
                "timestamp": datetime.now().isoformat()
            }
            devlogs.append(devlog)

        # Process all data types
        for message in comm_messages + status_messages:
            result = integration.index_message(message)
            assert result is True

        for devlog in devlogs:
            result = integration.index_devlog_entry(devlog)
            assert result is True

        # Verify all data was indexed
        expected_calls = len(comm_messages) + len(status_messages) + len(devlogs)
        assert mock_vector_db.add_document.call_count == expected_calls

        # Test cross-component search
        mock_results = []
        for message in comm_messages + status_messages:
            if "coordination" in message.content or "health check" in message.content:
                mock_result = Mock()
                mock_result.document.content = message.content
                mock_result.document.agent_id = message.recipient
                mock_result.score = 0.85
                mock_results.append(mock_result)

        for devlog in devlogs:
            if "vector integration" in devlog["content"]:
                mock_result = Mock()
                mock_result.document.content = f"{devlog['title']} {devlog['content']}"
                mock_result.document.agent_id = devlog["agent_id"]
                mock_result.score = 0.80
                mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Search across all components
        all_results = integration.search_all("coordination integration", limit=10)

        # Verify cross-component results
        assert len(all_results) > 0
        found_communication = False
        found_devlog = False

        for result in all_results:
            content = result.document.content.lower()
            if "coordination update" in content:
                found_communication = True
            if "vector integration" in content:
                found_devlog = True

        assert found_communication, "Communication messages not found in cross-component search"
        assert found_devlog, "Devlog entries not found in cross-component search"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_real_world_agent_interaction_scenario(self, mock_config_class, mock_vector_db_class):
        """Test real-world agent interaction scenario with vector search."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Simulate real-world agent interaction scenario
        # Agent-3 encounters an issue and seeks help
        issue_report = UnifiedMessage(
            content="Issue: CLI validation failing with 'mutual exclusion' error when using --agent and --bulk together. Need immediate assistance.",
            sender="Agent-3",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )

        # Agent-1 acknowledges and starts investigation
        acknowledgment = UnifiedMessage(
            content="Received urgent issue report. Investigating CLI validation mutual exclusion logic. Will provide solution shortly.",
            sender="Agent-1",
            recipient="Agent-3",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )

        # Agent-1 finds the root cause
        root_cause = UnifiedMessage(
            content="Root cause identified: CLI validator mutual exclusion logic incorrectly triggers when --agent and --bulk are both present. This is by design but error message is confusing.",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )

        # Agent-2 provides solution
        solution = UnifiedMessage(
            content="Solution: Use either --agent OR --bulk, not both. For bulk operations, use --bulk --message. For specific agent, use --agent AGENT_NAME --message.",
            sender="Agent-2",
            recipient="Agent-3",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )

        # Agent-3 confirms resolution
        resolution = UnifiedMessage(
            content="Issue resolved! Thanks for the quick solution. Using --bulk for system-wide messages and --agent for specific communications.",
            sender="Agent-3",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )

        # Index the entire interaction
        interaction_messages = [
            issue_report, acknowledgment, root_cause, solution, resolution
        ]

        for message in interaction_messages:
            result = integration.index_message(message)
            assert result is True

        # Test semantic search for troubleshooting
        mock_results = []
        for message in interaction_messages:
            if any(keyword in message.content.lower() for keyword in ["cli", "validation", "mutual exclusion", "error", "solution"]):
                mock_result = Mock()
                mock_result.document.content = message.content
                mock_result.document.agent_id = message.recipient
                mock_result.score = 0.9
                mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Search for CLI validation issues
        troubleshooting_results = integration.search_messages("CLI validation error", limit=10)

        # Verify troubleshooting information was found
        assert len(troubleshooting_results) > 0
        found_issue = False
        found_solution = False

        for result in troubleshooting_results:
            content = result.document.content.lower()
            if "cli validation failing" in content:
                found_issue = True
            if "solution:" in content and "use either" in content:
                found_solution = True

        assert found_issue, "Original issue description not found"
        assert found_solution, "Solution information not found"

        # Test finding related messages for this issue
        mock_vector_db.get_document.return_value = Mock(content=issue_report.content)

        # Mock related results (all messages in the conversation)
        related_results = []
        for message in interaction_messages[1:]:  # Exclude original
            mock_result = Mock()
            mock_result.document.id = f"msg_{interaction_messages.index(message)}"
            mock_result.document.content = message.content
            related_results.append(mock_result)

        mock_vector_db.search.return_value = related_results

        # Find related messages
        related = integration.get_related_messages(issue_report.message_id, limit=5)

        # Verify conversation thread was found
        assert len(related) > 0
        related_content = [r.document.content for r in related]

        # Should find acknowledgment, solution, and resolution
        assert any("Received urgent issue report" in content for content in related_content)
        assert any("Solution:" in content for content in related_content)
        assert any("Issue resolved" in content for content in related_content)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_system_monitoring_and_metrics_integration(self, mock_config_class, mock_vector_db_class):
        """Test system monitoring and metrics integration with vector database."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Mock stats
        mock_stats = Mock()
        mock_stats.to_dict.return_value = {
            "total_documents": 500,
            "total_collections": 3,
            "total_embeddings": 500,
            "collections": ["messages", "devlogs", "system_metrics"],
            "performance_metrics": {
                "avg_indexing_time": 0.05,
                "avg_search_time": 0.02,
                "cache_hit_rate": 0.85
            }
        }
        mock_vector_db.get_stats.return_value = mock_stats

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test metrics collection and monitoring
        # Simulate system monitoring messages
        monitoring_messages = []
        for i in range(5):
            message = UnifiedMessage(
                content=f"System monitoring alert {i}: Performance threshold exceeded",
                sender="System",
                recipient=f"Agent-{i % 8 + 1}",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT
            )
            monitoring_messages.append(message)

        # Index monitoring messages
        for message in monitoring_messages:
            result = integration.index_message(message)
            assert result is True

        # Test system stats retrieval
        stats = integration.get_database_stats()

        # Verify comprehensive stats
        assert stats["total_documents"] == 500
        assert stats["total_collections"] == 3
        assert "messages" in stats["collections"]
        assert "devlogs" in stats["collections"]
        assert "system_metrics" in stats["collections"]
        assert "performance_metrics" in stats

        # Verify performance metrics
        perf_metrics = stats["performance_metrics"]
        assert perf_metrics["avg_indexing_time"] == 0.05
        assert perf_metrics["avg_search_time"] == 0.02
        assert perf_metrics["cache_hit_rate"] == 0.85

        # Test monitoring message search
        mock_results = []
        for message in monitoring_messages:
            mock_result = Mock()
            mock_result.document.content = message.content
            mock_result.document.agent_id = message.recipient
            mock_result.score = 0.88
            mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Search for system monitoring alerts
        monitoring_alerts = integration.search_messages("system monitoring alert", limit=10)

        # Verify monitoring alerts were found
        assert len(monitoring_alerts) == 5
        for result in monitoring_alerts:
            assert "System monitoring alert" in result.document.content
            assert result.score > 0.8


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])

