#!/usr/bin/env python3
"""
Unified Coordinator Base Class - V2 Compliant
==============================================

This module provides a unified coordinator base class that consolidates all coordinator
patterns into a single, V2 compliant architecture.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate 30+ coordinator classes into unified architecture
"""

from ..core.unified_import_system import logging


@dataclass
class CoordinationTarget:
    """Represents a coordination target."""
    target_id: str
    target_type: str
    priority: int
    status: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class UnifiedCoordinatorBase:
    """
    Unified Coordinator Base Class - V2 Compliant
    
    Consolidates all coordinator patterns into single base class:
    - 30+ coordinator classes across the codebase
    - Unified initialization pattern
    - Unified target management
    - Unified coordination logic
    - Unified status tracking
    - Unified error handling
    """

    def __init__(self, name: str, config: Optional[Dict] = None):
        """
        Initialize unified coordinator.
        
        Args:
            name: Coordinator name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = self._get_unified_logger()
        self._initialized = False
        self.start_time = datetime.now()
        self.coordination_targets: List[CoordinationTarget] = []
        self.coordination_status = "initialized"
        self.operations_count = 0
        self.error_count = 0
        self._initialize()

    def _initialize(self):
        """Unified initialization pattern for all coordinators."""
        try:
            self.get_logger(__name__).info(f"Coordinator {self.name} initializing")
            
            # Load configuration
            self._load_configuration()
            
            # Initialize components
            self._initialize_components()
            
            # Validate initialization
            self._validate_initialization()
            
            self._initialized = True
            self.coordination_status = "operational"
            self.get_logger(__name__).info(f"Coordinator {self.name} initialized successfully")
            
        except Exception as e:
            self.error_count += 1
            self.coordination_status = "error"
            self.get_logger(__name__).error(f"Coordinator {self.name} initialization failed: {e}")
            raise

    def _get_unified_logger(self):
        """Get unified logger instance."""
        try:
            # Try to import unified logging system
            return get_unified_logger()
        except ImportError:
            # Fallback to standard logging
            return logging.getLogger(f"UnifiedCoordinator.{self.name}")

    def _load_configuration(self):
        """Load coordinator configuration."""
        try:
            # Load from unified configuration system
            
            unified_config = get_unified_config()
            
            # Merge with provided config
            if unified_config:
                self.config.update(unified_config.get_coordinator_config(self.name))
                
        except ImportError:
            # Fallback to basic config
            self.get_logger(__name__).warning(
                f"Unified configuration system not available for {self.name}"
            )

    def _initialize_components(self):
        """Initialize coordinator-specific components."""
        # Override in subclasses for specific initialization
        pass

    def _validate_initialization(self):
        """Validate coordinator initialization."""
        if not self.name:
            get_unified_validator().raise_validation_error("Coordinator name is required")
        
        if not get_unified_validator().validate_type(self.config, dict):
            get_unified_validator().raise_validation_error("Coordinator config must be a dictionary")

    def is_initialized(self) -> bool:
        """Check if coordinator is initialized."""
        return self._initialized

    def add_coordination_target(self, target: CoordinationTarget) -> bool:
        """
        Add a coordination target.
        
        Args:
            target: Coordination target to add
            
        Returns:
            bool: True if target added successfully
        """
        try:
            # Check if target already exists
            existing_target = self.get_coordination_target(target.target_id)
            if existing_target:
                self.get_logger(__name__).warning(f"Target {target.target_id} already exists, updating")
                self.update_coordination_target(target)
                return True
            
            self.coordination_targets.append(target)
            self.get_logger(__name__).info(f"Added coordination target: {target.target_id}")
            return True
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Failed to add coordination target {target.target_id}: {e}")
            return False

    def get_coordination_target(self, target_id: str) -> Optional[CoordinationTarget]:
        """
        Get coordination target by ID.
        
        Args:
            target_id: Target ID
            
        Returns:
            Optional[CoordinationTarget]: Target or None
        """
        for target in self.coordination_targets:
            if target.target_id == target_id:
                return target
        return None

    def update_coordination_target(self, target: CoordinationTarget) -> bool:
        """
        Update coordination target.
        
        Args:
            target: Updated target
            
        Returns:
            bool: True if update successful
        """
        try:
            for i, existing_target in enumerate(self.coordination_targets):
                if existing_target.target_id == target.target_id:
                    target.updated_at = datetime.now().isoformat()
                    self.coordination_targets[i] = target
                    self.get_logger(__name__).info(f"Updated coordination target: {target.target_id}")
                    return True
            
            self.get_logger(__name__).warning(f"Target {target.target_id} not found for update")
            return False
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Failed to update coordination target {target.target_id}: {e}")
            return False

    def remove_coordination_target(self, target_id: str) -> bool:
        """
        Remove coordination target.
        
        Args:
            target_id: Target ID to remove
            
        Returns:
            bool: True if removal successful
        """
        try:
            for i, target in enumerate(self.coordination_targets):
                if target.target_id == target_id:
                    del self.coordination_targets[i]
                    self.get_logger(__name__).info(f"Removed coordination target: {target_id}")
                    return True
            
            self.get_logger(__name__).warning(f"Target {target_id} not found for removal")
            return False
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Failed to remove coordination target {target_id}: {e}")
            return False

    def get_coordination_targets_by_type(self, target_type: str) -> List[CoordinationTarget]:
        """
        Get coordination targets by type.
        
        Args:
            target_type: Target type
            
        Returns:
            List[CoordinationTarget]: Targets of specified type
        """
        return [target for target in self.coordination_targets if target.target_type == target_type]

    def get_coordination_targets_by_priority(self, min_priority: int = 1) -> List[CoordinationTarget]:
        """
        Get coordination targets by minimum priority.
        
        Args:
            min_priority: Minimum priority level
            
        Returns:
            List[CoordinationTarget]: Targets with priority >= min_priority
        """
        return [target for target in self.coordination_targets if target.priority >= min_priority]

    def execute_coordination(
        self, operation_name: str, operation_func: Callable, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute coordination operation with unified error handling and logging.
        
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
            self.get_logger(__name__).info(f"Executing coordination operation: {operation_name}")
            
            # Execute the operation
            result = operation_func(*args, **kwargs)
            
            self.get_logger(__name__).info(f"Coordination operation {operation_name} completed successfully")
            
            return {
                "success": True,
                "operation": operation_name,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "coordinator": self.name,
            }
            
        except Exception as e:
            self.error_count += 1
            self.get_logger(__name__).error(f"Coordination operation {operation_name} failed: {e}")
            
            return {
                "success": False,
                "operation": operation_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "coordinator": self.name,
            }

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive coordinator status.
        
        Returns:
            Dict[str, Any]: Coordinator status information
        """
        return {
            "name": self.name,
            "initialized": self._initialized,
            "coordination_status": self.coordination_status,
            "config": self.config,
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "operations_count": self.operations_count,
            "error_count": self.error_count,
            "success_rate": self._calculate_success_rate(),
            "targets_count": len(self.coordination_targets),
            "targets_by_type": self._get_targets_by_type_summary(),
            "status": "OPERATIONAL" if self._initialized else "INITIALIZING",
        }

    def _calculate_success_rate(self) -> float:
        """Calculate coordinator success rate."""
        if self.operations_count == 0:
            return 100.0
        
        successful_operations = self.operations_count - self.error_count
        return (successful_operations / self.operations_count) * 100.0

    def _get_targets_by_type_summary(self) -> Dict[str, int]:
        """Get summary of targets by type."""
        summary = {}
        for target in self.coordination_targets:
            target_type = target.target_type
            summary[target_type] = summary.get(target_type, 0) + 1
        return summary

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
        Update coordinator configuration.
        
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
        """Reset coordinator statistics."""
        self.operations_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        self.get_logger(__name__).info(f"Statistics reset for {self.name}")

    def shutdown(self):
        """Shutdown coordinator gracefully."""
        try:
            self.get_logger(__name__).info(f"Shutting down coordinator {self.name}")
            
            # Perform cleanup operations
            self._cleanup()
            
            self._initialized = False
            self.coordination_status = "shutdown"
            self.get_logger(__name__).info(f"Coordinator {self.name} shut down successfully")
            
        except Exception as e:
            self.get_logger(__name__).error(f"Error during shutdown of {self.name}: {e}")

    def _cleanup(self):
        """Perform cleanup operations."""
        # Override in subclasses for specific cleanup
        pass

    def __str__(self) -> str:
        """String representation of coordinator."""
        return f"UnifiedCoordinator({self.name}, status={self.coordination_status})"

    def __repr__(self) -> str:
        """Detailed representation of coordinator."""
        return f"UnifiedCoordinator(name='{self.name}', status='{self.coordination_status}', targets={len(self.coordination_targets)}, operations={self.operations_count}, errors={self.error_count})"


