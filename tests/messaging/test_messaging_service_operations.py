#!/usr/bin/env python3
"""
Messaging Service Operations Tests - Modular Test Suite
=======================================================

Operations tests for messaging service.
Tests message sending, broadcasting, and PyAutoGUI integration.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from unittest.mock import patch

import pytest

from tests.utils.test_base_classes import MessagingServiceTestBase


class TestMessagingServiceSendMessage(MessagingServiceTestBase):
    """Test messaging service send message functionality."""

    @pytest.mark.unit
    @patch("services.messaging.core.messaging_service.pyautogui")
    @patch("services.messaging.core.messaging_service.pyperclip")
    def test_send_message_success(self, mock_pyperclip, mock_pyautogui, messaging_service):
        """Test successful message sending."""
        # Mock PyAutoGUI and Pyperclip
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None
        mock_pyperclip.copy.return_value = None

        result = messaging_service.send_message(
            "Agent-1", "Test message", "Discord-Commander", "NORMAL"
        )

        self.assert_message_sent_successfully(result, "Agent-1")
        mock_pyautogui.click.assert_called()
        mock_pyperclip.copy.assert_called()
        mock_pyautogui.hotkey.assert_called()

    @pytest.mark.unit
    @patch("services.messaging.core.messaging_service.pyautogui")
    @patch("services.messaging.core.messaging_service.pyperclip")
    def test_send_message_pyautogui_error(self, mock_pyperclip, mock_pyautogui, messaging_service):
        """Test message sending with PyAutoGUI error."""
        # Mock PyAutoGUI to raise exception
        mock_pyautogui.click.side_effect = Exception("PyAutoGUI error")
        mock_pyperclip.copy.return_value = None

        result = messaging_service.send_message(
            "Agent-1", "Test message", "Discord-Commander", "NORMAL"
        )
        assert result == False

    @pytest.mark.unit
    def test_send_message_invalid_agent(self, messaging_service):
        """Test message sending to invalid agent."""
        result = messaging_service.send_message(
            "InvalidAgent", "Test message", "Discord-Commander", "NORMAL"
        )
        self.assert_message_send_failed(result, "InvalidAgent")

    @pytest.mark.unit
    def test_send_message_inactive_agent(self, messaging_service):
        """Test message sending to inactive agent."""
        with patch.object(messaging_service, "_is_agent_active", return_value=False):
            result = messaging_service.send_message(
                "Agent-1", "Test message", "Discord-Commander", "NORMAL"
            )
            self.assert_message_send_failed(result, "Agent-1")


class TestMessagingServiceBroadcastMessage(MessagingServiceTestBase):
    """Test messaging service broadcast message functionality."""

    @pytest.mark.unit
    @patch("services.messaging.core.messaging_service.pyautogui")
    @patch("services.messaging.core.messaging_service.pyperclip")
    def test_broadcast_message_success(self, mock_pyperclip, mock_pyautogui, messaging_service):
        """Test successful broadcast message."""
        # Mock PyAutoGUI and Pyperclip
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None
        mock_pyperclip.copy.return_value = None

        results = messaging_service.broadcast_message(
            "Test broadcast", "Discord-Commander", "NORMAL"
        )

        self.assert_broadcast_results(results, 8)
        for agent_id in self.test_agents:
            assert agent_id in results
            assert results[agent_id] == True

    @pytest.mark.unit
    def test_broadcast_message_partial_failure(self, messaging_service):
        """Test broadcast message with partial failure."""

        # Mock send_message to fail for Agent-1
        def mock_send_message(agent_id, message, from_agent, priority):
            if agent_id == "Agent-1":
                return False
            return True

        with patch.object(messaging_service, "send_message", side_effect=mock_send_message):
            results = messaging_service.broadcast_message(
                "Test broadcast", "Discord-Commander", "NORMAL"
            )

        self.assert_broadcast_results(results, 8)
        assert results["Agent-1"] == False  # Should fail
        for agent_id in self.test_agents[1:]:  # Others should succeed
            assert results[agent_id] == True

    @pytest.mark.unit
    def test_broadcast_message_no_agents(self, messaging_service):
        """Test broadcast message with no active agents."""
        # Mock no active agents
        with patch.object(messaging_service, "_is_agent_active", return_value=False):
            results = messaging_service.broadcast_message(
                "Test broadcast", "Discord-Commander", "NORMAL"
            )
            self.assert_broadcast_results(results, 8)
            assert all(result == False for result in results.values())


class TestMessagingServicePyAutoGUIIntegration(MessagingServiceTestBase):
    """Test messaging service PyAutoGUI integration."""

    @pytest.mark.integration
    @patch("services.messaging.core.messaging_service.pyautogui")
    def test_pyautogui_coordinate_clicking(self, mock_pyautogui, messaging_service):
        """Test PyAutoGUI coordinate clicking."""
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None

        # Mock Pyperclip separately
        with patch("services.messaging.core.messaging_service.pyperclip") as mock_pyperclip:
            mock_pyperclip.copy.return_value = None

            result = messaging_service.send_message(
                "Agent-1", "Test message", "Discord-Commander", "NORMAL"
            )

        assert result == True
        # Verify PyAutoGUI was called with correct coordinates
        mock_pyautogui.click.assert_called()
        # The coordinates should match Agent-1's coordinates
        call_args = mock_pyautogui.click.call_args[0]
        assert call_args == (-1269, 481)  # Agent-1 coordinates

    @pytest.mark.integration
    @patch("services.messaging.core.messaging_service.pyautogui")
    def test_pyautogui_hotkey_sequence(self, mock_pyautogui, messaging_service):
        """Test PyAutoGUI hotkey sequence."""
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None

        # Mock Pyperclip separately
        with patch("services.messaging.core.messaging_service.pyperclip") as mock_pyperclip:
            mock_pyperclip.copy.return_value = None

            result = messaging_service.send_message(
                "Agent-1", "Test message", "Discord-Commander", "NORMAL"
            )

        assert result == True
        # Verify hotkey sequence was called
        mock_pyautogui.hotkey.assert_called()
        # Should call Ctrl+V to paste
        mock_pyautogui.hotkey.assert_called_with("ctrl", "v")

    @pytest.mark.integration
    @patch("services.messaging.core.messaging_service.pyautogui")
    def test_pyautogui_error_handling(self, mock_pyautogui, messaging_service):
        """Test PyAutoGUI error handling."""
        # Mock PyAutoGUI to raise different types of exceptions
        mock_pyautogui.click.side_effect = Exception("Screen not accessible")
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None

        # Mock Pyperclip separately
        with patch("services.messaging.core.messaging_service.pyperclip") as mock_pyperclip:
            mock_pyperclip.copy.return_value = None

            result = messaging_service.send_message(
                "Agent-1", "Test message", "Discord-Commander", "NORMAL"
            )

        # Should handle error gracefully
        assert result == False


class TestMessagingServicePerformance(MessagingServiceTestBase):
    """Test messaging service performance."""

    @pytest.mark.performance
    def test_message_formatting_performance(self, messaging_service):
        """Test message formatting performance."""

        def format_message():
            return messaging_service._format_a2a_message(
                "Discord-Commander", "Agent-1", "Test", "NORMAL"
            )

        # Should be fast (less than 1 second for 1000 messages)
        self.assert_performance_threshold(format_message, "message_formatting", 1000)

    @pytest.mark.performance
    def test_agent_validation_performance(self, messaging_service):
        """Test agent validation performance."""

        def validate_agent():
            return messaging_service._is_agent_active("Agent-1")

        # Should be very fast (less than 0.1 seconds for 1000 validations)
        self.assert_performance_threshold(validate_agent, "agent_validation", 1000)

    @pytest.mark.performance
    def test_coordinate_loading_performance(self, coordinate_loader):
        """Test coordinate loading performance."""

        def load_coordinates():
            coordinate_loader.load()

        # Should be fast (less than 10ms for loading)
        self.assert_performance_threshold(load_coordinates, "coordinate_loading", 1)


class TestMessagingServiceThreadSafety(MessagingServiceTestBase):
    """Test messaging service thread safety."""

    @pytest.mark.performance
    def test_thread_safety_agent_validation(self, messaging_service):
        """Test messaging service thread safety for agent validation."""

        def validate_agent():
            return messaging_service._is_agent_active("Agent-1")

        self.assert_thread_safety(validate_agent, 10)

    @pytest.mark.performance
    def test_thread_safety_message_formatting(self, messaging_service):
        """Test messaging service thread safety for message formatting."""

        def format_message():
            return messaging_service._format_a2a_message(
                "Discord-Commander", "Agent-1", "Test", "NORMAL"
            )

        self.assert_thread_safety(format_message, 10)

    @pytest.mark.performance
    def test_thread_safety_coordinate_access(self, coordinate_loader):
        """Test coordinate loader thread safety."""

        def get_coordinates():
            return coordinate_loader.get_agent_coordinates("Agent-1")

        self.assert_thread_safety(get_coordinates, 10)
