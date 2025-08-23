"""
Integration Coordinator for Agent_Cellphone_V2_Repository
Main orchestrator that coordinates all integration infrastructure components.
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
import signal
import sys

# Import our integration components
try:
    from .api_manager import APIManager, APIEndpoint, APIMethod
    from .middleware_orchestrator import (
        MiddlewareOrchestrator,
        MiddlewareChain,
        DataPacket,
    )
    from .service_registry import (
        ServiceRegistry,
        ServiceInfo,
        ServiceType,
        ServiceStatus,
    )
    from ..core.config_manager import ConfigManager
except ImportError:
    # Fallback for standalone usage
    import sys
    import os

    # Add current directory to path for standalone imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    from api_manager import APIManager, APIEndpoint, APIMethod
    from middleware_orchestrator import (
        MiddlewareOrchestrator,
        MiddlewareChain,
        DataPacket,
    )
    from service_registry import (
        ServiceRegistry,
        ServiceInfo,
        ServiceType,
        ServiceStatus,
    )
    from config_manager import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegrationStatus(Enum):
    """Status of the integration system."""

    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class IntegrationMetrics:
    """Metrics for the integration system."""

    uptime_seconds: float = 0.0
    total_requests_processed: int = 0
    total_data_packets_processed: int = 0
    active_services: int = 0
    healthy_services: int = 0
    middleware_chains_active: int = 0
    api_endpoints_registered: int = 0
    last_activity: float = 0.0
    error_count: int = 0
    start_time: float = field(default_factory=time.time)


class IntegrationCoordinator:
    """Main coordinator for the integration infrastructure."""

    def __init__(self, config_dir: Optional[str] = None):
        self.status = IntegrationStatus.STOPPED
        self.config_dir = config_dir or "config"

        # Initialize components
        self.config_manager = ConfigManager(self.config_dir)
        self.api_manager = APIManager()
        self.middleware_orchestrator = MiddlewareOrchestrator()
        self.service_registry = ServiceRegistry()

        # Metrics
        self.metrics = IntegrationMetrics()

        # Event callbacks
        self.status_change_callbacks: List[
            Callable[[IntegrationStatus, IntegrationStatus], None]
        ] = []
        self.error_callbacks: List[Callable[[str, Exception], None]] = []

        # Graceful shutdown
        self.shutdown_event = asyncio.Event()

        # Register signal handlers
        self._setup_signal_handlers()

        # Register default API endpoints
        self._register_default_endpoints()

        # Register default middleware
        self._register_default_middleware()

        # Register default services
        self._register_default_services()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown")
            asyncio.create_task(self.stop())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _register_default_endpoints(self):
        """Register default API endpoints for system management."""

        # Health check endpoint
        async def health_check_handler(
            request: Dict[str, Any], context: Dict[str, Any]
        ) -> Dict[str, Any]:
            return {
                "status_code": 200,
                "success": True,
                "data": {
                    "status": self.status.value,
                    "uptime": time.time() - self.metrics.start_time,
                    "timestamp": time.time(),
                },
            }

        health_endpoint = APIEndpoint(
            path="/api/health",
            method=APIMethod.GET,
            handler=health_check_handler,
            description="System health check endpoint",
            tags=["health", "monitoring"],
        )
        self.api_manager.register_endpoint(health_endpoint)

        # Metrics endpoint
        async def metrics_handler(
            request: Dict[str, Any], context: Dict[str, Any]
        ) -> Dict[str, Any]:
            return {
                "status_code": 200,
                "success": True,
                "data": self.get_system_metrics(),
            }

        metrics_endpoint = APIEndpoint(
            path="/api/metrics",
            method=APIMethod.GET,
            handler=metrics_handler,
            description="System metrics endpoint",
            tags=["metrics", "monitoring"],
        )
        self.api_manager.register_endpoint(metrics_endpoint)

        # Configuration endpoint
        async def config_handler(
            request: Dict[str, Any], context: Dict[str, Any]
        ) -> Dict[str, Any]:
            return {
                "status_code": 200,
                "success": True,
                "data": self.config_manager.get_config_summary(),
            }

        config_endpoint = APIEndpoint(
            path="/api/config",
            method=APIMethod.GET,
            handler=config_handler,
            description="Configuration summary endpoint",
            tags=["config", "management"],
        )
        self.api_manager.register_endpoint(config_endpoint)

        # Services endpoint
        async def services_handler(
            request: Dict[str, Any], context: Dict[str, Any]
        ) -> Dict[str, Any]:
            return {
                "status_code": 200,
                "success": True,
                "data": self.service_registry.get_registry_summary(),
            }

        services_endpoint = APIEndpoint(
            path="/api/services",
            method=APIMethod.GET,
            handler=services_handler,
            description="Service registry summary endpoint",
            tags=["services", "discovery"],
        )
        self.api_manager.register_endpoint(services_endpoint)

    def _register_default_middleware(self):
        """Register default middleware components."""
        # This will be populated by the middleware orchestrator
        # when it starts up with its default components
        pass

    def _register_default_services(self):
        """Register default services."""
        # Register the integration coordinator itself as a service
        coordinator_service = ServiceInfo(
            id="integration-coordinator",
            name="integration-coordinator",
            service_type=ServiceType.INTEGRATION,
            endpoints=[
                # Note: This service doesn't have external endpoints
                # It's registered for discovery purposes
            ],
            metadata={
                "version": "1.0.0",
                "description": "Main integration coordinator for Agent_Cellphone_V2_Repository",
                "tags": {"integration", "coordination", "orchestration"},
                "capabilities": {"coordination", "monitoring", "management"},
            },
        )

        # We'll register this when the service registry starts
        self._pending_services = [coordinator_service]

    async def start(self) -> None:
        """Start the integration coordinator and all components."""
        try:
            logger.info("Starting Integration Coordinator...")
            self._update_status(IntegrationStatus.STARTING)

            # Start configuration manager
            logger.info("Starting Configuration Manager...")
            # Configuration manager starts automatically

            # Start service registry
            logger.info("Starting Service Registry...")
            await self.service_registry.start()

            # Register pending services
            for service in getattr(self, "_pending_services", []):
                self.service_registry.register_service(service)

            # Start middleware orchestrator
            logger.info("Starting Middleware Orchestrator...")
            await self.middleware_orchestrator.start()

            # Start API manager
            logger.info("Starting API Manager...")
            await self.api_manager.start()

            # Start file watching for configuration
            logger.info("Starting Configuration File Watcher...")
            self.config_manager.start_file_watching()

            # Update metrics
            self.metrics.start_time = time.time()
            self._update_status(IntegrationStatus.RUNNING)

            logger.info("Integration Coordinator started successfully")

            # Start metrics collection loop
            asyncio.create_task(self._metrics_collection_loop())

        except Exception as e:
            logger.error(f"Error starting Integration Coordinator: {str(e)}")
            self._update_status(IntegrationStatus.ERROR)
            self._trigger_error_callback("startup", e)
            raise

    async def stop(self) -> None:
        """Stop the integration coordinator and all components."""
        try:
            logger.info("Stopping Integration Coordinator...")
            self._update_status(IntegrationStatus.STOPPING)

            # Set shutdown event
            self.shutdown_event.set()

            # Stop components in reverse order
            logger.info("Stopping Configuration File Watcher...")
            self.config_manager.stop_file_watching()

            logger.info("Stopping API Manager...")
            await self.api_manager.stop()

            logger.info("Stopping Middleware Orchestrator...")
            await self.middleware_orchestrator.stop()

            logger.info("Stopping Service Registry...")
            await self.service_registry.stop()

            # Cleanup
            self.config_manager.cleanup()

            self._update_status(IntegrationStatus.STOPPED)
            logger.info("Integration Coordinator stopped successfully")

        except Exception as e:
            logger.error(f"Error stopping Integration Coordinator: {str(e)}")
            self._update_status(IntegrationStatus.ERROR)
            self._trigger_error_callback("shutdown", e)
            raise

    def _update_status(self, new_status: IntegrationStatus) -> None:
        """Update the status and trigger callbacks."""
        old_status = self.status
        self.status = new_status

        if old_status != new_status:
            logger.info(
                f"Integration Coordinator status changed: {old_status.value} -> {new_status.value}"
            )

            # Trigger callbacks
            for callback in self.status_change_callbacks:
                try:
                    callback(old_status, new_status)
                except Exception as e:
                    logger.error(f"Error in status change callback: {str(e)}")

    def _trigger_error_callback(self, context: str, error: Exception) -> None:
        """Trigger error callbacks."""
        for callback in self.error_callbacks:
            try:
                callback(context, error)
            except Exception as e:
                logger.error(f"Error in error callback: {str(e)}")

    async def _metrics_collection_loop(self):
        """Collect system metrics periodically."""
        while (
            self.status == IntegrationStatus.RUNNING
            and not self.shutdown_event.is_set()
        ):
            try:
                await self._update_metrics()
                await asyncio.sleep(30)  # Update every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in metrics collection: {str(e)}")
                await asyncio.sleep(30)

    def _update_metrics(self):
        """Update system metrics."""
        current_time = time.time()

        # Update basic metrics
        self.metrics.uptime_seconds = current_time - self.metrics.start_time

        # Get metrics from components
        if self.api_manager.running:
            self.metrics.api_endpoints_registered = len(self.api_manager.endpoints)

        if self.middleware_orchestrator.running:
            middleware_metrics = self.middleware_orchestrator.get_performance_metrics()
            self.metrics.total_data_packets_processed = middleware_metrics.get(
                "total_packets_processed", 0
            )
            self.metrics.middleware_chains_active = middleware_metrics.get(
                "active_chains", 0
            )

        if self.service_registry.running:
            registry_summary = self.service_registry.get_registry_summary()
            self.metrics.active_services = registry_summary.get("total_services", 0)

            healthy_services = self.service_registry.get_healthy_services()
            self.metrics.healthy_services = len(healthy_services)

        self.metrics.last_activity = current_time

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics."""
        return {
            "coordinator": {
                "status": self.status.value,
                "uptime_seconds": self.metrics.uptime_seconds,
                "start_time": self.metrics.start_time,
                "last_activity": self.metrics.last_activity,
                "error_count": self.metrics.error_count,
            },
            "api_manager": {
                "running": self.api_manager.running,
                "endpoints_registered": self.metrics.api_endpoints_registered,
                "endpoints_summary": self.api_manager.get_endpoints_summary(),
            },
            "middleware_orchestrator": {
                "running": self.middleware_orchestrator.running,
                "total_packets_processed": self.metrics.total_data_packets_processed,
                "chains_active": self.metrics.middleware_chains_active,
                "performance_metrics": self.middleware_orchestrator.get_performance_metrics()
                if self.middleware_orchestrator.running
                else {},
            },
            "service_registry": {
                "running": self.service_registry.running,
                "total_services": self.metrics.active_services,
                "healthy_services": self.metrics.healthy_services,
                "registry_summary": self.service_registry.get_registry_summary()
                if self.service_registry.running
                else {},
            },
            "config_manager": {
                "config_summary": self.config_manager.get_config_summary()
            },
        }

    def add_status_change_callback(
        self, callback: Callable[[IntegrationStatus, IntegrationStatus], None]
    ):
        """Add callback for status changes."""
        self.status_change_callbacks.append(callback)

    def add_error_callback(self, callback: Callable[[str, Exception], None]):
        """Add callback for errors."""
        self.error_callbacks.append(callback)

    async def process_api_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process an API request through the system."""
        try:
            self.metrics.total_requests_processed += 1
            self.metrics.last_activity = time.time()

            # Process through API manager
            response = await self.api_manager.handle_request(request)

            return response

        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Error processing API request: {str(e)}")
            self._trigger_error_callback("api_request", e)

            return {
                "status_code": 500,
                "success": False,
                "error": str(e),
                "timestamp": time.time(),
            }

    async def process_data_packet(
        self, data_packet: DataPacket, chain_name: Optional[str] = None
    ) -> DataPacket:
        """Process a data packet through the middleware system."""
        try:
            self.metrics.total_data_packets_processed += 1
            self.metrics.last_activity = time.time()

            # Process through middleware orchestrator
            result = await self.middleware_orchestrator.process_data_packet(
                data_packet, chain_name
            )

            return result

        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Error processing data packet: {str(e)}")
            self._trigger_error_callback("data_packet", e)

            # Return packet with error
            data_packet.metadata["error"] = str(e)
            data_packet.metadata["processing_failed"] = True
            return data_packet

    def register_service(self, service: ServiceInfo) -> str:
        """Register a service with the service registry."""
        if not self.service_registry.running:
            raise RuntimeError("Service registry is not running")

        return self.service_registry.register_service(service)

    def get_service(self, service_id: str) -> Optional[ServiceInfo]:
        """Get a service by ID."""
        return self.service_registry.get_service(service_id)

    def find_services(self, **kwargs) -> List[ServiceInfo]:
        """Find services matching criteria."""
        return self.service_registry.find_services(**kwargs)

    # Configuration methods removed - use config_manager directly
    # get_config_value and set_config_value are available on config_manager

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        health_status = {
            "status": self.status.value,
            "healthy": self.status == IntegrationStatus.RUNNING,
            "components": {},
            "timestamp": time.time(),
        }

        # Check API manager health
        health_status["components"]["api_manager"] = {
            "healthy": self.api_manager.running,
            "endpoints": len(self.api_manager.endpoints),
        }

        # Check middleware orchestrator health
        health_status["components"]["middleware_orchestrator"] = {
            "healthy": self.middleware_orchestrator.running,
            "chains": len(self.middleware_orchestrator.middleware_chains),
        }

        # Check service registry health
        health_status["components"]["service_registry"] = {
            "healthy": self.service_registry.running,
            "services": len(self.service_registry.services),
        }

        # Check configuration manager health
        health_status["components"]["config_manager"] = {
            "healthy": True,  # Config manager is always healthy
            "config_sections": len(self.config_manager.configs),
        }

        # Overall health depends on all critical components
        critical_components = [
            "api_manager",
            "middleware_orchestrator",
            "service_registry",
        ]
        all_healthy = all(
            health_status["components"][comp]["healthy"] for comp in critical_components
        )
        health_status["healthy"] = all_healthy

        return health_status

    async def wait_for_shutdown(self):
        """Wait for shutdown signal."""
        await self.shutdown_event.wait()


# Example usage and testing
async def main():
    """Main function for testing the Integration Coordinator."""
    # Create coordinator
    coordinator = IntegrationCoordinator("test_config")

    # Add callbacks for monitoring
    def on_status_change(old_status: IntegrationStatus, new_status: IntegrationStatus):
        print(
            f"Integration Coordinator status changed: {old_status.value} -> {new_status.value}"
        )

    def on_error(context: str, error: Exception):
        print(f"Integration Coordinator error in {context}: {str(error)}")

    coordinator.add_status_change_callback(on_status_change)
    coordinator.add_error_callback(on_error)

    try:
        # Start coordinator
        await coordinator.start()

        # Wait a bit for components to initialize
        await asyncio.sleep(2)

        # Get system health
        health = coordinator.get_system_health()
        print(f"System Health: {json.dumps(health, indent=2)}")

        # Get metrics
        metrics = coordinator.get_system_metrics()
        print(f"System Metrics: {json.dumps(metrics, indent=2)}")

        # Test API request
        test_request = {
            "path": "/api/health",
            "method": "GET",
            "headers": {},
            "client_id": "test-client",
        }

        response = await coordinator.process_api_request(test_request)
        print(f"API Response: {json.dumps(response, indent=2)}")

        # Wait for shutdown signal
        print("Press Ctrl+C to stop...")
        await coordinator.wait_for_shutdown()

    except KeyboardInterrupt:
        print("\nShutdown requested...")
    finally:
        # Stop coordinator
        await coordinator.stop()


if __name__ == "__main__":
    asyncio.run(main())
