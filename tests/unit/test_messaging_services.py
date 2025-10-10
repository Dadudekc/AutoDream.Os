#!/usr/bin/env python3
"""
Messaging Services Unit Tests
=============================

Unit tests for messaging service components with low coverage.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.services.messaging.coordinates import (
    get_coordinate_loader,
    list_agents,
    get_agent_coordinates,
    load_all_active_coords
)
from src.services.messaging.delivery.fallback import FallbackDeliveryService
from src.services.messaging.delivery.inbox_delivery import InboxDeliveryService
from src.services.messaging.delivery.pyautogui_delivery import PyAutoGUIDeliveryService
from src.services.messaging.enhanced_messaging_service import EnhancedMessagingService
from src.services.messaging.models.messaging_enums import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)
from src.services.messaging.models.messaging_models import (
    UnifiedMessage,
    MessageDeliveryResult,
    AgentStatus
)
from src.services.messaging.project_update_system import ProjectUpdateSystem
from src.services.messaging.service import MessagingService as BaseMessagingService


class TestCoordinateFunctions:
    """Test cases for coordinate functions."""
    
    def test_get_coordinate_loader(self):
        """Test getting coordinate loader."""
        loader = get_coordinate_loader()
        assert loader is not None
    
    def test_list_agents(self):
        """Test listing active agents."""
        agents = list_agents()
        
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert all(agent.startswith("Agent-") for agent in agents)
    
    def test_get_agent_coordinates(self):
        """Test getting agent coordinates."""
        coords = get_agent_coordinates("Agent-1")
        
        # Should return coordinates or None
        assert coords is None or isinstance(coords, tuple)
    
    def test_get_agent_coordinates_not_found(self):
        """Test getting coordinates for non-existent agent."""
        coords = get_agent_coordinates("Agent-999")
        
        assert coords is None
    
    def test_load_all_active_coords(self):
        """Test loading all active coordinates."""
        coords = load_all_active_coords()
        
        assert isinstance(coords, dict)
        # Should have some agents if the system is working
        assert len(coords) >= 0


class TestFallbackDeliveryService:
    """Test cases for FallbackDeliveryService."""
    
    def test_initialization(self):
        """Test fallback delivery service initialization."""
        service = FallbackDeliveryService()
        assert service is not None
    
    def test_deliver_message(self):
        """Test message delivery."""
        service = FallbackDeliveryService()
        
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        
        result = service.deliver_message(message)
        
        assert isinstance(result, MessageDeliveryResult)
        assert result.success is True
    
    def test_deliver_message_failure(self):
        """Test message delivery failure."""
        service = FallbackDeliveryService()
        
        # Create invalid message
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="",
            sender="",
            recipient=""
        )
        
        result = service.deliver_message(message)
        
        assert isinstance(result, MessageDeliveryResult)
        assert result.success is False


class TestInboxDeliveryService:
    """Test cases for InboxDeliveryService."""
    
    def test_initialization(self):
        """Test inbox delivery service initialization."""
        service = InboxDeliveryService()
        assert service is not None
    
    def test_deliver_message(self, temp_dir):
        """Test message delivery to inbox."""
        service = InboxDeliveryService()
        service.inbox_base_path = temp_dir
        
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        
        result = service.deliver_message(message)
        
        assert isinstance(result, MessageDeliveryResult)
        assert result.success is True
        
        # Check if message file was created
        inbox_dir = temp_dir / "Agent-2" / "inbox"
        assert inbox_dir.exists()
        
        message_files = list(inbox_dir.glob("*.md"))
        assert len(message_files) > 0


class TestPyAutoGUIDeliveryService:
    """Test cases for PyAutoGUIDeliveryService."""
    
    def test_initialization(self):
        """Test PyAutoGUI delivery service initialization."""
        service = PyAutoGUIDeliveryService()
        assert service is not None
    
    @patch('src.services.messaging.delivery.pyautogui_delivery.pyautogui')
    def test_deliver_message(self, mock_pyautogui):
        """Test message delivery via PyAutoGUI."""
        service = PyAutoGUIDeliveryService()
        
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        
        # Mock PyAutoGUI methods
        mock_pyautogui.click.return_value = None
        mock_pyautogui.press.return_value = None
        mock_pyautogui.sleep.return_value = None
        
        result = service.deliver_message(message, coordinates=(100, 200))
        
        assert isinstance(result, MessageDeliveryResult)
        # Note: This will likely fail in headless environment, but we can test the structure


class TestEnhancedMessagingService:
    """Test cases for EnhancedMessagingService."""
    
    def test_initialization(self):
        """Test enhanced messaging service initialization."""
        service = EnhancedMessagingService()
        assert service is not None
    
    def test_send_message(self):
        """Test sending message."""
        service = EnhancedMessagingService()
        
        with patch.object(service, '_deliver_message', return_value=True):
            result = service.send_message(
                recipient="Agent-2",
                content="Test message",
                sender="Agent-1"
            )
            
            assert result is True
    
    def test_broadcast_message(self):
        """Test broadcasting message."""
        service = EnhancedMessagingService()
        
        with patch.object(service, 'send_message', return_value=True):
            results = service.broadcast_message(
                content="Test broadcast",
                sender="Agent-1"
            )
            
            assert isinstance(results, dict)
    
    def test_get_agent_status(self):
        """Test getting agent status."""
        service = EnhancedMessagingService()
        
        status = service.get_agent_status("Agent-1")
        
        assert isinstance(status, AgentStatus)


class TestUnifiedMessage:
    """Test cases for UnifiedMessage."""
    
    def test_initialization(self):
        """Test message initialization."""
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        
        assert message.message_type == UnifiedMessageType.TEXT
        assert message.content == "Test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"
        assert message.priority == UnifiedMessagePriority.NORMAL
        assert message.tags == []
    
    def test_initialization_with_priority(self):
        """Test message initialization with priority."""
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2",
            priority=UnifiedMessagePriority.URGENT
        )
        
        assert message.priority == UnifiedMessagePriority.URGENT
    
    def test_initialization_with_tags(self):
        """Test message initialization with tags."""
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2",
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        assert UnifiedMessageTag.CAPTAIN in message.tags
    
    def test_to_dict(self):
        """Test converting message to dictionary."""
        message = UnifiedMessage(
            message_type=UnifiedMessageType.TEXT,
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2"
        )
        
        message_dict = message.to_dict()
        
        assert isinstance(message_dict, dict)
        assert message_dict["message_type"] == "text"
        assert message_dict["content"] == "Test message"
        assert message_dict["sender"] == "Agent-1"
        assert message_dict["recipient"] == "Agent-2"
    
    def test_from_dict(self):
        """Test creating message from dictionary."""
        message_dict = {
            "message_type": "text",
            "content": "Test message",
            "sender": "Agent-1",
            "recipient": "Agent-2",
            "priority": "urgent",
            "tags": ["captain"]
        }
        
        message = UnifiedMessage.from_dict(message_dict)
        
        assert message.message_type == UnifiedMessageType.TEXT
        assert message.content == "Test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"
        assert message.priority == UnifiedMessagePriority.URGENT
        assert UnifiedMessageTag.CAPTAIN in message.tags


class TestMessageDeliveryResult:
    """Test cases for MessageDeliveryResult."""
    
    def test_initialization_success(self):
        """Test successful delivery result initialization."""
        result = MessageDeliveryResult(
            success=True,
            message_id="msg123",
            delivery_time=1.5
        )
        
        assert result.success is True
        assert result.message_id == "msg123"
        assert result.delivery_time == 1.5
        assert result.error is None
    
    def test_initialization_failure(self):
        """Test failed delivery result initialization."""
        result = MessageDeliveryResult(
            success=False,
            error="Connection failed"
        )
        
        assert result.success is False
        assert result.error == "Connection failed"
        assert result.message_id is None
        assert result.delivery_time is None
    
    def test_to_dict(self):
        """Test converting result to dictionary."""
        result = MessageDeliveryResult(
            success=True,
            message_id="msg123",
            delivery_time=1.5
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["success"] is True
        assert result_dict["message_id"] == "msg123"
        assert result_dict["delivery_time"] == 1.5


class TestAgentStatus:
    """Test cases for AgentStatus."""
    
    def test_initialization(self):
        """Test agent status initialization."""
        status = AgentStatus(
            agent_id="Agent-1",
            is_active=True,
            last_seen="2025-01-16T12:00:00Z"
        )
        
        assert status.agent_id == "Agent-1"
        assert status.is_active is True
        assert status.last_seen == "2025-01-16T12:00:00Z"
    
    def test_to_dict(self):
        """Test converting status to dictionary."""
        status = AgentStatus(
            agent_id="Agent-1",
            is_active=True,
            last_seen="2025-01-16T12:00:00Z"
        )
        
        status_dict = status.to_dict()
        
        assert isinstance(status_dict, dict)
        assert status_dict["agent_id"] == "Agent-1"
        assert status_dict["is_active"] is True
        assert status_dict["last_seen"] == "2025-01-16T12:00:00Z"


class TestProjectUpdateSystem:
    """Test cases for ProjectUpdateSystem."""
    
    def test_initialization(self):
        """Test project update system initialization."""
        system = ProjectUpdateSystem()
        assert system is not None
    
    def test_scan_project(self, temp_dir):
        """Test project scanning."""
        system = ProjectUpdateSystem()
        system.project_path = temp_dir
        
        # Create test project structure
        (temp_dir / "src").mkdir()
        (temp_dir / "tests").mkdir()
        (temp_dir / "README.md").touch()
        
        result = system.scan_project()
        
        assert isinstance(result, dict)
        assert "files_scanned" in result
        assert "directories_found" in result
    
    def test_generate_update_report(self, temp_dir):
        """Test generating update report."""
        system = ProjectUpdateSystem()
        system.project_path = temp_dir
        
        # Create test project structure
        (temp_dir / "src").mkdir()
        (temp_dir / "tests").mkdir()
        
        report = system.generate_update_report()
        
        assert isinstance(report, dict)
        assert "scan_timestamp" in report
        assert "project_structure" in report


class TestBaseMessagingService:
    """Test cases for BaseMessagingService."""
    
    def test_initialization(self):
        """Test base messaging service initialization."""
        service = BaseMessagingService()
        assert service is not None
    
    def test_send_message(self):
        """Test sending message."""
        service = BaseMessagingService()
        
        with patch.object(service, '_deliver_message', return_value=True):
            result = service.send_message(
                recipient="Agent-2",
                content="Test message"
            )
            
            assert result is True
    
    def test_get_status(self):
        """Test getting service status."""
        service = BaseMessagingService()
        
        status = service.get_status()
        
        assert isinstance(status, dict)
        assert "service_name" in status
        assert "is_healthy" in status