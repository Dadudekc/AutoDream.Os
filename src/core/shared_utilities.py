"""
Shared Utilities - Core Manager Utilities
==========================================

Shared utility classes for manager components implementing SSOT principles.
Provides common functionality for cleanup, configuration, error handling, etc.

Author: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic
from datetime import datetime

# Type variables for generic utilities
T = TypeVar('T')


class BaseUtility(ABC):
    """Base class for all shared utilities."""

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the utility."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up resources."""
        pass


class CleanupManager(BaseUtility):
    """Manages cleanup operations for managers."""

    def __init__(self):
        super().__init__()
        self.cleanup_handlers = []

    def initialize(self) -> bool:
        """Initialize cleanup manager."""
        self.logger.info("CleanupManager initialized")
        return True

    def cleanup(self) -> bool:
        """Execute all registered cleanup handlers."""
        success = True
        for handler in reversed(self.cleanup_handlers):
            try:
                handler()
            except Exception as e:
                self.logger.error(f"Cleanup handler failed: {e}")
                success = False
        self.cleanup_handlers.clear()
        return success

    def register_handler(self, handler: callable) -> None:
        """Register a cleanup handler."""
        self.cleanup_handlers.append(handler)


class ConfigurationManager(BaseUtility):
    """Manages configuration for managers."""

    def __init__(self):
        super().__init__()
        self.config = {}

    def initialize(self) -> bool:
        """Initialize configuration manager."""
        self.logger.info("ConfigurationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up configuration resources."""
        self.config.clear()
        return True

    def set_config(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)


class ErrorHandler(BaseUtility):
    """Handles errors for managers."""

    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.last_error = None

    def initialize(self) -> bool:
        """Initialize error handler."""
        self.logger.info("ErrorHandler initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up error handler resources."""
        self.error_count = 0
        self.last_error = None
        return True

    def handle_error(self, error: Exception, context: str = None) -> bool:
        """Handle an error."""
        self.error_count += 1
        self.last_error = error
        self.logger.error(f"Error in {context or 'unknown'}: {error}")
        return True

    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return {
            'error_count': self.error_count,
            'last_error': str(self.last_error) if self.last_error else None
        }


class InitializationManager(BaseUtility):
    """Manages initialization operations."""

    def __init__(self):
        super().__init__()
        self.initialized = False
        self.init_time = None

    def initialize(self) -> bool:
        """Initialize the initialization manager."""
        if not self.initialized:
            self.initialized = True
            self.init_time = datetime.now()
            self.logger.info("InitializationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up initialization resources."""
        self.initialized = False
        self.init_time = None
        return True

    def is_initialized(self) -> bool:
        """Check if initialized."""
        return self.initialized

    def get_init_time(self) -> Optional[datetime]:
        """Get initialization time."""
        return self.init_time


class LoggingManager(BaseUtility):
    """Manages logging for managers."""

    def __init__(self):
        super().__init__()
        self.log_level = logging.INFO

    def initialize(self) -> bool:
        """Initialize logging manager."""
        logging.basicConfig(level=self.log_level)
        self.logger.info("LoggingManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up logging resources."""
        return True

    def set_log_level(self, level: int) -> None:
        """Set logging level."""
        self.log_level = level
        logging.getLogger().setLevel(level)

    def log_info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)


class ResultManager(BaseUtility, Generic[T]):
    """Manages results for operations."""

    def __init__(self):
        super().__init__()
        self.results = []
        self.last_result = None

    def initialize(self) -> bool:
        """Initialize result manager."""
        self.logger.info("ResultManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up result resources."""
        self.results.clear()
        self.last_result = None
        return True

    def add_result(self, result: T) -> None:
        """Add a result."""
        self.results.append(result)
        self.last_result = result

    def get_results(self) -> list[T]:
        """Get all results."""
        return self.results.copy()

    def get_last_result(self) -> Optional[T]:
        """Get last result."""
        return self.last_result

    def clear_results(self) -> None:
        """Clear all results."""
        self.results.clear()
        self.last_result = None


class StatusManager(BaseUtility):
    """Manages status for managers."""

    def __init__(self):
        super().__init__()
        self.status = "initialized"
        self.status_history = []

    def initialize(self) -> bool:
        """Initialize status manager."""
        self.set_status("initialized")
        self.logger.info("StatusManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up status resources."""
        self.status_history.clear()
        return True

    def set_status(self, status: str) -> None:
        """Set current status."""
        old_status = self.status
        self.status = status
        timestamp = datetime.now()

        self.status_history.append({
            'timestamp': timestamp,
            'old_status': old_status,
            'new_status': status
        })

        self.logger.info(f"Status changed: {old_status} -> {status}")

    def get_status(self) -> str:
        """Get current status."""
        return self.status

    def get_status_history(self) -> list:
        """Get status history."""
        return self.status_history.copy()


class ValidationManager(BaseUtility):
    """Manages validation operations."""

    def __init__(self):
        super().__init__()
        self.validation_rules = {}
        self.validation_results = []

    def initialize(self) -> bool:
        """Initialize validation manager."""
        self.logger.info("ValidationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up validation resources."""
        self.validation_rules.clear()
        self.validation_results.clear()
        return True

    def add_validation_rule(self, name: str, rule: callable) -> None:
        """Add a validation rule."""
        self.validation_rules[name] = rule

    def validate(self, data: Any) -> Dict[str, Any]:
        """Validate data against all rules."""
        results = {}

        for name, rule in self.validation_rules.items():
            try:
                result = rule(data)
                results[name] = result
            except Exception as e:
                results[name] = f"Validation error: {e}"

        self.validation_results.append({
            'timestamp': datetime.now(),
            'data': str(data),
            'results': results
        })

        return results

    def get_validation_results(self) -> list:
        """Get validation results history."""
        return self.validation_results.copy()


# Convenience functions for creating utility instances
def create_cleanup_manager() -> CleanupManager:
    """Create a new cleanup manager instance."""
    return CleanupManager()


def create_configuration_manager() -> ConfigurationManager:
    """Create a new configuration manager instance."""
    return ConfigurationManager()


def create_error_handler() -> ErrorHandler:
    """Create a new error handler instance."""
    return ErrorHandler()


def create_initialization_manager() -> InitializationManager:
    """Create a new initialization manager instance."""
    return InitializationManager()


def create_logging_manager() -> LoggingManager:
    """Create a new logging manager instance."""
    return LoggingManager()


def create_result_manager() -> ResultManager:
    """Create a new result manager instance."""
    return ResultManager()


def create_status_manager() -> StatusManager:
    """Create a new status manager instance."""
    return StatusManager()


def create_validation_manager() -> ValidationManager:
    """Create a new validation manager instance."""
    return ValidationManager()


__all__ = [
    'BaseUtility',
    'CleanupManager',
    'ConfigurationManager',
    'ErrorHandler',
    'InitializationManager',
    'LoggingManager',
    'ResultManager',
    'StatusManager',
    'ValidationManager',
    # Factory functions
    'create_cleanup_manager',
    'create_configuration_manager',
    'create_error_handler',
    'create_initialization_manager',
    'create_logging_manager',
    'create_result_manager',
    'create_status_manager',
    'create_validation_manager',
]
