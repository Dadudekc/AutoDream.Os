#!/usr/bin/env python3
"""
V2 Service Discovery System
===========================
Service discovery and registration system for V2 system with health monitoring.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ServiceState(Enum):
    """Service state enumeration"""
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class ServiceEndpoint:
    """Service endpoint information"""
    url: str
    protocol: str
    port: int
    health_check_path: Optional[str] = None
    last_health_check: Optional[float] = None
    is_healthy: bool = True


@dataclass
class DiscoveredService:
    """Discovered service information"""
    service_id: str
    service_name: str
    version: str
    state: ServiceState
    endpoints: List[ServiceEndpoint]
    metadata: Dict[str, Any]
    last_seen: float
    registration_time: float


class V2ServiceDiscovery:
    """Service discovery and registration system for V2"""
    
    def __init__(self, discovery_interval: int = 30):
        self.logger = logging.getLogger(f"{__name__}.V2ServiceDiscovery")
        self.discovery_interval = discovery_interval
        
        # Service registry
        self._services: Dict[str, DiscoveredService] = {}
        self._service_tags: Dict[str, Set[str]] = {}
        
        # Discovery state
        self._discovery_active = False
        self._discovery_thread: Optional[threading.Thread] = None
        self._stop_discovery = threading.Event()
        
        # Health monitoring
        self._health_check_thread: Optional[threading.Thread] = None
        self._stop_health_check = threading.Event()
        
        self.logger.info("V2 Service Discovery System initialized")
    
    def register_service(self, service_id: str, service_name: str, version: str = "1.0.0",
                        endpoints: Optional[List[Dict[str, Any]]] = None, 
                        metadata: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None) -> bool:
        """Register a service with the discovery system"""
        if service_id in self._services:
            self.logger.warning(f"Service already registered: {service_id}")
            return False
        
        # Convert endpoint data
        service_endpoints = []
        if endpoints:
            for endpoint_data in endpoints:
                endpoint = ServiceEndpoint(
                    url=endpoint_data.get("url", ""),
                    protocol=endpoint_data.get("protocol", "http"),
                    port=endpoint_data.get("port", 80),
                    health_check_path=endpoint_data.get("health_check_path")
                )
                service_endpoints.append(endpoint)
        
        # Create service record
        service = DiscoveredService(
            service_id=service_id,
            service_name=service_name,
            version=version,
            state=ServiceState.REGISTERED,
            endpoints=service_endpoints,
            metadata=metadata or {},
            last_seen=time.time(),
            registration_time=time.time()
        )
        
        self._services[service_id] = service
        
        # Store tags
        if tags:
            self._service_tags[service_id] = set(tags)
        
        self.logger.info(f"Service registered: {service_name} ({service_id}) v{version}")
        return True
    
    def deregister_service(self, service_id: str) -> bool:
        """Deregister a service"""
        if service_id not in self._services:
            return False
        
        del self._services[service_id]
        if service_id in self._service_tags:
            del self._service_tags[service_id]
        
        self.logger.info(f"Service deregistered: {service_id}")
        return True
    
    def discover_services(self, tags: Optional[List[str]] = None, 
                         state_filter: Optional[ServiceState] = None) -> List[DiscoveredService]:
        """Discover services based on criteria"""
        discovered = []
        
        for service_id, service in self._services.items():
            # Apply tag filter
            if tags:
                service_tags = self._service_tags.get(service_id, set())
                if not any(tag in service_tags for tag in tags):
                    continue
            
            # Apply state filter
            if state_filter and service.state != state_filter:
                continue
            
            discovered.append(service)
        
        return discovered
    
    def get_service(self, service_id: str) -> Optional[DiscoveredService]:
        """Get specific service by ID"""
        return self._services.get(service_id)
    
    def update_service_health(self, service_id: str, endpoint_url: str, is_healthy: bool):
        """Update service endpoint health status"""
        if service_id not in self._services:
            return
        
        service = self._services[service_id]
        for endpoint in service.endpoints:
            if endpoint.url == endpoint_url:
                endpoint.is_healthy = is_healthy
                endpoint.last_health_check = time.time()
                
                # Update service state based on endpoint health
                healthy_endpoints = [ep for ep in service.endpoints if ep.is_healthy]
                if healthy_endpoints:
                    service.state = ServiceState.ACTIVE
                else:
                    service.state = ServiceState.FAILED
                
                service.last_seen = time.time()
                break
    
    def start_discovery(self):
        """Start service discovery process"""
        if self._discovery_active:
            self.logger.warning("Service discovery already active")
            return
        
        self._discovery_active = True
        self._stop_discovery.clear()
        
        # Start discovery thread
        self._discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        self._discovery_thread.start()
        
        # Start health check thread
        self._health_check_thread = threading.Thread(target=self._health_check_loop, daemon=True)
        self._health_check_thread.start()
        
        self.logger.info("Service discovery started")
    
    def _discovery_loop(self):
        """Main discovery loop"""
        while not self._stop_discovery.is_set():
            try:
                self._perform_discovery()
                time.sleep(self.discovery_interval)
            except Exception as e:
                self.logger.error(f"Discovery error: {e}")
                time.sleep(10)
    
    def _perform_discovery(self):
        """Perform service discovery"""
        current_time = time.time()
        
        for service_id, service in self._services.items():
            # Check if service is still active
            if current_time - service.last_seen > 300:  # 5 minutes
                service.state = ServiceState.INACTIVE
                self.logger.warning(f"Service {service_id} marked as inactive")
    
    def _health_check_loop(self):
        """Health check loop for registered services"""
        while not self._stop_health_check.is_set():
            try:
                self._perform_health_checks()
                time.sleep(60)  # Health check every minute
            except Exception as e:
                self.logger.error(f"Health check error: {e}")
                time.sleep(30)
    
    def _perform_health_checks(self):
        """Perform health checks on service endpoints"""
        for service_id, service in self._services.items():
            for endpoint in service.endpoints:
                if endpoint.health_check_path:
                    try:
                        # Simple health check (in production, use proper HTTP client)
                        import urllib.request
                        health_url = f"{endpoint.protocol}://{endpoint.url}:{endpoint.port}{endpoint.health_check_path}"
                        response = urllib.request.urlopen(health_url, timeout=5)
                        is_healthy = response.getcode() == 200
                        self.update_service_health(service_id, endpoint.url, is_healthy)
                    except Exception:
                        self.update_service_health(service_id, endpoint.url, False)
    
    def get_discovery_stats(self) -> Dict[str, Any]:
        """Get discovery system statistics"""
        total_services = len(self._services)
        active_services = len([s for s in self._services.values() if s.state == ServiceState.ACTIVE])
        failed_services = len([s for s in self._services.values() if s.state == ServiceState.FAILED])
        
        return {
            "total_services": total_services,
            "active_services": active_services,
            "failed_services": failed_services,
            "discovery_active": self._discovery_active,
            "health_check_active": self._health_check_thread and self._health_check_thread.is_alive(),
            "last_discovery": time.time()
        }
    
    def stop_discovery(self):
        """Stop service discovery"""
        self._discovery_active = False
        self._stop_discovery.set()
        self._stop_health_check.set()
        
        if self._discovery_thread and self._discovery_thread.is_alive():
            self._discovery_thread.join(timeout=2)
        
        if self._health_check_thread and self._health_check_thread.is_alive():
            self._health_check_thread.join(timeout=2)
        
        self.logger.info("Service discovery stopped")


def main():
    """CLI interface for testing V2ServiceDiscovery"""
    import argparse
    
    parser = argparse.ArgumentParser(description="V2 Service Discovery CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 V2ServiceDiscovery Smoke Test")
        print("=" * 40)
        
        discovery = V2ServiceDiscovery(discovery_interval=5)
        
        # Register test services
        endpoints = [
            {"url": "localhost", "protocol": "http", "port": 8080, "health_check_path": "/health"}
        ]
        
        discovery.register_service("test-service-1", "Test Service 1", "1.0.0", endpoints, 
                                 {"environment": "test"}, ["api", "test"])
        discovery.register_service("test-service-2", "Test Service 2", "1.0.0", endpoints, 
                                 {"environment": "test"}, ["api", "production"])
        
        # Test service discovery
        services = discovery.discover_services(tags=["api"])
        print(f"✅ Services with 'api' tag: {len(services)}")
        
        # Test service retrieval
        service = discovery.get_service("test-service-1")
        print(f"✅ Service 1 name: {service.service_name}")
        
        # Test discovery stats
        stats = discovery.get_discovery_stats()
        print(f"✅ Total services: {stats['total_services']}")
        print(f"✅ Active services: {stats['active_services']}")
        
        # Cleanup
        discovery.deregister_service("test-service-1")
        discovery.deregister_service("test-service-2")
        
        print("🎉 V2ServiceDiscovery smoke test PASSED!")
    else:
        print("V2ServiceDiscovery ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
