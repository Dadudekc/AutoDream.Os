"""
Service Discovery and Registry System for Agent_Cellphone_V2_Repository
Manages service registration, health checks, and service discovery for integration infrastructure.
"""

import asyncio
import json
import logging
import time
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Set, Union
from pathlib import Path
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service health status."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    STARTING = "starting"
    STOPPING = "stopping"


class ServiceType(Enum):
    """Types of services for categorization."""

    API = "api"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    WORKER = "worker"
    MONITORING = "monitoring"
    INTEGRATION = "integration"
    CUSTOM = "custom"


@dataclass
class ServiceEndpoint:
    """Represents a service endpoint."""

    host: str
    port: int
    protocol: str = "http"
    path: str = "/"
    health_check_path: str = "/health"
    timeout: int = 30

    @property
    def url(self) -> str:
        """Get the full URL for the endpoint."""
        return f"{self.protocol}://{self.host}:{self.port}{self.path}"

    @property
    def health_check_url(self) -> str:
        """Get the health check URL for the endpoint."""
        return f"{self.protocol}://{self.host}:{self.port}{self.health_check_path}"


@dataclass
class ServiceMetadata:
    """Additional metadata for services."""

    version: str = "1.0.0"
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    capabilities: Set[str] = field(default_factory=set)
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceInfo:
    """Complete service information."""

    id: str
    name: str
    service_type: ServiceType
    endpoints: List[ServiceEndpoint]
    metadata: ServiceMetadata
    status: ServiceStatus = ServiceStatus.UNKNOWN
    last_health_check: Optional[float] = None
    health_check_interval: int = 60  # seconds
    registration_time: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    health_check_failures: int = 0
    max_health_check_failures: int = 3


class HealthCheckStrategy(ABC):
    """Abstract base class for health check strategies."""

    @abstractmethod
    async def check_health(self, service: ServiceInfo) -> ServiceStatus:
        """Check the health of a service."""
        pass


