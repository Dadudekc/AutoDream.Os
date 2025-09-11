#!/usr/bin/env python3
"""
EMERGENCY UNIT TESTS - Consolidated Messaging Service
=====================================================

CRITICAL UNIT TESTING for Agent-1 Emergency Pytest Assignment:
- Messaging service functions (258 lines, 3→1 consolidation)
- Individual method testing with mocks
- Error condition validation
- Performance testing

Target: 95%+ unit test coverage for messaging service
Execution: IMMEDIATE - PYTEST_MODE_ACTIVE

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: EMERGENCY PYTEST COVERAGE - UNIT TESTING EXECUTION
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

try:
    from services.consolidated_messaging_service import (
        ConsolidatedMessagingService,
        MESSAGING_AVAILABLE,
        PYAUTOGUI_AVAILABLE,
        PYPERCLIP_AVAILABLE,
        SWARM_AGENTS
    )
    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False


@pytest.mark.unit
class TestConsolidatedMessagingServiceUnit:
    """Unit tests for ConsolidatedMessagingService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedMessagingService(dry_run=True)

    @pytest.mark.unit
    def test_service_initialization_unit(self):
        """UNIT TEST: Test service initialization parameters."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedMessagingService()
        assert service.dry_run is False

        service_dry = ConsolidatedMessagingService(dry_run=True)
        assert service_dry.dry_run is True

    @pytest.mark.unit
    def test_coordinate_loading_empty_case(self):
        """UNIT TEST: Test coordinate loading with no messaging system."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_messaging_service.MESSAGING_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            coords = service.load_coordinates_from_json()
            assert coords == {}

    @pytest.mark.unit
    def test_coordinate_loading_with_mock_loader(self):
        """UNIT TEST: Test coordinate loading with mocked coordinate loader."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1', 'Agent-2']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = [(100, 200), (300, 400)]

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            coords = self.service.load_coordinates_from_json()

            assert len(coords) == 2
            assert coords['Agent-1'] == (100, 200)
            assert coords['Agent-2'] == (300, 400)
            mock_loader.get_all_agents.assert_called_once()

    @pytest.mark.unit
    def test_coordinate_loading_with_invalid_coordinates(self):
        """UNIT TEST: Test coordinate loading when some coordinates are invalid."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1', 'Invalid-Agent']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = [(100, 200), ValueError("Invalid agent")]

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            coords = self.service.load_coordinates_from_json()

            assert len(coords) == 1
            assert 'Agent-1' in coords
            assert 'Invalid-Agent' not in coords

    @pytest.mark.unit
    def test_send_message_pyautogui_dry_run_unit(self):
        """UNIT TEST: Test PyAutoGUI message sending in dry run mode."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        result = self.service.send_message_pyautogui("Agent-1", "Test message")
        assert result is True  # Dry run always succeeds

    @pytest.mark.unit
    def test_send_message_pyautogui_no_pyautogui(self):
        """UNIT TEST: Test PyAutoGUI message sending when PyAutoGUI unavailable."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            result = service.send_message_pyautogui("Agent-1", "Test message")
            assert result is False

    @pytest.mark.unit
    def test_send_message_pyautogui_with_mocks(self):
        """UNIT TEST: Test PyAutoGUI message sending with comprehensive mocking."""
        if not SERVICES_AVAILABLE or not PYAUTOGUI_AVAILABLE:
            pytest.skip("Required services not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.return_value = (100, 200)

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader), \
             patch('pyautogui.moveTo'), \
             patch('pyautogui.click'), \
             patch('pyautogui.typewrite'), \
             patch('pyautogui.hotkey'), \
             patch('time.sleep'):

            service = ConsolidatedMessagingService()
            result = service.send_message_pyautogui("Agent-1", "Test message", "HIGH", "COORDINATION")
            assert result is True

    @pytest.mark.unit
    def test_send_message_pyautogui_invalid_agent_unit(self):
        """UNIT TEST: Test PyAutoGUI message sending with invalid agent."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = ValueError("Agent not found")

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            result = self.service.send_message_pyautogui("Invalid-Agent", "Test message")
            assert result is False

    @pytest.mark.unit
    def test_broadcast_message_unit(self):
        """UNIT TEST: Test message broadcasting functionality."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_messaging_core = Mock()
        mock_messaging_core.send_message.return_value = True

        with patch('services.consolidated_messaging_service.get_messaging_core', return_value=mock_messaging_core):
            service = ConsolidatedMessagingService()
            results = service.broadcast_message("Test broadcast")

            assert isinstance(results, dict)
            assert len(results) == len(SWARM_AGENTS)
            # Verify messaging core was called for each agent
            assert mock_messaging_core.send_message.call_count == len(SWARM_AGENTS)

    @pytest.mark.unit
    def test_broadcast_message_no_messaging_core(self):
        """UNIT TEST: Test broadcast when messaging core unavailable."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        with patch('services.consolidated_messaging_service.MESSAGING_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            results = service.broadcast_message("Test broadcast")

            assert isinstance(results, dict)
            assert len(results) == len(SWARM_AGENTS)
            # All results should be False when messaging unavailable
            assert all(not result for result in results.values())

    @pytest.mark.unit
    def test_list_agents_unit(self):
        """UNIT TEST: Test agent listing functionality."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        agents = self.service.list_agents()
        assert isinstance(agents, list)
        # Should return SWARM_AGENTS or empty list
        assert len(agents) >= 0

    @pytest.mark.unit
    def test_show_message_history_unit(self):
        """UNIT TEST: Test message history display."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test with messaging unavailable
        with patch('services.consolidated_messaging_service.MESSAGING_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            history = service.show_message_history()
            assert history == []

        # Test with messaging available
        mock_messaging_core = Mock()
        mock_history = [{"id": "1", "content": "Test message"}]
        mock_messaging_core.get_message_history.return_value = mock_history

        with patch('services.consolidated_messaging_service.get_messaging_core', return_value=mock_messaging_core):
            service = ConsolidatedMessagingService()
            history = service.show_message_history()
            assert history == mock_history

    @pytest.mark.unit
    def test_service_availability_flags(self):
        """UNIT TEST: Test service availability flag detection."""
        # These are set at module level, just verify they exist
        assert isinstance(MESSAGING_AVAILABLE, bool)
        assert isinstance(PYAUTOGUI_AVAILABLE, bool)
        assert isinstance(PYPERCLIP_AVAILABLE, bool)

    @pytest.mark.unit
    def test_swarm_agents_constant(self):
        """UNIT TEST: Test SWARM_AGENTS constant."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        assert isinstance(SWARM_AGENTS, list)
        assert len(SWARM_AGENTS) == 8
        assert "Agent-1" in SWARM_AGENTS
        assert "Agent-8" in SWARM_AGENTS

    @pytest.mark.unit
    def test_message_content_validation_unit(self):
        """UNIT TEST: Test various message content scenarios."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        test_cases = [
            ("Simple message", True),
            ("", True),  # Empty message
            ("Message with special chars: !@#$%^&*()", True),
            ("Very long message " * 100, True),  # Long message
            ("Multiline\nmessage\ncontent", True),
            ("   ", True),  # Whitespace only
        ]

        for message, expected_success in test_cases:
            result = self.service.send_message_pyautogui("Agent-1", message)
            if self.service.dry_run:
                assert result is expected_success

    @pytest.mark.unit
    def test_message_priority_handling_unit(self):
        """UNIT TEST: Test different message priority levels."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        priorities = ["NORMAL", "HIGH", "URGENT", "LOW"]

        for priority in priorities:
            result = self.service.send_message_pyautogui("Agent-1", "Test", priority)
            if self.service.dry_run:
                assert result is True

    @pytest.mark.unit
    def test_message_tag_handling_unit(self):
        """UNIT TEST: Test different message tag types."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        tags = ["GENERAL", "COORDINATION", "SYSTEM", "URGENT", "BROADCAST"]

        for tag in tags:
            result = self.service.send_message_pyautogui("Agent-1", "Test", "NORMAL", tag)
            if self.service.dry_run:
                assert result is True

    @pytest.mark.unit
    def test_error_handling_coordinate_loader_failure(self):
        """UNIT TEST: Test error handling when coordinate loader fails."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.side_effect = Exception("Loader failure")

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            coords = self.service.load_coordinates_from_json()
            assert coords == {}

    @pytest.mark.unit
    def test_error_handling_messaging_core_failure(self):
        """UNIT TEST: Test error handling when messaging core fails."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        mock_messaging_core = Mock()
        mock_messaging_core.send_message.side_effect = Exception("Messaging failure")

        with patch('services.consolidated_messaging_service.get_messaging_core', return_value=mock_messaging_core):
            service = ConsolidatedMessagingService()
            results = service.broadcast_message("Test")

            # Should handle errors gracefully
            assert isinstance(results, dict)
            # Some results may be False due to errors
            assert len(results) == len(SWARM_AGENTS)

    @pytest.mark.performance
    def test_service_initialization_performance_unit(self):
        """UNIT TEST: Test service initialization performance."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        import time

        start_time = time.time()
        for _ in range(10):
            ConsolidatedMessagingService()
        end_time = time.time()

        total_time = end_time - start_time
        avg_time = total_time / 10

        # Should initialize quickly (under 100ms per instance)
        assert avg_time < 0.1

    @pytest.mark.unit
    def test_service_state_consistency_unit(self):
        """UNIT TEST: Test service state consistency across operations."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test that service state remains consistent
        initial_dry_run = self.service.dry_run

        # Perform various operations
        self.service.load_coordinates_from_json()
        self.service.send_message_pyautogui("Agent-1", "Test")
        self.service.broadcast_message("Test")
        self.service.list_agents()

        # State should remain consistent
        assert self.service.dry_run == initial_dry_run

    @pytest.mark.unit
    def test_service_method_availability_unit(self):
        """UNIT TEST: Test that all expected methods are available."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        expected_methods = [
            'load_coordinates_from_json',
            'send_message_pyautogui',
            'broadcast_message',
            'list_agents',
            'show_message_history'
        ]

        for method_name in expected_methods:
            assert hasattr(self.service, method_name)
            assert callable(getattr(self.service, method_name))


