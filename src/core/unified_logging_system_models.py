#!/usr/bin/env python3
"""
Unified Logging System Models - V2 Compliance Module
===================================================

Data models for unified logging system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime


class LogLevel(Enum):
    """Standardized log levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class LogEntry:
    """Log entry data structure."""
    level: LogLevel
    message: str
    timestamp: datetime
    module: str
    function: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: LogLevel = LogLevel.INFO
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    enable_file_logging: bool = True
    enable_console_logging: bool = True
    log_file_path: str = "logs/system.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
