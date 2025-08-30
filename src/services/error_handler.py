#!/usr/bin/env python3
"""Error handling utilities for centralized error management."""

import logging
from typing import Any, Callable, TypeVar, Optional
from functools import wraps

T = TypeVar('T')


class ErrorHandler:
    """Centralized error handling utilities to eliminate duplication."""
    
    @staticmethod
    def handle_operation(operation_name: str, logger: logging.Logger, default_return: Any = False):
        """Decorator for consistent error handling across operations."""
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"{operation_name} failed: {e}")
                    return default_return
            return wrapper
        return decorator
    
    @staticmethod
    def safe_execute(operation_name: str, logger: logging.Logger, func: Callable[..., T], 
                    *args, default_return: Any = False, **kwargs) -> T:
        """Safely execute a function with consistent error handling."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{operation_name} failed: {e}")
            return default_return
    
    @staticmethod
    def log_and_continue(operation_name: str, logger: logging.Logger, 
                        error: Exception, default_return: Any = False) -> Any:
        """Log error and return default value to continue execution."""
        logger.error(f"{operation_name} encountered error: {error}")
        return default_return
    
    @staticmethod
    def validate_required_args(agent_id: Optional[str], operation_name: str, logger: logging.Logger) -> bool:
        """Validate that required agent ID is provided."""
        if not agent_id:
            logger.error(f"❌ Agent ID required for {operation_name}. Use --agent Agent-X")
            return False
        return True
