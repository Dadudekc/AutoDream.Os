#!/usr/bin/env python3
"""
Unified Logging Utility - V2 Compliant
======================================

This module provides a unified logging utility that consolidates all logging
patterns across the codebase, eliminating DRY violations.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate all logging patterns into unified utility
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


class UnifiedLoggingUtility:
    """
    Unified logging utility that consolidates all logging patterns.
    
    CONSOLIDATES:
    - Standard logging patterns
    - Custom logging configurations
    - Error logging patterns
    - Debug logging patterns
    - Info logging patterns
    - Warning logging patterns
    """
    
    _loggers: Dict[str, logging.Logger] = {}
    _configured = False
    
    @classmethod
    def configure_logging(cls, level: str = "INFO", log_file: Optional[str] = None) -> None:
        """
        Configure unified logging system.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
        """
        if cls._configured:
            return
        
        # Set up logging configuration
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if not cls._configured:
            cls.configure_logging()
        
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        
        return cls._loggers[name]
    
    @classmethod
    def log_info(cls, message: str, logger_name: str = None) -> None:
        """Log info message."""
        logger = cls.get_logger(logger_name or __name__)
        logger.info(message)
    
    @classmethod
    def log_warning(cls, message: str, logger_name: str = None) -> None:
        """Log warning message."""
        logger = cls.get_logger(logger_name or __name__)
        logger.warning(message)
    
    @classmethod
    def log_error(cls, message: str, logger_name: str = None) -> None:
        """Log error message."""
        logger = cls.get_logger(logger_name or __name__)
        logger.error(message)
    
    @classmethod
    def log_debug(cls, message: str, logger_name: str = None) -> None:
        """Log debug message."""
        logger = cls.get_logger(logger_name or __name__)
        logger.debug(message)
    
    @classmethod
    def log_critical(cls, message: str, logger_name: str = None) -> None:
        """Log critical message."""
        logger = cls.get_logger(logger_name or __name__)
        logger.critical(message)


# Convenience functions for backward compatibility
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return UnifiedLoggingUtility.get_logger(name)

def configure_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Configure unified logging system."""
    UnifiedLoggingUtility.configure_logging(level, log_file)