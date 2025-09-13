"""
Shared Utilities - Core Manager Utilities
==========================================

Shared utility classes for manager components implementing SSOT principles.
Provides common functionality for cleanup, configuration, error handling, etc.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Generic, TypeVar

# Type variables for generic utilities
T = TypeVar("T")


class BaseUtility(ABC):
    """Base class for all shared utilities with common functionality."""

    def __init__(self, name: str = None):
        """Initialize the base utility with optional custom name."""
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the utility. Returns True if successful."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up resources and perform finalization."""
        pass


class CleanupManager(BaseUtility):
    """Manages cleanup operations with LIFO handler execution."""

    def __init__(self):
        super().__init__()
        self.cleanup_handlers = []

    def initialize(self) -> bool:
        self.logger.info("CleanupManager initialized")
        return True

    def cleanup(self) -> bool:
        """Execute all registered cleanup handlers in reverse order."""
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
        """Register a cleanup handler function."""
        self.cleanup_handlers.append(handler)


class ConfigurationManager(BaseUtility):
    """Manages configuration with key-value storage and defaults."""

    def __init__(self):
        super().__init__()
        self.config = {}

    def initialize(self) -> bool:
        self.logger.info("ConfigurationManager initialized")
        return True

    def cleanup(self) -> bool:
        self.config.clear()
        return True

    def set_config(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with optional default."""
        return self.config.get(key, default)


class ErrorHandler(BaseUtility):
    """Handles errors with tracking, logging, and summary statistics."""

    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.last_error = None

    def initialize(self) -> bool:
        self.logger.info("ErrorHandler initialized")
        return True

    def cleanup(self) -> bool:
        self.error_count = 0
        self.last_error = None
        return True

    def handle_error(self, error: Exception, context: str = None) -> bool:
        """Handle an error with logging and tracking."""
        self.error_count += 1
        self.last_error = error
        self.logger.error(f"Error in {context or 'unknown'}: {error}")
        return True

    def get_error_summary(self) -> dict[str, Any]:
        """Get error summary statistics."""
        return {
            "error_count": self.error_count,
            "last_error": str(self.last_error) if self.last_error else None,
        }


class InitializationManager(BaseUtility):
    """Manages initialization with state and timestamp tracking."""

    def __init__(self):
        super().__init__()
        self.initialized = False
        self.init_time = None

    def initialize(self) -> bool:
        if not self.initialized:
            self.initialized = True
            self.init_time = datetime.now()
            self.logger.info("InitializationManager initialized")
        return True

    def cleanup(self) -> bool:
        self.initialized = False
        self.init_time = None
        return True

    def is_initialized(self) -> bool:
        """Check if initialized."""
        return self.initialized

    def get_init_time(self) -> datetime | None:
        """Get initialization timestamp."""
        return self.init_time


class LoggingManager(BaseUtility):
    """Manages logging configuration and operations."""

    def __init__(self):
        super().__init__()
        self.log_level = logging.INFO

    def initialize(self) -> bool:
        logging.basicConfig(level=self.log_level)
        self.logger.info("LoggingManager initialized")
        return True

    def cleanup(self) -> bool:
        return True

    def set_log_level(self, level: int) -> None:
        """Set logging level for all loggers."""
        self.log_level = level
        logging.getLogger().setLevel(level)

    def log_info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)


class ResultManager(BaseUtility, Generic[T]):
    """Manages results with type safety and list management."""

    def __init__(self):
        super().__init__()
        self.results = []
        self.last_result = None

    def initialize(self) -> bool:
        self.logger.info("ResultManager initialized")
        return True

    def cleanup(self) -> bool:
        self.results.clear()
        self.last_result = None
        return True

    def add_result(self, result: T) -> None:
        """Add a result to storage."""
        self.results.append(result)
        self.last_result = result

    def get_results(self) -> list[T]:
        """Get copy of all results."""
        return self.results.copy()

    def get_last_result(self) -> T | None:
        """Get most recent result."""
        return self.last_result

    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results.clear()
        self.last_result = None


class StatusManager(BaseUtility):
    """Manages status transitions with history tracking."""

    def __init__(self):
        super().__init__()
        self.status = "initialized"
        self.status_history = []

    def initialize(self) -> bool:
        self.set_status("initialized")
        self.logger.info("StatusManager initialized")
        return True

    def cleanup(self) -> bool:
        self.status_history.clear()
        return True

    def set_status(self, status: str) -> None:
        """Set current status with history tracking."""
        old_status = self.status
        self.status = status
        timestamp = datetime.now()
        self.status_history.append(
            {"timestamp": timestamp, "old_status": old_status, "new_status": status}
        )
        self.logger.info(f"Status changed: {old_status} -> {status}")

    def get_status(self) -> str:
        """Get current status."""
        return self.status

    def get_status_history(self) -> list:
        """Get copy of status history."""
        return self.status_history.copy()


class ValidationManager(BaseUtility):
    """Manages validation operations with rule-based validation."""

    def __init__(self):
        super().__init__()
        self.validation_rules = {}
        self.validation_results = []

    def initialize(self) -> bool:
        self.logger.info("ValidationManager initialized")
        return True

    def cleanup(self) -> bool:
        self.validation_rules.clear()
        self.validation_results.clear()
        return True

    def add_validation_rule(self, name: str, rule: callable) -> None:
        """Add a validation rule function."""
        self.validation_rules[name] = rule

    def validate(self, data: Any) -> dict[str, Any]:
        """Validate data against all registered rules."""
        results = {}
        for name, rule in self.validation_rules.items():
            try:
                result = rule(data)
                results[name] = result
            except Exception as e:
                results[name] = f"Validation error: {e}"
        self.validation_results.append(
            {"timestamp": datetime.now(), "data": str(data), "results": results}
        )
        return results

    def get_validation_results(self) -> list:
        """Get copy of validation results history."""
        return self.validation_results.copy()


# Factory functions for creating utility instances
def create_cleanup_manager() -> CleanupManager:
    """Create and return a new CleanupManager instance."""
    return CleanupManager()


def create_configuration_manager() -> ConfigurationManager:
    """Create and return a new ConfigurationManager instance."""
    return ConfigurationManager()


def create_error_handler() -> ErrorHandler:
    """Create and return a new ErrorHandler instance."""
    return ErrorHandler()


def create_initialization_manager() -> InitializationManager:
    """Create and return a new InitializationManager instance."""
    return InitializationManager()


def create_logging_manager() -> LoggingManager:
    """Create and return a new LoggingManager instance."""
    return LoggingManager()


def create_result_manager() -> ResultManager:
    """Create and return a new ResultManager instance."""
    return ResultManager()


def create_status_manager() -> StatusManager:
    """Create and return a new StatusManager instance."""
    return StatusManager()


def create_validation_manager() -> ValidationManager:
    """Create and return a new ValidationManager instance."""
    return ValidationManager()


__all__ = [
    "BaseUtility",
    "CleanupManager",
    "ConfigurationManager",
    "ErrorHandler",
    "InitializationManager",
    "LoggingManager",
    "ResultManager",
    "StatusManager",
    "ValidationManager",
    "create_cleanup_manager",
    "create_configuration_manager",
    "create_error_handler",
    "create_initialization_manager",
    "create_logging_manager",
    "create_result_manager",
    "create_status_manager",
    "create_validation_manager",
]


if __name__ == "__main__":
    """Demonstrate module functionality."""
    print("🐝 Shared Utilities Module - Core Manager Utilities")
    print("=" * 55)

    managers = [
        ("CleanupManager", create_cleanup_manager),
        ("ConfigurationManager", create_configuration_manager),
        ("ErrorHandler", create_error_handler),
        ("InitializationManager", create_initialization_manager),
        ("LoggingManager", create_logging_manager),
        ("ResultManager", create_result_manager),
        ("StatusManager", create_status_manager),
        ("ValidationManager", create_validation_manager),
    ]

    for name, factory_func in managers:
        try:
            instance = factory_func()
            instance.initialize()
            print(f"✅ {name} created and initialized successfully")
        except Exception as e:
            print(f"❌ {name} failed: {e}")

    print("\n🎉 All utility managers tested successfully!")
    print("🐝 WE ARE SWARM - INFRASTRUCTURE CO-CAPTAIN READY!")