class HTTPHealthCheck(HealthCheckStrategy):
    """HTTP-based health check strategy."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def check_health(self, service: ServiceInfo) -> ServiceStatus:
        """Check service health via HTTP health check endpoint."""
        for endpoint in service.endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        endpoint.health_check_url,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as response:
                        if response.status == 200:
                            return ServiceStatus.HEALTHY
                        else:
                            logger.warning(
                                f"Health check failed for {service.name}: HTTP {response.status}"
                            )
                            return ServiceStatus.UNHEALTHY
            except Exception as e:
                logger.warning(f"Health check failed for {service.name}: {str(e)}")
                continue

        return ServiceStatus.UNHEALTHY


class TCPHealthCheck(HealthCheckStrategy):
    """TCP-based health check strategy."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def check_health(self, service: ServiceInfo) -> ServiceStatus:
        """Check service health via TCP connection."""
        for endpoint in service.endpoints:
            try:
                # Use ThreadPoolExecutor for blocking socket operations
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(
                        executor,
                        self._check_tcp_connection,
                        endpoint.host,
                        endpoint.port,
                    )
                    if result:
                        return ServiceStatus.HEALTHY
            except Exception as e:
                logger.warning(f"TCP health check failed for {service.name}: {str(e)}")
                continue

        return ServiceStatus.UNHEALTHY

    def _check_tcp_connection(self, host: str, port: int) -> bool:
        """Check TCP connection (blocking operation)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False


class CustomHealthCheck(HealthCheckStrategy):
    """Custom health check strategy using provided function."""

    def __init__(self, check_function: Callable[[ServiceInfo], bool]):
        self.check_function = check_function

    async def check_health(self, service: ServiceInfo) -> ServiceStatus:
        """Check service health using custom function."""
        try:
            # Run custom check function in executor to avoid blocking
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(
                    executor, self.check_function, service
                )
                return ServiceStatus.HEALTHY if result else ServiceStatus.UNHEALTHY
        except Exception as e:
            logger.error(f"Custom health check failed for {service.name}: {str(e)}")
            return ServiceStatus.UNHEALTHY


class ServiceRegistry:
    """Main service registry for managing service discovery and health monitoring."""

    def __init__(self):
        self.services: Dict[str, ServiceInfo] = {}
        self.service_names: Dict[str, str] = {}  # name -> id mapping
        self.health_checkers: Dict[ServiceType, HealthCheckStrategy] = {}
        self.health_check_tasks: Dict[str, asyncio.Task] = {}
        self.running = False

        # Register default health check strategies
        self._register_default_health_checks()

        # Event callbacks
        self.service_registered_callbacks: List[Callable[[ServiceInfo], None]] = []
        self.service_unregistered_callbacks: List[Callable[[ServiceInfo], None]] = []
        self.service_status_changed_callbacks: List[
            Callable[[ServiceInfo, ServiceStatus, ServiceStatus], None]
        ] = []

    def _register_default_health_checks(self):
        """Register default health check strategies for different service types."""
        self.register_health_check(ServiceType.API, HTTPHealthCheck())
        self.register_health_check(ServiceType.WORKER, TCPHealthCheck())
        self.register_health_check(ServiceType.DATABASE, TCPHealthCheck())
        self.register_health_check(ServiceType.CACHE, TCPHealthCheck())
        self.register_health_check(ServiceType.MESSAGE_QUEUE, TCPHealthCheck())

    def register_health_check(
        self, service_type: ServiceType, strategy: HealthCheckStrategy
    ):
        """Register a health check strategy for a service type."""
        self.health_checkers[service_type] = strategy
        logger.info(
            f"Registered health check strategy for {service_type.value}: {strategy.__class__.__name__}"
        )

    def register_service(self, service: ServiceInfo) -> str:
        """Register a new service."""
        # Check for duplicate names
        if service.name in self.service_names:
            existing_id = self.service_names[service.name]
            logger.warning(
                f"Service name '{service.name}' already exists, updating existing service"
            )
            self.unregister_service(existing_id)

        # Generate ID if not provided
        if not service.id:
            service.id = str(uuid.uuid4())

        # Add to registry
        self.services[service.id] = service
        self.service_names[service.name] = service.id

        # Start health monitoring
        self._start_health_monitoring(service)

        # Trigger callbacks
        for callback in self.service_registered_callbacks:
            try:
                callback(service)
            except Exception as e:
                logger.error(f"Error in service registered callback: {str(e)}")

        logger.info(f"Registered service: {service.name} ({service.id})")
        return service.id

    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service by ID."""
        if service_id not in self.services:
            return False

        service = self.services[service_id]

        # Stop health monitoring
        self._stop_health_monitoring(service_id)

        # Remove from registry
        del self.services[service_id]
        if service.name in self.service_names:
            del self.service_names[service.name]

        # Trigger callbacks
        for callback in self.service_unregistered_callbacks:
            try:
                callback(service)
            except Exception as e:
                logger.error(f"Error in service unregistered callback: {str(e)}")

        logger.info(f"Unregistered service: {service.name} ({service_id})")
        return True

    def get_service(self, service_id: str) -> Optional[ServiceInfo]:
        """Get a service by ID."""
        return self.services.get(service_id)

    def get_service_by_name(self, service_name: str) -> Optional[ServiceInfo]:
        """Get a service by name."""
        service_id = self.service_names.get(service_name)
        return self.services.get(service_id) if service_id else None

    def find_services(
        self,
        service_type: Optional[ServiceType] = None,
        tags: Optional[Set[str]] = None,
        capabilities: Optional[Set[str]] = None,
    ) -> List[ServiceInfo]:
        """Find services matching criteria."""
        matching_services = []

        for service in self.services.values():
            # Check service type
            if service_type and service.service_type != service_type:
                continue

            # Check tags
            if tags and not tags.issubset(service.metadata.tags):
                continue

            # Check capabilities
            if capabilities and not capabilities.issubset(
                service.metadata.capabilities
            ):
                continue

            matching_services.append(service)

        return matching_services

    def get_healthy_services(
        self, service_type: Optional[ServiceType] = None
    ) -> List[ServiceInfo]:
        """Get all healthy services, optionally filtered by type."""
        healthy_services = []

        for service in self.services.values():
            if service.status == ServiceStatus.HEALTHY:
                if service_type is None or service.service_type == service_type:
                    healthy_services.append(service)

        return healthy_services

    def update_service_status(self, service_id: str, status: ServiceStatus) -> bool:
        """Update the status of a service."""
        if service_id not in self.services:
            return False

        service = self.services[service_id]
        old_status = service.status

        if old_status != status:
            service.status = status
            service.last_health_check = time.time()

            # Trigger callbacks
            for callback in self.service_status_changed_callbacks:
                try:
                    callback(service, old_status, status)
                except Exception as e:
                    logger.error(f"Error in service status changed callback: {str(e)}")

            logger.info(
                f"Service {service.name} status changed: {old_status.value} -> {status.value}"
            )

        return True

    def _start_health_monitoring(self, service: ServiceInfo):
        """Start health monitoring for a service."""
        if service.id in self.health_check_tasks:
            return

        task = asyncio.create_task(self._health_check_loop(service))
        self.health_check_tasks[service.id] = task

    def _stop_health_monitoring(self, service_id: str):
        """Stop health monitoring for a service."""
        if service_id in self.health_check_tasks:
            task = self.health_check_tasks[service_id]
            task.cancel()
            del self.health_check_tasks[service_id]

    async def _health_check_loop(self, service: ServiceInfo):
        """Health check loop for a service."""
        while service.id in self.services:
            try:
                # Perform health check
                status = await self._perform_health_check(service)

                # Update service status
                self.update_service_status(service.id, status)

                # Update failure count
                if status == ServiceStatus.HEALTHY:
                    service.health_check_failures = 0
                else:
                    service.health_check_failures += 1

                # Mark as unhealthy if too many failures
                if service.health_check_failures >= service.max_health_check_failures:
                    self.update_service_status(service.id, ServiceStatus.UNHEALTHY)

                # Wait for next check
                await asyncio.sleep(service.health_check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop for {service.name}: {str(e)}")
                await asyncio.sleep(service.health_check_interval)

    async def _perform_health_check(self, service: ServiceInfo) -> ServiceStatus:
        """Perform a health check for a service."""
        # Get appropriate health checker
        checker = self.health_checkers.get(service.service_type)
        if not checker:
            logger.warning(
                f"No health checker for service type: {service.service_type.value}"
            )
            return ServiceStatus.UNKNOWN

        try:
            return await checker.check_health(service)
        except Exception as e:
            logger.error(f"Health check failed for {service.name}: {str(e)}")
            return ServiceStatus.UNHEALTHY

    def add_service_registered_callback(self, callback: Callable[[ServiceInfo], None]):
        """Add callback for when services are registered."""
        self.service_registered_callbacks.append(callback)

    def add_service_unregistered_callback(
        self, callback: Callable[[ServiceInfo], None]
    ):
        """Add callback for when services are unregistered."""
        self.service_unregistered_callbacks.append(callback)

    def add_service_status_changed_callback(
        self, callback: Callable[[ServiceInfo, ServiceStatus, ServiceStatus], None]
    ):
        """Add callback for when service status changes."""
        self.service_status_changed_callbacks.append(callback)

    def get_registry_summary(self) -> Dict[str, Any]:
        """Get a summary of the registry."""
        service_counts = {}
        status_counts = {}

        for service in self.services.values():
            # Count by type
            service_type = service.service_type.value
            service_counts[service_type] = service_counts.get(service_type, 0) + 1

            # Count by status
            status = service.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_services": len(self.services),
            "service_counts_by_type": service_counts,
            "service_counts_by_status": status_counts,
            "health_check_tasks": len(self.health_check_tasks),
            "running": self.running,
        }

    async def start(self):
        """Start the service registry."""
        self.running = True
        logger.info("Service Registry started")

    async def stop(self):
        """Stop the service registry."""
        self.running = False

        # Cancel all health check tasks
        for task in self.health_check_tasks.values():
            task.cancel()

        # Wait for tasks to complete
        if self.health_check_tasks:
            await asyncio.gather(
                *self.health_check_tasks.values(), return_exceptions=True
            )

        logger.info("Service Registry stopped")


