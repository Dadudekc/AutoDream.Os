import pytest

import src.services.api_manager as api_manager_module
from src.services.service_registry import (
    ServiceRegistry,
    ServiceInfo,
    ServiceType,
    ServiceStatus,
    ServiceEndpoint,
    ServiceMetadata,
)


@pytest.fixture(autouse=True)
def reset_api_manager():
    api_manager_module.api_manager.endpoints.clear()
    yield
    api_manager_module.api_manager.endpoints.clear()
    api_manager_module.service_registry = ServiceRegistry()


@pytest.mark.asyncio
async def test_health_endpoint_lists_registered_services():
    registry = ServiceRegistry()
    api_manager_module.setup_example_endpoints(registry)

    service = ServiceInfo(
        id="svc-1",
        name="test-service",
        service_type=ServiceType.API,
        endpoints=[ServiceEndpoint(host="localhost", port=80)],
        metadata=ServiceMetadata(),
        status=ServiceStatus.HEALTHY,
    )
    registry.register_service(service)

    response = await api_manager_module.api_manager.process_request(
        method="GET", path="/api/health", client_id="test"
    )
    await registry.stop()

    assert response["success"]
    services = response["data"]["services"]
    assert any(
        s["name"] == "test-service" and s["status"] == "healthy" for s in services
    )


@pytest.mark.asyncio
async def test_health_endpoint_handles_missing_registry():
    api_manager_module.service_registry = None
    api_manager_module.setup_example_endpoints(None)

    response = await api_manager_module.api_manager.process_request(
        method="GET", path="/api/health", client_id="test"
    )

    assert response["success"]
    assert response["data"]["services"] == []
