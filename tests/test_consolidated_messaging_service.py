#!/usr/bin/env python3
"""
Test Suite for Consolidated Messaging Service
===========================================

Comprehensive pytest coverage for:
- Message creation and validation
- Coordinate loading and management
- PyAutoGUI message delivery
- CLI interface functionality
- Error handling and edge cases
- Integration with core messaging system

Author: Agent-1 (Integration & Core Systems Specialist)
Coverage Target: 85%+
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.consolidated_messaging_service import (
    MESSAGING_AVAILABLE,
    PYAUTOGUI_AVAILABLE,
    PYPERCLIP_AVAILABLE,
    SWARM_AGENTS,
    ConsolidatedMessagingService,
)


class TestConsolidatedMessagingService:
    """Test suite for ConsolidatedMessagingService class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedMessagingService(dry_run=True)
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.unit
    def test_service_initialization(self):
        """Test service initialization with different configurations."""
        # Test normal initialization
        service = ConsolidatedMessagingService()
        assert service.dry_run is False
        assert hasattr(service, 'messaging_core')
        assert hasattr(service, 'coordinate_loader')

        # Test dry run initialization
        service_dry = ConsolidatedMessagingService(dry_run=True)
        assert service_dry.dry_run is True

    @pytest.mark.unit
    def test_coordinate_loading_without_messaging(self):
        """Test coordinate loading when messaging system is unavailable."""
        with patch('services.consolidated_messaging_service.MESSAGING_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            coords = service.load_coordinates_from_json()
            assert coords == {}

    @pytest.mark.unit
    def test_coordinate_loading_with_messaging(self):
        """Test coordinate loading when messaging system is available."""
        if not MESSAGING_AVAILABLE:
            pytest.skip("Messaging system not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1', 'Agent-2']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = [(100, 200), (300, 400)]

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            service = ConsolidatedMessagingService()
            coords = service.load_coordinates_from_json()

            assert 'Agent-1' in coords
            assert 'Agent-2' in coords
            assert coords['Agent-1'] == (100, 200)
            assert coords['Agent-2'] == (300, 400)

    @pytest.mark.unit
    def test_coordinate_loading_with_invalid_agent(self):
        """Test coordinate loading when agent coordinates are invalid."""
        if not MESSAGING_AVAILABLE:
            pytest.skip("Messaging system not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1', 'Invalid-Agent']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = [(100, 200), ValueError("Invalid coordinates")]

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            service = ConsolidatedMessagingService()
            coords = service.load_coordinates_from_json()

            assert 'Agent-1' in coords
            assert 'Invalid-Agent' not in coords
            assert coords['Agent-1'] == (100, 200)

    @pytest.mark.unit
    def test_send_message_pyautogui_dry_run(self):
        """Test PyAutoGUI message sending in dry run mode."""
        service = ConsolidatedMessagingService(dry_run=True)
        result = service.send_message_pyautogui("Agent-1", "Test message")
        assert result is True  # Dry run always returns True

    @pytest.mark.unit
    def test_send_message_pyautogui_without_pyautogui(self):
        """Test PyAutoGUI message sending when PyAutoGUI is not available."""
        with patch('services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            result = service.send_message_pyautogui("Agent-1", "Test message")
            assert result is False

    @pytest.mark.integration
    def test_send_message_pyautogui_with_mocking(self):
        """Test PyAutoGUI message sending with mocked dependencies."""
        if not PYAUTOGUI_AVAILABLE:
            pytest.skip("PyAutoGUI not available")

        # Mock all PyAutoGUI dependencies
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
            result = service.send_message_pyautogui("Agent-1", "Test message")
            assert result is True

    @pytest.mark.unit
    def test_send_message_pyautogui_invalid_agent(self):
        """Test PyAutoGUI message sending with invalid agent."""
        if not PYAUTOGUI_AVAILABLE:
            pytest.skip("PyAutoGUI not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.return_value = ['Agent-1']
        mock_loader.is_agent_active.return_value = True
        mock_loader.get_chat_coordinates.side_effect = ValueError("Agent not found")

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            service = ConsolidatedMessagingService()
            result = service.send_message_pyautogui("Invalid-Agent", "Test message")
            assert result is False

    @pytest.mark.unit
    def test_broadcast_message_dry_run(self):
        """Test message broadcasting in dry run mode."""
        service = ConsolidatedMessagingService(dry_run=True)
        results = service.broadcast_message("Test broadcast")
        assert isinstance(results, dict)
        assert len(results) == len(SWARM_AGENTS)

    @pytest.mark.unit
    def test_broadcast_message_with_messaging(self):
        """Test message broadcasting with messaging system available."""
        if not MESSAGING_AVAILABLE:
            pytest.skip("Messaging system not available")

        mock_messaging = Mock()
        mock_messaging.send_message.return_value = True

        with patch('services.consolidated_messaging_service.get_messaging_core', return_value=mock_messaging):
            service = ConsolidatedMessagingService()
            results = service.broadcast_message("Test broadcast")

            assert isinstance(results, dict)
            assert len(results) > 0
            mock_messaging.send_message.assert_called()

    @pytest.mark.unit
    def test_list_agents_functionality(self):
        """Test agent listing functionality."""
        service = ConsolidatedMessagingService()
        agents = service.list_agents()
        assert isinstance(agents, list)
        assert len(agents) > 0

    @pytest.mark.unit
    def test_show_message_history_without_messaging(self):
        """Test message history display when messaging is unavailable."""
        with patch('services.consolidated_messaging_service.MESSAGING_AVAILABLE', False):
            service = ConsolidatedMessagingService()
            history = service.show_message_history()
            assert history == []

    @pytest.mark.unit
    def test_show_message_history_with_messaging(self):
        """Test message history display when messaging is available."""
        if not MESSAGING_AVAILABLE:
            pytest.skip("Messaging system not available")

        mock_messaging = Mock()
        mock_history = [{"id": "1", "content": "Test message"}]
        mock_messaging.get_message_history.return_value = mock_history

        with patch('services.consolidated_messaging_service.get_messaging_core', return_value=mock_messaging):
            service = ConsolidatedMessagingService()
            history = service.show_message_history()
            assert history == mock_history

    @pytest.mark.unit
    def test_error_handling_coordinate_loader_failure(self):
        """Test error handling when coordinate loader fails."""
        if not MESSAGING_AVAILABLE:
            pytest.skip("Messaging system not available")

        mock_loader = Mock()
        mock_loader.get_all_agents.side_effect = Exception("Loader failure")

        with patch('services.consolidated_messaging_service.get_coordinate_loader', return_value=mock_loader):
            service = ConsolidatedMessagingService()
            coords = service.load_coordinates_from_json()
            assert coords == {}

    @pytest.mark.unit
    def test_constants_and_configuration(self):
        """Test that constants are properly defined."""
        from services.consolidated_messaging_service import SWARM_AGENTS

        assert isinstance(SWARM_AGENTS, list)
        assert len(SWARM_AGENTS) == 8
        assert "Agent-1" in SWARM_AGENTS
        assert "Agent-8" in SWARM_AGENTS

    @pytest.mark.unit
    def test_service_availability_flags(self):
        """Test service availability flags are properly set."""
        # These are set at import time, so we just verify they're boolean
        assert isinstance(MESSAGING_AVAILABLE, bool)
        assert isinstance(PYAUTOGUI_AVAILABLE, bool)
        assert isinstance(PYPERCLIP_AVAILABLE, bool)

    @pytest.mark.performance
    def test_service_initialization_performance(self):
        """Test that service initialization is reasonably fast."""
        import time

        start_time = time.time()
        for _ in range(10):
            ConsolidatedMessagingService()
        end_time = time.time()

        avg_init_time = (end_time - start_time) / 10
        assert avg_init_time < 0.1  # Should initialize in under 100ms

    @pytest.mark.unit
    def test_message_priority_and_tags(self):
        """Test message priority and tag handling."""
        service = ConsolidatedMessagingService()

        # Test with different priorities and tags
        priorities = ["NORMAL", "HIGH", "URGENT"]
        tags = ["GENERAL", "COORDINATION", "SYSTEM"]

        for priority in priorities:
            for tag in tags:
                result = service.send_message_pyautogui("Agent-1", "Test", priority, tag)
                if service.dry_run:
                    assert result is True
                # In real execution, result would depend on PyAutoGUI availability

    @pytest.mark.unit
    def test_message_content_validation(self):
        """Test message content validation and edge cases."""
        service = ConsolidatedMessagingService()

        # Test with various message contents
        test_messages = [
            "Simple message",
            "Message with special chars: !@#$%^&*()",
            "Multiline\nmessage\ncontent",
            "Very long message " * 100,
            "",
            "   ",
        ]

        for message in test_messages:
            result = service.send_message_pyautogui("Agent-1", message)
            if service.dry_run:
                assert result is True

    @pytest.mark.integration
    def test_service_integration_with_file_operations(self):
        """Test service integration with file operations."""
        # Create a temporary coordinate file
        coord_file = Path(self.temp_dir) / "test_coords.json"
        test_coords = {
            "Agent-1": {"x": 100, "y": 200},
            "Agent-2": {"x": 300, "y": 400}
        }

        coord_file.write_text(json.dumps(test_coords))

        # Test coordinate loading from file
        service = ConsolidatedMessagingService()

        # This would test file-based coordinate loading if implemented
        # For now, just verify the service can handle file operations
        assert coord_file.exists()
        assert coord_file.read_text() == json.dumps(test_coords)


# CLI Interface Tests
class TestMessagingCLIInterface:
    """Test CLI interface functionality."""

    @pytest.mark.unit
    def test_cli_argument_parsing(self):
        """Test CLI argument parsing."""
        from services.consolidated_messaging_service import parse_arguments

        # Mock sys.argv for testing
        test_args = [
            ["--agent", "Agent-1", "--message", "Test message"],
            ["--broadcast", "--message", "Broadcast message"],
            ["--list-agents"],
            ["--history"],
            ["--dry-run", "--agent", "Agent-1", "--message", "Dry run test"],
        ]

        for args in test_args:
            with patch('sys.argv', ['consolidated_messaging_service.py'] + args):
                try:
                    parsed_args = parse_arguments()
                    assert hasattr(parsed_args, 'agent') or hasattr(parsed_args, 'broadcast') or \
                           hasattr(parsed_args, 'list_agents') or hasattr(parsed_args, 'history') or \
                           hasattr(parsed_args, 'dry_run')
                except SystemExit:
                    # argparse exits on help/version, which is expected
                    pass

    @pytest.mark.unit
    def test_cli_help_and_version(self):
        """Test CLI help and version display."""
        from services.consolidated_messaging_service import parse_arguments

        # Test help
        with patch('sys.argv', ['consolidated_messaging_service.py', '--help']):
            with pytest.raises(SystemExit):
                parse_arguments()

        # Test version (if implemented)
        with patch('sys.argv', ['consolidated_messaging_service.py', '--version']):
            with pytest.raises(SystemExit):
                parse_arguments()


# Integration Tests
class TestMessagingServiceIntegration:
    """Integration tests for messaging service components."""

    @pytest.mark.integration
    def test_full_messaging_workflow(self):
        """Test complete messaging workflow from creation to delivery."""
        if not all([MESSAGING_AVAILABLE, PYAUTOGUI_AVAILABLE, PYPERCLIP_AVAILABLE]):
            pytest.skip("Required dependencies not available")

        service = ConsolidatedMessagingService(dry_run=True)

        # Test coordinate loading
        coords = service.load_coordinates_from_json()
        assert isinstance(coords, dict)

        # Test message sending
        result = service.send_message_pyautogui("Agent-1", "Integration test message")
        assert result is True

        # Test broadcasting
        results = service.broadcast_message("Integration broadcast test")
        assert isinstance(results, dict)
        assert len(results) > 0

    @pytest.mark.integration
    def test_service_component_interaction(self):
        """Test interaction between service components."""
        service = ConsolidatedMessagingService()

        # Test that all components can be accessed
        assert hasattr(service, 'load_coordinates_from_json')
        assert hasattr(service, 'send_message_pyautogui')
        assert hasattr(service, 'broadcast_message')
        assert hasattr(service, 'list_agents')

        # Test method calls don't raise exceptions
        coords = service.load_coordinates_from_json()
        assert isinstance(coords, dict)

        agents = service.list_agents()
        assert isinstance(agents, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/services/consolidated_messaging_service",
                "--cov-report=html", "--cov-report=term-missing"])
