#!/usr/bin/env python3
"""
Enhanced Logging System - Agent Cellphone V2
===========================================

V2 compliant logging infrastructure with structured logging,
performance monitoring, and configurable outputs.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import logging.config
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class V2Logger:
    """V2 compliant logger with enhanced capabilities."""

    def __init__(self, name: str, log_level: str = "INFO", log_to_file: bool = True):
        """Initialize V2 logger.

        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to file in addition to console
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Console handler with structured format
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for persistent logging
        if log_to_file:
            self._setup_file_handler()

        # Prevent duplicate messages from parent loggers
        self.logger.propagate = False

    def _setup_file_handler(self):
        """Setup file handler for persistent logging."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        self._log(logging.DEBUG, message, extra)

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message."""
        self._log(logging.INFO, message, extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        self._log(logging.WARNING, message, extra)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log error message."""
        self._log(logging.ERROR, message, extra)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log critical message."""
        self._log(logging.CRITICAL, message, extra)

    def _log(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
        """Internal logging method."""
        if extra:
            # Add extra fields to log record
            extra_fields = {'extra_fields': extra}
            self.logger.log(level, message, extra=extra_fields)
        else:
            self.logger.log(level, message)


# Global logger instances for different components
_messaging_logger = None
_contract_logger = None
_core_logger = None


def get_messaging_logger() -> V2Logger:
    """Get messaging system logger."""
    global _messaging_logger
    if _messaging_logger is None:
        _messaging_logger = V2Logger("messaging", log_level="INFO")
    return _messaging_logger


def get_contract_logger() -> V2Logger:
    """Get contract system logger."""
    global _contract_logger
    if _contract_logger is None:
        _contract_logger = V2Logger("contract", log_level="INFO")
    return _contract_logger


def get_core_logger() -> V2Logger:
    """Get core system logger."""
    global _core_logger
    if _core_logger is None:
        _core_logger = V2Logger("core", log_level="INFO")
    return _core_logger


def get_logger(name: str, log_level: str = "INFO") -> V2Logger:
    """Get a configured V2 logger with the given name.

    Args:
        name: Logger name
        log_level: Logging level

    Returns:
        V2Logger: Configured logger instance
    """
    return V2Logger(name, log_level)
