"""
Integration Infrastructure Test Suite for Agent_Cellphone_V2_Repository
Comprehensive testing of all integration components following TDD principles.
"""

import pytest
import asyncio
import json
import time
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import tempfile
import shutil

# Import the components we're testing
from src.services.api_manager import (
    APIManager,
    APIEndpoint,
    APIMethod,
    LoggingMiddleware,
    RateLimitMiddleware,
    AuthenticationMiddleware,
)
from src.services.middleware_orchestrator import (
    MiddlewareOrchestrator,
    MiddlewareChain,
    DataPacket,
    DataTransformationMiddleware,
    ValidationMiddleware,
    RoutingMiddleware,
)
from src.services.service_registry import (
    ServiceRegistry,
    ServiceInfo,
    ServiceType,
    ServiceStatus,
    ServiceEndpoint,
    ServiceMetadata,
    HTTPHealthCheck,
    TCPHealthCheck,
)
from src.core.config_manager import ConfigManager
from src.services.integration_coordinator import (
    IntegrationCoordinator,
    IntegrationStatus,
    IntegrationMetrics,
)


class TestAPIManager:
    """Test suite for the API Manager component."""

    @pytest.fixture
    def api_manager(self):
        """Create a fresh API manager for each test."""
        return APIManager()

    @pytest.fixture
    def sample_endpoint(self):
        """Create a sample API endpoint for testing."""

        async def sample_handler(request, context):
            return {"status_code": 200, "data": "test"}

        return APIEndpoint(
            path="/test",
            method=APIMethod.GET,
            handler=sample_handler,
            description="Test endpoint",
        )

    def test_api_manager_initialization(self, api_manager):
        """Test that API manager initializes correctly."""
        assert api_manager.endpoints == []
        assert api_manager.middleware == []
        assert api_manager.services == {}
        assert not api_manager.running

    def test_add_endpoint(self, api_manager, sample_endpoint):
        """Test adding an endpoint to the API manager."""
        api_manager.add_endpoint(sample_endpoint)
        assert len(api_manager.endpoints) == 1
        assert api_manager.endpoints[0] == sample_endpoint

    def test_add_duplicate_endpoint(self, api_manager, sample_endpoint):
        """Test that duplicate endpoints are rejected."""
        api_manager.add_endpoint(sample_endpoint)

        with pytest.raises(ValueError, match="already exists"):
            api_manager.add_endpoint(sample_endpoint)

    def test_add_middleware(self, api_manager):
        """Test adding middleware to the API manager."""
        middleware = LoggingMiddleware()
        api_manager.add_middleware(middleware, priority=100)

        assert len(api_manager.middleware) == 1
        assert api_manager.middleware[0].handler == middleware
        assert api_manager.middleware[0].priority == 100

    def test_register_service(self, api_manager):
        """Test registering a service with the API manager."""
        test_service = Mock()
        api_manager.register_service("test_service", test_service)

        assert api_manager.services["test_service"] == test_service

    def test_get_service(self, api_manager):
        """Test retrieving a registered service."""
        test_service = Mock()
        api_manager.register_service("test_service", test_service)

        retrieved_service = api_manager.get_service("test_service")
        assert retrieved_service == test_service

    def test_get_nonexistent_service(self, api_manager):
        """Test that requesting a non-existent service raises an error."""
        with pytest.raises(KeyError, match="not found"):
            api_manager.get_service("nonexistent")

    @pytest.mark.asyncio
    async def test_handle_request_success(self, api_manager, sample_endpoint):
        """Test successful request handling."""
        api_manager.add_endpoint(sample_endpoint)
        await api_manager.start()

        request = {
            "path": "/test",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await api_manager.handle_request(request)

        assert response["status_code"] == 200
        assert response["data"] == "test"

        await api_manager.stop()

    @pytest.mark.asyncio
    async def test_handle_request_endpoint_not_found(self, api_manager):
        """Test handling requests to non-existent endpoints."""
        await api_manager.start()

        request = {
            "path": "/nonexistent",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await api_manager.handle_request(request)

        assert response["status_code"] == 404
        assert not response["success"]
        assert "Endpoint not found" in response["error"]

        await api_manager.stop()

    @pytest.mark.asyncio
    async def test_middleware_pipeline(self, api_manager, sample_endpoint):
        """Test that middleware processes requests correctly."""

        # Create custom middleware that adds headers
        class TestMiddleware:
            def __init__(self):
                self.name = "TestMiddleware"

            async def before(self, request, context):
                request["headers"]["X-Test"] = "test-value"
                return request

            async def after(self, response, context):
                response["headers"]["X-Response-Test"] = "response-value"
                return response

        # Add middleware and endpoint
        test_middleware = TestMiddleware()
        api_manager.add_middleware(test_middleware, priority=50)
        api_manager.add_endpoint(sample_endpoint)

        await api_manager.start()

        request = {
            "path": "/test",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await api_manager.handle_request(request)

        # Check that middleware processed the request
        assert response["status_code"] == 200
        assert "X-Response-Test" in response["headers"]

        await api_manager.stop()


class TestMiddlewareOrchestrator:
    """Test suite for the Middleware Orchestrator component."""

    @pytest.fixture
    def orchestrator(self):
        """Create a fresh middleware orchestrator for each test."""
        return MiddlewareOrchestrator()

    @pytest.fixture
    def sample_data_packet(self):
        """Create a sample data packet for testing."""
        return DataPacket(
            id="test-1",
            data={"message": "test"},
            metadata={"source": "test"},
            tags={"test"},
        )

    def test_orchestrator_initialization(self, orchestrator):
        """Test that middleware orchestrator initializes correctly."""
        assert orchestrator.middleware_components == {}
        assert orchestrator.middleware_chains == []
        assert orchestrator.running == False

    def test_register_middleware(self, orchestrator):
        """Test registering middleware components."""
        middleware = DataTransformationMiddleware()
        orchestrator.register_middleware(middleware)

        assert middleware.name in orchestrator.middleware_components
        assert orchestrator.middleware_components[middleware.name] == middleware

    def test_create_chain(self, orchestrator):
        """Test creating middleware chains."""
        # Register middleware first
        middleware = DataTransformationMiddleware()
        orchestrator.register_middleware(middleware)

        chain = MiddlewareChain(
            name="test_chain",
            middleware_list=[middleware.name],
            description="Test chain",
        )

        orchestrator.create_chain(chain)

        assert len(orchestrator.middleware_chains) == 1
        assert orchestrator.middleware_chains[0].name == "test_chain"

    def test_create_chain_with_nonexistent_middleware(self, orchestrator):
        """Test that creating chains with non-existent middleware fails."""
        chain = MiddlewareChain(
            name="test_chain",
            middleware_list=["nonexistent_middleware"],
            description="Test chain",
        )

        with pytest.raises(ValueError, match="not found"):
            orchestrator.create_chain(chain)

    @pytest.mark.asyncio
    async def test_process_data_packet(self, orchestrator, sample_data_packet):
        """Test processing data packets through middleware chains."""
        # Register middleware
        transformation_middleware = DataTransformationMiddleware(
            {"transformations": {"test": "string_uppercase"}}
        )
        orchestrator.register_middleware(transformation_middleware)

        # Create chain
        chain = MiddlewareChain(
            name="test_chain",
            middleware_list=[transformation_middleware.name],
            description="Test chain",
        )
        orchestrator.create_chain(chain)

        await orchestrator.start()

        # Process packet
        result = await orchestrator.process_data_packet(sample_data_packet)

        # Check that packet was processed
        assert result.id == sample_data_packet.id
        assert "transformed" in result.metadata

        await orchestrator.stop()

    def test_get_performance_metrics(self, orchestrator):
        """Test retrieving performance metrics."""
        metrics = orchestrator.get_performance_metrics()

        assert "uptime_seconds" in metrics
        assert "total_packets_processed" in metrics
        assert "middleware_components" in metrics
        assert "active_chains" in metrics


class TestServiceRegistry:
    """Test suite for the Service Registry component."""

    @pytest.fixture
    def registry(self):
        """Create a fresh service registry for each test."""
        return ServiceRegistry()

    @pytest.fixture
    def sample_service(self):
        """Create a sample service for testing."""
        return ServiceInfo(
            id="test-service-1",
            name="test-service",
            service_type=ServiceType.API,
            endpoints=[
                ServiceEndpoint(
                    host="localhost", port=8000, health_check_path="/health"
                )
            ],
            metadata=ServiceMetadata(
                version="1.0.0",
                description="Test service",
                tags={"test", "api"},
                capabilities={"read", "write"},
            ),
        )

    def test_registry_initialization(self, registry):
        """Test that service registry initializes correctly."""
        assert registry.services == {}
        assert registry.service_names == {}
        assert registry.running == False

    def test_register_service(self, registry, sample_service):
        """Test registering a service."""
        service_id = registry.register_service(sample_service)

        assert service_id == sample_service.id
        assert registry.services[service_id] == sample_service
        assert registry.service_names[sample_service.name] == service_id

    def test_register_duplicate_service_name(self, registry, sample_service):
        """Test that registering services with duplicate names updates the existing one."""
        # Register first service
        first_id = registry.register_service(sample_service)

        # Create second service with same name but different ID
        second_service = ServiceInfo(
            id="test-service-2",
            name=sample_service.name,  # Same name
            service_type=ServiceType.API,
            endpoints=[],
            metadata=ServiceMetadata(),
        )

        second_id = registry.register_service(second_service)

        # Should have updated the existing service
        assert second_id == second_service.id
        assert registry.services[second_id] == second_service
        assert registry.service_names[sample_service.name] == second_id
        assert first_id not in registry.services

    def test_unregister_service(self, registry, sample_service):
        """Test unregistering a service."""
        service_id = registry.register_service(sample_service)

        success = registry.unregister_service(service_id)

        assert success == True
        assert service_id not in registry.services
        assert sample_service.name not in registry.service_names

    def test_unregister_nonexistent_service(self, registry):
        """Test that unregistering a non-existent service returns False."""
        success = registry.unregister_service("nonexistent")
        assert success == False

    def test_get_service_by_id(self, registry, sample_service):
        """Test retrieving a service by ID."""
        service_id = registry.register_service(sample_service)

        retrieved_service = registry.get_service(service_id)
        assert retrieved_service == sample_service

    def test_get_service_by_name(self, registry, sample_service):
        """Test retrieving a service by name."""
        registry.register_service(sample_service)

        retrieved_service = registry.get_service_by_name(sample_service.name)
        assert retrieved_service == sample_service

    def test_find_services_by_type(self, registry, sample_service):
        """Test finding services by type."""
        registry.register_service(sample_service)

        api_services = registry.find_services(service_type=ServiceType.API)
        assert len(api_services) == 1
        assert api_services[0] == sample_service

        db_services = registry.find_services(service_type=ServiceType.DATABASE)
        assert len(db_services) == 0

    def test_find_services_by_tags(self, registry, sample_service):
        """Test finding services by tags."""
        registry.register_service(sample_service)

        test_tag_services = registry.find_services(tags={"test"})
        assert len(test_tag_services) == 1
        assert test_tag_services[0] == sample_service

        api_tag_services = registry.find_services(tags={"api"})
        assert len(api_tag_services) == 1

        nonexistent_tag_services = registry.find_services(tags={"nonexistent"})
        assert len(nonexistent_tag_services) == 0

    def test_get_healthy_services(self, registry, sample_service):
        """Test getting healthy services."""
        registry.register_service(sample_service)

        # Initially services are UNKNOWN status
        healthy_services = registry.get_healthy_services()
        assert len(healthy_services) == 0

        # Update status to HEALTHY
        registry.update_service_status(sample_service.id, ServiceStatus.HEALTHY)

        healthy_services = registry.get_healthy_services()
        assert len(healthy_services) == 1
        assert healthy_services[0] == sample_service


# TestIntegrationConfigManager class removed - functionality consolidated into main ConfigManager


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
        # Start coordinator
        await coordinator.start()
        assert coordinator.status == IntegrationStatus.RUNNING

        # Stop coordinator
        await coordinator.stop()
        assert coordinator.status == IntegrationStatus.STOPPED

    @pytest.mark.asyncio
    async def test_api_request_processing(self, coordinator):
        """Test processing API requests through the coordinator."""
        await coordinator.start()

        # Test health check endpoint
        request = {
            "path": "/api/health",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await coordinator.process_api_request(request)

        assert response["status_code"] == 200
        assert response["success"] == True
        assert "status" in response["data"]

        await coordinator.stop()

    def test_get_system_health(self, coordinator):
        """Test getting system health status."""
        health = coordinator.get_system_health()

        assert "status" in health
        assert "healthy" in health
        assert "components" in health
        assert "timestamp" in health

        # Check component health
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
        # Set config value
        coordinator.set_config_value("test.key", "test_value")

        # Get config value
        value = coordinator.get_config_value("test.key")
        assert value == "test_value"

    def test_service_registration(self, coordinator):
        """Test service registration through coordinator."""
        # Create test service
        service = ServiceInfo(
            id="test-service",
            name="test-service",
            service_type=ServiceType.API,
            endpoints=[],
            metadata=ServiceMetadata(),
        )

        # Register service
        service_id = coordinator.register_service(service)
        assert service_id == service.id

        # Retrieve service
        retrieved_service = coordinator.get_service(service_id)
        assert retrieved_service == service


# Integration tests that test multiple components together
class TestIntegrationInfrastructure:
    """Integration tests for the complete infrastructure."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary configuration directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_full_integration_workflow(self, temp_config_dir):
        """Test a complete integration workflow."""
        # Create coordinator
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            # Start coordinator
            await coordinator.start()

            # Verify all components are running
            assert coordinator.status == IntegrationStatus.RUNNING
            assert coordinator.api_manager.running
            assert coordinator.middleware_orchestrator.running
            assert coordinator.service_registry.running

            # Test API endpoints
            health_request = {
                "path": "/api/health",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            health_response = await coordinator.process_api_request(health_request)
            assert health_response["status_code"] == 200

            # Test metrics endpoint
            metrics_request = {
                "path": "/api/metrics",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            metrics_response = await coordinator.process_api_request(metrics_request)
            assert metrics_response["status_code"] == 200

            # Test configuration endpoint
            config_request = {
                "path": "/api/config",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            config_response = await coordinator.process_api_request(config_request)
            assert config_response["status_code"] == 200

            # Test services endpoint
            services_request = {
                "path": "/api/services",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            services_response = await coordinator.process_api_request(services_request)
            assert services_response["status_code"] == 200

            # Verify system health
            health = coordinator.get_system_health()
            assert health["healthy"] == True

            # Verify metrics
            metrics = coordinator.get_system_metrics()
            assert "coordinator" in metrics
            assert "api_manager" in metrics

        finally:
            # Cleanup
            await coordinator.stop()

    @pytest.mark.asyncio
    async def test_middleware_data_flow(self, temp_config_dir):
        """Test data flow through the middleware system."""
        # Create coordinator
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            # Create test data packet
            data_packet = DataPacket(
                id="test-packet-1",
                data={"message": "Hello World"},
                metadata={"source": "test", "priority": "high"},
                tags={"test", "high_priority"},
            )

            # Process through middleware
            result = await coordinator.process_data_packet(data_packet)

            # Verify packet was processed
            assert result.id == data_packet.id
            assert result.data == data_packet.data

        finally:
            await coordinator.stop()


# Performance and stress tests
class TestPerformanceAndStress:
    """Performance and stress tests for the integration infrastructure."""

    @pytest.mark.asyncio
    async def test_concurrent_api_requests(self, temp_config_dir):
        """Test handling multiple concurrent API requests."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            # Create multiple concurrent requests
            async def make_request(request_id):
                request = {
                    "path": "/api/health",
                    "method": "GET",
                    "headers": {},
                    "client_id": f"client-{request_id}",
                }
                return await coordinator.process_api_request(request)

            # Make 10 concurrent requests
            tasks = [make_request(i) for i in range(10)]
            responses = await asyncio.gather(*tasks)

            # Verify all requests succeeded
            for response in responses:
                assert response["status_code"] == 200
                assert response["success"] == True

        finally:
            await coordinator.stop()

    @pytest.mark.asyncio
    async def test_large_data_packet_processing(self, temp_config_dir):
        """Test processing large data packets."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            # Create large data packet
            large_data = {
                "items": [{"id": i, "data": f"item-{i}" * 100} for i in range(1000)]
            }

            data_packet = DataPacket(
                id="large-packet-1",
                data=large_data,
                metadata={"source": "test", "size": "large"},
                tags={"test", "large_data"},
            )

            # Process large packet
            start_time = time.time()
            result = await coordinator.process_data_packet(data_packet)
            processing_time = time.time() - start_time

            # Verify processing completed
            assert result.id == data_packet.id
            assert processing_time < 5.0  # Should complete within 5 seconds

        finally:
            await coordinator.stop()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
