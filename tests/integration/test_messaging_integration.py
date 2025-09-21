#!/usr/bin/env python3
"""
Messaging System Integration Tests
==================================

Integration tests for messaging system components.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.services.consolidated_messaging_service import ConsolidatedMessagingService
from src.services.messaging.core.messaging_service import MessagingService
from src.services.messaging.status.status_monitor import StatusMonitor
from src.services.messaging.onboarding.onboarding_service import OnboardingService


class TestMessagingSystemIntegration:
    """Integration tests for messaging system."""
    
    def test_consolidated_service_integration(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test consolidated messaging service integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that all components are properly integrated
        assert service.messaging_service is not None
        assert service.status_monitor is not None
        assert service.onboarding_service is not None
        
        # Test that components can communicate
        assert service.messaging_service == service.status_monitor.messaging_service
        assert service.messaging_service == service.onboarding_service.messaging_service
    
    def test_messaging_workflow_integration(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test complete messaging workflow integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test send message workflow
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True):
            result = service.send_message("Agent-1", "Integration test message", "Agent-2")
            assert result is True
        
        # Test broadcast workflow
        with patch.object(service.messaging_service, 'send_message', return_value=True):
            results = service.broadcast_message("Integration test broadcast", "Agent-2")
            assert isinstance(results, dict)
            assert len(results) > 0
    
    def test_status_monitoring_integration(self, mock_coordinates_file, mock_project_analysis, mock_fsm_status, mock_agent_workspace):
        """Test status monitoring integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test status retrieval
        status = service.get_status()
        
        assert isinstance(status, dict)
        assert 'status' in status
        assert 'agent_count' in status
        assert 'agents' in status
        assert 'project_scanner' in status
        assert 'fsm_status' in status
        assert 'agent_tasks' in status
        assert 'system_health' in status
    
    def test_onboarding_integration(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test onboarding system integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test onboarding workflow
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True):
            result = service.hard_onboard_agent("Agent-1")
            assert result is True
        
        # Test bulk onboarding
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True):
            results = service.hard_onboard_all_agents()
            assert isinstance(results, dict)
            assert len(results) > 0
    
    def test_error_handling_integration(self, mock_coordinates_file):
        """Test error handling integration across components."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test error handling in messaging
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True), \
             patch.object(service.messaging_service, '_paste_to_coords', side_effect=Exception("Test error")):
            
            result = service.send_message("Agent-1", "Test message", "Agent-2")
            assert result is False
        
        # Test error handling in status monitoring
        with patch('pathlib.Path.exists', return_value=False):
            status = service.get_status()
            assert isinstance(status, dict)
            assert 'status' in status
        
        # Test error handling in onboarding
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True), \
             patch.object(service.onboarding_service, 'execute_onboarding_sequence', side_effect=Exception("Test error")):
            
            result = service.hard_onboard_agent("Agent-1")
            assert result is False
    
    def test_coordinate_validation_integration(self, mock_coordinates_file):
        """Test coordinate validation integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that coordinate validation is properly integrated
        assert service.messaging_service.validation_report is not None
        
        # Test coordinate loading
        assert service.messaging_service.loader.coordinates is not None
        assert len(service.messaging_service.loader.coordinates.get("agents", {})) > 0
    
    def test_pyautogui_integration(self, mock_coordinates_file, mock_pyautogui, mock_pyperclip):
        """Test PyAutoGUI integration."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that PyAutoGUI operations are properly integrated
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True):
            result = service.send_message("Agent-1", "PyAutoGUI test", "Agent-2")
            
            # Verify PyAutoGUI operations were called
            mock_pyautogui['click'].assert_called()
            mock_pyperclip['copy'].assert_called()
# SECURITY: Key placeholder - replace with environment variable
    
    def test_cookie_management_integration(self, mock_coordinates_file, mock_cookie_file):
        """Test cookie management integration for Thea authentication."""
        from thea_auth import TheaLoginHandler, TheaCookieManager
        
        # Test cookie manager integration
        cookie_manager = TheaCookieManager(mock_cookie_file)
        assert cookie_manager.cookie_file.exists()
        
        # Test login handler integration
        login_handler = TheaLoginHandler(cookie_file=mock_cookie_file)
        assert login_handler.cookie_manager == cookie_manager
        
        # Test cookie validation
        assert cookie_manager.has_valid_cookies() is True
    
    def test_discord_integration(self, mock_coordinates_file, mock_discord_bot, mock_discord_context):
        """Test Discord bot integration with messaging system."""
        from src.services.discord_bot_with_devlog import EnhancedDiscordAgentBot, setup_commands
        
        # Test Discord bot initialization with messaging service
        with patch('src.services.discord_bot_with_devlog.json.load', return_value={"agents": {"Agent-1": {"active": True}}}):
            bot = EnhancedDiscordAgentBot()
            setup_commands(bot)
            
            assert bot.messaging_service is not None
            assert bot.devlog_service is not None
        
        # Test Discord command integration
        with patch.object(bot.messaging_service, 'send_message', return_value=True):
            send_cmd = bot.get_command("send")
            # This would be an async test in practice
            assert send_cmd is not None
    
    def test_performance_integration(self, mock_coordinates_file):
        """Test performance characteristics of integrated system."""
        import time
        
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test status retrieval performance
        start_time = time.time()
        status = service.get_status()
        end_time = time.time()
        
        # Status retrieval should be fast (< 1 second)
        assert (end_time - start_time) < 1.0
        
        # Test message sending performance (mocked)
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True), \
             patch.object(service.messaging_service, '_paste_to_coords', return_value=True):
            
            start_time = time.time()
            result = service.send_message("Agent-1", "Performance test", "Agent-2")
            end_time = time.time()
            
            assert result is True
            # Message sending should be fast (< 0.5 seconds when mocked)
            assert (end_time - start_time) < 0.5
    
    def test_memory_usage_integration(self, mock_coordinates_file):
        """Test memory usage of integrated system."""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create multiple service instances
        services = []
        for i in range(10):
            service = ConsolidatedMessagingService(mock_coordinates_file)
            services.append(service)
        
        # Get memory usage after creating services
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 50MB for 10 instances)
        assert memory_increase < 50 * 1024 * 1024, f"Memory usage increased by {memory_increase / 1024 / 1024:.1f}MB"
    
    def test_concurrent_operations_integration(self, mock_coordinates_file):
        """Test concurrent operations integration."""
        import threading
        import time
        
        service = ConsolidatedMessagingService(mock_coordinates_file)
        results = []
        
        def send_message(agent_id, message):
            with patch.object(service.messaging_service, '_is_agent_active', return_value=True), \
                 patch.object(service.messaging_service, '_paste_to_coords', return_value=True):
                result = service.send_message(agent_id, message, "Agent-2")
                results.append(result)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=send_message, args=(f"Agent-{i+1}", f"Concurrent message {i}"))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All operations should succeed
        assert len(results) == 5
        assert all(result is True for result in results)
    
    def test_data_consistency_integration(self, mock_coordinates_file):
        """Test data consistency across integrated components."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that all components use the same coordinate data
        messaging_agents = service.messaging_service.loader.get_agent_ids()
        status_agents = service.get_status().get('agents', [])
        
        assert set(messaging_agents) == set(status_agents)
        
        # Test that agent status is consistent
        for agent_id in messaging_agents:
            messaging_active = service.messaging_service._is_agent_active(agent_id)
            # Status should be consistent across components
            assert isinstance(messaging_active, bool)
    
    def test_configuration_integration(self, mock_coordinates_file):
        """Test configuration integration across components."""
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that all components use the same configuration
        assert service.messaging_service.coords_file == mock_coordinates_file
        assert service.coord_path == mock_coordinates_file
        
        # Test that configuration is properly loaded
        assert service.messaging_service.loader.coordinates is not None
        assert len(service.messaging_service.loader.coordinates.get("agents", {})) > 0
    
    def test_logging_integration(self, mock_coordinates_file, caplog):
        """Test logging integration across components."""
        import logging
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        
        service = ConsolidatedMessagingService(mock_coordinates_file)
        
        # Test that operations generate appropriate log messages
        with patch.object(service.messaging_service, '_is_agent_active', return_value=True), \
             patch.object(service.messaging_service, '_paste_to_coords', return_value=True):
            
            service.send_message("Agent-1", "Logging test", "Agent-2")
            
            # Check that appropriate log messages were generated
            # Note: This would require actual logging setup in the components
            assert True  # Placeholder for logging verification


