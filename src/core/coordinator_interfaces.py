#!/usr/bin/env python3
"""
Coordinator Interfaces - V2 Compliant
====================================

Interfaces and abstract base classes for the unified coordinator system.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: Define contracts for coordinator components
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from .coordinator_models import CoordinationTarget, CoordinationResult, CoordinatorStatus


class ICoordinatorTargetManager(ABC):
    """Interface for managing coordination targets."""
    
    @abstractmethod
    def add_target(self, target: CoordinationTarget) -> bool:
        """Add a coordination target."""
        pass
    
    @abstractmethod
    def get_target(self, target_id: str) -> Optional[CoordinationTarget]:
        """Get coordination target by ID."""
        pass
    
    @abstractmethod
    def update_target(self, target: CoordinationTarget) -> bool:
        """Update coordination target."""
        pass
    
    @abstractmethod
    def remove_target(self, target_id: str) -> bool:
        """Remove coordination target."""
        pass
    
    @abstractmethod
    def get_targets_by_type(self, target_type: str) -> List[CoordinationTarget]:
        """Get targets by type."""
        pass
    
    @abstractmethod
    def get_targets_by_priority(self, min_priority: int) -> List[CoordinationTarget]:
        """Get targets by minimum priority."""
        pass
    
    @abstractmethod
    def get_all_targets(self) -> List[CoordinationTarget]:
        """Get all targets."""
        pass
    
    @abstractmethod
    def get_targets_count(self) -> int:
        """Get total targets count."""
        pass


class ICoordinatorOperationEngine(ABC):
    """Interface for coordination operation execution."""
    
    @abstractmethod
    def execute_operation(
        self, 
        operation_name: str, 
        operation_func: Callable, 
        *args, 
        **kwargs
    ) -> CoordinationResult:
        """Execute coordination operation."""
        pass
    
    @abstractmethod
    def execute_with_retry(
        self, 
        operation_name: str, 
        operation_func: Callable, 
        max_retries: int = 3,
        *args, 
        **kwargs
    ) -> CoordinationResult:
        """Execute operation with retry logic."""
        pass
    
    @abstractmethod
    def execute_batch(
        self, 
        operations: List[Dict[str, Any]]
    ) -> List[CoordinationResult]:
        """Execute multiple operations in batch."""
        pass


class ICoordinatorStatusTracker(ABC):
    """Interface for coordinator status tracking."""
    
    @abstractmethod
    def get_status(self) -> CoordinatorStatus:
        """Get comprehensive coordinator status."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Get coordinator metrics."""
        pass
    
    @abstractmethod
    def reset_statistics(self) -> None:
        """Reset coordinator statistics."""
        pass
    
    @abstractmethod
    def update_operation_count(self) -> None:
        """Update operation count."""
        pass
    
    @abstractmethod
    def update_error_count(self) -> None:
        """Update error count."""
        pass


class ICoordinatorConfigManager(ABC):
    """Interface for coordinator configuration management."""
    
    @abstractmethod
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        pass
    
    @abstractmethod
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate configuration."""
        pass
    
    @abstractmethod
    def reload_config(self) -> bool:
        """Reload configuration from source."""
        pass


class ICoordinatorLifecycle(ABC):
    """Interface for coordinator lifecycle management."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize coordinator."""
        pass
    
    @abstractmethod
    def is_initialized(self) -> bool:
        """Check if coordinator is initialized."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown coordinator gracefully."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Perform cleanup operations."""
        pass


class ICoordinatorLogger(ABC):
    """Interface for coordinator logging."""
    
    @abstractmethod
    def info(self, message: str) -> None:
        """Log info message."""
        pass
    
    @abstractmethod
    def warning(self, message: str) -> None:
        """Log warning message."""
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        """Log error message."""
        pass
    
    @abstractmethod
    def debug(self, message: str) -> None:
        """Log debug message."""
        pass


class ICoordinatorRegistry(ABC):
    """Interface for coordinator registry management."""
    
    @abstractmethod
    def register_coordinator(self, coordinator: Any) -> bool:
        """Register a coordinator."""
        pass
    
    @abstractmethod
    def get_coordinator(self, name: str) -> Optional[Any]:
        """Get coordinator by name."""
        pass
    
    @abstractmethod
    def get_all_coordinators(self) -> Dict[str, Any]:
        """Get all coordinators."""
        pass
    
    @abstractmethod
    def unregister_coordinator(self, name: str) -> bool:
        """Unregister a coordinator."""
        pass
    
    @abstractmethod
    def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all coordinators."""
        pass
