#!/usr/bin/env python3
"""
Unified Logger - V2 Compliance Module
=====================================

Logging functionality extracted from unified_logging_time.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Enumeration of log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LoggingConfig:
    """Configuration for logging operations."""

    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    console_enabled: bool = True
    file_enabled: bool = True
    log_file: str = "logs/unified.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_colors: bool = True


class LoggerInterface(ABC):
    """Abstract interface for logging operations."""

    @abstractmethod
    def debug(self, message: str, **context: Any) -> None:
        """Log debug message."""
        pass

    @abstractmethod
    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        pass

    @abstractmethod
    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        pass

    @abstractmethod
    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log error message."""
        pass

    @abstractmethod
    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log critical message."""
        pass

    @abstractmethod
    def log(
        self, level: LogLevel, message: str, exception: Exception = None, **context: Any
    ) -> None:
        """Log message with specific level."""
        pass


class ColorFormatter(logging.Formatter):
    """Logging formatter with color support."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def __init__(self, fmt: str, datefmt: str, use_colors: bool = True):
        """Initialize color formatter."""
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with optional colors."""
        if self.use_colors and record.levelname in self.COLORS:
            colored_level = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
            )
            record.levelname = colored_level

        return super().format(record)


class UnifiedLogger(LoggerInterface):
    """Unified logger implementation combining multiple logging targets."""

    def __init__(self, name: str, config: LoggingConfig):
        """Initialize unified logger."""
        self.name = name
        self.config = config
        self._logger = logging.getLogger(name)

        # Prevent duplicate handlers
        if self._logger.handlers:
            self._logger.handlers.clear()

        # Set log level
        level_mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        self._logger.setLevel(level_mapping[config.level])

        # Add handlers
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup logging handlers based on configuration."""
        formatter = ColorFormatter(
            self.config.format, self.config.date_format, self.config.enable_colors
        )

        # Console handler
        if self.config.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

        # File handler
        if self.config.file_enabled:
            # Ensure log directory exists
            log_dir = Path(self.config.log_file).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            # Rotating file handler
            file_handler = RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count,
            )
            file_handler.setFormatter(
                ColorFormatter(
                    self.config.format,
                    self.config.date_format,
                    False,  # No colors in log files
                )
            )
            self._logger.addHandler(file_handler)

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
        """Log debug message."""
        self._logger.debug(message, extra=context)

    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        self._logger.info(message, extra=context)

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        self._logger.warning(message, extra=context)

    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log error message."""
        if exception:
            context["exception"] = str(exception)
        self._logger.error(message, extra=context)

    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log critical message."""
        if exception:
            context["exception"] = str(exception)
        self._logger.critical(message, extra=context)

    def log(
        self, level: LogLevel, message: str, exception: Exception = None, **context: Any
    ) -> None:
        """Log message with specific level."""
        if exception:
            context["exception"] = str(exception)
        self._logger.log(self._map_log_level(level), message, extra=context)


class LogStatistics:
    """Provides statistics about logging operations."""

    def __init__(self, logger: UnifiedLogger):
        """Initialize log statistics."""
        self.logger = logger
        self.stats: dict[str, int] = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }

    def increment_stat(self, level: str) -> None:
        """Increment statistics for a log level."""
        if level.lower() in self.stats:
            self.stats[level.lower()] += 1

    def get_stats(self) -> dict[str, int]:
        """Get logging statistics."""
        return self.stats.copy()

    def reset_stats(self) -> None:
        """Reset all statistics."""
        for key in self.stats:
            self.stats[key] = 0
