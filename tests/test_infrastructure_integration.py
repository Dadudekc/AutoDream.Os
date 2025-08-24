"""Integration and performance tests for the infrastructure."""

import asyncio
import shutil
import tempfile
import time

import pytest

from src.services.integration_coordinator import IntegrationCoordinator, IntegrationStatus
from src.services.middleware_orchestrator import DataPacket


@pytest.fixture
def temp_config_dir():
    """Create a temporary configuration directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


class TestIntegrationInfrastructure:
    """Integration tests for the complete infrastructure."""

    @pytest.mark.asyncio
    async def test_full_integration_workflow(self, temp_config_dir):
        """Test a complete integration workflow."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            assert coordinator.status == IntegrationStatus.RUNNING
            assert coordinator.api_manager.running
            assert coordinator.middleware_orchestrator.running
            assert coordinator.service_registry.running

            health_request = {
                "path": "/api/health",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            health_response = await coordinator.process_api_request(health_request)
            assert health_response["status_code"] == 200

            metrics_request = {
                "path": "/api/metrics",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            metrics_response = await coordinator.process_api_request(metrics_request)
            assert metrics_response["status_code"] == 200

            config_request = {
                "path": "/api/config",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            config_response = await coordinator.process_api_request(config_request)
            assert config_response["status_code"] == 200

            services_request = {
                "path": "/api/services",
                "method": "GET",
                "headers": {},
                "client_id": "test-client",
            }

            services_response = await coordinator.process_api_request(services_request)
            assert services_response["status_code"] == 200

            health = coordinator.get_system_health()
            assert health["healthy"] is True

            metrics = coordinator.get_system_metrics()
            assert "coordinator" in metrics
            assert "api_manager" in metrics

        finally:
            await coordinator.stop()

    @pytest.mark.asyncio
    async def test_middleware_data_flow(self, temp_config_dir):
        """Test data flow through the middleware system."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            data_packet = DataPacket(
                id="test-packet-1",
                data={"message": "Hello World"},
                metadata={"source": "test", "priority": "high"},
                tags={"test", "high_priority"},
            )

            result = await coordinator.process_data_packet(data_packet)

            assert result.id == data_packet.id
            assert result.data == data_packet.data

        finally:
            await coordinator.stop()


class TestPerformanceAndStress:
    """Performance and stress tests for the integration infrastructure."""

    @pytest.mark.asyncio
    async def test_concurrent_api_requests(self, temp_config_dir):
        """Test handling multiple concurrent API requests."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            async def make_request(request_id):
                request = {
                    "path": "/api/health",
                    "method": "GET",
                    "headers": {},
                    "client_id": f"client-{request_id}",
                }
                return await coordinator.process_api_request(request)

            tasks = [make_request(i) for i in range(10)]
            responses = await asyncio.gather(*tasks)

            for response in responses:
                assert response["status_code"] == 200
                assert response["success"] is True

        finally:
            await coordinator.stop()

    @pytest.mark.asyncio
    async def test_large_data_packet_processing(self, temp_config_dir):
        """Test processing large data packets."""
        coordinator = IntegrationCoordinator(temp_config_dir)

        try:
            await coordinator.start()

            large_data = {
                "items": [{"id": i, "data": f"item-{i}" * 100} for i in range(1000)]
            }

            data_packet = DataPacket(
                id="large-packet-1",
                data=large_data,
                metadata={"source": "test", "size": "large"},
                tags={"test", "large_data"},
            )

            start_time = time.time()
            result = await coordinator.process_data_packet(data_packet)
            processing_time = time.time() - start_time

            assert result.id == data_packet.id
            assert processing_time < 5.0

        finally:
            await coordinator.stop()

