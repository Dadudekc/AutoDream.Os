"""
Base Manager - Phase 2 Manager Consolidation (V2 Compliant)
===========================================================
Unified base class for all managers implementing SSOT principles.
Refactored for V2 compliance while maintaining Agent-2's architecture.

Author: Agent-2 (Architecture & Design Specialist)
Refactored: Agent-5 (V2 Compliance)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..shared_utilities import (
    CleanupManager,
    ConfigurationManager,
    ErrorHandler,
    InitializationManager,
    LoggingManager,
    ResultManager,
    StatusManager,
    ValidationManager,
)
from .contracts import Manager, ManagerContext, ManagerResult
from .manager_lifecycle import ManagerLifecycleHelper
from .manager_metrics import ManagerMetricsTracker
from .manager_state import ManagerState, ManagerStateTracker, ManagerType


class BaseManager(Manager, ABC):
    """
    Unified base class for all managers - SSOT implementation.

    Consolidates common functionality using Phase 1 shared utilities and
    extracted state/metrics/lifecycle components for V2 compliance.
    """

    def __init__(self, manager_type: ManagerType, manager_name: str = None):
        """Initialize base manager with shared utilities and extracted components."""
        
        # V2: Use extracted state tracker
        self.state_tracker = ManagerStateTracker(manager_type, manager_name)
        self.metrics_tracker = ManagerMetricsTracker()

        # Phase 1 shared utilities integration
        self.status_manager = StatusManager()
        self.error_handler = ErrorHandler()
        self.logging_manager = LoggingManager(self.state_tracker.manager_name)
        self.result_manager = ResultManager()
        self.validation_manager = ValidationManager()
        self.configuration_manager = ConfigurationManager()
        self.initialization_manager = InitializationManager()
        self.cleanup_manager = CleanupManager()

        # V2: Lifecycle helper
        self.lifecycle_helper = ManagerLifecycleHelper(
            self.state_tracker,
            self.initialization_manager,
            self.cleanup_manager,
            self.status_manager,
            self.logging_manager.get_logger(),
        )

        # Initialize logging
        self.logger = self.logging_manager.get_logger()
        
        # Backward compatibility properties
        self.manager_type = self.state_tracker.manager_type
        self.manager_name = self.state_tracker.manager_name
        self.manager_id = self.state_tracker.manager_id
        self.state = self.state_tracker.state
        self.initialized_at = self.state_tracker.initialized_at
        self.last_operation_at = self.state_tracker.last_operation_at
        self.last_error = self.state_tracker.last_error
        self.context = self.state_tracker.context
        self.config = self.state_tracker.config
        self.operation_count = self.metrics_tracker.operation_count
        self.success_count = self.metrics_tracker.success_count
        self.error_count = self.metrics_tracker.error_count

    def initialize(self, context: ManagerContext) -> bool:
        """Standard initialization using lifecycle helper."""
        success = self.lifecycle_helper.initialize(context, ManagerState)
        # Sync metrics tracker
        if success:
            self.metrics_tracker.set_initialized_at(self.state_tracker.initialized_at)
        # Update backward compatibility properties
        self._sync_properties()
        return success

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Standard execution using Phase 1 utilities."""
        try:
            self.metrics_tracker.record_operation_start()
            self.state_tracker.mark_operation()

            # Validate input using ValidationManager
            validation_result = self.validation_manager.validate_operation(
                operation=operation,
                payload=payload,
                component_type=self.state_tracker.manager_type.value,
            )

            if not validation_result.is_valid:
                self.metrics_tracker.record_error()
                return self.result_manager.create_error_result(
                    error=f"Validation failed: {validation_result.errors}",
                    operation=operation,
                    component_id=self.state_tracker.manager_id,
                )

            # Execute operation (implemented by subclasses)
            result = self._execute_operation(context, operation, payload)

            if result.success:
                self.metrics_tracker.record_success()
            else:
                self.metrics_tracker.record_error()
                self.state_tracker.last_error = result.error

            # Create standardized result using ResultManager
            return self.result_manager.create_result(
                data=result.data if result.success else {},
                operation=operation,
                component_id=self.state_tracker.manager_id,
                success=result.success,
                error=result.error,
                metrics=result.metrics,
            )

        except Exception as e:
            self.metrics_tracker.record_error()
            self.state_tracker.mark_error(str(e))

            # Use ErrorHandler for standardized error handling
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": operation,
                    "payload": payload,
                    "manager_id": self.state_tracker.manager_id,
                },
                component_id=self.state_tracker.manager_id,
                severity="medium",
            )

            return self.result_manager.create_error_result(
                error=str(e), operation=operation, component_id=self.state_tracker.manager_id
            )

        finally:
            self.state_tracker.mark_ready()
            self._sync_properties()

    @abstractmethod
    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute manager-specific operation. Must be implemented by subclasses."""
        pass

    def cleanup(self, context: ManagerContext) -> bool:
        """Standard cleanup using lifecycle helper."""
        success = self.lifecycle_helper.cleanup(context, ManagerState)
        self._sync_properties()
        return success

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive manager status."""
        try:
            # Get status from StatusManager
            base_status = self.status_manager.get_component_status(self.state_tracker.manager_id)
            
            # Get state status
            manager_status = self.state_tracker.get_status_dict()
            
            # Add metrics
            manager_status.update(self.metrics_tracker.get_metrics_for_status())

            # Merge with base status
            if base_status:
                manager_status.update(base_status)

            return manager_status

        except Exception as e:
            self.logger.error(f"Error getting status for {self.state_tracker.manager_name}: {e}")
            return {
                "manager_id": self.state_tracker.manager_id,
                "state": "error",
                "error": str(e),
                "last_error": str(e),
            }

    def get_health_check(self) -> dict[str, Any]:
        """Get health check using StatusManager."""
        return self.status_manager.get_health_check_for_component(self.state_tracker.manager_id)

    def update_configuration(self, updates: dict[str, Any]) -> bool:
        """Update manager configuration using ConfigurationManager."""
        try:
            # Validate configuration updates
            validation_result = self.validation_manager.validate_config(
                config_data=updates, component_type=self.state_tracker.manager_type.value
            )

            if not validation_result.is_valid:
                self.logger.error(f"Invalid configuration updates: {validation_result.errors}")
                return False

            # Update configuration using ConfigurationManager
            success = self.configuration_manager.update_component_config(
                component_id=self.state_tracker.manager_id, updates=updates
            )

            if success:
                # Update local config
                self.state_tracker.config.update(updates)
                self.logger.info(f"Configuration updated for {self.state_tracker.manager_name}")
                self._sync_properties()
                return True
            else:
                self.logger.error(
                    f"Failed to update configuration for {self.state_tracker.manager_name}"
                )
                return False

        except Exception as e:
            self.logger.error(
                f"Error updating configuration for {self.state_tracker.manager_name}: {e}"
            )
            return False

    def get_metrics(self) -> dict[str, Any]:
        """Get manager metrics."""
        return self.metrics_tracker.get_metrics()

    def reset_metrics(self) -> bool:
        """Reset manager metrics."""
        try:
            success = self.metrics_tracker.reset()
            if success:
                self.logger.info(f"Metrics reset for {self.state_tracker.manager_name}")
                self._sync_properties()
            return success
        except Exception as e:
            self.logger.error(f"Error resetting metrics for {self.state_tracker.manager_name}: {e}")
            return False

    def _sync_properties(self) -> None:
        """Sync backward compatibility properties with trackers."""
        self.state = self.state_tracker.state
        self.initialized_at = self.state_tracker.initialized_at
        self.last_operation_at = self.state_tracker.last_operation_at
        self.last_error = self.state_tracker.last_error
        self.context = self.state_tracker.context
        self.config = self.state_tracker.config
        self.operation_count = self.metrics_tracker.operation_count
        self.success_count = self.metrics_tracker.success_count
        self.error_count = self.metrics_tracker.error_count

    def __repr__(self) -> str:
        """String representation of the manager."""
        return (
            f"{self.__class__.__name__}(id={self.state_tracker.manager_id}, "
            f"type={self.state_tracker.manager_type.value}, "
            f"state={self.state_tracker.state.value})"
        )
