"""
Base Manager - Phase 2 Manager Consolidation
============================================

Unified base class for all managers implementing SSOT principles.
Consolidates 43+ manager classes into unified framework using Phase 1 shared utilities.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
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


class ManagerType(Enum):
    """Manager type enumeration for specialization."""

    CONFIGURATION = "configuration"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    ONBOARDING = "onboarding"
    RECOVERY = "recovery"
    RESOURCE = "resource"
    RESULTS = "results"
    SERVICE = "service"
    COORDINATION = "coordination"
    PERFORMANCE = "performance"
    SECURITY = "security"


class ManagerState(Enum):
    """Manager lifecycle states."""

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"
    CLEANING_UP = "cleaning_up"
    TERMINATED = "terminated"


class BaseManager(Manager, ABC):
    """
    Unified base class for all managers - SSOT implementation.

    Consolidates common functionality using Phase 1 shared utilities:
    - StatusManager: Centralized status reporting
    - ErrorHandler: Centralized error handling
    - LoggingManager: Centralized logging
    - ResultManager: Standardized result objects
    - ValidationManager: Unified validation
    - ConfigurationManager: Centralized configuration
    - InitializationManager: Standardized initialization
    - CleanupManager: Standardized cleanup
    """

    def __init__(self, manager_type: ManagerType, manager_name: str = None):
        """Initialize base manager with shared utilities."""

        # Core identity
        self.manager_type = manager_type
        self.manager_name = manager_name or f"{manager_type.value}_manager"
        self.manager_id = f"{self.manager_name}_{id(self)}"

        # Lifecycle state
        self.state = ManagerState.UNINITIALIZED
        self.initialized_at: datetime | None = None
        self.last_operation_at: datetime | None = None

        # Phase 1 shared utilities integration
        self.status_manager = StatusManager()
        self.error_handler = ErrorHandler()
        self.logging_manager = LoggingManager(self.manager_name)
        self.result_manager = ResultManager()
        self.validation_manager = ValidationManager()
        self.configuration_manager = ConfigurationManager()
        self.initialization_manager = InitializationManager()
        self.cleanup_manager = CleanupManager()

        # Operation tracking
        self.operation_count = 0
        self.success_count = 0
        self.error_count = 0
        self.last_error: str | None = None

        # Context and configuration
        self.context: ManagerContext | None = None
        self.config: dict[str, Any] = {}

        # Initialize logging
        self.logger = self.logging_manager.get_logger()

    def initialize(self, context: ManagerContext) -> bool:
        """
        Standard initialization using Phase 1 InitializationManager.

        Args:
            context: Manager context with configuration and dependencies

        Returns:
            bool: True if initialization successful
        """
        try:
            self.state = ManagerState.INITIALIZING
            self.context = context
            self.config = context.config.copy()

            # Log initialization start
            self.logger.info(f"Initializing {self.manager_name} manager")

            # Use InitializationManager for standardized initialization
            init_context = {
                "manager_id": self.manager_id,
                "manager_type": self.manager_type.value,
                "config": self.config,
                "timestamp": context.timestamp,
            }

            success = self.initialization_manager.initialize_component(
                component_id=self.manager_id, component_type="manager", context=init_context
            )

            if success:
                self.state = ManagerState.READY
                self.initialized_at = datetime.now()

                # Register with StatusManager
                self.status_manager.register_component(
                    component_id=self.manager_id,
                    component_type=self.manager_type.value,
                    metadata={
                        "manager_name": self.manager_name,
                        "initialized_at": self.initialized_at.isoformat(),
                        "config_keys": list(self.config.keys()),
                    },
                )

                self.logger.info(f"{self.manager_name} manager initialized successfully")
                return True
            else:
                self.state = ManagerState.ERROR
                self.last_error = "Initialization failed"
                self.logger.error(f"Failed to initialize {self.manager_name} manager")
                return False

        except Exception as e:
            self.state = ManagerState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for standardized error handling
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": "initialize",
                    "manager_id": self.manager_id,
                    "manager_type": self.manager_type.value,
                },
                component_id=self.manager_id,
                severity="high",
            )

            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """
        Standard execution using Phase 1 utilities.

        Args:
            context: Manager context
            operation: Operation to execute
            payload: Operation payload

        Returns:
            ManagerResult: Standardized result object
        """
        try:
            self.operation_count += 1
            self.last_operation_at = datetime.now()
            self.state = ManagerState.ACTIVE

            # Validate input using ValidationManager
            validation_result = self.validation_manager.validate_operation(
                operation=operation, payload=payload, component_type=self.manager_type.value
            )

            if not validation_result.is_valid:
                self.error_count += 1
                return self.result_manager.create_error_result(
                    error=f"Validation failed: {validation_result.errors}",
                    operation=operation,
                    component_id=self.manager_id,
                )

            # Execute operation (implemented by subclasses)
            result = self._execute_operation(context, operation, payload)

            if result.success:
                self.success_count += 1
            else:
                self.error_count += 1
                self.last_error = result.error

            # Create standardized result using ResultManager
            return self.result_manager.create_result(
                data=result.data if result.success else {},
                operation=operation,
                component_id=self.manager_id,
                success=result.success,
                error=result.error,
                metrics=result.metrics,
            )

        except Exception as e:
            self.error_count += 1
            self.state = ManagerState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for standardized error handling
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": operation,
                    "payload": payload,
                    "manager_id": self.manager_id,
                },
                component_id=self.manager_id,
                severity="medium",
            )

            return self.result_manager.create_error_result(
                error=str(e), operation=operation, component_id=self.manager_id
            )

        finally:
            self.state = ManagerState.READY

    @abstractmethod
    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """
        Execute manager-specific operation.

        Must be implemented by subclasses to provide specialized functionality.
        """
        pass

    def cleanup(self, context: ManagerContext) -> bool:
        """
        Standard cleanup using Phase 1 CleanupManager.

        Args:
            context: Manager context

        Returns:
            bool: True if cleanup successful
        """
        try:
            self.state = ManagerState.CLEANING_UP

            # Log cleanup start
            self.logger.info(f"Cleaning up {self.manager_name} manager")

            # Use CleanupManager for standardized cleanup
            cleanup_context = {
                "manager_id": self.manager_id,
                "manager_type": self.manager_type.value,
                "operation_count": self.operation_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
            }

            success = self.cleanup_manager.cleanup_component(
                component_id=self.manager_id, component_type="manager", context=cleanup_context
            )

            if success:
                self.state = ManagerState.TERMINATED

                # Unregister from StatusManager
                self.status_manager.unregister_component(self.manager_id)

                self.logger.info(f"{self.manager_name} manager cleaned up successfully")
                return True
            else:
                self.state = ManagerState.ERROR
                self.logger.error(f"Failed to cleanup {self.manager_name} manager")
                return False

        except Exception as e:
            self.state = ManagerState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for cleanup errors
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": "cleanup",
                    "manager_id": self.manager_id,
                },
                component_id=self.manager_id,
                severity="medium",
            )

            return False

    def get_status(self) -> dict[str, Any]:
        """
        Get comprehensive manager status using StatusManager.

        Returns:
            Dict containing status information
        """
        try:
            # Get status from StatusManager
            base_status = self.status_manager.get_component_status(self.manager_id)

            # Add manager-specific status
            manager_status = {
                "manager_id": self.manager_id,
                "manager_name": self.manager_name,
                "manager_type": self.manager_type.value,
                "state": self.state.value,
                "initialized_at": self.initialized_at.isoformat() if self.initialized_at else None,
                "last_operation_at": (
                    self.last_operation_at.isoformat() if self.last_operation_at else None
                ),
                "operation_count": self.operation_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "success_rate": (self.success_count / max(self.operation_count, 1)) * 100,
                "last_error": self.last_error,
                "config_keys": list(self.config.keys()),
            }

            # Merge with base status
            if base_status:
                manager_status.update(base_status)

            return manager_status

        except Exception as e:
            self.logger.error(f"Error getting status for {self.manager_name}: {e}")
            return {
                "manager_id": self.manager_id,
                "state": "error",
                "error": str(e),
                "last_error": str(e),
            }

    def get_health_check(self) -> dict[str, Any]:
        """
        Get health check using StatusManager.

        Returns:
            Dict containing health status
        """
        return self.status_manager.get_health_check_for_component(self.manager_id)

    def update_configuration(self, updates: dict[str, Any]) -> bool:
        """
        Update manager configuration using ConfigurationManager.

        Args:
            updates: Configuration updates

        Returns:
            bool: True if update successful
        """
        try:
            # Validate configuration updates
            validation_result = self.validation_manager.validate_config(
                config_data=updates, component_type=self.manager_type.value
            )

            if not validation_result.is_valid:
                self.logger.error(f"Invalid configuration updates: {validation_result.errors}")
                return False

            # Update configuration using ConfigurationManager
            success = self.configuration_manager.update_component_config(
                component_id=self.manager_id, updates=updates
            )

            if success:
                # Update local config
                self.config.update(updates)
                self.logger.info(f"Configuration updated for {self.manager_name}")
                return True
            else:
                self.logger.error(f"Failed to update configuration for {self.manager_name}")
                return False

        except Exception as e:
            self.logger.error(f"Error updating configuration for {self.manager_name}: {e}")
            return False

    def get_metrics(self) -> dict[str, Any]:
        """
        Get manager metrics.

        Returns:
            Dict containing performance metrics
        """
        return {
            "operation_count": self.operation_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": (self.success_count / max(self.operation_count, 1)) * 100,
            "average_operations_per_hour": self._calculate_ops_per_hour(),
            "uptime_seconds": self._calculate_uptime(),
            "error_rate": (self.error_count / max(self.operation_count, 1)) * 100,
        }

    def _calculate_ops_per_hour(self) -> float:
        """Calculate average operations per hour."""
        if not self.initialized_at:
            return 0.0

        uptime_hours = (datetime.now() - self.initialized_at).total_seconds() / 3600
        return self.operation_count / max(uptime_hours, 0.01)

    def _calculate_uptime(self) -> float:
        """Calculate uptime in seconds."""
        if not self.initialized_at:
            return 0.0

        return (datetime.now() - self.initialized_at).total_seconds()

    def reset_metrics(self) -> bool:
        """
        Reset manager metrics.

        Returns:
            bool: True if reset successful
        """
        try:
            self.operation_count = 0
            self.success_count = 0
            self.error_count = 0
            self.last_error = None
            self.last_operation_at = None

            self.logger.info(f"Metrics reset for {self.manager_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error resetting metrics for {self.manager_name}: {e}")
            return False

    def __repr__(self) -> str:
        """String representation of the manager."""
        return f"{self.__class__.__name__}(id={self.manager_id}, type={self.manager_type.value}, state={self.state.value})"
