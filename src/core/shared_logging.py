#!/usr/bin/env python3
"""
Shared Logging Utilities
========================

Centralized logging configuration and utilities for the Agent Cellphone V2 system.
Eliminates duplicate logging setup across the project.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import sys
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime


class SharedLogger:
    """Shared logging configuration and utilities."""
    
    _configured = False
    _loggers: Dict[str, logging.Logger] = {}
    
    @classmethod
    def configure_logging(
        cls,
        level: str = "INFO",
        log_file: Optional[Path] = None,
        format_string: Optional[str] = None
    ) -> None:
        """Configure logging for the entire application."""
        if cls._configured:
            return
            
        # Default format
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=format_string,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Add file handler if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(format_string))
            logging.getLogger().addHandler(file_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a logger instance for a module."""
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        return cls._loggers[name]
    
    @classmethod
    def log_function_call(
        cls,
        logger: logging.Logger,
        function_name: str,
        args: Optional[Dict[str, Any]] = None,
        level: str = "DEBUG"
    ) -> None:
        """Log function call with arguments."""
        log_level = getattr(logging, level.upper())
        if args:
            logger.log(log_level, f"Calling {function_name} with args: {args}")
        else:
            logger.log(log_level, f"Calling {function_name}")
    
    @classmethod
    def log_error_with_context(
        cls,
        logger: logging.Logger,
        error: Exception,
        context: str,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log error with context and additional information."""
        error_msg = f"Error in {context}: {str(error)}"
        if additional_info:
            error_msg += f" | Additional info: {additional_info}"
        logger.error(error_msg, exc_info=True)
    
    @classmethod
    def log_performance(
        cls,
        logger: logging.Logger,
        operation: str,
        duration: float,
        additional_metrics: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log performance metrics."""
        perf_msg = f"Performance: {operation} took {duration:.3f}s"
        if additional_metrics:
            perf_msg += f" | Metrics: {additional_metrics}"
        logger.info(perf_msg)


def get_module_logger(module_name: str) -> logging.Logger:
    """Convenience function to get a logger for a module."""
    return SharedLogger.get_logger(module_name)


def log_function_entry(logger: logging.Logger, function_name: str, **kwargs) -> None:
    """Log function entry with keyword arguments."""
    SharedLogger.log_function_call(logger, function_name, kwargs, "DEBUG")


def log_function_exit(logger: logging.Logger, function_name: str, result: Any = None) -> None:
    """Log function exit with optional result."""
    if result is not None:
        logger.debug(f"Exiting {function_name} with result: {result}")
    else:
        logger.debug(f"Exiting {function_name}")


def log_error(logger: logging.Logger, error: Exception, context: str, **kwargs) -> None:
    """Log error with context and keyword arguments."""
    SharedLogger.log_error_with_context(logger, error, context, kwargs)


def log_performance(logger: logging.Logger, operation: str, duration: float, **kwargs) -> None:
    """Log performance metrics with keyword arguments."""
    SharedLogger.log_performance(logger, operation, duration, kwargs)


# Initialize logging for the application
SharedLogger.configure_logging()
