#!/usr/bin/env python3
"""
Test suite for Multimedia Integration Coordinator
Comprehensive testing of agent coordination and multimedia integration
"""

import pytest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.services.multimedia_integration_coordinator import (
    MultimediaIntegrationCoordinator,
)


class TestMultimediaIntegrationCoordinator:
    """Test suite for MultimediaIntegrationCoordinator"""

    @pytest.fixture
    def coordinator(self):
        """Create a fresh MultimediaIntegrationCoordinator instance"""
        return MultimediaIntegrationCoordinator()

    @pytest.fixture
    def mock_multimedia_services(self):
        """Create mock multimedia services"""
        mock_media_processor = Mock()
        mock_media_processor.get_system_status.return_value = {"status": "healthy"}

        mock_content_manager = Mock()
        mock_content_manager.get_pipeline_status.return_value = {"status": "active"}

        mock_streaming = Mock()
        mock_streaming.get_streaming_status.return_value = {"status": "live"}

        return {
            "media_processor": mock_media_processor,
            "content_manager": mock_content_manager,
            "streaming": mock_streaming,
        }

    def test_initialization(self, coordinator):
        """Test MultimediaIntegrationCoordinator initialization"""
        assert coordinator.multimedia_services is not None
        assert coordinator.agent_connections is not None
        assert coordinator.integration_status is not None
        assert coordinator.coordination_events is not None

        # Check that all 8 agents are initialized
        assert len(coordinator.agent_connections) == 8
        assert "agent_1" in coordinator.agent_connections
        assert "agent_2" in coordinator.agent_connections
        assert "agent_3" in coordinator.agent_connections
        assert "agent_4" in coordinator.agent_connections
        assert "agent_5" in coordinator.agent_connections
        assert "agent_6" in coordinator.agent_connections
        assert "agent_7" in coordinator.agent_connections
        assert "agent_8" in coordinator.agent_connections

    def test_agent_roles_initialization(self, coordinator):
        """Test that agent roles are properly initialized"""
        expected_roles = {
            "agent_1": "Repository Development Specialist",
            "agent_2": "Enhanced Collaborative System Specialist",
            "agent_3": "Multimedia & Content Specialist (SELF)",
            "agent_4": "Quality Assurance & Testing Specialist",
            "agent_5": "Captain & Coordination Specialist",
            "agent_6": "Performance & Optimization Specialist",
            "agent_7": "Integration & API Specialist",
            "agent_8": "Workflow & Automation Specialist",
        }

        for agent_id, expected_role in expected_roles.items():
            assert coordinator.agent_connections[agent_id]["role"] == expected_role
            assert coordinator.agent_connections[agent_id]["status"] == "active"
            assert "multimedia_needs" in coordinator.agent_connections[agent_id]

    def test_multimedia_services_initialization(self, coordinator):
        """Test that multimedia services are properly initialized"""
        assert "media_processor" in coordinator.multimedia_services
        assert "content_manager" in coordinator.multimedia_services
        assert "streaming" in coordinator.multimedia_services

        # Check that services are not None
        for service_name, service in coordinator.multimedia_services.items():
            assert service is not None
            assert hasattr(service, "__class__")

    def test_integration_status_initialization(self, coordinator):
        """Test that integration status is properly initialized"""
        assert coordinator.integration_status["overall_status"] == "active"
        assert coordinator.integration_status["multimedia_services_healthy"] == True
        assert coordinator.integration_status["agent_communications_active"] == True
        assert "last_coordination_check" in coordinator.integration_status
        assert coordinator.integration_status["total_coordination_events"] == 0

    def test_coordinate_with_agent_success(self, coordinator):
        """Test successful coordination with an agent"""
        # Test content generation request
        request = {
            "type": "content_generation",
            "content_type": "blog",
            "source_data": {"title": "Test Blog", "description": "Test Description"},
        }

        result = coordinator.coordinate_with_agent("agent_1", request)

        assert result["status"] == "success"
        assert "pipeline_name" in result
        assert "message" in result
        assert "pipeline_status" in result

        # Check that agent communication time was updated
        assert coordinator.agent_connections["agent_1"]["last_communication"] > 0

    def test_coordinate_with_agent_not_found(self, coordinator):
        """Test coordination with non-existent agent"""
        request = {"type": "content_generation"}
        result = coordinator.coordinate_with_agent("nonexistent_agent", request)

        assert "error" in result
        assert "not found" in result["error"]

    def test_content_generation_request_handling(self, coordinator):
        """Test content generation request handling"""
        request = {
            "type": "content_generation",
            "content_type": "blog",
            "source_data": {"title": "Test Content", "description": "Test Description"},
            "output_format": "markdown",
        }

        result = coordinator.coordinate_with_agent("agent_2", request)

        assert result["status"] == "success"
        assert "pipeline_name" in result
        assert result["pipeline_name"].startswith("agent_2_")

    def test_streaming_setup_request_handling(self, coordinator):
        """Test streaming setup request handling"""
        request = {
            "type": "streaming_setup",
            "stream_name": "test_stream",
            "source": "webcam",
            "platforms": ["youtube", "twitch"],
            "quality": "1080p",
            "fps": 60,
        }

        result = coordinator.coordinate_with_agent("agent_5", request)

        assert result["status"] == "success"
        assert "stream_name" in result
        assert "stream_status" in result

    def test_media_processing_request_handling(self, coordinator):
        """Test media processing request handling"""
        request = {
            "type": "media_processing",
            "pipeline_name": "test_pipeline",
            "enable_video": True,
            "enable_audio": True,
            "video": {"device_id": 0},
            "audio": {"device_id": 0},
            "video_effects": [{"type": "grayscale"}],
            "audio_effects": [{"type": "normalize"}],
        }

        result = coordinator.coordinate_with_agent("agent_4", request)

        assert result["status"] == "success"
        assert "pipeline_name" in result
        assert "pipeline_status" in result

    def test_status_report_request_handling(self, coordinator):
        """Test status report request handling"""
        request = {"type": "status_report"}

        result = coordinator.coordinate_with_agent("agent_6", request)

        assert result["status"] == "success"
        assert "agent_id" in result
        assert "multimedia_services_status" in result
        assert "integration_status" in result
        assert "agent_connections" in result

    def test_unknown_request_type_handling(self, coordinator):
        """Test handling of unknown request types"""
        request = {"type": "unknown_request_type"}

        result = coordinator.coordinate_with_agent("agent_7", request)

        assert "error" in result
        assert "Unknown request type" in result["error"]

    def test_coordination_event_logging(self, coordinator):
        """Test that coordination events are properly logged"""
        initial_event_count = coordinator.integration_status[
            "total_coordination_events"
        ]

        request = {"type": "content_generation", "content_type": "blog"}
        coordinator.coordinate_with_agent("agent_8", request)

        # Check that event count increased
        assert (
            coordinator.integration_status["total_coordination_events"]
            > initial_event_count
        )

        # Check that coordination events were logged
        assert len(coordinator.coordination_events) > 0

    def test_get_coordination_status(self, coordinator):
        """Test getting overall coordination status"""
        status = coordinator.get_coordination_status()

        assert "integration_status" in status
        assert "agent_connections" in status
        assert "multimedia_services" in status
        assert "recent_coordination_events" in status
        assert "timestamp" in status

        # Check multimedia services status
        multimedia_status = status["multimedia_services"]
        assert "media_processor" in multimedia_status
        assert "content_manager" in multimedia_status
        assert "streaming" in multimedia_status

    def test_broadcast_multimedia_update(self, coordinator):
        """Test broadcasting multimedia updates to all agents"""
        update_data = {"message": "Test broadcast message", "timestamp": time.time()}

        result = coordinator.broadcast_multimedia_update("test_update", update_data)

        assert result["status"] == "success"
        assert "broadcast_results" in result
        assert "total_agents" in result
        assert "active_agents" in result

        # Check that all agents received the broadcast
        broadcast_results = result["broadcast_results"]
        assert len(broadcast_results) == 8  # All 8 agents

        # Check that active agents have successful results
        for agent_id, agent_info in coordinator.agent_connections.items():
            if agent_info["status"] == "active":
                assert agent_id in broadcast_results
                assert broadcast_results[agent_id]["status"] == "success"

    def test_agent_communication_status_monitoring(self, coordinator):
        """Test agent communication status monitoring"""
        # Simulate agent becoming inactive
        old_time = time.time() - 400  # 6+ minutes ago
        coordinator.agent_connections["agent_1"]["last_communication"] = old_time

        # Run communication status check
        coordinator._check_agent_communication_status()

        # Check that agent status was updated
        assert coordinator.agent_connections["agent_1"]["status"] == "inactive"

        # Check overall status
        assert coordinator.integration_status["agent_communications_active"] == False

    def test_multimedia_services_monitoring(self, coordinator):
        """Test multimedia services health monitoring"""
        # Test with healthy services
        coordinator._monitor_multimedia_services()
        assert coordinator.integration_status["multimedia_services_healthy"] == True

        # Test with unhealthy service
        coordinator.multimedia_services["media_processor"] = None
        coordinator._monitor_multimedia_services()
        assert coordinator.integration_status["multimedia_services_healthy"] == False

    def test_coordination_metrics_update(self, coordinator):
        """Test coordination metrics update"""
        initial_time = coordinator.integration_status["last_coordination_check"]

        # Update metrics
        coordinator._update_coordination_metrics()

        # Check that time was updated
        assert coordinator.integration_status["last_coordination_check"] > initial_time

        # Check overall status calculation
        if (
            coordinator.integration_status["multimedia_services_healthy"]
            and coordinator.integration_status["agent_communications_active"]
        ):
            assert coordinator.integration_status["overall_status"] == "healthy"
        else:
            assert coordinator.integration_status["overall_status"] == "degraded"

    def test_error_handling_in_coordination(self, coordinator):
        """Test error handling during coordination"""
        # Test with invalid agent ID
        result = coordinator.coordinate_with_agent("invalid_agent", {})
        assert "error" in result

        # Test with invalid request
        result = coordinator.coordinate_with_agent("agent_1", None)
        assert "error" in result

    def test_coordination_event_cleanup(self, coordinator):
        """Test that old coordination events are cleaned up"""
        # Add many events to trigger cleanup
        for i in range(150):
            event_id = f"test_event_{i}"
            coordinator.coordination_events[event_id] = {
                "timestamp": time.time() - i,
                "agent_id": "test_agent",
                "request_type": "test",
                "request_data": {},
                "response": {"status": "success"},
                "status": "success",
            }

        # Trigger cleanup by adding one more event
        coordinator._log_coordination_event("test_agent", {}, {"status": "success"})

        # Check that events were cleaned up (should be around 100)
        assert len(coordinator.coordination_events) <= 100

    def test_multimedia_service_integration(self, coordinator):
        """Test integration with actual multimedia services"""
        # Test that services respond to basic operations
        media_processor = coordinator.multimedia_services["media_processor"]
        content_manager = coordinator.multimedia_services["content_manager"]
        streaming = coordinator.multimedia_services["streaming"]

        # Check that services have expected methods
        assert hasattr(media_processor, "get_system_status")
        assert hasattr(content_manager, "get_pipeline_status")
        assert hasattr(streaming, "get_streaming_status")

    def test_agent_specific_multimedia_needs(self, coordinator):
        """Test that agents have appropriate multimedia needs defined"""
        expected_needs = {
            "agent_1": ["content_generation", "documentation_videos"],
            "agent_2": ["collaboration_streams", "team_meetings"],
            "agent_4": ["test_videos", "quality_demos"],
            "agent_5": ["coordination_streams", "status_reports"],
            "agent_6": ["performance_metrics", "optimization_demos"],
            "agent_7": ["api_demos", "integration_tutorials"],
            "agent_8": ["workflow_demos", "automation_videos"],
        }

        for agent_id, expected_need_list in expected_needs.items():
            agent_needs = coordinator.agent_connections[agent_id]["multimedia_needs"]
            for need in expected_need_list:
                assert need in agent_needs, f"Agent {agent_id} missing need: {need}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