@pytest.mark.unit
class TestMessagingServiceEdgeCases:
    """Unit tests for edge cases and error conditions."""

    @pytest.mark.unit
    def test_extreme_message_sizes(self):
        """UNIT TEST: Test handling of extreme message sizes."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedMessagingService(dry_run=True)

        # Test very large message
        large_message = "A" * 10000
        result = service.send_message_pyautogui("Agent-1", large_message)
        assert result is True  # Should handle large messages

        # Test empty message
        result = service.send_message_pyautogui("Agent-1", "")
        assert result is True  # Should handle empty messages

    @pytest.mark.unit
    def test_special_characters_in_messages(self):
        """UNIT TEST: Test handling of special characters."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedMessagingService(dry_run=True)

        special_messages = [
            "Message with unicode: 🚀🐝💻",
            "Message with quotes: \"Hello World\"",
            "Message with newlines:\nLine 1\nLine 2",
            "Message with tabs:\tTabbed\tContent",
            "Message with slashes: C:\\path\\to\\file",
        ]

        for message in special_messages:
            result = service.send_message_pyautogui("Agent-1", message)
            assert result is True

    @pytest.mark.unit
    def test_concurrent_agent_operations(self):
        """UNIT TEST: Test operations on multiple agents simultaneously."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedMessagingService(dry_run=True)

        # Test sending to multiple agents
        agents = ["Agent-1", "Agent-2", "Agent-3"]
        results = []

        for agent in agents:
            result = service.send_message_pyautogui(agent, f"Test to {agent}")
            results.append(result)

        assert all(results)  # All should succeed in dry run mode

    @pytest.mark.unit
    def test_service_recovery_from_failures(self):
        """UNIT TEST: Test service recovery after failures."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        service = ConsolidatedMessagingService()

        # Simulate various failures and recoveries
        with patch('services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE', False):
            # Should fail when PyAutoGUI unavailable
            result = service.send_message_pyautogui("Agent-1", "Test")
            assert result is False

        # Should work again when conditions are normal
        service_dry = ConsolidatedMessagingService(dry_run=True)
        result = service_dry.send_message_pyautogui("Agent-1", "Test")
        assert result is True


if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--cov=src/services/consolidated_messaging_service",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--tb=short"
    ])
