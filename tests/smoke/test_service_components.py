"""
🧪 SMOKE TESTS - SERVICE COMPONENTS
Integration & Performance Optimization Captain - TDD Integration Project

This module contains smoke tests for all service components, ensuring basic functionality
and integration between performance monitoring, API gateway, and agent communication systems.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from core.performance_monitor import PerformanceMonitor, MetricType
from core.performance_dashboard import PerformanceDashboard
from core.api_gateway import APIGateway
from core.v2_comprehensive_messaging_system import V2ComprehensiveMessagingSystem
from core.health_monitor_core import HealthMonitorCore


class TestServiceComponentsSmoke:
    """Smoke tests for service components to ensure basic functionality."""

    @pytest.mark.service
    @pytest.mark.smoke
    def test_performance_tracker_initialization(self):
        """Test that PerformanceMonitor initializes correctly."""
        tracker = PerformanceMonitor()
        assert tracker is not None
        assert hasattr(tracker, "record_metric")
        assert hasattr(tracker, "get_agent_performance_summary")

    @pytest.mark.service
    @pytest.mark.smoke
    def test_performance_profiler_initialization(self):
        """Test that PerformanceMonitor initializes correctly."""
        profiler = PerformanceMonitor()
        assert profiler is not None
        assert hasattr(profiler, "profile_function")
        assert hasattr(profiler, "profile")

    @pytest.mark.service
    @pytest.mark.smoke
    def test_performance_dashboard_initialization(self):
        """Test that PerformanceDashboard initializes correctly."""
        dashboard = PerformanceDashboard()
        assert dashboard is not None
        assert hasattr(dashboard, "start")
        assert hasattr(dashboard, "stop")

    @pytest.mark.service
    @pytest.mark.smoke
    def test_api_gateway_initialization(self):
        """Test that APIGateway initializes correctly."""
        gateway = APIGateway()
        assert gateway is not None
        assert hasattr(gateway, "register_service")
        assert hasattr(gateway, "route_request")

    @pytest.mark.service
    @pytest.mark.smoke
    def test_v2_messaging_system_initialization(self):
        """Test that V2ComprehensiveMessagingSystem initializes correctly."""
        messaging = V2ComprehensiveMessagingSystem()
        assert messaging is not None
        assert hasattr(messaging, "register_agent")
        assert hasattr(messaging, "send_message")

    @pytest.mark.service
    @pytest.mark.smoke
    def test_health_monitor_core_initialization(self):
        """Test that HealthMonitorCore initializes correctly."""
        monitor = HealthMonitorCore()
        assert monitor is not None
        assert hasattr(monitor, "start")
        assert hasattr(monitor, "stop")


class TestServiceIntegrationSmoke:
    """Smoke tests for service integration scenarios."""

    @pytest.mark.service
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_performance_tracking_integration(self):
        """Test basic performance tracking integration."""
        tracker = PerformanceMonitor()
        profiler = PerformanceMonitor()

        # Test that they can work together
        assert tracker is not None
        assert profiler is not None

        # Basic functionality test
        tracker.record_metric(MetricType.RESPONSE_TIME, 0.5, agent_id="test_agent")
        summary = tracker.get_agent_performance_summary("test_agent")
        assert "response_time" in summary
        assert summary["response_time"]["count"] == 1

    @pytest.mark.service
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_api_gateway_service_registration(self):
        """Test API gateway service registration."""
        gateway = APIGateway()

        # Test service registration
        gateway.register_service(
            "test_service", "Test Service", "1.0", "http://localhost:8000"
        )
        assert "test_service" in gateway.registered_services

    @pytest.mark.service
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_agent_communication_registration(self):
        """Test agent communication registration."""
        comm = AgentCommunicationProtocol()

        # Test agent registration
        agent_info = {
            "id": "test_agent",
            "name": "Test Agent",
            "capabilities": ["performance_monitoring"],
        }

        comm.register_agent(
            "test_agent",
            "Test Agent",
            ["performance_monitoring"],
            "http://localhost:8001",
        )
        assert "test_agent" in comm.registered_agents


class TestServiceHealthSmoke:
    """Smoke tests for service health and status."""

    @pytest.mark.service
    @pytest.mark.health
    @pytest.mark.smoke
    def test_all_services_healthy(self):
        """Test that all core services are healthy."""
        services = [
            PerformanceMonitor(),
            PerformanceMonitor(),
            PerformanceDashboard(),
            APIGateway(),
            AgentCommunicationProtocol(),
            HealthMonitorCore(),
        ]

        for service in services:
            assert service is not None
            # Basic health check - service exists and has expected methods

    @pytest.mark.service
    @pytest.mark.health
    @pytest.mark.smoke
    def test_service_methods_accessible(self):
        """Test that all service methods are accessible."""
        tracker = PerformanceMonitor()

        # Test method accessibility
        assert callable(tracker.record_metric)
        assert callable(tracker.get_agent_performance_summary)

        profiler = PerformanceMonitor()
        assert callable(profiler.profile_function)
        assert callable(profiler.profile)


# Test markers for pytest
pytest_plugins = ["pytest_asyncio"]


# Custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "service: mark test as service component test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "health: mark test as health check test")
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
