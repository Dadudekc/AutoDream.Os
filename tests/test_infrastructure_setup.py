"""Infrastructure setup tests for APIManager and MiddlewareOrchestrator."""

import asyncio
from unittest.mock import Mock

import pytest

from src.services.api_manager import (
    APIManager,
    APIEndpoint,
    APIMethod,
    LoggingMiddleware,
)
from src.services.middleware_orchestrator import (
    MiddlewareOrchestrator,
    MiddlewareChain,
    DataPacket,
    DataTransformationMiddleware,
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

        class TestMiddleware:
            def __init__(self):
                self.name = "TestMiddleware"

            async def before(self, request, context):
                request["headers"]["X-Test"] = "test-value"
                return request

            async def after(self, response, context):
                response["headers"]["X-Response-Test"] = "response-value"
                return response

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
        assert orchestrator.running is False

    def test_register_middleware(self, orchestrator):
        """Test registering middleware components."""
        middleware = DataTransformationMiddleware()
        orchestrator.register_middleware(middleware)

        assert middleware.name in orchestrator.middleware_components
        assert orchestrator.middleware_components[middleware.name] == middleware

    def test_create_chain(self, orchestrator):
        """Test creating middleware chains."""
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
        transformation_middleware = DataTransformationMiddleware(
            {"transformations": {"test": "string_uppercase"}}
        )
        orchestrator.register_middleware(transformation_middleware)

        chain = MiddlewareChain(
            name="test_chain",
            middleware_list=[transformation_middleware.name],
            description="Test chain",
        )
        orchestrator.create_chain(chain)

        await orchestrator.start()
        result = await orchestrator.process_data_packet(sample_data_packet)

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

