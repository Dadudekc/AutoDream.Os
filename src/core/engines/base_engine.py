"""
Base Engine - Phase 3 Engine Consolidation
==========================================

Unified base class for all engines implementing SSOT principles.
Consolidates 92+ engine classes into unified framework using Phase 1 shared utilities.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from .contracts import Engine, EngineContext, EngineResult
from ..shared_utilities import (
    StatusManager,
    ErrorHandler,
    LoggingManager,
    ResultManager,
    ValidationManager,
    ConfigurationManager,
    InitializationManager,
    CleanupManager,
)


class EngineType(Enum):
    """Engine type enumeration for specialization."""

    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    CONFIGURATION = "configuration"
    COORDINATION = "coordination"
    DATA = "data"
    INTEGRATION = "integration"
    ML = "ml"
    MONITORING = "monitoring"
    ORCHESTRATION = "orchestration"
    PERFORMANCE = "performance"
    PROCESSING = "processing"
    SECURITY = "security"
    STORAGE = "storage"
    UTILITY = "utility"
    VALIDATION = "validation"


class EngineState(Enum):
    """Engine lifecycle states."""

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"
    CLEANING_UP = "cleaning_up"
    TERMINATED = "terminated"


class BaseEngine(Engine, ABC):
    """
    Unified base class for all engines - SSOT implementation.

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

    def __init__(self, engine_type: EngineType, engine_name: str = None):
        """Initialize base engine with shared utilities."""

        # Core identity
        self.engine_type = engine_type
        self.engine_name = engine_name or f"{engine_type.value}_engine"
        self.engine_id = f"{self.engine_name}_{id(self)}"

        # Lifecycle state
        self.state = EngineState.UNINITIALIZED
        self.initialized_at: Optional[datetime] = None
        self.last_operation_at: Optional[datetime] = None

        # Phase 1 shared utilities integration
        self.status_manager = StatusManager()
        self.error_handler = ErrorHandler()
        self.logging_manager = LoggingManager(self.engine_name)
        self.result_manager = ResultManager()
        self.validation_manager = ValidationManager()
        self.configuration_manager = ConfigurationManager()
        self.initialization_manager = InitializationManager()
        self.cleanup_manager = CleanupManager()

        # Operation tracking
        self.operation_count = 0
        self.success_count = 0
        self.error_count = 0
        self.last_error: Optional[str] = None

        # Context and configuration
        self.context: Optional[EngineContext] = None
        self.config: Dict[str, Any] = {}

        # Initialize logging
        self.logger = self.logging_manager.get_logger()

    def initialize(self, context: EngineContext) -> bool:
        """
        Standard initialization using Phase 1 InitializationManager.

        Args:
            context: Engine context with configuration and dependencies

        Returns:
            bool: True if initialization successful
        """
        try:
            self.state = EngineState.INITIALIZING
            self.context = context
            self.config = context.config.copy()

            # Log initialization start
            self.logger.info(f"Initializing {self.engine_name} engine")

            # Use InitializationManager for standardized initialization
            init_context = {
                "engine_id": self.engine_id,
                "engine_type": self.engine_type.value,
                "config": self.config,
                "timestamp": context.timestamp,
            }

            success = self.initialization_manager.initialize_component(
                component_id=self.engine_id,
                component_type="engine",
                context=init_context
            )

            if success:
                self.state = EngineState.READY
                self.initialized_at = datetime.now()

                # Register with StatusManager
                self.status_manager.register_component(
                    component_id=self.engine_id,
                    component_type=self.engine_type.value,
                    metadata={
                        "engine_name": self.engine_name,
                        "initialized_at": self.initialized_at.isoformat(),
                        "config_keys": list(self.config.keys()),
                    }
                )

                self.logger.info(f"{self.engine_name} engine initialized successfully")
                return True
            else:
                self.state = EngineState.ERROR
                self.last_error = "Initialization failed"
                self.logger.error(f"Failed to initialize {self.engine_name} engine")
                return False

        except Exception as e:
            self.state = EngineState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for standardized error handling
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": "initialize",
                    "engine_id": self.engine_id,
                    "engine_type": self.engine_type.value,
                },
                component_id=self.engine_id,
                severity="high"
            )

            return False

    def execute(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """
        Standard execution using Phase 1 utilities.

        Args:
            context: Engine context
            payload: Operation payload

        Returns:
            EngineResult: Standardized result object
        """
        try:
            self.operation_count += 1
            self.last_operation_at = datetime.now()
            self.state = EngineState.ACTIVE

            # Validate input using ValidationManager
            validation_result = self.validation_manager.validate_operation(
                operation=payload.get("operation", "execute"),
                payload=payload,
                component_type=self.engine_type.value
            )

            if not validation_result.is_valid:
                self.error_count += 1
                return EngineResult(
                    success=False,
                    data={},
                    metrics={"operation": payload.get("operation", "execute")},
                    error=f"Validation failed: {validation_result.errors}"
                )

            # Execute operation (implemented by subclasses)
            result = self._execute_operation(context, payload)

            if result.success:
                self.success_count += 1
            else:
                self.error_count += 1
                self.last_error = result.error

            # Create standardized result using ResultManager
            return self.result_manager.create_result(
                data=result.data if result.success else {},
                operation=payload.get("operation", "execute"),
                component_id=self.engine_id,
                success=result.success,
                error=result.error,
                metrics=result.metrics
            )

        except Exception as e:
            self.error_count += 1
            self.state = EngineState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for standardized error handling
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": payload.get("operation", "execute"),
                    "payload": payload,
                    "engine_id": self.engine_id,
                },
                component_id=self.engine_id,
                severity="medium"
            )

            return EngineResult(
                success=False,
                data={},
                metrics={"operation": payload.get("operation", "execute")},
                error=str(e)
            )

        finally:
            self.state = EngineState.READY

    @abstractmethod
    def _execute_operation(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """
        Execute engine-specific operation.

        Must be implemented by subclasses to provide specialized functionality.
        """
        pass

    def cleanup(self, context: EngineContext) -> bool:
        """
        Standard cleanup using Phase 1 CleanupManager.

        Args:
            context: Engine context

        Returns:
            bool: True if cleanup successful
        """
        try:
            self.state = EngineState.CLEANING_UP

            # Log cleanup start
            self.logger.info(f"Cleaning up {self.engine_name} engine")

            # Use CleanupManager for standardized cleanup
            cleanup_context = {
                "engine_id": self.engine_id,
                "engine_type": self.engine_type.value,
                "operation_count": self.operation_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
            }

            success = self.cleanup_manager.cleanup_component(
                component_id=self.engine_id,
                component_type="engine",
                context=cleanup_context
            )

            if success:
                self.state = EngineState.TERMINATED

                # Unregister from StatusManager
                self.status_manager.unregister_component(self.engine_id)

                self.logger.info(f"{self.engine_name} engine cleaned up successfully")
                return True
            else:
                self.state = EngineState.ERROR
                self.logger.error(f"Failed to cleanup {self.engine_name} engine")
                return False

        except Exception as e:
            self.state = EngineState.ERROR
            self.last_error = str(e)

            # Use ErrorHandler for cleanup errors
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": "cleanup",
                    "engine_id": self.engine_id,
                },
                component_id=self.engine_id,
                severity="medium"
            )

            return False

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive engine status using StatusManager.

        Returns:
            Dict containing status information
        """
        try:
            # Get status from StatusManager
            base_status = self.status_manager.get_component_status(self.engine_id)

            # Add engine-specific status
            engine_status = {
                "engine_id": self.engine_id,
                "engine_name": self.engine_name,
                "engine_type": self.engine_type.value,
                "state": self.state.value,
                "initialized_at": self.initialized_at.isoformat() if self.initialized_at else None,
                "last_operation_at": self.last_operation_at.isoformat() if self.last_operation_at else None,
                "operation_count": self.operation_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "success_rate": (self.success_count / max(self.operation_count, 1)) * 100,
                "last_error": self.last_error,
                "config_keys": list(self.config.keys()),
            }

            # Merge with base status
            if base_status:
                engine_status.update(base_status)

            return engine_status

        except Exception as e:
            self.logger.error(f"Error getting status for {self.engine_name}: {e}")
            return {
                "engine_id": self.engine_id,
                "state": "error",
                "error": str(e),
                "last_error": str(e),
            }

    def get_health_check(self) -> Dict[str, Any]:
        """
        Get health check using StatusManager.

        Returns:
            Dict containing health status
        """
        return self.status_manager.get_health_check_for_component(self.engine_id)

    def update_configuration(self, updates: Dict[str, Any]) -> bool:
        """
        Update engine configuration using ConfigurationManager.

        Args:
            updates: Configuration updates

        Returns:
            bool: True if update successful
        """
        try:
            # Validate configuration updates
            validation_result = self.validation_manager.validate_config(
                config_data=updates,
                component_type=self.engine_type.value
            )

            if not validation_result.is_valid:
                self.logger.error(f"Invalid configuration updates: {validation_result.errors}")
                return False

            # Update configuration using ConfigurationManager
            success = self.configuration_manager.update_component_config(
                component_id=self.engine_id,
                updates=updates
            )

            if success:
                # Update local config
                self.config.update(updates)
                self.logger.info(f"Configuration updated for {self.engine_name}")
                return True
            else:
                self.logger.error(f"Failed to update configuration for {self.engine_name}")
                return False

        except Exception as e:
            self.logger.error(f"Error updating configuration for {self.engine_name}: {e}")
            return False

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get engine metrics.

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
        Reset engine metrics.

        Returns:
            bool: True if reset successful
        """
        try:
            self.operation_count = 0
            self.success_count = 0
            self.error_count = 0
            self.last_error = None
            self.last_operation_at = None

            self.logger.info(f"Metrics reset for {self.engine_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error resetting metrics for {self.engine_name}: {e}")
            return False

    def validate_input(self, input_data: Any) -> Dict[str, Any]:
        """
        Validate input data using ValidationManager.

        Args:
            input_data: Data to validate

        Returns:
            Dict containing validation results
        """
        try:
            validation_result = self.validation_manager.validate_input(
                input_data=input_data,
                component_type=self.engine_type.value
            )

            return {
                "is_valid": validation_result.is_valid,
                "errors": validation_result.errors,
                "warnings": validation_result.warnings,
                "validated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error validating input for {self.engine_name}: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": [],
                "validated_at": datetime.now().isoformat(),
            }

    def process_result(self, result: Any) -> Dict[str, Any]:
        """
        Process result using ResultManager.

        Args:
            result: Result to process

        Returns:
            Dict containing processed result
        """
        try:
            processed_result = self.result_manager.create_result(
                data=result,
                operation="process_result",
                component_id=self.engine_id,
                success=True,
                metrics={"processed_at": datetime.now().isoformat()}
            )

            return processed_result.data

        except Exception as e:
            self.logger.error(f"Error processing result for {self.engine_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "processed_at": datetime.now().isoformat(),
            }

    def __repr__(self) -> str:
        """String representation of the engine."""
        return f"{self.__class__.__name__}(id={self.engine_id}, type={self.engine_type.value}, state={self.state.value})"
