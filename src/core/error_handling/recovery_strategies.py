"""
Recovery Strategies Module
===========================

Concrete recovery strategy implementations extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from collections.abc import Callable
from datetime import datetime, timedelta

from .error_handling_core import ErrorContext, ErrorSeverity

logger = logging.getLogger(__name__)


class RecoveryStrategy:
    """Base class for error recovery strategies."""

    def __init__(self, name: str, description: str = ""):
        """Initialize recovery strategy."""
        self.name = name
        self.description = description or name

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if this strategy can recover from the error."""
        raise NotImplementedError("Subclasses must implement can_recover")

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute the recovery strategy."""
        raise NotImplementedError("Subclasses must implement execute_recovery")


class ServiceRestartStrategy(RecoveryStrategy):
    """Strategy for restarting failed services."""

    def __init__(self, service_manager: Callable):
        """Initialize service restart strategy."""
        super().__init__("service_restart", "Restart failed service components")
        self.service_manager = service_manager
        self.last_restart = None
        self.restart_cooldown = timedelta(minutes=5)

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if service restart is appropriate."""
        if self.last_restart and datetime.now() - self.last_restart < self.restart_cooldown:
            return False
        return error_context.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute service restart."""
        try:
            logger.info(f"Executing service restart for {error_context.operation}")
            success = self.service_manager()
            if success:
                self.last_restart = datetime.now()
                logger.info(f"Service restart successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Service restart failed: {e}")
            return False


class ConfigurationResetStrategy(RecoveryStrategy):
    """Strategy for resetting configuration to defaults."""

    def __init__(self, config_reset_func: Callable):
        """Initialize configuration reset strategy."""
        super().__init__("config_reset", "Reset configuration to safe defaults")
        self.config_reset_func = config_reset_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if configuration reset is appropriate."""
        return (
            "config" in error_context.operation.lower()
            or error_context.severity == ErrorSeverity.CRITICAL
        )

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute configuration reset."""
        try:
            logger.info(f"Executing configuration reset for {error_context.operation}")
            success = self.config_reset_func()
            if success:
                logger.info(f"Configuration reset successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Configuration reset failed: {e}")
            return False


class ResourceCleanupStrategy(RecoveryStrategy):
    """Strategy for cleaning up stuck resources."""

    def __init__(self, cleanup_func: Callable):
        """Initialize resource cleanup strategy."""
        super().__init__("resource_cleanup", "Clean up stuck resources and locks")
        self.cleanup_func = cleanup_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if resource cleanup is appropriate."""
        error_data = str(error_context.additional_data).lower()
        return "resource" in error_data or "lock" in error_data

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute resource cleanup."""
        try:
            logger.info(f"Executing resource cleanup for {error_context.operation}")
            success = self.cleanup_func()
            if success:
                logger.info(f"Resource cleanup successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Resource cleanup failed: {e}")
            return False
