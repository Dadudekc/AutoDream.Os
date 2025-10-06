#!/usr/bin/env python3
"""
Unified Logging System - V2 Compliance
=====================================

Centralized logging system for the Agent Cellphone V2 project.
Provides consistent logging across all modules.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


class UnifiedLoggingSystem:
    """Unified logging system for the project."""

    def __init__(self):
        """Initialize the unified logging system."""
        self._loggers = {}
        self._configured = False

    def configure(self,
                  level: str = "INFO",
                  log_file: Optional[Path] = None,
                  format_string: Optional[str] = None) -> None:
        """Configure the logging system."""
        if self._configured:
            return

        # Set up basic configuration
        log_level = getattr(logging, level.upper(), logging.INFO)

        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=format_string,
            handlers=self._get_handlers(log_file)
        )

        self._configured = True

    def _get_handlers(self, log_file: Optional[Path] = None) -> list:
        """Get logging handlers."""
        handlers = []

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        # File handler if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            handlers.append(file_handler)

        return handlers

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance."""
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)
        return self._loggers[name]


# Global logging system instance
_logging_system = UnifiedLoggingSystem()


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return _logging_system.get_logger(name)


def configure_logging(level: str = "INFO",
                     log_file: Optional[Path] = None,
                     format_string: Optional[str] = None) -> None:
    """Configure the unified logging system."""
    _logging_system.configure(level, log_file, format_string)


def get_logging_system() -> UnifiedLoggingSystem:
    """Get the global logging system instance."""
    return _logging_system
