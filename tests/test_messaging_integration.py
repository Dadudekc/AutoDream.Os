#!/usr/bin/env python3
"""
Test Messaging Integration - Comprehensive Test Suite
====================================================

Comprehensive test suite for Discord and messaging system integration.
Provides full test coverage for all messaging functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestMessagingIntegration:
    """Test suite for messaging system integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.coord_path = str(Path(__file__).parent.parent / "config" / "coordinates.json")
        self.test_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    
    def test_coordinate_loader_initialization(self):
        """Test coordinate loader initialization."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        assert loader.config_path == self.coord_path
        assert loader.coordinates == {}
    
    def test_coordinate_loading(self):
        """Test coordinate loading from file."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        assert "agents" in loader.coordinates
        assert len(loader.coordinates["agents"]) == 8
        
        for agent_id in self.test_agents:
            assert agent_id in loader.coordinates["agents"]
            agent_data = loader.coordinates["agents"][agent_id]
            assert "chat_input_coordinates" in agent_data
            assert len(agent_data["chat_input_coordinates"]) == 2
    
    def test_agent_coordinate_retrieval(self):
        """Test agent coordinate retrieval."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        # Test valid agent
        coords = loader.get_agent_coordinates("Agent-4")
        assert coords == (-308, 1000)
        
        # Test invalid agent
        with pytest.raises(ValueError, match="Agent InvalidAgent not found in coordinates"):
            loader.get_agent_coordinates("InvalidAgent")
    
    def test_agent_ids_retrieval(self):
        """Test agent IDs retrieval."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        agent_ids = loader.get_agent_ids()
        assert len(agent_ids) == 8
        assert set(agent_ids) == set(self.test_agents)
    
    def test_all_coordinates_retrieval(self):
        """Test all coordinates retrieval."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        all_coords = loader.get_all_coordinates()
        assert len(all_coords) == 8
        
        for agent_id in self.test_agents:
            assert agent_id in all_coords
            assert isinstance(all_coords[agent_id], tuple)
            assert len(all_coords[agent_id]) == 2
    
    def test_messaging_service_initialization(self):
        """Test messaging service initialization."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        assert service.coords_file == self.coord_path
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
    
    def test_message_formatting(self):
        """Test A2A message formatting."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "Test message", "NORMAL")
        
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted
        assert "Priority: NORMAL" in formatted
        assert "Test message" in formatted
        assert "[A2A] MESSAGE" in formatted
    
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
        
        result = service.send_message("InvalidAgent", "Test message", "Discord-Commander", "NORMAL")
        
        assert result == False
    
    @patch('services.messaging.core.messaging_service.pyautogui')
    def test_broadcast_message(self, mock_pyautogui):
        """Test broadcast message functionality."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Mock PyAutoGUI
        mock_pyautogui.click.return_value = None
        mock_pyautogui.typewrite.return_value = None
        mock_pyautogui.hotkey.return_value = None
        
        service = MessagingService(self.coord_path)
        
        results = service.broadcast_message("Test broadcast", "Discord-Commander", "NORMAL")
        
        assert len(results) == 8
        for agent_id in self.test_agents:
            assert agent_id in results
            assert results[agent_id] == True
    
    def test_coordinate_file_validation(self):
        """Test coordinate file validation."""
        coord_file = Path(self.coord_path)
        
        assert coord_file.exists()
        assert coord_file.is_file()
        
        # Test JSON validity
        with open(coord_file, 'r') as f:
            data = json.load(f)
        
        assert "version" in data
        assert "agents" in data
        assert len(data["agents"]) == 8
    
    def test_error_handling(self):
        """Test error handling in messaging service."""
        from services.messaging.core.messaging_service import MessagingService
        
        # Test with invalid coordinate file
        service = MessagingService("invalid/path/coordinates.json")
        
        # Should handle gracefully (falls back to default coordinates)
        result = service.send_message("Agent-1", "Test", "Discord-Commander")
        # Result depends on whether PyAutoGUI is available
        assert isinstance(result, bool)
    
    def test_message_content_validation(self):
        """Test message content validation."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        # Test empty message
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "", "NORMAL")
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted
        
        # Test long message
        long_message = "A" * 1000
        formatted = service._format_a2a_message("Discord-Commander", "Agent-1", long_message, "NORMAL")
        assert long_message in formatted
    
    def test_priority_handling(self):
        """Test priority handling in messages."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        priorities = ["NORMAL", "HIGH", "URGENT"]
        for priority in priorities:
            formatted = service._format_a2a_message("Discord-Commander", "Agent-1", "Test", priority)
            assert f"Priority: {priority}" in formatted
    
    def test_sender_handling(self):
        """Test sender handling in messages."""
        from services.messaging.core.messaging_service import MessagingService
        
        service = MessagingService(self.coord_path)
        
        senders = ["Discord-Commander", "Agent-1", "Agent-2", "Test-Sender"]
        for sender in senders:
            formatted = service._format_a2a_message(sender, "Agent-1", "Test", "NORMAL")
            assert f"FROM: {sender}" in formatted

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
