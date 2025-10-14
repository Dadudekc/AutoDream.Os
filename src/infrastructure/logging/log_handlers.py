#!/usr/bin/env python3
"""
Log Handlers Module
==================

Logging handlers and setup logic extracted from unified_logger.py.

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .log_config import LoggingConfig

from .log_formatters import ColorFormatter, PlainFormatter


class LogHandlerFactory:
    """Factory for creating logging handlers."""

    @staticmethod
    def create_console_handler(config: "LoggingConfig") -> logging.Handler:
        """Create console (stdout) handler with color formatting."""
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = ColorFormatter(config.format, config.date_format, config.enable_colors)
        console_handler.setFormatter(formatter)
        return console_handler

    @staticmethod
    def create_file_handler(config: "LoggingConfig") -> logging.Handler:
        """Create rotating file handler with plain formatting."""
        # Ensure log directory exists
        log_dir = Path(config.log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Rotating file handler
        file_handler = RotatingFileHandler(
            config.log_file,
            maxBytes=config.max_file_size,
            backupCount=config.backup_count,
        )

        # Plain formatter for files (no colors)
        formatter = PlainFormatter(config.format, config.date_format)
        file_handler.setFormatter(formatter)

        return file_handler


class LogHandlerManager:
    """Manages logging handlers for a logger instance."""

    def __init__(self, logger: logging.Logger, config: "LoggingConfig"):
        """Initialize handler manager."""
        self.logger = logger
        self.config = config
        self._handlers: list[logging.Handler] = []

    def setup_handlers(self) -> None:
        """Setup logging handlers based on configuration."""
        # Clear existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        self._handlers.clear()

        # Add console handler
        if self.config.console_enabled:
            console_handler = LogHandlerFactory.create_console_handler(self.config)
            self.logger.addHandler(console_handler)
            self._handlers.append(console_handler)

        # Add file handler
        if self.config.file_enabled:
            file_handler = LogHandlerFactory.create_file_handler(self.config)
            self.logger.addHandler(file_handler)
            self._handlers.append(file_handler)

    def get_handlers(self) -> list[logging.Handler]:
        """Get list of active handlers."""
        return self._handlers.copy()

    def remove_all_handlers(self) -> None:
        """Remove all handlers from the logger."""
        for handler in self._handlers:
            self.logger.removeHandler(handler)
        self._handlers.clear()
