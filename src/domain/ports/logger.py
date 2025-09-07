"""
Logger Port - Domain Interface
==============================

Defines the contract for logging operations.
This enables domain objects to log events without depending on specific logging frameworks.
"""

from typing import Protocol, Any
from enum import Enum


class LogLevel(Enum):
    """Log levels for different types of messages."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger(Protocol):
    """
    Port for logging operations.

    This protocol allows domain objects to log events and debug information
    without depending on specific logging implementations.
    """

    def debug(self, message: str, **context: Any) -> None:
        """
        Log debug message.

        Args:
            message: Log message
            **context: Additional context data
        """
        ...

    def info(self, message: str, **context: Any) -> None:
        """
        Log info message.

        Args:
            message: Log message
            **context: Additional context data
        """
        ...

    def warning(self, message: str, **context: Any) -> None:
        """
        Log warning message.

        Args:
            message: Log message
            **context: Additional context data
        """
        ...

    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """
        Log error message.

        Args:
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        ...

    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """
        Log critical message.

        Args:
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        ...

    def log(self, level: LogLevel, message: str, exception: Exception = None, **context: Any) -> None:
        """
        Log message with specific level.

        Args:
            level: Log level
            message: Log message
            exception: Optional exception object
            **context: Additional context data
        """
        ...
