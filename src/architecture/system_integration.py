"""
System Integration - V2 Compliant (Simplified)
==============================================

Core system integration with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import threading

logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Integration type enumeration."""
    API = "api"
    DATABASE = "database"
    MESSAGING = "messaging"
    FILE_SYSTEM = "file_system"
    EXTERNAL_SERVICE = "external_service"


class IntegrationStatus(Enum):
    """Integration status enumeration."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class IntegrationConfig:
    """Configuration for system integrations."""
    integration_type: IntegrationType
    name: str
    endpoint: str
    timeout: int = 30
    retry_attempts: int = 3
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrationMetrics:
    """Metrics for integration performance."""
    connection_count: int = 0
    success_count: int = 0
    error_count: int = 0
    last_connection: Optional[datetime] = None
    last_error: Optional[str] = None


class ServiceRegistry:
    """Simple service registry for system integration."""
    
    def __init__(self):
        self._services: Dict[str, IntegrationConfig] = {}
        self._instances: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def register_service(self, config: IntegrationConfig) -> None:
        """Register a service."""
        with self._lock:
            self._services[config.name] = config
            logger.debug(f"Service registered: {config.name}")
    
    def unregister_service(self, name: str) -> None:
        """Unregister a service."""
        with self._lock:
            if name in self._services:
                del self._services[name]
                if name in self._instances:
                    del self._instances[name]
                logger.debug(f"Service unregistered: {name}")
    
    def get_service(self, name: str) -> Optional[IntegrationConfig]:
        """Get a service configuration."""
        return self._services.get(name)
    
    def get_all_services(self) -> Dict[str, IntegrationConfig]:
        """Get all service configurations."""
        return self._services.copy()
    
    def get_services_by_type(self, integration_type: IntegrationType) -> Dict[str, IntegrationConfig]:
        """Get services by type."""
        return {name: config for name, config in self._services.items() 
                if config.integration_type == integration_type}
    
    def is_service_registered(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services


class EventBus:
    """Simple event bus for system integration."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)
            logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        with self._lock:
            if event_type in self._subscribers:
                if handler in self._subscribers[event_type]:
                    self._subscribers[event_type].remove(handler)
                    logger.debug(f"Unsubscribed from event: {event_type}")
    
    def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event."""
        with self._lock:
            if event_type in self._subscribers:
                for handler in self._subscribers[event_type]:
                    try:
                        handler(event_type, data)
                        logger.debug(f"Event published: {event_type}")
                    except Exception as e:
                        logger.error(f"Error publishing event {event_type}: {e}")
    
    def get_subscriber_count(self, event_type: str) -> int:
        """Get the number of subscribers for an event type."""
        return len(self._subscribers.get(event_type, []))


class IntegrationManager:
    """Manager for system integrations."""
    
    def __init__(self):
        self._integrations: Dict[str, IntegrationConfig] = {}
        self._metrics: Dict[str, IntegrationMetrics] = {}
        self._status: Dict[str, IntegrationStatus] = {}
        self._lock = threading.Lock()
    
    def add_integration(self, config: IntegrationConfig) -> None:
        """Add an integration."""
        with self._lock:
            self._integrations[config.name] = config
            self._metrics[config.name] = IntegrationMetrics()
            self._status[config.name] = IntegrationStatus.DISCONNECTED
            logger.debug(f"Integration added: {config.name}")
    
    def remove_integration(self, name: str) -> None:
        """Remove an integration."""
        with self._lock:
            if name in self._integrations:
                del self._integrations[name]
                if name in self._metrics:
                    del self._metrics[name]
                if name in self._status:
                    del self._status[name]
                logger.debug(f"Integration removed: {name}")
    
    def get_integration(self, name: str) -> Optional[IntegrationConfig]:
        """Get an integration configuration."""
        return self._integrations.get(name)
    
    def get_integration_status(self, name: str) -> Optional[IntegrationStatus]:
        """Get the status of an integration."""
        return self._status.get(name)
    
    def set_integration_status(self, name: str, status: IntegrationStatus) -> None:
        """Set the status of an integration."""
        with self._lock:
            if name in self._status:
                self._status[name] = status
                logger.debug(f"Integration {name} status set to: {status.value}")
    
    def get_integration_metrics(self, name: str) -> Optional[IntegrationMetrics]:
        """Get the metrics of an integration."""
        return self._metrics.get(name)
    
    def update_metrics(self, name: str, success: bool = True, error_message: str = None) -> None:
        """Update integration metrics."""
        with self._lock:
            if name in self._metrics:
                metrics = self._metrics[name]
                if success:
                    metrics.success_count += 1
                else:
                    metrics.error_count += 1
                    metrics.last_error = error_message
                
                metrics.last_connection = datetime.now()
                logger.debug(f"Metrics updated for integration: {name}")
    
    def get_all_integrations(self) -> Dict[str, IntegrationConfig]:
        """Get all integrations."""
        return self._integrations.copy()
    
    def get_integrations_by_type(self, integration_type: IntegrationType) -> Dict[str, IntegrationConfig]:
        """Get integrations by type."""
        return {name: config for name, config in self._integrations.items() 
                if config.integration_type == integration_type}
    
    def get_connected_integrations(self) -> List[str]:
        """Get list of connected integrations."""
        return [name for name, status in self._status.items() 
                if status == IntegrationStatus.CONNECTED]
    
    def get_error_integrations(self) -> List[str]:
        """Get list of integrations with errors."""
        return [name for name, status in self._status.items() 
                if status == IntegrationStatus.ERROR]


# Global instances
service_registry = ServiceRegistry()
event_bus = EventBus()
integration_manager = IntegrationManager()


def register_service(integration_type: IntegrationType, name: str, endpoint: str,
                    timeout: int = 30, retry_attempts: int = 3, enabled: bool = True,
                    config: Dict[str, Any] = None) -> None:
    """Convenience function to register a service."""
    service_config = IntegrationConfig(
        integration_type=integration_type,
        name=name,
        endpoint=endpoint,
        timeout=timeout,
        retry_attempts=retry_attempts,
        enabled=enabled,
        config=config or {}
    )
    service_registry.register_service(service_config)
    integration_manager.add_integration(service_config)


def get_service(name: str) -> Optional[IntegrationConfig]:
    """Convenience function to get a service."""
    return service_registry.get_service(name)


def publish_event(event_type: str, data: Any = None) -> None:
    """Convenience function to publish an event."""
    event_bus.publish(event_type, data)


def subscribe_to_event(event_type: str, handler: Callable) -> None:
    """Convenience function to subscribe to an event."""
    event_bus.subscribe(event_type, handler)
