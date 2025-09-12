#!/usr/bin/env python3
"""
EMERGENCY INTEGRATION TESTS - Consolidated Services Integration
================================================================

CRITICAL INTEGRATION TESTING for Agent-1 Emergency Pytest Assignment:
- Consolidated Messaging Service (258 lines, 3→1 consolidation)
- Consolidated Vector Service (233 lines, embedding integration)
- Consolidated Coordination Service (dependencies validation)

Target: 90%+ integration coverage by EOD
Execution: IMMEDIATE - PYTEST_MODE_ACTIVE

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: EMERGENCY PYTEST COVERAGE - INTEGRATION TESTING LEAD
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import consolidated services for integration testing
try:
    from services.consolidated_coordination_service import ConsolidatedCoordinationService
    from services.consolidated_messaging_service import ConsolidatedMessagingService
    from services.consolidated_vector_service import ConsolidatedVectorService
    from services.models.messaging_models import (
        UnifiedMessage,
        UnifiedMessagePriority,
        UnifiedMessageType,
    )
    from services.models.vector_models import EmbeddingModel, VectorDocument

    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Services not available: {e}")
    SERVICES_AVAILABLE = False

    # Create mock classes for testing
    class MockConsolidatedMessagingService:
        def __init__(self, dry_run=False, **kwargs):
            self.dry_run = dry_run

    class MockConsolidatedVectorService:
        def __init__(self, agent_id=None, dry_run=False, **kwargs):
            self.agent_id = agent_id
            self.dry_run = dry_run

    class MockConsolidatedCoordinationService:
        def __init__(self, coordinator_id=None, dry_run=False, **kwargs):
            self.coordinator_id = coordinator_id
            self.dry_run = dry_run

    ConsolidatedMessagingService = MockConsolidatedMessagingService
    ConsolidatedVectorService = MockConsolidatedVectorService
    ConsolidatedCoordinationService = MockConsolidatedCoordinationService


@pytest.mark.integration
class TestConsolidatedServicesIntegration:
    """Critical integration tests for consolidated services interaction."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup for each test method."""
        self.messaging_service = ConsolidatedMessagingService(dry_run=True)
        self.vector_service = ConsolidatedVectorService(agent_id="test-agent")
        self.coordination_service = ConsolidatedCoordinationService("integration-test-coordinator")

    @pytest.mark.critical
    def test_messaging_service_initialization_integration(self):
        """INTEGRATION TEST: Verify messaging service initializes correctly."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test service initialization
        assert self.messaging_service is not None
        assert hasattr(self.messaging_service, "load_coordinates_from_json")
        assert hasattr(self.messaging_service, "send_message_pyautogui")
        assert hasattr(self.messaging_service, "broadcast_message")

        # Verify service attributes
        assert self.messaging_service.dry_run is True

    @pytest.mark.critical
    def test_vector_service_initialization_integration(self):
        """INTEGRATION TEST: Verify vector service initializes correctly."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test service initialization
        assert self.vector_service is not None
        assert hasattr(self.vector_service, "generate_embeddings")
        assert hasattr(self.vector_service, "store_document")
        assert hasattr(self.vector_service, "search_documents")

        # Verify service configuration
        assert self.vector_service.agent_id == "test-agent"
        assert self.vector_service.config is not None

    @pytest.mark.critical
    def test_coordination_service_initialization_integration(self):
        """INTEGRATION TEST: Verify coordination service initializes correctly."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test service initialization
        assert self.coordination_service is not None
        assert hasattr(self.coordination_service, "determine_coordination_strategy")
        assert hasattr(self.coordination_service, "process_message")
        assert hasattr(self.coordination_service, "get_command_stats")

        # Verify service configuration
        assert self.coordination_service.name == "integration-test-coordinator"

    @pytest.mark.integration
    def test_cross_service_coordinate_loading(self):
        """INTEGRATION TEST: Test coordinate loading across messaging service."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Mock coordinate loader
        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ["Agent-1", "Agent-2", "Agent-3"]
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = [(100, 200), (300, 400), (500, 600)]

        with patch(
            "services.consolidated_messaging_service.get_coordinate_loader",
            return_value=mock_loader,
        ):
            coords = self.messaging_service.load_coordinates_from_json()

            assert len(coords) == 3
            assert "Agent-1" in coords
            assert "Agent-2" in coords
            assert "Agent-3" in coords
            assert coords["Agent-1"] == (100, 200)

    @pytest.mark.integration
    def test_cross_service_embedding_generation(self):
        """INTEGRATION TEST: Test embedding generation with vector service."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        test_texts = ["Integration test message", "Vector service validation"]

        with patch("services.consolidated_vector_service.SentenceTransformer") as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = [
                [0.1, 0.2, 0.3, 0.4, 0.5],
                [0.6, 0.7, 0.8, 0.9, 1.0],
            ]
            mock_transformer.return_value = mock_encoder

            embeddings = self.vector_service.generate_embeddings(test_texts)

            assert len(embeddings) == 2
            assert len(embeddings[0]) == 5
            assert all(isinstance(val, float) for val in embeddings[0])

    @pytest.mark.integration
    def test_cross_service_message_coordination(self):
        """INTEGRATION TEST: Test message coordination processing."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        test_message = UnifiedMessage(
            content="Integration test coordination message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.COORDINATION,
            priority=UnifiedMessagePriority.URGENT,
            sender_type="agent",
        )

        result = self.coordination_service.process_message(test_message)

        assert result["status"] == "processed"
        assert "strategy" in result
        assert "timestamp" in result
        assert len(self.coordination_service.command_history) == 1

    @pytest.mark.integration
    def test_service_interaction_messaging_to_coordination(self):
        """INTEGRATION TEST: Test messaging service interaction with coordination."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Create a coordination message via messaging service
        with patch("services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE", False):
            result = self.messaging_service.send_message_pyautogui(
                "Agent-2", "Coordination test message", "HIGH", "COORDINATION"
            )

            # In dry run mode, should succeed
            assert result is True

    @pytest.mark.integration
    def test_service_interaction_vector_to_messaging(self):
        """INTEGRATION TEST: Test vector service interaction with messaging."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Create vector document and test storage
        doc = VectorDocument(
            id="integration-test-doc",
            content="Test document for integration validation",
            metadata={"test_type": "integration", "service": "vector"},
        )

        # Mock the engine for testing
        mock_engine = Mock()
        mock_engine.store.return_value = Mock(success=True, message="Stored successfully")

        with patch.object(self.vector_service, "_engine", mock_engine):
            result = self.vector_service.store_document(doc)

            assert result.success is True
            mock_engine.store.assert_called_once()

    @pytest.mark.integration
    def test_broadcast_integration_across_services(self):
        """INTEGRATION TEST: Test broadcast functionality integration."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Mock messaging core for broadcast testing
        mock_messaging_core = Mock()
        mock_messaging_core.send_message.return_value = True

        with patch(
            "services.consolidated_messaging_service.get_messaging_core",
            return_value=mock_messaging_core,
        ):
            results = self.messaging_service.broadcast_message("Integration broadcast test")

            assert isinstance(results, dict)
            assert len(results) > 0
            # Verify messaging core was called for broadcast
            mock_messaging_core.send_message.assert_called()

    @pytest.mark.integration
    def test_error_handling_integration(self):
        """INTEGRATION TEST: Test error handling across services."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test messaging service error handling
        with patch("services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE", False):
            result = self.messaging_service.send_message_pyautogui("Invalid-Agent", "Test")
            assert result is False

        # Test vector service error handling
        with patch.object(self.vector_service, "_engine", None):
            doc = VectorDocument(id="test", content="test")
            result = self.vector_service.store_document(doc)
            assert result.success is False

        # Test coordination service error handling
        with patch.object(
            self.coordination_service,
            "determine_coordination_strategy",
            side_effect=Exception("Coordination error"),
        ):
            test_message = UnifiedMessage(
                content="Error test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
            )

            result = self.coordination_service.process_message(test_message)
            assert result["status"] == "failed"
            assert "error" in result

    @pytest.mark.performance
    def test_service_performance_integration(self):
        """INTEGRATION TEST: Test service performance under load."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        import time

        # Test messaging service performance
        start_time = time.time()
        for i in range(10):
            self.messaging_service.send_message_pyautogui(
                f"Agent-{i % 3 + 1}", f"Performance test {i}"
            )
        messaging_time = time.time() - start_time

        # Should complete within reasonable time (dry run is fast)
        assert messaging_time < 1.0

        # Test coordination service performance
        start_time = time.time()
        messages = []
        for i in range(10):
            messages.append(
                UnifiedMessage(
                    content=f"Performance message {i}",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=UnifiedMessageType.AGENT_TO_AGENT,
                    priority=UnifiedMessagePriority.NORMAL,
                )
            )

        results = self.coordination_service.process_bulk_messages(messages)
        coordination_time = time.time() - start_time

        assert len(results) == 10
        assert all(result["status"] == "processed" for result in results)
        assert coordination_time < 2.0  # Should complete within 2 seconds

    @pytest.mark.integration
    def test_service_state_persistence_integration(self):
        """INTEGRATION TEST: Test service state persistence and recovery."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test coordination service state
        initial_commands = len(self.coordination_service.command_history)

        # Process several messages
        for i in range(3):
            message = UnifiedMessage(
                content=f"State test {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
            )
            self.coordination_service.process_message(message)

        # Verify state changes
        assert len(self.coordination_service.command_history) == initial_commands + 3
        assert self.coordination_service.command_count == initial_commands + 3

        # Test stats
        stats = self.coordination_service.get_command_stats()
        assert stats["total_commands"] == initial_commands + 3
        assert stats["successful_commands"] == initial_commands + 3
        assert stats["failed_commands"] == 0

    @pytest.mark.critical
    def test_end_to_end_service_workflow(self):
        """CRITICAL INTEGRATION TEST: End-to-end service workflow."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Create a complete workflow: Message -> Coordination -> Processing

        # Step 1: Create and send message
        with patch("services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE", False):
            message_result = self.messaging_service.send_message_pyautogui(
                "Agent-2", "End-to-end integration test message"
            )
            assert message_result is True

        # Step 2: Process through coordination service
        coord_message = UnifiedMessage(
            content="End-to-end coordination test",
            sender="Agent-1",
            recipient="coordinator",
            message_type=UnifiedMessageType.COORDINATION,
            priority=UnifiedMessagePriority.HIGH,
        )

        coord_result = self.coordination_service.process_message(coord_message)
        assert coord_result["status"] == "processed"
        assert coord_result["strategy"] == "coordination_priority"

        # Step 3: Verify state consistency
        stats = self.coordination_service.get_command_stats()
        assert stats["total_commands"] >= 1
        assert stats["successful_commands"] >= 1

        # Step 4: Test service health
        service_status = self.coordination_service.get_service_status()
        assert service_status["status"] == "active"
        assert service_status["name"] == "integration-test-coordinator"


# Critical Service Integration Tests
@pytest.mark.integration
class TestCriticalServiceIntegration:
    """Critical integration tests for emergency validation."""

    @pytest.mark.critical
    def test_messaging_service_line_coverage(self):
        """CRITICAL TEST: Validate messaging service (258 lines) coverage."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        # Test core messaging functionality
        service = ConsolidatedMessagingService()

        # Test coordinate loading
        coords = service.load_coordinates_from_json()
        assert isinstance(coords, dict)

        # Test message sending (various scenarios)
        with patch("services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE", False):
            assert service.send_message_pyautogui("Agent-1", "test") is True

        # Test broadcasting
        results = service.broadcast_message("test broadcast")
        assert isinstance(results, dict)

        # Test agent listing
        agents = service.list_agents()
        assert isinstance(agents, list)

    @pytest.mark.critical
    def test_vector_service_line_coverage(self):
        """CRITICAL TEST: Validate vector service (233 lines) coverage."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        service = ConsolidatedVectorService()

        # Test embedding generation
        test_texts = ["Vector integration test"]
        with patch("services.consolidated_vector_service.SentenceTransformer") as mock_transformer:
            mock_encoder = Mock()
            mock_encoder.encode.return_value = [[0.1, 0.2, 0.3]]
            mock_transformer.return_value = mock_encoder

            embeddings = service.generate_embeddings(test_texts)
            assert len(embeddings) == 1

        # Test document operations
        doc = VectorDocument(id="test", content="test content")

        # Mock engine for testing
        mock_engine = Mock()
        mock_engine.store.return_value = Mock(success=True)
        mock_engine.search.return_value = Mock(documents=[], scores=[], total_found=0)

        with patch.object(service, "_engine", mock_engine):
            store_result = service.store_document(doc)
            assert store_result.success is True

            search_results = service.search_documents(Mock(query="test"))
            assert hasattr(search_results, "documents")

    @pytest.mark.critical
    def test_coordination_service_line_coverage(self):
        """CRITICAL TEST: Validate coordination service dependency coverage."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Consolidated services not available")

        service = ConsolidatedCoordinationService()

        # Test message processing
        test_message = UnifiedMessage(
            content="Coordination integration test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
        )

        result = service.process_message(test_message)
        assert result["status"] == "processed"

        # Test strategy determination
        strategy = service.determine_coordination_strategy(test_message)
        assert isinstance(strategy, str)

        # Test bulk processing
        messages = [test_message, test_message]
        results = service.process_bulk_messages(messages)
        assert len(results) == 2

        # Test statistics
        stats = service.get_command_stats()
        assert "total_commands" in stats


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
            "--cov=src/services",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--tb=short",
            "-k",
            "test_consolidated_services_integration or test_critical_service_integration",
        ]
    )
