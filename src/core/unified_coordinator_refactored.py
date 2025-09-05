#!/usr/bin/env python3
"""
Unified Coordinator - V2 Compliant Refactored
============================================

Refactored unified coordinator using modular architecture.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: V2 compliant modular coordinator system
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from .coordinator_models import (
    CoordinationTarget, 
    CoordinationResult, 
    CoordinatorStatus,
    CoordinationStatus as Status,
    TargetType,
    Priority,
    CoordinatorConfig
)
from .coordinator_interfaces import (
    ICoordinatorTargetManager,
    ICoordinatorOperationEngine,
    ICoordinatorStatusTracker,
    ICoordinatorConfigManager,
    ICoordinatorLifecycle,
    ICoordinatorLogger
)
from .coordinator_engines import (
    TargetManager,
    OperationEngine,
    StatusTracker,
    ConfigManager
)
from .coordinator_registry import CoordinatorRegistry


class UnifiedCoordinator(ICoordinatorLifecycle):
    """
    Unified Coordinator - V2 Compliant Refactored
    
    Modular architecture with separated concerns:
    - Target management
    - Operation execution
    - Status tracking
    - Configuration management
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None, logger: Optional[ICoordinatorLogger] = None):
        """Initialize unified coordinator with modular components."""
        self.name = name
        self.config = config or {}
        self.logger = logger or self._create_default_logger()
        
        # Initialize modular components
        self.target_manager = TargetManager(self.logger)
        self.status_tracker = StatusTracker(name, self.config, self.logger)
        self.config_manager = ConfigManager(self.config, self.logger)
        self.operation_engine = OperationEngine(self.logger, self.status_tracker)
        
        # Initialize coordinator
        self._initialized = False
        self._initialize()
    
    def _create_default_logger(self) -> ICoordinatorLogger:
        """Create default logger if none provided."""
        import logging
        return logging.getLogger(f"UnifiedCoordinator.{self.name}")
    
    def _initialize(self) -> None:
        """Initialize coordinator with modular components."""
        try:
            self.logger.info(f"Coordinator {self.name} initializing")
            
            # Validate configuration
            if not self.config_manager.validate_config():
                raise ValueError("Invalid configuration")
            
            # Initialize components
            self._initialize_components()
            
            # Set initialized status
            self.status_tracker.set_initialized(True)
            self._initialized = True
            
            self.logger.info(f"Coordinator {self.name} initialized successfully")
            
        except Exception as e:
            self.status_tracker.set_status(Status.ERROR)
            self.logger.error(f"Coordinator {self.name} initialization failed: {e}")
            raise
    
    def _initialize_components(self) -> None:
        """Initialize coordinator-specific components."""
        # Override in subclasses for specific initialization
        pass
    
    # ICoordinatorLifecycle implementation
    def initialize(self) -> bool:
        """Initialize coordinator."""
        try:
            if not self._initialized:
                self._initialize()
            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if coordinator is initialized."""
        return self._initialized
    
    def shutdown(self) -> None:
        """Shutdown coordinator gracefully."""
        try:
            self.logger.info(f"Shutting down coordinator {self.name}")
            
            # Perform cleanup
            self.cleanup()
            
            # Update status
            self.status_tracker.set_status(Status.SHUTDOWN)
            self._initialized = False
            
            self.logger.info(f"Coordinator {self.name} shut down successfully")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown of {self.name}: {e}")
    
    def cleanup(self) -> None:
        """Perform cleanup operations."""
        # Override in subclasses for specific cleanup
        pass
    
    # Target management methods
    def add_coordination_target(self, target: CoordinationTarget) -> bool:
        """Add a coordination target."""
        return self.target_manager.add_target(target)
    
    def get_coordination_target(self, target_id: str) -> Optional[CoordinationTarget]:
        """Get coordination target by ID."""
        return self.target_manager.get_target(target_id)
    
    def update_coordination_target(self, target: CoordinationTarget) -> bool:
        """Update coordination target."""
        return self.target_manager.update_target(target)
    
    def remove_coordination_target(self, target_id: str) -> bool:
        """Remove coordination target."""
        return self.target_manager.remove_target(target_id)
    
    def get_coordination_targets_by_type(self, target_type: str) -> List[CoordinationTarget]:
        """Get coordination targets by type."""
        return self.target_manager.get_targets_by_type(target_type)
    
    def get_coordination_targets_by_priority(self, min_priority: int) -> List[CoordinationTarget]:
        """Get coordination targets by minimum priority."""
        return self.target_manager.get_targets_by_priority(min_priority)
    
    def get_all_coordination_targets(self) -> List[CoordinationTarget]:
        """Get all coordination targets."""
        return self.target_manager.get_all_targets()
    
    # Operation execution methods
    def execute_coordination(
        self, operation_name: str, operation_func: Callable, *args, **kwargs
    ) -> CoordinationResult:
        """Execute coordination operation."""
        return self.operation_engine.execute_operation(operation_name, operation_func, *args, **kwargs)
    
    def execute_with_retry(
        self, operation_name: str, operation_func: Callable, max_retries: int = 3, *args, **kwargs
    ) -> CoordinationResult:
        """Execute operation with retry logic."""
        return self.operation_engine.execute_with_retry(operation_name, operation_func, max_retries, *args, **kwargs)
    
    def execute_batch(self, operations: List[Dict[str, Any]]) -> List[CoordinationResult]:
        """Execute multiple operations in batch."""
        return self.operation_engine.execute_batch(operations)
    
    # Status and configuration methods
    def get_status(self) -> CoordinatorStatus:
        """Get comprehensive coordinator status."""
        status = self.status_tracker.get_status()
        
        # Update with target information
        status.targets_count = self.target_manager.get_targets_count()
        status.targets_by_type = self._get_targets_by_type_summary()
        
        return status
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get coordinator metrics."""
        return self.status_tracker.get_metrics()
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config_manager.get_config_value(key, default)
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration."""
        success = self.config_manager.update_config(updates)
        if success:
            self.config.update(updates)
        return success
    
    def reset_statistics(self) -> None:
        """Reset coordinator statistics."""
        self.status_tracker.reset_statistics()
    
    # Utility methods
    def _get_targets_by_type_summary(self) -> Dict[str, int]:
        """Get summary of targets by type."""
        summary = {}
        for target in self.target_manager.get_all_targets():
            target_type = target.target_type.value
            summary[target_type] = summary.get(target_type, 0) + 1
        return summary
    
    def __str__(self) -> str:
        """String representation of coordinator."""
        return f"UnifiedCoordinator({self.name}, status={self.status_tracker.coordination_status.value})"
    
    def __repr__(self) -> str:
        """Detailed representation of coordinator."""
        return (f"UnifiedCoordinator(name='{self.name}', "
                f"status='{self.status_tracker.coordination_status.value}', "
                f"targets={self.target_manager.get_targets_count()}, "
                f"operations={self.status_tracker.operations_count}, "
                f"errors={self.status_tracker.error_count})")


# Backward compatibility aliases
UnifiedCoordinatorBase = UnifiedCoordinator
