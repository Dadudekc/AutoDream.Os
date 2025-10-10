#!/usr/bin/env python3
"""
Messaging System Unit Tests
===========================

Unit tests for messaging system components.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.services.messaging.core.messaging_service import MessagingService
from src.services.messaging.status.status_monitor import StatusMonitor
from src.services.messaging.onboarding.onboarding_service import OnboardingService
from src.services.consolidated_messaging_service import ConsolidatedMessagingService


class TestMessagingService:
    """Test cases for MessagingService."""
    
    def test_initialization(self, mock_coordinates_file):
        """Test messaging service initialization."""
        service = MessagingService(mock_coordinates_file)
        assert service.coords_file == mock_coordinates_file
        assert service.loader is not None
        assert service.validation_report is not None
    
    def test_send_message_success(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test successful message sending."""
        service = MessagingService(mock_coordinates_file)
        
        with patch.object(service, '_is_agent_active', return_value=True):
            result = service.send_message("Agent-1", "Test message", "Agent-2")
            
            assert result is True
            mock_pyautogui['click'].assert_called_once()
            mock_pyperclip['copy'].assert_called_once()
    
    def test_send_message_inactive_agent(self, mock_coordinates_file):
        """Test message sending to inactive agent."""
        service = MessagingService(mock_coordinates_file)
        
        with patch.object(service, '_is_agent_active', return_value=False):
            result = service.send_message("Agent-3", "Test message", "Agent-2")
            
            assert result is False
    
    def test_send_message_agent_not_found(self, mock_coordinates_file):
        """Test message sending to non-existent agent."""
        service = MessagingService(mock_coordinates_file)
        
        with patch.object(service, '_is_agent_active', return_value=True):
            result = service.send_message("Agent-999", "Test message", "Agent-2")
            
            assert result is False
    
    def test_broadcast_message(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test broadcast message functionality."""
        service = MessagingService(mock_coordinates_file)
        
        with patch.object(service, 'send_message', return_value=True):
            results = service.broadcast_message("Test broadcast", "Agent-2")
            
            assert isinstance(results, dict)
            assert len(results) > 0
            assert all(result is True for result in results.values())
    
    def test_format_a2a_message(self, mock_coordinates_file):
        """Test A2A message formatting."""
        service = MessagingService(mock_coordinates_file)
        
        message = service._format_a2a_message("Agent-1", "Agent-2", "Test message", "HIGH")
        
        assert "FROM: Agent-1" in message
        assert "TO: Agent-2" in message
        assert "Test message" in message
        assert "Priority: HIGH" in message
        assert "DISCORD DEVLOG REMINDER" in message
    
    def test_is_agent_active(self, mock_coordinates_file):
        """Test agent active status checking."""
        service = MessagingService(mock_coordinates_file)
        
        # Test active agent
        assert service._is_agent_active("Agent-1") is True
        
        # Test inactive agent
        assert service._is_agent_active("Agent-3") is False
        
        # Test non-existent agent (should default to True)
        assert service._is_agent_active("Agent-999") is True


class TestStatusMonitor:
    """Test cases for StatusMonitor."""
    
    def test_initialization(self, mock_coordinates_file):
        """Test status monitor initialization."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        assert monitor.messaging_service == messaging_service
    
    def test_get_comprehensive_status(self, mock_coordinates_file, mock_project_analysis, mock_fsm_status, mock_agent_workspace):
        """Test comprehensive status retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        # Mock the project analysis file path
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_project_analysis.open('r')):
            
            status = monitor.get_comprehensive_status()
            
            assert isinstance(status, dict)
            assert 'status' in status
            assert 'agent_count' in status
            assert 'agents' in status
            assert 'project_scanner' in status
            assert 'fsm_status' in status
            assert 'agent_tasks' in status
            assert 'system_health' in status
    
    def test_get_project_scanner_status(self, mock_coordinates_file, mock_project_analysis):
        """Test project scanner status retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_project_analysis.open('r')):
            
            status = monitor._get_project_scanner_status()
            
            assert isinstance(status, dict)
            assert 'project_analysis_exists' in status
            assert 'chatgpt_context_exists' in status
            assert 'last_scan' in status
    
    def test_get_fsm_status(self, mock_coordinates_file, mock_fsm_status):
        """Test FSM status retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.glob', return_value=[mock_fsm_status / "Agent-1.json"]):
            
            status = monitor._get_fsm_status()
            
            assert isinstance(status, dict)
            assert 'status' in status
            assert 'agents' in status
            assert 'total_agents' in status
    
    def test_get_agent_task_statuses(self, mock_coordinates_file, mock_agent_workspace):
        """Test agent task status retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.iterdir', return_value=[mock_agent_workspace]):
            
            status = monitor._get_agent_task_statuses()
            
            assert isinstance(status, dict)
            assert 'status' in status
            assert 'agents' in status
            assert 'total_agents' in status
    
    def test_get_system_health(self, mock_coordinates_file):
        """Test system health retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        monitor = StatusMonitor(messaging_service)
        
        status = monitor._get_system_health()
        
        assert isinstance(status, dict)
        assert 'coordinates_valid' in status
        assert 'pyautogui_available' in status
        assert 'agent_count' in status
        assert 'overall_status' in status


class TestOnboardingService:
    """Test cases for OnboardingService."""
    
    def test_initialization(self, mock_coordinates_file):
        """Test onboarding service initialization."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        assert service.messaging_service == messaging_service
    
    def test_get_onboarding_coordinates(self, mock_coordinates_file):
        """Test onboarding coordinates retrieval."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        coords = service.get_onboarding_coordinates()
        
        assert isinstance(coords, dict)
        # Should have agent coordinates or be empty
        assert len(coords) >= 0
    
    def test_verify_coordinates(self, mock_coordinates_file):
        """Test coordinate verification."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        # Test valid coordinates
        assert service.verify_coordinates((100, 200)) is True
        assert service.verify_coordinates((0, 0)) is True
        
        # Test invalid coordinates
        assert service.verify_coordinates((100,)) is False
        assert service.verify_coordinates(()) is False
        assert service.verify_coordinates(("100", "200")) is False
    
    def test_click_coordinates(self, mock_coordinates_file, mock_pyautogui):
        """Test coordinate clicking."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        result = service.click_coordinates((100, 200))
        
        assert result is True
        mock_pyautogui['click'].assert_called_once_with(100, 200)
        mock_pyautogui['sleep'].assert_called_once()
    
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        # Test enter key
# SECURITY: Key placeholder - replace with environment variable
        assert result is True
        mock_pyautogui['press'].assert_called_with('enter')
        
        # Test ctrl+enter
# SECURITY: Key placeholder - replace with environment variable
        assert result is True
# SECURITY: Key placeholder - replace with environment variable
        
        # Test ctrl+n
# SECURITY: Key placeholder - replace with environment variable
        assert result is True
# SECURITY: Key placeholder - replace with environment variable
    
    def test_paste_message(self, mock_coordinates_file, mock_pyperclip, mock_pyautogui):
        """Test message pasting."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        result = service.paste_message("Test message")
        
        assert result is True
        mock_pyperclip['copy'].assert_called_once_with("Test message")
