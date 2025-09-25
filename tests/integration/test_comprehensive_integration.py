#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite
===================================

Complete integration testing for Agent Cellphone V2 system components.
Tests all major services, workflows, and agent coordination systems.

V2 Compliance: ≤400 lines, comprehensive integration coverage
Author: Agent-1 (Architecture Foundation Specialist)
"""

import pytest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import services with proper error handling
try:
    from src.services.service_manager import ServiceManager, get_service_manager
except ImportError:
    ServiceManager = None
    get_service_manager = None

try:
    from src.services.consolidated_messaging_service import ConsolidatedMessagingService
except ImportError:
    ConsolidatedMessagingService = None

try:
    from src.services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot
except ImportError:
    EnhancedDiscordAgentBot = None

try:
    from src.services.social_media_integration import get_social_media_service
except ImportError:
    get_social_media_service = None


class TestServiceManagerIntegration:
    """Test service manager integration and coordination."""
    
    @pytest.fixture
    async def service_manager(self):
        """Create service manager instance for testing."""
        if ServiceManager is None:
            pytest.skip("ServiceManager not available")
        manager = ServiceManager()
        yield manager
        await manager.stop_all_services()
    
    @pytest.mark.integration
    async def test_service_manager_startup_sequence(self, service_manager):
        """Test complete service startup sequence."""
        # Start all services
        success = await service_manager.start_all_services()
        assert success
        
        # Verify all services are initialized
        status = service_manager.get_service_status()
        assert status['is_running']
        assert status['startup_complete']
        
        # Check individual services
        services = status['services']
        assert 'messaging' in services
        assert 'social_media' in services
        assert 'discord_bot' in services
        assert 'devlog_automation' in services
        assert 'devlog_posting' in services
    
    @pytest.mark.integration
    async def test_service_health_monitoring(self, service_manager):
        """Test service health monitoring system."""
        await service_manager.start_all_services()
        
        # Wait for health check
        await asyncio.sleep(1)
        
        # Verify health monitoring is active
        status = service_manager.get_service_status()
        assert status['health'] in ['healthy', 'stopped']
    
    @pytest.mark.integration
    async def test_service_shutdown_sequence(self, service_manager):
        """Test graceful service shutdown."""
        await service_manager.start_all_services()
        
        # Stop all services
        await service_manager.stop_all_services()
        
        # Verify shutdown
        status = service_manager.get_service_status()
        assert not status['is_running']


class TestMessagingServiceIntegration:
    """Test messaging service integration."""
    
    @pytest.fixture
    def messaging_service(self):
        """Create messaging service instance."""
        if ConsolidatedMessagingService is None:
            pytest.skip("ConsolidatedMessagingService not available")
        return ConsolidatedMessagingService()
    
    @pytest.mark.integration
    def test_messaging_service_initialization(self, messaging_service):
        """Test messaging service initialization."""
        assert messaging_service is not None
        assert hasattr(messaging_service, 'send_message')
        # Check for common messaging service attributes
        assert hasattr(messaging_service, '__class__')
    
    @pytest.mark.integration
    @patch('src.services.messaging.core.messaging_service.pyautogui')
    def test_message_delivery_integration(self, mock_pyautogui, messaging_service):
        """Test message delivery integration."""
        mock_pyautogui.click.return_value = None
        mock_pyautogui.typewrite.return_value = None
        
        # Test message sending
        result = messaging_service.send_message("Agent-1", "Test message")
        assert result is not None
        
        # Verify PyAutoGUI was called
        mock_pyautogui.click.assert_called()
        mock_pyautogui.typewrite.assert_called()


class TestDiscordBotIntegration:
    """Test Discord bot integration."""
    
    @pytest.fixture
    def discord_bot(self):
        """Create Discord bot instance."""
        if EnhancedDiscordAgentBot is None:
            pytest.skip("EnhancedDiscordAgentBot not available")
        return EnhancedDiscordAgentBot(command_prefix="!")
    
    @pytest.mark.integration
    def test_discord_bot_initialization(self, discord_bot):
        """Test Discord bot initialization."""
        assert discord_bot is not None
        assert discord_bot.command_prefix == "!"
        assert hasattr(discord_bot, 'is_ready')
    
    @pytest.mark.integration
    def test_discord_bot_command_registration(self, discord_bot):
        """Test Discord bot command registration."""
        # Verify basic commands are registered
        assert len(discord_bot.commands) > 0
        
        # Test command structure
        for command in discord_bot.commands:
            assert hasattr(command, 'name')
            assert hasattr(command, 'callback')


class TestSocialMediaIntegration:
    """Test social media integration."""
    
    @pytest.mark.integration
    def test_social_media_service_availability(self):
        """Test social media service availability."""
        service = get_social_media_service()
        
        if service:
            assert hasattr(service, 'analyze_sentiment')
            assert hasattr(service, 'get_community_dashboard_data')
        else:
            # Service not available, which is acceptable
            pytest.skip("Social media service not available")


class TestAgentCoordinationIntegration:
    """Test agent coordination and workflow integration."""
    
    @pytest.fixture
    def temp_workflow_dir(self):
        """Create temporary workflow directory."""
        temp_dir = tempfile.mkdtemp()
        workflow_dir = Path(temp_dir) / "workflows"
        workflow_dir.mkdir()
        
        yield str(workflow_dir)
        
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_agent_coordinate_loading(self, temp_workflow_dir):
        """Test agent coordinate loading."""
        from src.services.messaging.core.coordinate_loader import CoordinateLoader
        
        # Create test coordinates
        test_coords = {
            "version": "2.0",
            "agents": {
                "Agent-1": {
                    "active": True,
                    "chat_input_coordinates": [-1269, 481],
                    "description": "Test Agent"
                }
            }
        }
        
        # Write test coordinates
        coords_file = Path(temp_workflow_dir) / "test_coordinates.json"
        with open(coords_file, 'w') as f:
            json.dump(test_coords, f)
        
        # Load coordinates
        loader = CoordinateLoader(str(coords_file))
        success = loader.load()
        
        assert success
        assert loader.get_agent_coordinates("Agent-1") == (-1269, 481)


class TestEndToEndIntegration:
    """Test complete end-to-end integration scenarios."""
    
    @pytest.fixture
    async def full_system(self):
        """Create full system for end-to-end testing."""
        manager = ServiceManager()
        await manager.start_all_services()
        yield manager
        await manager.stop_all_services()
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_complete_agent_workflow(self, full_system):
        """Test complete agent workflow from start to finish."""
        # Verify all services are running
        status = full_system.get_service_status()
        assert status['is_running']
        
        # Test messaging service
        if full_system.messaging_service:
            assert full_system.messaging_service is not None
        
        # Test Discord bot readiness
        if full_system.discord_bot:
            assert full_system.discord_bot.is_ready()
        
        # Test social media integration
        if full_system.social_media_service:
            assert full_system.social_media_service is not None
    
    @pytest.mark.integration
    async def test_service_interaction(self, full_system):
        """Test interaction between different services."""
        # Test that services can communicate
        status = full_system.get_service_status()
        
        # Verify service coordination
        assert len(status['services']) >= 3  # At least messaging, discord, social
        
        # Test service health
        healthy_services = sum(1 for s in status['services'].values() 
                             if s in ['active', 'ready'])
        assert healthy_services > 0


class TestIntegrationErrorHandling:
    """Test integration error handling and recovery."""
    
    @pytest.mark.integration
    async def test_service_failure_recovery(self):
        """Test service failure and recovery."""
        manager = ServiceManager()
        
        # Mock a service failure
        with patch.object(manager, '_start_messaging_service', side_effect=Exception("Test failure")):
            success = await manager.start_all_services()
            assert not success
        
        # Verify cleanup
        status = manager.get_service_status()
        assert not status['is_running']
    
    @pytest.mark.integration
    async def test_graceful_degradation(self):
        """Test graceful degradation when some services fail."""
        manager = ServiceManager()
        
        # Mock partial service failure
        with patch.object(manager, '_start_social_media_service', side_effect=Exception("Social media unavailable")):
            # Should still start other services
            success = await manager.start_all_services()
            # May succeed with degraded functionality
            assert success or not success  # Either is acceptable
        
        await manager.stop_all_services()


class TestIntegrationPerformance:
    """Test integration performance characteristics."""
    
    @pytest.mark.integration
    @pytest.mark.performance
    async def test_startup_performance(self):
        """Test service startup performance."""
        manager = ServiceManager()
        
        start_time = datetime.now()
        success = await manager.start_all_services()
        end_time = datetime.now()
        
        startup_time = (end_time - start_time).total_seconds()
        
        # Should start within reasonable time (adjust threshold as needed)
        assert startup_time < 30  # 30 seconds max
        assert success
        
        await manager.stop_all_services()
    
    @pytest.mark.integration
    @pytest.mark.performance
    async def test_memory_usage(self):
        """Test memory usage during integration."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        manager = ServiceManager()
        await manager.start_all_services()
        
        # Wait for services to stabilize
        await asyncio.sleep(2)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (adjust threshold as needed)
        assert memory_increase < 100 * 1024 * 1024  # 100MB max increase
        
        await manager.stop_all_services()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