class CoordinatorRegistry:
    """
    Registry for managing all unified coordinators.
    
    Provides centralized management of all coordinator instances.
    """

    def __init__(self):
        self.coordinators: Dict[str, UnifiedCoordinatorBase] = {}
        self.logger = logging.getLogger("CoordinatorRegistry")

    def register_coordinator(self, coordinator: UnifiedCoordinatorBase) -> bool:
        """
        Register a coordinator instance.
        
        Args:
            coordinator: Coordinator instance to register
            
        Returns:
            bool: True if registration successful
        """
        try:
            if coordinator.name in self.coordinators:
                self.get_logger(__name__).warning(
                    f"Coordinator {coordinator.name} already registered, replacing"
                )
            
            self.coordinators[coordinator.name] = coordinator
            self.get_logger(__name__).info(f"Coordinator {coordinator.name} registered successfully")
            return True
            
        except Exception as e:
            self.get_logger(__name__).error(f"Failed to register coordinator {coordinator.name}: {e}")
            return False

    def get_coordinator(self, name: str) -> Optional[UnifiedCoordinatorBase]:
        """
        Get coordinator by name.
        
        Args:
            name: Coordinator name
            
        Returns:
            Optional[UnifiedCoordinatorBase]: Coordinator instance or None
        """
        return self.coordinators.get(name)

    def get_all_coordinators(self) -> Dict[str, UnifiedCoordinatorBase]:
        """
        Get all registered coordinators.
        
        Returns:
            Dict[str, UnifiedCoordinatorBase]: All coordinators
        """
        return self.coordinators.copy()

    def get_coordinator_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all coordinators.
        
        Returns:
            Dict[str, Dict[str, Any]]: Status of all coordinators
        """
        return {name: coordinator.get_status() for name, coordinator in self.coordinators.items()}

    def shutdown_all_coordinators(self):
        """Shutdown all registered coordinators."""
        for name, coordinator in self.coordinators.items():
            try:
                coordinator.shutdown()
            except Exception as e:
                self.get_logger(__name__).error(f"Error shutting down coordinator {name}: {e}")


# Global coordinator registry instance
_coordinator_registry = None


def get_coordinator_registry() -> CoordinatorRegistry:
    """Get global coordinator registry instance."""
    global _coordinator_registry
    if _coordinator_registry is None:
        _coordinator_registry = CoordinatorRegistry()
    return _coordinator_registry


def register_coordinator(coordinator: UnifiedCoordinatorBase) -> bool:
    """Register a coordinator with the global registry."""
    return get_coordinator_registry().register_coordinator(coordinator)


def get_coordinator(name: str) -> Optional[UnifiedCoordinatorBase]:
    """Get a coordinator by name from the global registry."""
    return get_coordinator_registry().get_coordinator(name)


def get_all_coordinators() -> Dict[str, UnifiedCoordinatorBase]:
    """Get all coordinators from the global registry."""
    return get_coordinator_registry().get_all_coordinators()


def get_all_coordinator_statuses() -> Dict[str, Dict[str, Any]]:
    """Get status of all coordinators from the global registry."""
    return get_coordinator_registry().get_coordinator_statuses()
