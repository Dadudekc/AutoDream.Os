#!/usr/bin/env python3
"""
Unified Service Base Class - V2 Compliant
==========================================

This module provides a unified service base class that consolidates all service
patterns into a single, V2 compliant architecture.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate 50+ service classes into unified architecture
"""

from ..core.unified_import_system import logging


class UnifiedServiceBase:
    """
    Unified Service Base Class - V2 Compliant
    
    Consolidates all service patterns into single base class:
    - 50+ service classes across the codebase
    - Unified initialization pattern
    - Unified configuration management
    - Unified logging integration
    - Unified error handling
    - Unified status reporting
    """

    def __init__(self, name: str, config: Optional[Dict] = None):
        """
        Initialize unified service.
        
        Args:
            name: Service name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = self._get_unified_logger()
        self._initialized = False
        self.start_time = datetime.now()
        self.operations_count = 0
        self.error_count = 0
        self._initialize()

    def _initialize(self):
        """Unified initialization pattern for all services."""
        try:
            self.get_logger(__name__).info(f"Service {self.name} initializing")
            
            # Load configuration
            self._load_configuration()
            
            # Initialize components
            self._initialize_components()
            
            # Validate initialization
            self._validate_initialization()
            
            self._initialized = True
            self.get_logger(__name__).info(f"Service {self.name} initialized successfully")
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Service {self.name} initialization failed: {e}")
            raise

    def _get_unified_logger(self):
        """Get unified logger instance."""
        try:
            # Try to import unified logging system
            return get_unified_logger()
        except ImportError:
            # Fallback to standard logging
            return logging.getLogger(f"UnifiedService.{self.name}")

    def _load_configuration(self):
        """Load service configuration."""
        try:
            # Load from unified configuration system
            
            unified_config = get_unified_config()
            
            # Merge with provided config
            if unified_config:
                self.config.update(unified_config.get_service_config(self.name))
                
        except ImportError:
            # Fallback to basic config
            self.get_logger(__name__).warning(
                f"Unified configuration system not available for {self.name}"
            )

    def _initialize_components(self):
        """Initialize service-specific components."""
        # Override in subclasses for specific initialization
        pass

    def _validate_initialization(self):
        """Validate service initialization."""
        if not self.name:
            get_unified_validator().raise_validation_error("Service name is required")
        
        if not get_unified_validator().validate_type(self.config, dict):
            get_unified_validator().raise_validation_error("Service config must be a dictionary")

    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        return self._initialized

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive service status.
        
        Returns:
            Dict[str, Any]: Service status information
        """
        return {
            "name": self.name,
            "initialized": self._initialized,
            "config": self.config,
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "operations_count": self.operations_count,
            "error_count": self.error_count,
            "success_rate": self._calculate_success_rate(),
            "status": "OPERATIONAL" if self._initialized else "INITIALIZING",
        }

    def _calculate_success_rate(self) -> float:
        """Calculate service success rate."""
        if self.operations_count == 0:
            return 100.0
        
        successful_operations = self.operations_count - self.error_count
        return (successful_operations / self.operations_count) * 100.0

    def execute_operation(
        self, operation_name: str, operation_func: Callable, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute operation with unified error handling and logging.
        
        Args:
            operation_name: Name of the operation
            operation_func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Dict[str, Any]: Operation result
        """
        self.operations_count += 1
        
        try:
            self.get_logger(__name__).info(f"Executing operation: {operation_name}")
            
            # Execute the operation
            result = operation_func(*args, **kwargs)
            
            self.get_logger(__name__).info(f"Operation {operation_name} completed successfully")
            
            return {
                "success": True,
                "operation": operation_name,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "service": self.name,
            }
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Operation {operation_name} failed: {e}")
            
            return {
                "success": False,
                "operation": operation_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "service": self.name,
            }

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with fallback.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value or default
        """
        return self.config.get(key, default)

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update service configuration.
        
        Args:
            updates: Configuration updates
            
        Returns:
            bool: True if update successful
        """
        try:
            self.config.update(updates)
            self.get_logger(__name__).info(f"Configuration updated for {self.name}")
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"Configuration update failed for {self.name}: {e}")
            return False

    def reset_statistics(self):
        """Reset service statistics."""
        self.operations_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        self.get_logger(__name__).info(f"Statistics reset for {self.name}")

    def shutdown(self):
        """Shutdown service gracefully."""
        try:
            self.get_logger(__name__).info(f"Shutting down service {self.name}")
            
            # Perform cleanup operations
            self._cleanup()
            
            self._initialized = False
            self.get_logger(__name__).info(f"Service {self.name} shut down successfully")
            
        except Exception as e:
            self.get_logger(__name__).error(f"Error during shutdown of {self.name}: {e}")

    def _cleanup(self):
        """Perform cleanup operations."""
        # Override in subclasses for specific cleanup
        pass

    def __str__(self) -> str:
        """String representation of service."""
        return f"UnifiedService({self.name}, initialized={self._initialized})"

    def __repr__(self) -> str:
        """Detailed representation of service."""
        return f"UnifiedService(name='{self.name}', initialized={self._initialized}, operations={self.operations_count}, errors={self.error_count})"


class ServiceRegistry:
    """
    Registry for managing all unified services.
    
    Provides centralized management of all service instances.
    """

    def __init__(self):
        self.services: Dict[str, UnifiedServiceBase] = {}
        self.logger = logging.getLogger("ServiceRegistry")

    def register_service(self, service: UnifiedServiceBase) -> bool:
        """
        Register a service instance.
        
        Args:
            service: Service instance to register
            
        Returns:
            bool: True if registration successful
        """
        try:
            if service.name in self.services:
                self.get_logger(__name__).warning(
                    f"Service {service.name} already registered, replacing"
                )
            
            self.services[service.name] = service
            self.get_logger(__name__).info(f"Service {service.name} registered successfully")
            return True
            
        except Exception as e:
            self.get_logger(__name__).error(f"Failed to register service {service.name}: {e}")
            return False

    def get_service(self, name: str) -> Optional[UnifiedServiceBase]:
        """
        Get service by name.
        
        Args:
            name: Service name
            
        Returns:
            Optional[UnifiedServiceBase]: Service instance or None
        """
        return self.services.get(name)

    def get_all_services(self) -> Dict[str, UnifiedServiceBase]:
        """
        Get all registered services.
        
        Returns:
            Dict[str, UnifiedServiceBase]: All services
        """
        return self.services.copy()

    def get_service_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all services.
        
        Returns:
            Dict[str, Dict[str, Any]]: Status of all services
        """
        return {name: service.get_status() for name, service in self.services.items()}

    def shutdown_all_services(self):
        """Shutdown all registered services."""
        for name, service in self.services.items():
            try:
                service.shutdown()
            except Exception as e:
                self.get_logger(__name__).error(f"Error shutting down service {name}: {e}")


# Global service registry instance
_service_registry = None


def get_service_registry() -> ServiceRegistry:
    """Get global service registry instance."""
    global _service_registry
    if _service_registry is None:
        _service_registry = ServiceRegistry()
    return _service_registry


def register_service(service: UnifiedServiceBase) -> bool:
    """Register a service with the global registry."""
    return get_service_registry().register_service(service)


def get_service(name: str) -> Optional[UnifiedServiceBase]:
    """Get a service by name from the global registry."""
    return get_service_registry().get_service(name)


def get_all_services() -> Dict[str, UnifiedServiceBase]:
    """Get all services from the global registry."""
    return get_service_registry().get_all_services()


def get_all_service_statuses() -> Dict[str, Dict[str, Any]]:
    """Get status of all services from the global registry."""
    return get_service_registry().get_service_statuses()
