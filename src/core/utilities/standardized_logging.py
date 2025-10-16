"""
Standardized Logging - DUP-007 Logging Patterns Consolidation
============================================================

Simple, standardized logging utilities for the entire codebase.
Consolidates 419 logger assignments across 295 files.

**Usage (Simple):**
```python
from src.core.utilities.standardized_logging import get_logger

logger = get_logger(__name__)
logger.info("Simple standardized logging!")
```

**Usage (With Configuration):**
```python
from src.core.utilities.standardized_logging import LoggerFactory, LogLevel

factory = LoggerFactory(level=LogLevel.DEBUG, enable_file=True)
logger = factory.create_logger(__name__)
```

Author: Agent-2 (Architecture & Design Specialist) - DUP-007
License: MIT
"""

import logging
import sys
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class LogLevel(Enum):
    """Standard log levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class StandardizedFormatter(logging.Formatter):
    """Standardized log formatter with consistent format across codebase."""
    
    # Single consistent format for entire codebase
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self, use_colors: bool = False):
        """Initialize formatter.
        
        Args:
            use_colors: Enable colored output (for console only)
        """
        super().__init__(self.DEFAULT_FORMAT, self.DEFAULT_DATE_FORMAT)
        self.use_colors = use_colors and sys.stdout.isatty()
        
        # Color codes for different log levels
        self.colors = {
            logging.DEBUG: "\033[36m",     # Cyan
            logging.INFO: "\033[32m",      # Green
            logging.WARNING: "\033[33m",   # Yellow
            logging.ERROR: "\033[31m",     # Red
            logging.CRITICAL: "\033[35m",  # Magenta
        }
        self.reset = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with optional colors."""
        formatted = super().format(record)
        
        if self.use_colors and record.levelno in self.colors:
            color = self.colors[record.levelno]
            return f"{color}{formatted}{self.reset}"
        
        return formatted


class LoggerFactory:
    """Factory for creating standardized loggers with consistent configuration."""
    
    def __init__(
        self,
        level: LogLevel = LogLevel.INFO,
        enable_console: bool = True,
        enable_file: bool = False,
        log_dir: str = "logs",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        use_colors: bool = True
    ):
        """Initialize logger factory.
        
        Args:
            level: Default log level
            enable_console: Enable console output
            enable_file: Enable file output
            log_dir: Directory for log files
            max_file_size: Maximum size per log file
            backup_count: Number of backup files to keep
            use_colors: Enable colored console output
        """
        self.level = level
        self.enable_console = enable_console
        self.enable_file = enable_file
        self.log_dir = Path(log_dir)
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.use_colors = use_colors
        
        # Ensure log directory exists if file logging is enabled
        if self.enable_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def create_logger(self, name: str) -> logging.Logger:
        """Create standardized logger instance.
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Avoid adding duplicate handlers
        if logger.handlers:
            return logger
        
        logger.setLevel(self.level.value)
        logger.propagate = False  # Don't propagate to root logger
        
        # Add console handler
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level.value)
            console_handler.setFormatter(StandardizedFormatter(use_colors=self.use_colors))
            logger.addHandler(console_handler)
        
        # Add file handler with rotation
        if self.enable_file:
            log_file = self.log_dir / f"{name.replace('.', '_')}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self.max_file_size,
                backupCount=self.backup_count
            )
            file_handler.setLevel(self.level.value)
            file_handler.setFormatter(StandardizedFormatter(use_colors=False))
            logger.addHandler(file_handler)
        
        return logger


# Global factory instance for simple usage
_default_factory = LoggerFactory()


def get_logger(name: str) -> logging.Logger:
    """Get standardized logger instance (simple usage).
    
    This is the recommended way to get a logger in most files.
    
    Example:
        logger = get_logger(__name__)
        logger.info("Message")
    
    Args:
        name: Logger name (use __name__ for current module)
        
    Returns:
        Configured logger instance
    """
    return _default_factory.create_logger(name)


def configure_logging(
    level: LogLevel = LogLevel.INFO,
    enable_console: bool = True,
    enable_file: bool = False,
    log_dir: str = "logs",
    use_colors: bool = True
) -> None:
    """Configure global logging settings.
    
    Call this once at application startup to configure logging for entire app.
    
    Example:
        configure_logging(level=LogLevel.DEBUG, enable_file=True)
    
    Args:
        level: Global log level
        enable_console: Enable console output
        enable_file: Enable file output
        log_dir: Directory for log files
        use_colors: Enable colored console output
    """
    global _default_factory
    _default_factory = LoggerFactory(
        level=level,
        enable_console=enable_console,
        enable_file=enable_file,
        log_dir=log_dir,
        use_colors=use_colors
    )


# Backward compatibility aliases
setup_logger = get_logger  # Common pattern in existing code
create_logger = get_logger  # Another common pattern


__all__ = [
    "get_logger",
    "configure_logging",
    "LoggerFactory",
    "LogLevel",
    "StandardizedFormatter",
    # Backward compatibility
    "setup_logger",
    "create_logger",
]