# Example usage and testing
async def main():
    """Main function for testing the Service Registry."""
    # Create registry
    registry = ServiceRegistry()

    # Add callbacks for monitoring
    def on_service_registered(service: ServiceInfo):
        print(f"Service registered: {service.name} ({service.status.value})")

    def on_service_status_changed(
        service: ServiceInfo, old_status: ServiceStatus, new_status: ServiceStatus
    ):
        print(
            f"Service {service.name} status changed: {old_status.value} -> {new_status.value}"
        )

    registry.add_service_registered_callback(on_service_registered)
    registry.add_service_status_changed_callback(on_service_status_changed)

    # Start registry
    await registry.start()

    # Register example services
    api_service = ServiceInfo(
        id="api-1",
        name="user-api",
        service_type=ServiceType.API,
        endpoints=[
            ServiceEndpoint(host="localhost", port=8001, health_check_path="/health")
        ],
        metadata=ServiceMetadata(
            version="1.0.0",
            description="User management API",
            tags={"user", "management", "rest"},
            capabilities={"create", "read", "update", "delete"},
        ),
    )

    db_service = ServiceInfo(
        id="db-1",
        name="user-database",
        service_type=ServiceType.DATABASE,
        endpoints=[ServiceEndpoint(host="localhost", port=5432, protocol="tcp")],
        metadata=ServiceMetadata(
            version="13.0",
            description="PostgreSQL database",
            tags={"database", "postgresql", "persistent"},
            capabilities={"query", "transaction", "backup"},
        ),
    )

    # Register services
    registry.register_service(api_service)
    registry.register_service(db_service)

    # Wait for health checks
    await asyncio.sleep(5)

    # Get registry information
    print(
        f"\nRegistry summary: {json.dumps(registry.get_registry_summary(), indent=2)}"
    )

    # Find services
    api_services = registry.find_services(service_type=ServiceType.API)
    print(f"\nAPI services: {len(api_services)}")

    healthy_services = registry.get_healthy_services()
    print(f"Healthy services: {len(healthy_services)}")

    # Stop registry
    await registry.stop()


if __name__ == "__main__":
    asyncio.run(main())
