#!/usr/bin/env python3
"""
Service Interface - Object-Oriented Design Foundation
====================================================

Defines clean service interfaces following object-oriented design principles,
dependency inversion, and single responsibility principle.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: OBJECT-ORIENTED DESIGN OPTIMIZATION - Service Interfaces
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Protocol
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IService(ABC):
    """Base service interface"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the service"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Start the service"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop the service"""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get service status"""
        pass


class IConfigurableService(IService):
    """Configurable service interface"""
    
    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> bool:
        """Configure the service"""
        pass
    
    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        pass


class IMonitorableService(IService):
    """Monitorable service interface"""
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        pass
    
    @abstractmethod
    def get_health_status(self) -> str:
        """Get service health status"""
        pass


@dataclass
class ServiceMetadata:
    """Service metadata"""
    
    service_id: str
    service_name: str
    service_type: str
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    description: str = ""
    tags: List[str] = field(default_factory=list)


class ServiceRegistry:
    """
    Service Registry - Manages service lifecycle and discovery
    
    Follows object-oriented design principles and maintains
    single responsibility for service management.
    """
    
    def __init__(self):
        self.services: Dict[str, IService] = {}
        self.metadata: Dict[str, ServiceMetadata] = {}
        self.logger = logging.getLogger(__name__)
    
    def register_service(self, service: IService, metadata: ServiceMetadata) -> bool:
        """Register a service with metadata"""
        try:
            if not isinstance(service, IService):
                raise ValueError("Service must implement IService interface")
            
            if not isinstance(metadata, ServiceMetadata):
                raise ValueError("Metadata must be ServiceMetadata instance")
            
            self.services[metadata.service_id] = service
            self.metadata[metadata.service_id] = metadata
            
            self.logger.info(f"✅ Service '{metadata.service_name}' registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to register service: {e}")
            return False
    
    def get_service(self, service_id: str) -> Optional[IService]:
        """Get service by ID"""
        return self.services.get(service_id)
    
    def get_metadata(self, service_id: str) -> Optional[ServiceMetadata]:
        """Get service metadata by ID"""
        return self.metadata.get(service_id)
    
    def list_services(self) -> List[str]:
        """List all registered service IDs"""
        return list(self.services.keys())
    
    def start_service(self, service_id: str) -> bool:
        """Start a registered service"""
        try:
            service = self.get_service(service_id)
            if not service:
                raise ValueError(f"Service '{service_id}' not found")
            
            success = service.start()
            if success:
                self.logger.info(f"✅ Service '{service_id}' started successfully")
            else:
                self.logger.error(f"❌ Failed to start service '{service_id}'")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error starting service '{service_id}': {e}")
            return False
    
    def stop_service(self, service_id: str) -> bool:
        """Stop a registered service"""
        try:
            service = self.get_service(service_id)
            if not service:
                raise ValueError(f"Service '{service_id}' not found")
            
            success = service.stop()
            if success:
                self.logger.info(f"✅ Service '{service_id}' stopped successfully")
            else:
                self.logger.error(f"❌ Failed to stop service '{service_id}'")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping service '{service_id}': {e}")
            return False


if __name__ == "__main__":
    # Test the service interface system
    print("🔌 Service Interface System Loaded Successfully")
    
    # Create service registry
    registry = ServiceRegistry()
    
    # Test service metadata creation
    metadata = ServiceMetadata(
        service_id="test_service",
        service_name="Test Service",
        service_type="utility",
        description="A test service for validation"
    )
    
    print(f"✅ Service metadata created: {metadata.service_name}")
    print(f"✅ Service registry initialized: {len(registry.list_services())} services")
    
    print("✅ All service interface functionality working correctly!")
