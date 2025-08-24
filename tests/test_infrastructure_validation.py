"""Validation tests for the integration coordinator."""

import asyncio
import shutil
import tempfile

import pytest

from src.services.integration_coordinator import (
    IntegrationCoordinator,
    IntegrationStatus,
)
from src.services.service_registry import ServiceInfo, ServiceType, ServiceMetadata


class TestIntegrationCoordinator:
    """Test suite for the Integration Coordinator component."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary configuration directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def coordinator(self, temp_config_dir):
        """Create an integration coordinator with temporary directory."""
        return IntegrationCoordinator(temp_config_dir)

    def test_coordinator_initialization(self, coordinator):
        """Test that integration coordinator initializes correctly."""
        assert coordinator.status == IntegrationStatus.STOPPED
        assert coordinator.config_manager is not None
        assert coordinator.api_manager is not None
        assert coordinator.middleware_orchestrator is not None
        assert coordinator.service_registry is not None

    @pytest.mark.asyncio
    async def test_coordinator_start_stop(self, coordinator):
        """Test starting and stopping the coordinator."""
        await coordinator.start()
        assert coordinator.status == IntegrationStatus.RUNNING

        await coordinator.stop()
        assert coordinator.status == IntegrationStatus.STOPPED

    @pytest.mark.asyncio
    async def test_api_request_processing(self, coordinator):
        """Test processing API requests through the coordinator."""
        await coordinator.start()

        request = {
            "path": "/api/health",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await coordinator.process_api_request(request)

        assert response["status_code"] == 200
        assert response["success"] is True
        assert "status" in response["data"]

        await coordinator.stop()

    def test_get_system_health(self, coordinator):
        """Test getting system health status."""
        health = coordinator.get_system_health()

        assert "status" in health
        assert "healthy" in health
        assert "components" in health
        assert "timestamp" in health

        components = health["components"]
        assert "api_manager" in components
        assert "middleware_orchestrator" in components
        assert "service_registry" in components
        assert "config_manager" in components

    def test_get_system_metrics(self, coordinator):
        """Test getting system metrics."""
        metrics = coordinator.get_system_metrics()

        assert "coordinator" in metrics
        assert "api_manager" in metrics
        assert "middleware_orchestrator" in metrics
        assert "service_registry" in metrics
        assert "config_manager" in metrics

    def test_config_value_management(self, coordinator):
        """Test configuration value management through coordinator."""
        coordinator.set_config_value("test.key", "test_value")

        value = coordinator.get_config_value("test.key")
        assert value == "test_value"

    def test_service_registration(self, coordinator):
        """Test service registration through coordinator."""
        service = ServiceInfo(
            id="test-service",
            name="test-service",
            service_type=ServiceType.API,
            endpoints=[],
            metadata=ServiceMetadata(),
        )

        service_id = coordinator.register_service(service)
        assert service_id == service.id

        retrieved_service = coordinator.get_service(service_id)
        assert retrieved_service == service

