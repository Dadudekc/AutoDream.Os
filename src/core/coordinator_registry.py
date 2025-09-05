#!/usr/bin/env python3
"""
Coordinator Registry - V2 Compliant
=================================

Registry for managing all unified coordinators.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: Centralized coordinator management
"""

from typing import Any, Dict, Optional
from .coordinator_interfaces import ICoordinatorRegistry, ICoordinatorLogger
from .coordinator_models import CoordinationStatus


class CoordinatorRegistry(ICoordinatorRegistry):
    """Registry for managing all unified coordinators."""
    
    def __init__(self, logger: ICoordinatorLogger):
        self.coordinators: Dict[str, Any] = {}
        self.logger = logger
    
    def register_coordinator(self, coordinator: Any) -> bool:
        """Register a coordinator instance."""
        try:
            if not hasattr(coordinator, 'name'):
                self.logger.error("Coordinator must have a 'name' attribute")
                return False
            
            if coordinator.name in self.coordinators:
                self.logger.warning(f"Coordinator {coordinator.name} already registered, replacing")
            
            self.coordinators[coordinator.name] = coordinator
            self.logger.info(f"Coordinator {coordinator.name} registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register coordinator: {e}")
            return False
    
    def get_coordinator(self, name: str) -> Optional[Any]:
        """Get coordinator by name."""
        return self.coordinators.get(name)
    
    def get_all_coordinators(self) -> Dict[str, Any]:
        """Get all registered coordinators."""
        return self.coordinators.copy()
    
    def unregister_coordinator(self, name: str) -> bool:
        """Unregister a coordinator."""
        try:
            if name in self.coordinators:
                coordinator = self.coordinators[name]
                
                # Shutdown coordinator if it has shutdown method
                if hasattr(coordinator, 'shutdown'):
                    coordinator.shutdown()
                
                del self.coordinators[name]
                self.logger.info(f"Coordinator {name} unregistered successfully")
                return True
            else:
                self.logger.warning(f"Coordinator {name} not found for unregistration")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to unregister coordinator {name}: {e}")
            return False
    
    def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all coordinators."""
        statuses = {}
        
        for name, coordinator in self.coordinators.items():
            try:
                if hasattr(coordinator, 'get_status'):
                    status = coordinator.get_status()
                    if hasattr(status, 'to_dict'):
                        statuses[name] = status.to_dict()
                    else:
                        statuses[name] = status
                else:
                    statuses[name] = {
                        "name": name,
                        "status": "unknown",
                        "error": "No get_status method available"
                    }
            except Exception as e:
                statuses[name] = {
                    "name": name,
                    "status": "error",
                    "error": str(e)
                }
        
        return statuses
    
    def shutdown_all_coordinators(self) -> None:
        """Shutdown all registered coordinators."""
        for name, coordinator in self.coordinators.items():
            try:
                if hasattr(coordinator, 'shutdown'):
                    coordinator.shutdown()
                    self.logger.info(f"Coordinator {name} shut down successfully")
                else:
                    self.logger.warning(f"Coordinator {name} has no shutdown method")
            except Exception as e:
                self.logger.error(f"Error shutting down coordinator {name}: {e}")
    
    def get_coordinator_count(self) -> int:
        """Get total number of registered coordinators."""
        return len(self.coordinators)
    
    def get_coordinators_by_status(self, status: str) -> Dict[str, Any]:
        """Get coordinators by status."""
        filtered = {}
        
        for name, coordinator in self.coordinators.items():
            try:
                if hasattr(coordinator, 'get_status'):
                    coord_status = coordinator.get_status()
                    if hasattr(coord_status, 'coordination_status'):
                        if coord_status.coordination_status.value == status:
                            filtered[name] = coordinator
                    elif isinstance(coord_status, dict) and coord_status.get('coordination_status') == status:
                        filtered[name] = coordinator
            except Exception:
                continue
        
        return filtered
    
    def clear_all_coordinators(self) -> None:
        """Clear all coordinators from registry."""
        self.shutdown_all_coordinators()
        self.coordinators.clear()
        self.logger.info("All coordinators cleared from registry")


# Global registry instance
_global_registry: Optional[CoordinatorRegistry] = None


def get_global_registry(logger: ICoordinatorLogger) -> CoordinatorRegistry:
    """Get global coordinator registry instance."""
    global _global_registry
    if _global_registry is None:
        _global_registry = CoordinatorRegistry(logger)
    return _global_registry


def register_coordinator(coordinator: Any, logger: ICoordinatorLogger) -> bool:
    """Register a coordinator with the global registry."""
    registry = get_global_registry(logger)
    return registry.register_coordinator(coordinator)


def get_coordinator(name: str, logger: ICoordinatorLogger) -> Optional[Any]:
    """Get a coordinator by name from the global registry."""
    registry = get_global_registry(logger)
    return registry.get_coordinator(name)


def get_all_coordinators(logger: ICoordinatorLogger) -> Dict[str, Any]:
    """Get all coordinators from the global registry."""
    registry = get_global_registry(logger)
    return registry.get_all_coordinators()


def get_all_coordinator_statuses(logger: ICoordinatorLogger) -> Dict[str, Dict[str, Any]]:
    """Get status of all coordinators from the global registry."""
    registry = get_global_registry(logger)
    return registry.get_coordinator_statuses()


def shutdown_all_coordinators(logger: ICoordinatorLogger) -> None:
    """Shutdown all coordinators in the global registry."""
    registry = get_global_registry(logger)
    registry.shutdown_all_coordinators()
