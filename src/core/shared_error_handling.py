#!/usr/bin/env python3
"""
Shared Error Handling Utilities
===============================

Centralized error handling patterns for the Agent Cellphone V2 system.
Eliminates duplicate error handling logic across the project.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import traceback
from typing import Any, Dict, Optional, Callable, Type, Union
from functools import wraps
from .shared_logging import get_module_logger

logger = get_module_logger(__name__)


class SharedErrorHandler:
    """Shared error handling utilities."""
    
    @staticmethod
    def handle_discord_interaction_error(
        interaction: Any,
        error: Exception,
        context: str = "Discord interaction",
        user_message: str = "❌ An error occurred while processing your request."
    ) -> None:
        """Handle Discord interaction errors with user feedback."""
        logger.error(f"Error in {context}: {error}", exc_info=True)
        
        try:
            if hasattr(interaction, 'response') and not interaction.response.is_done():
                interaction.response.send_message(user_message, ephemeral=True)
            elif hasattr(interaction, 'followup'):
                interaction.followup.send(user_message, ephemeral=True)
        except Exception as followup_error:
            logger.error(f"Failed to send error response: {followup_error}")
    
    @staticmethod
    def handle_database_error(
        error: Exception,
        operation: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle database errors with context."""
        error_context = f"Database operation: {operation}"
        if context:
            error_context += f" | Context: {context}"
        
        logger.error(f"Database error in {error_context}: {error}", exc_info=True)
    
    @staticmethod
    def handle_network_error(
        error: Exception,
        endpoint: str,
        method: str = "GET",
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle network errors with context."""
        error_context = f"Network request: {method} {endpoint}"
        if context:
            error_context += f" | Context: {context}"
        
        logger.error(f"Network error in {error_context}: {error}", exc_info=True)
    
    @staticmethod
    def handle_file_operation_error(
        error: Exception,
        operation: str,
        file_path: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle file operation errors with context."""
        error_context = f"File operation: {operation} on {file_path}"
        if context:
            error_context += f" | Context: {context}"
        
        logger.error(f"File operation error in {error_context}: {error}", exc_info=True)
    
    @staticmethod
    def handle_validation_error(
        error: Exception,
        field_name: str,
        value: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle validation errors with context."""
        error_context = f"Validation error for field: {field_name}"
        if context:
            error_context += f" | Context: {context}"
        
        logger.error(f"Validation error in {error_context}: {error}")
        logger.debug(f"Invalid value: {value}")


def error_handler(
    error_types: Union[Type[Exception], tuple] = Exception,
    default_return: Any = None,
    log_error: bool = True,
    reraise: bool = False
):
    """Decorator for handling errors in functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types as e:
                if log_error:
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                
                if reraise:
                    raise
                
                return default_return
            except Exception as e:
                if log_error:
                    logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
                
                if reraise:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    error_context: str = "Function execution",
    **kwargs
) -> Any:
    """Safely execute a function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {error_context}: {e}", exc_info=True)
        return default_return


def handle_async_error(
    error: Exception,
    context: str,
    additional_info: Optional[Dict[str, Any]] = None
) -> None:
    """Handle async operation errors."""
    error_msg = f"Async error in {context}: {error}"
    if additional_info:
        error_msg += f" | Additional info: {additional_info}"
    
    logger.error(error_msg, exc_info=True)


def create_error_response(
    error: Exception,
    user_friendly_message: str = "An error occurred. Please try again.",
    include_details: bool = False
) -> Dict[str, Any]:
    """Create a standardized error response."""
    response = {
        "success": False,
        "error": user_friendly_message,
        "timestamp": logger.handlers[0].formatter.formatTime(
            logger.makeRecord("", 0, "", 0, "", (), None)
        ) if logger.handlers else None
    }
    
    if include_details:
        response["details"] = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }
    
    return response


def log_and_continue(
    error: Exception,
    context: str,
    continue_message: str = "Continuing execution..."
) -> None:
    """Log error and continue execution."""
    logger.error(f"Error in {context}: {error}", exc_info=True)
    logger.info(continue_message)


def log_and_raise(
    error: Exception,
    context: str,
    custom_message: Optional[str] = None
) -> None:
    """Log error and re-raise with custom message."""
    error_msg = custom_message or f"Error in {context}: {error}"
    logger.error(error_msg, exc_info=True)
    raise type(error)(error_msg) from error
