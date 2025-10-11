"""
Base Manager - Phase 2 Manager Consolidation (V2 Compliant)
===========================================================
Unified base class for all managers implementing SSOT principles.
Refactored for V2 compliance: 273→<200 lines.

Author: Agent-2 (Architecture & Design Specialist - V2 Refactor)
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
from .base_manager_helpers import ManagerConfigHelper, ManagerPropertySync, ManagerStatusHelper
from .contracts import Manager, ManagerContext, ManagerResult
from .manager_lifecycle import ManagerLifecycleHelper
from .manager_metrics import ManagerMetricsTracker
from .manager_state import ManagerState, ManagerStateTracker, ManagerType


class BaseManager(Manager, ABC):
    """
    Unified base class for all managers - SSOT implementation.
    Consolidates common functionality using shared utilities and helpers.
    """

    def __init__(self, manager_type: ManagerType, manager_name: str = None):
        """Initialize base manager with shared utilities and extracted components."""
        # State and metrics trackers
        self.state_tracker = ManagerStateTracker(manager_type, manager_name)
        self.metrics_tracker = ManagerMetricsTracker()

        # Shared utilities
        self.status_manager = StatusManager()
        self.error_handler = ErrorHandler()
        self.logging_manager = LoggingManager(self.state_tracker.manager_name)
        self.result_manager = ResultManager()
        self.validation_manager = ValidationManager()
        self.configuration_manager = ConfigurationManager()
        self.initialization_manager = InitializationManager()
        self.cleanup_manager = CleanupManager()

        # Lifecycle helper
        self.lifecycle_helper = ManagerLifecycleHelper(
            self.state_tracker,
            self.initialization_manager,
            self.cleanup_manager,
            self.status_manager,
            self.logging_manager.get_logger(),
        )

        self.logger = self.logging_manager.get_logger()

        # Sync backward compatibility properties
        ManagerPropertySync.sync_properties(self, self.state_tracker, self.metrics_tracker)

    def initialize(self, context: ManagerContext) -> bool:
        """Standard initialization using lifecycle helper."""
        success = self.lifecycle_helper.initialize(context, ManagerState)
        if success:
            self.metrics_tracker.set_initialized_at(self.state_tracker.initialized_at)
        ManagerPropertySync.sync_properties(self, self.state_tracker, self.metrics_tracker)
        return success

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Standard execution using Phase 1 utilities."""
        try:
            self.metrics_tracker.record_operation_start()
            self.state_tracker.mark_operation()

            # Validate input
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

            # Create standardized result
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

            # Standardized error handling
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
            ManagerPropertySync.sync_properties(self, self.state_tracker, self.metrics_tracker)

    @abstractmethod
    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute manager-specific operation. Must be implemented by subclasses."""
        pass

    def cleanup(self, context: ManagerContext) -> bool:
        """Standard cleanup using lifecycle helper."""
        success = self.lifecycle_helper.cleanup(context, ManagerState)
        ManagerPropertySync.sync_properties(self, self.state_tracker, self.metrics_tracker)
        return success

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive manager status."""
        return ManagerStatusHelper.get_comprehensive_status(
            self, self.state_tracker, self.metrics_tracker, self.status_manager, self.logger
        )

    def get_health_check(self) -> dict[str, Any]:
        """Get health check using StatusManager."""
        return self.status_manager.get_health_check_for_component(self.state_tracker.manager_id)

    def update_configuration(self, updates: dict[str, Any]) -> bool:
        """Update manager configuration using ConfigurationManager."""
        return ManagerConfigHelper.update_config(
            self,
            updates,
            self.state_tracker,
            self.validation_manager,
            self.configuration_manager,
            self.logger,
        )

    def get_metrics(self) -> dict[str, Any]:
        """Get manager metrics."""
        return self.metrics_tracker.get_metrics()

    def reset_metrics(self) -> bool:
        """Reset manager metrics."""
        try:
            success = self.metrics_tracker.reset()
            if success:
                self.logger.info(f"Metrics reset for {self.state_tracker.manager_name}")
                ManagerPropertySync.sync_properties(self, self.state_tracker, self.metrics_tracker)
            return success
        except Exception as e:
            self.logger.error(f"Error resetting metrics for {self.state_tracker.manager_name}: {e}")
            return False

    def __repr__(self) -> str:
        """String representation of the manager."""
        return (
            f"{self.__class__.__name__}(id={self.state_tracker.manager_id}, "
            f"type={self.state_tracker.manager_type.value}, "
            f"state={self.state_tracker.state.value})"
        )