# SECURITY: Key placeholder - replace with environment variable
    
    def test_get_base_onboarding_message(self, mock_coordinates_file):
        """Test base onboarding message generation."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        message = service.get_base_onboarding_message("Agent-1")
        
        assert "Agent-1" in message
        assert "V2_SWARM" in message
        assert "ONBOARDING" in message
        assert "Quick Start Guide" in message
        assert "DISCORD DEVLOG REMINDER" in message
    
    def test_hard_onboard_agent(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test hard onboarding of specific agent."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True):
            result = service.hard_onboard_agent("Agent-1")
            
            assert result is True
    
    def test_hard_onboard_inactive_agent(self, mock_coordinates_file):
        """Test hard onboarding of inactive agent."""
        messaging_service = MessagingService(mock_coordinates_file)
        service = OnboardingService(messaging_service)
        
        with patch.object(service.messaging_service, '_is_agent_active', return_value=False):
            result = service.hard_onboard_agent("Agent-3")
            
            assert result is False


class TestConsolidatedMessagingService:
    """Test cases for ConsolidatedMessagingService."""
    
    def test_initialization(self, mock_coordinates_file):
        """Test consolidated messaging service initialization."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        assert service.coord_path == mock_coordinates_file
        assert service.messaging_service is not None
        assert service.status_monitor is not None
        assert service.onboarding_service is not None
    
    def test_send_message_delegation(self, mock_coordinates_file):
        """Test message sending delegation."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        with patch.object(service.messaging_service, 'send_message', return_value=True) as mock_send:
            result = service.send_message("Agent-1", "Test message", "Agent-2")
            
            assert result is True
            mock_send.assert_called_once_with("Agent-1", "Test message", "Agent-2", "NORMAL")
    
    def test_broadcast_message_delegation(self, mock_coordinates_file):
        """Test broadcast message delegation."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        with patch.object(service.messaging_service, 'broadcast_message', return_value={"Agent-1": True}) as mock_broadcast:
            result = service.broadcast_message("Test broadcast", "Agent-2")
            
            assert result == {"Agent-1": True}
            mock_broadcast.assert_called_once_with("Test broadcast", "Agent-2", "NORMAL")
    
    def test_get_status_delegation(self, mock_coordinates_file):
        """Test status retrieval delegation."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        mock_status = {"status": "operational", "agent_count": 3}
        with patch.object(service.status_monitor, 'get_comprehensive_status', return_value=mock_status) as mock_get_status:
            result = service.get_status()
            
            assert result == mock_status
            mock_get_status.assert_called_once()
    
    def test_hard_onboard_agent_delegation(self, mock_coordinates_file):
        """Test hard onboarding delegation."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        with patch.object(service.onboarding_service, 'hard_onboard_agent', return_value=True) as mock_onboard:
            result = service.hard_onboard_agent("Agent-1")
            
            assert result is True
            mock_onboard.assert_called_once_with("Agent-1")
    
    def test_hard_onboard_all_agents_delegation(self, mock_coordinates_file):
        """Test hard onboarding all agents delegation."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        mock_results = {"Agent-1": True, "Agent-2": True}
        with patch.object(service.onboarding_service, 'hard_onboard_all_agents', return_value=mock_results) as mock_onboard_all:
            result = service.hard_onboard_all_agents()
            
            assert result == mock_results
            mock_onboard_all.assert_called_once()


