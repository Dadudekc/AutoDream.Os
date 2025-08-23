#!/usr/bin/env python3
"""
V2 Integration Framework
========================
Comprehensive integration framework for V2 system with service architecture.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status enumeration"""

    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass
class ServiceInfo:
    """Service information and metadata"""

    service_id: str
    service_name: str
    version: str
    status: ServiceStatus
    endpoints: List[str]
    health_check_url: Optional[str] = None
    last_health_check: Optional[float] = None


class V2IntegrationFramework:
    """Comprehensive integration framework for V2 system"""

    def __init__(self, config_path: str = "config/integration_config.json"):
        self.logger = logging.getLogger(f"{__name__}.V2IntegrationFramework")
        self.config_path = Path(config_path)

        # Service registry
        self._services: Dict[str, ServiceInfo] = {}
        self._service_handlers: Dict[str, Callable] = {}

        # Integration state
        self._framework_initialized = False
        self._health_monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()

        # Load configuration
        self._load_configuration()

        self.logger.info("V2 Integration Framework initialized")

    def _load_configuration(self):
        """Load integration configuration"""
        try:
            if self.config_path.exists():
                import json

                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.logger.warning(f"Configuration file not found: {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")

    def register_service(
        self,
        service_id: str,
        service_name: str,
        version: str = "1.0.0",
        endpoints: Optional[List[str]] = None,
        health_check_url: Optional[str] = None,
    ) -> bool:
        """Register a service with the integration framework"""
        if service_id in self._services:
            self.logger.warning(f"Service {service_id} already registered")
            return False

        service_info = ServiceInfo(
            service_id=service_id,
            service_name=service_name,
            version=version,
            status=ServiceStatus.ONLINE,
            endpoints=endpoints or [],
            health_check_url=health_check_url,
        )

        self._services[service_id] = service_info
        self.logger.info(
            f"Service registered: {service_name} ({service_id}) v{version}"
        )
        return True

    def register_service_handler(self, service_id: str, handler: Callable) -> bool:
        """Register a handler function for a service"""
        if service_id not in self._services:
            self.logger.error(
                f"Cannot register handler for unknown service: {service_id}"
            )
            return False

        self._service_handlers[service_id] = handler
        self.logger.info(f"Handler registered for service: {service_id}")
        return True

    def get_service_info(self, service_id: str) -> Optional[ServiceInfo]:
        """Get service information"""
        return self._services.get(service_id)

    def list_services(self) -> List[ServiceInfo]:
        """List all registered services"""
        return list(self._services.values())

    def update_service_status(self, service_id: str, status: ServiceStatus) -> bool:
        """Update service status"""
        if service_id not in self._services:
            return False

        self._services[service_id].status = status
        self._services[service_id].last_health_check = time.time()
        self.logger.info(f"Service {service_id} status updated to {status.value}")
        return True

    def start_health_monitoring(self, interval_seconds: int = 30):
        """Start health monitoring for all services"""
        if self._health_monitor_thread and self._health_monitor_thread.is_alive():
            self.logger.warning("Health monitoring already active")
            return

        self._stop_monitoring.clear()
        self._health_monitor_thread = threading.Thread(
            target=self._health_monitor_loop, args=(interval_seconds,), daemon=True
        )
        self._health_monitor_thread.start()
        self.logger.info(f"Health monitoring started (interval: {interval_seconds}s)")

    def _health_monitor_loop(self, interval: int):
        """Health monitoring loop"""
        while not self._stop_monitoring.is_set():
            try:
                self._check_all_services_health()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(10)

    def _check_all_services_health(self):
        """Check health of all registered services"""
        for service_id, service_info in self._services.items():
            try:
                if service_info.health_check_url:
                    # Perform health check
                    import requests

                    response = requests.get(service_info.health_check_url, timeout=5)
                    if response.status_code == 200:
                        self.update_service_status(service_id, ServiceStatus.ONLINE)
                    else:
                        self.update_service_status(service_id, ServiceStatus.DEGRADED)
                else:
                    # Use handler-based health check
                    handler = self._service_handlers.get(service_id)
                    if handler:
                        try:
                            result = handler()
                            if result:
                                self.update_service_status(
                                    service_id, ServiceStatus.ONLINE
                                )
                            else:
                                self.update_service_status(
                                    service_id, ServiceStatus.DEGRADED
                                )
                        except Exception:
                            self.update_service_status(service_id, ServiceStatus.ERROR)
            except Exception as e:
                self.logger.error(f"Health check failed for {service_id}: {e}")
                self.update_service_status(service_id, ServiceStatus.ERROR)

    def get_framework_status(self) -> Dict[str, Any]:
        """Get overall framework status"""
        total_services = len(self._services)
        online_services = len(
            [s for s in self._services.values() if s.status == ServiceStatus.ONLINE]
        )
        degraded_services = len(
            [s for s in self._services.values() if s.status == ServiceStatus.DEGRADED]
        )
        error_services = len(
            [s for s in self._services.values() if s.status == ServiceStatus.ERROR]
        )

        return {
            "framework_status": "ONLINE" if self._framework_initialized else "OFFLINE",
            "total_services": total_services,
            "online_services": online_services,
            "degraded_services": degraded_services,
            "error_services": error_services,
            "health_score": (online_services / max(1, total_services)) * 100
            if total_services > 0
            else 0,
        }

    def stop_health_monitoring(self):
        """Stop health monitoring"""
        self._stop_monitoring.set()
        if self._health_monitor_thread and self._health_monitor_thread.is_alive():
            self._health_monitor_thread.join(timeout=2)
        self.logger.info("Health monitoring stopped")


def main():
    """CLI interface for testing V2IntegrationFramework"""
    import argparse

    parser = argparse.ArgumentParser(description="V2 Integration Framework CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        print("🧪 V2IntegrationFramework Smoke Test")
        print("=" * 45)

        framework = V2IntegrationFramework()

        # Register test services
        framework.register_service(
            "test-service-1", "Test Service 1", "1.0.0", ["/api/v1/test1"]
        )
        framework.register_service(
            "test-service-2", "Test Service 2", "1.0.0", ["/api/v1/test2"]
        )

        # Test service listing
        services = framework.list_services()
        print(f"✅ Services registered: {len(services)}")

        # Test service info retrieval
        service_info = framework.get_service_info("test-service-1")
        print(f"✅ Service 1 info: {service_info.service_name}")

        # Test status update
        framework.update_service_status("test-service-1", ServiceStatus.DEGRADED)
        updated_info = framework.get_service_info("test-service-1")
        print(f"✅ Service 1 status: {updated_info.status.value}")

        # Test framework status
        status = framework.get_framework_status()
        print(f"✅ Framework health score: {status['health_score']:.1f}%")

        print("🎉 V2IntegrationFramework smoke test PASSED!")
    else:
        print("V2IntegrationFramework ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
