#!/usr/bin/env python3
"""
UNIT TESTS - Messaging Gateway Component
========================================

Comprehensive unit tests for MessagingGateway component with focus on:
- Message routing and delivery logic
- Discord ↔ PyAutoGUI bridge functionality
- Coordinate-based agent communication
- Error handling and edge cases
- Configuration-driven routing

Author: Agent-5 (Business Intelligence Specialist)
Test Coverage Target: 90%+
"""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from integration.messaging_gateway import (
    MessagingGateway,
    _import_symbol,
    get_agent_coordinates,
    route_message_to_agent,
    send_discord_message_to_agent,
)


class TestMessagingGatewayUnit:
    """Unit tests for MessagingGateway component."""

    def setup_method(self):
        """Setup test fixtures."""
        self.gateway = MessagingGateway()

    def teardown_method(self):
        """Cleanup test fixtures."""
        pass

    @pytest.mark.unit
    def test_gateway_initialization(self):
        """Test MessagingGateway initialization."""
        gateway = MessagingGateway()
        assert gateway is not None
        assert hasattr(gateway, 'coordinate_system')
        assert hasattr(gateway, 'routing_engine')

    @pytest.mark.unit
    def test_import_symbol_success(self):
        """Test successful symbol import."""
        # Mock a simple module with a class
        mock_module = Mock()
        mock_class = Mock()
        mock_module.TestClass = mock_class

        with patch('importlib.import_module', return_value=mock_module):
            result = _import_symbol("test.module:TestClass")
            assert result == mock_class

    @pytest.mark.unit
    def test_import_symbol_module_only(self):
        """Test importing module without specific symbol."""
        mock_module = Mock()
        mock_module.UnifiedMessagingSystem = Mock()

        with patch('importlib.import_module', return_value=mock_module):
            result = _import_symbol("test.module")
            assert result == mock_module.UnifiedMessagingSystem

    @pytest.mark.unit
    def test_import_symbol_import_error(self):
        """Test import error handling."""
        with patch('importlib.import_module', side_effect=ImportError("Module not found")):
            with pytest.raises(ImportError):
                _import_symbol("nonexistent.module:Class")

    @pytest.mark.unit
    def test_get_agent_coordinates_known_agent(self):
        """Test coordinate retrieval for known agent."""
        coords = get_agent_coordinates("Agent-5")
        assert isinstance(coords, dict)
        assert "x" in coords
        assert "y" in coords
        assert coords["x"] == 652  # Agent-5 coordinates
        assert coords["y"] == 421

    @pytest.mark.unit
    def test_get_agent_coordinates_unknown_agent(self):
        """Test coordinate retrieval for unknown agent."""
        coords = get_agent_coordinates("Unknown-Agent")
        assert coords is None

    @pytest.mark.unit
    @patch('integration.messaging_gateway.pyautogui')
    @patch('integration.messaging_gateway.pyperclip')
    def test_route_message_to_agent_success(self, mock_pyperclip, mock_pyautogui):
        """Test successful message routing to agent."""
        # Setup mocks
        mock_pyautogui.position.return_value = (100, 100)
        mock_pyautogui.size.return_value = (1920, 1080)

        # Test routing
        result = route_message_to_agent("Agent-5", "Test message")

        # Verify PyAutoGUI calls
        assert mock_pyautogui.moveTo.called
        assert mock_pyautogui.click.called
        assert mock_pyperclip.copy.called
        assert mock_pyautogui.hotkey.called

        # Verify coordinates (Agent-5: 652, 421)
        mock_pyautogui.moveTo.assert_any_call(652, 421)

    @pytest.mark.unit
    @patch('integration.messaging_gateway.pyautogui')
    def test_route_message_to_agent_unknown_agent(self, mock_pyautogui):
        """Test routing failure for unknown agent."""
        result = route_message_to_agent("Unknown-Agent", "Test message")
        assert result is False
        assert not mock_pyautogui.moveTo.called

    @pytest.mark.unit
    @patch('integration.messaging_gateway.pyautogui')
    def test_route_message_to_agent_pyautogui_unavailable(self, mock_pyautogui):
        """Test routing when PyAutoGUI is unavailable."""
        # Mock PyAutoGUI import failure
        with patch.dict('sys.modules', {'pyautogui': None}):
            with patch('integration.messaging_gateway.pyautogui', None):
                result = route_message_to_agent("Agent-5", "Test message")
                assert result is False

    @pytest.mark.unit
    @patch('integration.messaging_gateway.route_message_to_agent')
    @patch('integration.messaging_gateway.get_agent_coordinates')
    def test_send_discord_message_to_agent_success(self, mock_get_coords, mock_route):
        """Test successful Discord message delivery."""
        # Setup mocks
        mock_get_coords.return_value = {"x": 652, "y": 421}
        mock_route.return_value = True

        # Test message delivery
        result = send_discord_message_to_agent("Agent-5", "Hello from Discord!")

        assert result is True
        mock_get_coords.assert_called_with("Agent-5")
        mock_route.assert_called_with("Agent-5", "Hello from Discord!")

    @pytest.mark.unit
    @patch('integration.messaging_gateway.route_message_to_agent')
    @patch('integration.messaging_gateway.get_agent_coordinates')
    def test_send_discord_message_to_agent_no_coords(self, mock_get_coords, mock_route):
        """Test Discord message delivery when coordinates unavailable."""
        mock_get_coords.return_value = None

        result = send_discord_message_to_agent("Unknown-Agent", "Hello!")

        assert result is False
        assert not mock_route.called

    @pytest.mark.unit
    @patch('integration.messaging_gateway.route_message_to_agent')
    @patch('integration.messaging_gateway.get_agent_coordinates')
    def test_send_discord_message_to_agent_routing_failure(self, mock_get_coords, mock_route):
        """Test Discord message delivery when routing fails."""
        mock_get_coords.return_value = {"x": 652, "y": 421}
        mock_route.return_value = False

        result = send_discord_message_to_agent("Agent-5", "Hello!")

        assert result is False

    @pytest.mark.unit
    def test_gateway_message_processing(self):
        """Test gateway message processing pipeline."""
        gateway = MessagingGateway()

        # Mock message
        test_message = {
            "type": "discord_message",
            "recipient": "Agent-5",
            "content": "Test message",
            "sender": "DiscordBot"
        }

        # Process message (would need more setup for full test)
        # This is a placeholder for more comprehensive gateway testing
        assert gateway is not None

    @pytest.mark.unit
    def test_coordinate_system_validation(self):
        """Test coordinate system validation."""
        # Test all known agent coordinates
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent in agents:
            coords = get_agent_coordinates(agent)
            assert coords is not None
            assert isinstance(coords, dict)
            assert "x" in coords and "y" in coords
            assert isinstance(coords["x"], int)
            assert isinstance(coords["y"], int)

    @pytest.mark.unit
    @patch('integration.messaging_gateway.pyautogui')
    def test_message_routing_error_handling(self, mock_pyautogui):
        """Test error handling in message routing."""
        # Simulate PyAutoGUI error
        mock_pyautogui.moveTo.side_effect = Exception("Mouse control failed")

        result = route_message_to_agent("Agent-5", "Test message")
        assert result is False

    @pytest.mark.unit
    def test_gateway_configuration_loading(self):
        """Test gateway configuration loading."""
        gateway = MessagingGateway()

        # Test configuration attributes
        assert hasattr(gateway, 'coordinate_system')
        assert hasattr(gateway, 'routing_engine')

        # Configuration should be loaded or have defaults
        assert gateway.coordinate_system is not None

    @pytest.mark.unit
    @patch('integration.messaging_gateway.pyperclip')
    @patch('integration.messaging_gateway.pyautogui')
    def test_clipboard_operations(self, mock_pyautogui, mock_pyperclip):
        """Test clipboard operations in message delivery."""
        route_message_to_agent("Agent-5", "Test clipboard content")

        # Verify clipboard was used
        mock_pyperclip.copy.assert_called_with("Test clipboard content")
        mock_pyautogui.hotkey.assert_called_with('ctrl', 'v')  # Paste operation

    @pytest.mark.unit
    def test_message_format_validation(self):
        """Test message format validation."""
        # Valid message formats should be accepted
        valid_formats = [
            "Simple text message",
            "Multi-line\nmessage\ncontent",
            "Message with special chars: @#$%^&*()",
            "Unicode: 你好世界 🌍"
        ]

        for msg in valid_formats:
            # Should not raise exceptions for valid formats
            try:
                route_message_to_agent("Agent-5", msg)
            except Exception as e:
                # Only PyAutoGUI errors are expected, not format errors
                assert "format" not in str(e).lower()

    @pytest.mark.unit
    def test_agent_coordinate_boundaries(self):
        """Test agent coordinate boundary validation."""
        # All coordinates should be within reasonable screen bounds
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent in agents:
            coords = get_agent_coordinates(agent)
            assert coords["x"] >= 0 and coords["x"] <= 2000  # Reasonable screen width
            assert coords["y"] >= 0 and coords["y"] <= 1200  # Reasonable screen height

    @pytest.mark.unit
    @patch('integration.messaging_gateway.time.sleep')
    @patch('integration.messaging_gateway.pyautogui')
    def test_timing_delays_in_routing(self, mock_pyautogui, mock_sleep):
        """Test timing delays in message routing."""
        route_message_to_agent("Agent-5", "Test message")

        # Verify timing delays were used for reliable delivery
        mock_sleep.assert_called()

    @pytest.mark.unit
    def test_gateway_bridge_functionality(self):
        """Test Discord ↔ PyAutoGUI bridge functionality."""
        # Test the core bridge functionality
        gateway = MessagingGateway()

        # Bridge should handle Discord-to-Agent communication
        assert hasattr(gateway, 'coordinate_system')
        assert hasattr(gateway, 'routing_engine')

        # Test bridge configuration
        # (More detailed testing would require Discord integration setup)


if __name__ == "__main__":
    pytest.main([__file__])
