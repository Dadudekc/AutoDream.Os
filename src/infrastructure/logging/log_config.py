#!/usr/bin/env python3
"""
Log Configuration Module
========================

Logging configuration and enums extracted from unified_logger.py.

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

from dataclasses import dataclass
from enum import Enum


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
