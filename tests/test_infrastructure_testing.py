"""Infrastructure testing for the service registry component."""

import pytest

from src.services.service_registry import (
    ServiceRegistry,
    ServiceInfo,
    ServiceType,
    ServiceStatus,
    ServiceEndpoint,
    ServiceMetadata,
)


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
        assert registry.running is False

    def test_register_service(self, registry, sample_service):
        """Test registering a service."""
        service_id = registry.register_service(sample_service)

        assert service_id == sample_service.id
        assert registry.services[service_id] == sample_service
        assert registry.service_names[sample_service.name] == service_id

    def test_register_duplicate_service_name(self, registry, sample_service):
        """Test that registering services with duplicate names updates the existing one."""
        first_id = registry.register_service(sample_service)

        second_service = ServiceInfo(
            id="test-service-2",
            name=sample_service.name,
            service_type=ServiceType.API,
            endpoints=[],
            metadata=ServiceMetadata(),
        )

        second_id = registry.register_service(second_service)

        assert second_id == second_service.id
        assert registry.services[second_id] == second_service
        assert registry.service_names[sample_service.name] == second_id
        assert first_id not in registry.services

    def test_unregister_service(self, registry, sample_service):
        """Test unregistering a service."""
        service_id = registry.register_service(sample_service)

        success = registry.unregister_service(service_id)

        assert success is True
        assert service_id not in registry.services
        assert sample_service.name not in registry.service_names

    def test_unregister_nonexistent_service(self, registry):
        """Test that unregistering a non-existent service returns False."""
        success = registry.unregister_service("nonexistent")
        assert success is False

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

        healthy_services = registry.get_healthy_services()
        assert len(healthy_services) == 0

        registry.update_service_status(sample_service.id, ServiceStatus.HEALTHY)

        healthy_services = registry.get_healthy_services()
        assert len(healthy_services) == 1
        assert healthy_services[0] == sample_service

