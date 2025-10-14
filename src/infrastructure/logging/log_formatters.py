#!/usr/bin/env python3
"""
Log Formatters Module
====================

Logging formatters extracted from unified_logger.py for better modularity.

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import logging


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


class PlainFormatter(logging.Formatter):
    """Plain logging formatter without colors (for files)."""

    def __init__(self, fmt: str, datefmt: str):
        """Initialize plain formatter."""
        super().__init__(fmt, datefmt)
