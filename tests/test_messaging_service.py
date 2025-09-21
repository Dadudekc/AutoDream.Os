#!/usr/bin/env python3
"""
Test Messaging Service - Comprehensive Test Suite
=================================================

Comprehensive test suite for messaging service functionality.
Tests all messaging operations, PyAutoGUI integration, and error handling.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestMessagingService:
    """Test suite for messaging service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.coord_path = str(Path(__file__).parent.parent / "config" / "coordinates.json")
        self.test_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        self.expected_coordinates = {
            "Agent-1": (-1269, 481),
            "Agent-2": (-308, 480),
            "Agent-3": (-1269, 1001),
            "Agent-4": (-308, 1000),
            "Agent-5": (652, 421),
            "Agent-6": (1612, 419),
            "Agent-7": (920, 851),
            "Agent-8": (1611, 941)
        }
    
    def test_messaging_service_initialization(self):
        """Test messaging service initialization."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        assert service.coords_file == self.coord_path
        assert service.loader is not None
        assert service.validation_report is not None
    
    def test_messaging_service_default_initialization(self):
        """Test messaging service with default coordinate path."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService()
        assert service.coords_file == "config/coordinates.json"
        assert service.loader is not None
    
    def test_agent_validation(self):
        """Test agent validation."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Test valid agents
        for agent_id in self.test_agents:
            assert service._is_agent_active(agent_id) == True
        
        # Test invalid agent (defaults to True if not found)
        assert service._is_agent_active("InvalidAgent") == True
        
        # Test empty agent ID (defaults to True if not found)
        assert service._is_agent_active("") == True
        
        # Test None agent ID (defaults to True if not found)
        assert service._is_agent_active(None) == True
    
    def test_message_formatting(self):
        """Test A2A message formatting."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Test basic message formatting
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "Test message", "NORMAL")
        
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted
        assert "Priority: NORMAL" in formatted
        assert "Test message" in formatted
        assert "[A2A] MESSAGE" in formatted
        assert "DISCORD DEVLOG REMINDER" in formatted
    
    def test_message_formatting_different_priorities(self):
        """Test message formatting with different priorities."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        priorities = ["NORMAL", "HIGH", "URGENT"]
        for priority in priorities:
            formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "Test", priority)
            assert f"Priority: {priority}" in formatted
    
    def test_message_formatting_different_senders(self):
        """Test message formatting with different senders."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        senders = ["Discord-Commander", "Agent-1", "Agent-2", "Test-Sender"]
        for sender in senders:
            formatted = service._format_a2a_message(sender, "Agent-1", "Test", "NORMAL")
            assert f"FROM: {sender}" in formatted
    
    def test_message_formatting_special_characters(self):
        """Test message formatting with special characters."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        special_messages = [
            "Message with émojis 🚀",
            "Message with newlines\nand tabs\t",
            "Message with quotes \"test\" and 'single'",
            "Message with symbols @#$%^&*()",
            "Message with unicode: 中文测试"
        ]
        
        for message in special_messages:
            formatted = service._format_a2a_message("Discord-Commander", "Agent-1", message, "NORMAL")
            assert message in formatted
    
    def test_message_formatting_long_message(self):
        """Test message formatting with long message."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        long_message = "A" * 2000
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", long_message, "NORMAL")
        assert long_message in formatted
    
    @patch('services.messaging.core.messaging_service.pyautogui')
    @patch('services.messaging.core.messaging_service.pyperclip')
    def test_send_message_success(self, mock_pyperclip, mock_pyautogui):
        """Test successful message sending."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Mock PyAutoGUI and Pyperclip
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None
        mock_pyperclip.copy.return_value = None
        
        service = MessagingService(self.coord_path)
        
        result = service.send_message("Agent-1", "Test message", "Discord-Commander", "NORMAL")
        
        assert result == True
        mock_pyautogui.click.assert_called()
        mock_pyperclip.copy.assert_called()
        mock_pyautogui.hotkey.assert_called()
    
    def test_send_message_invalid_agent(self):
        """Test message sending to invalid agent."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Invalid agent will default to active=True, so it will try to send
        # but fail at coordinate retrieval
        result = service.send_message("InvalidAgent", "Test message", "Discord-Commander", "NORMAL")
        assert result == False
    
    def test_send_message_inactive_agent(self):
        """Test message sending to inactive agent."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Mock inactive agent
        with patch.object(service, '_is_agent_active', return_value=False):
            result = service.send_message("Agent-1", "Test message", "Discord-Commander", "NORMAL")
            assert result == False
    
    @patch('services.messaging.core.messaging_service.pyautogui')
    @patch('services.messaging.core.messaging_service.pyperclip')
    def test_send_message_pyautogui_error(self, mock_pyperclip, mock_pyautogui):
        """Test message sending with PyAutoGUI error."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Mock PyAutoGUI to raise exception
        mock_pyautogui.click.side_effect = Exception("PyAutoGUI error")
        mock_pyperclip.copy.return_value = None
        
        service = MessagingService(self.coord_path)
        
        result = service.send_message("Agent-1", "Test message", "Discord-Commander", "NORMAL")
        assert result == False
    
    @patch('services.messaging.core.messaging_service.pyautogui')
    @patch('services.messaging.core.messaging_service.pyperclip')
    def test_broadcast_message_success(self, mock_pyperclip, mock_pyautogui):
        """Test successful broadcast message."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Mock PyAutoGUI and Pyperclip
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None
        mock_pyperclip.copy.return_value = None
        
        service = MessagingService(self.coord_path)
        
        results = service.broadcast_message("Test broadcast", "Discord-Commander", "NORMAL")
        
        assert len(results) == 8
        for agent_id in self.test_agents:
            assert agent_id in results
            assert results[agent_id] == True
    
    def test_broadcast_message_partial_failure(self):
        """Test broadcast message with partial failure."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Mock send_message to fail for Agent-1
        def mock_send_message(agent_id, message, from_agent, priority):
            if agent_id == "Agent-1":
                return False
            return True
        
        with patch.object(service, 'send_message', side_effect=mock_send_message):
            results = service.broadcast_message("Test broadcast", "Discord-Commander", "NORMAL")
        
        assert len(results) == 8
        assert results["Agent-1"] == False  # Should fail
        for agent_id in self.test_agents[1:]:  # Others should succeed
            assert results[agent_id] == True
    
    def test_broadcast_message_no_agents(self):
        """Test broadcast message with no active agents."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Mock no active agents
        with patch.object(service, '_is_agent_active', return_value=False):
            results = service.broadcast_message("Test broadcast", "Discord-Commander", "NORMAL")
            assert len(results) == 8
            assert all(result == False for result in results.values())
    
    def test_messaging_service_error_handling(self):
        """Test messaging service error handling."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Test with invalid coordinate file
        service = MessagingService("invalid/path/coordinates.json")
        
        # Should handle gracefully (falls back to default coordinates)
        result = service.send_message("Agent-1", "Test", "Discord-Commander")
        # Result depends on whether PyAutoGUI is available
        assert isinstance(result, bool)
    
    def test_messaging_service_validation_report(self):
        """Test messaging service validation report."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        assert service.validation_report is not None
        assert hasattr(service.validation_report, 'is_all_ok')
        assert hasattr(service.validation_report, 'issues')
    
    def test_messaging_service_coordinate_loading(self):
        """Test messaging service coordinate loading."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Test coordinate loading
        agent_ids = service.loader.get_agent_ids()
        assert len(agent_ids) == 8
        assert set(agent_ids) == set(self.test_agents)
        
        # Test coordinate retrieval
        for agent_id, expected_coords in self.expected_coordinates.items():
            coords = service.loader.get_agent_coordinates(agent_id)
            assert coords == expected_coords
    
    def test_messaging_service_thread_safety(self):
        """Test messaging service thread safety."""
        from services.messaging.core.messaging_service import MessagingService
        import threading
        
        service = MessagingService(self.coord_path)
        results = []
        
        def send_test_message():
            result = service._is_agent_active("Agent-1")
            results.append(result)
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=send_test_message)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all results are correct
        assert len(results) == 10
        assert all(result == True for result in results)
    
    def test_messaging_service_performance(self):
        """Test messaging service performance."""
        from services.messaging.core.messaging_service import MessagingService
        import time
        
        service = MessagingService(self.coord_path)
        
        # Test message formatting performance
        start_time = time.time()
        for _ in range(1000):
            formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "Test", "NORMAL")
        formatting_time = time.time() - start_time
        
        # Formatting should be fast (less than 1 second for 1000 messages)
        assert formatting_time < 1.0
        
        # Test agent validation performance
        start_time = time.time()
        for _ in range(1000):
            is_active = service._is_agent_active("Agent-1")
        validation_time = time.time() - start_time
        
        # Validation should be very fast (less than 0.1 seconds for 1000 validations)
        assert validation_time < 0.1
    
    def test_messaging_service_edge_cases(self):
        """Test messaging service edge cases."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Test with empty message
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "", "NORMAL")
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted
        
        # Test with None message
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", None, "NORMAL")
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted
        
        # Test with very long sender name
        long_sender = "A" * 100
        formatted = service._format_a2a_message(long_sender, "Agent-1", "Test", "NORMAL")
        assert f"FROM: {long_sender}" in formatted
    
    def test_messaging_service_custom_coordinates(self):
        """Test messaging service with custom coordinates."""
        from services.messaging.core.messaging_service import MessagingService
        import tempfile
        import json
        
        # Create custom coordinates
        custom_coords = {
            "version": "2.0",
            "agents": {
                "CustomAgent-1": {
                    "active": True,
                    "chat_input_coordinates": [100, 200],
                    "onboarding_coordinates": [150, 250],
                    "description": "Custom Agent 1"
                }
            }
        }
        
        # Create temporary file with custom coordinates
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_coords, f)
            temp_path = f.name
        
        try:
            service = MessagingService(temp_path)
            
            # Test with custom agent
            assert service._is_agent_active("CustomAgent-1") == True
            assert service._is_agent_active("Agent-1") == True  # Defaults to True if not found
            
            # Test message formatting
            formatted = service._format_a2a_message("Discord-Commander", "CustomAgent-1", "Test", "NORMAL")
            assert "TO: CustomAgent-1" in formatted
            
        finally:
            Path(temp_path).unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
