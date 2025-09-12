"""
Standard Logger - Infrastructure Adapter
========================================

Concrete implementation of Logger using Python's logging module.
"""

import logging
from typing import Any

from ...domain.ports.logger import Logger, LogLevel


class StdLogger(Logger):
    """
    Standard library logger implementation.

    This adapter provides logging functionality using Python's built-in logging module.
    """

    def __init__(self, name: str = "domain"):
        """
        Initialize the logger.

        Args:
            name: Logger name for identification
        """
        self._logger = logging.getLogger(name)

    def _map_log_level(self, level: LogLevel) -> int:
        """Map domain LogLevel to logging module level."""
        mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        return mapping[level]

    def debug(self, message: str, **context: Any) -> None:

EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.logging.std_logger import Std_Logger

# Initialize and use
instance = Std_Logger()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Std_Logger(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """
        Log debug message.

        Args:
            message: Log message
            **context: Additional context data
        """
        self._logger.debug(message, extra=context)

    def info(self, message: str, **context: Any) -> None:
        """
        Log info message.

        Args:
            message: Log message
            **context: Additional context data
        """
        self._logger.info(message, extra=context)

    def warning(self, message: str, **context: Any) -> None:
        """
        Log warning message.

        Args:
            message: Log message
            **context: Additional context data
        """
        self._logger.warning(message, extra=context)

    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """
        Log error message.

        Args:
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        if exception:
            context["exception"] = str(exception)
        self._logger.error(message, extra=context)

    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """
        Log critical message.

        Args:
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        if exception:
            context["exception"] = str(exception)
        self._logger.critical(message, extra=context)

    def log(
        self, level: LogLevel, message: str, exception: Exception = None, **context: Any
    ) -> None:
        """
        Log message with specific level.

        Args:
            level: Log level
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        if exception:
            context["exception"] = str(exception)
        self._logger.log(self._map_log_level(level), message, extra=context)
