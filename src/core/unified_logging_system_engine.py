#!/usr/bin/env python3
"""
Unified Logging System Engine - V2 Compliance Module
===================================================

Core engine logic for unified logging system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from .unified_logging_system_models import LogLevel, LogEntry, LoggingConfig


class LoggingTemplates:
    """Unified logging message templates."""
    
    @staticmethod
    def operation_start(operation: str, module: str = "Unknown") -> str:
        """Template for operation start."""
        return f"🚀 {operation} started in {module}"
    
    @staticmethod
    def operation_complete(operation: str, module: str = "Unknown", duration: float = 0.0) -> str:
        """Template for operation completion."""
        return f"✅ {operation} completed in {module} (Duration: {duration:.2f}s)"
    
    @staticmethod
    def operation_failed(operation: str, module: str = "Unknown", error: str = "Unknown error") -> str:
        """Template for operation failure."""
        return f"❌ {operation} failed in {module}: {error}"
    
    @staticmethod
    def data_processed(record_count: int, data_type: str = "records") -> str:
        """Template for data processing."""
        return f"📊 Processed {record_count} {data_type}"
    
    @staticmethod
    def validation_passed(validation_type: str) -> str:
        """Template for validation success."""
        return f"✅ {validation_type} validation passed"
    
    @staticmethod
    def validation_failed(validation_type: str, error: str = "Validation failed") -> str:
        """Template for validation failure."""
        return f"❌ {validation_type} validation failed: {error}"


class UnifiedLoggingEngine:
    """Core engine for unified logging operations."""
    
    def __init__(self, config: LoggingConfig = None):
        """Initialize logging engine."""
        self.config = config or LoggingConfig()
        self.logger = self._setup_logger()
        self.templates = LoggingTemplates()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with configuration."""
        logger = logging.getLogger("unified_logging")
        logger.setLevel(getattr(logging, self.config.level.value.upper()))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler
        if self.config.enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.config.level.value.upper()))
            console_formatter = logging.Formatter(self.config.format_string)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # File handler
        if self.config.enable_file_logging:
            file_handler = logging.FileHandler(self.config.log_file_path)
            file_handler.setLevel(getattr(logging, self.config.level.value.upper()))
            file_formatter = logging.Formatter(self.config.format_string)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def log(self, level: LogLevel, message: str, module: str = "Unknown", 
            function: str = "Unknown", metadata: Dict[str, Any] = None):
        """Log a message with specified level."""
        log_entry = LogEntry(
            level=level,
            message=message,
            timestamp=datetime.now(),
            module=module,
            function=function,
            metadata=metadata or {}
        )
        
        log_method = getattr(self.logger, level.value.lower())
        log_method(f"[{module}.{function}] {message}")
    
    def debug(self, message: str, module: str = "Unknown", function: str = "Unknown", **kwargs):
        """Log debug message."""
        self.log(LogLevel.DEBUG, message, module, function, kwargs)
    
    def info(self, message: str, module: str = "Unknown", function: str = "Unknown", **kwargs):
        """Log info message."""
        self.log(LogLevel.INFO, message, module, function, kwargs)
    
    def warning(self, message: str, module: str = "Unknown", function: str = "Unknown", **kwargs):
        """Log warning message."""
        self.log(LogLevel.WARNING, message, module, function, kwargs)
    
    def error(self, message: str, module: str = "Unknown", function: str = "Unknown", **kwargs):
        """Log error message."""
        self.log(LogLevel.ERROR, message, module, function, kwargs)
    
    def critical(self, message: str, module: str = "Unknown", function: str = "Unknown", **kwargs):
        """Log critical message."""
        self.log(LogLevel.CRITICAL, message, module, function, kwargs)
