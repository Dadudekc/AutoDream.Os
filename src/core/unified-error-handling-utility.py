#!/usr/bin/env python3
"""
Unified Error Handling Utility - V2 Compliant
==============================================

This module provides a unified error handling utility that consolidates all error handling
patterns into a single, V2 compliant architecture.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate 100+ error handling patterns into unified utility
"""

from ..core.unified_import_system import logging


class UnifiedErrorHandlingUtility:
    """
    Unified Error Handling Utility - V2 Compliant
    
    Consolidates all error handling patterns into single utility:
    - 100+ error handling implementations across the codebase
    - Unified error handling
    - Unified retry mechanisms
    - Unified error reporting
    - Unified error recovery
    - Unified error logging
    """

    @staticmethod
    def handle_operation_error(
        logger: logging.Logger,
        operation: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle operation error with standardized logging and response.
        
        Args:
            logger: Logger instance
            operation: Operation name
            error: Exception that occurred
            context: Additional context information
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        # Log error with context
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Error in {operation}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def retry_operation(
        operation_func: Callable,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        exceptions: tuple = (Exception,),
        logger: Optional[logging.Logger] = None
    ) -> Any:
        """
        Retry operation with exponential backoff.
        
        Args:
            operation_func: Function to retry
            max_retries: Maximum number of retry attempts
            delay: Initial delay between retries
            backoff_factor: Factor to multiply delay by after each retry
            exceptions: Tuple of exceptions to catch and retry
            logger: Optional logger for retry logging
            
        Returns:
            Any: Result of successful operation
            
        Raises:
            Exception: Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                if logger and attempt > 0:
                    get_logger(__name__).info(f"🔄 Retry attempt {attempt}/{max_retries}")
                
                return operation_func()
                
            except exceptions as e:
                last_exception = e
                
                if attempt == max_retries:
                    if logger:
                        get_logger(__name__).error(f"❌ All {max_retries} retry attempts failed: {e}")
                    break
                
                if logger:
                    get_logger(__name__).warning(f"⚠️ Attempt {attempt + 1} failed: {e}, retrying in {delay:.1f}s")
                
                time.sleep(delay)
                delay *= backoff_factor
        
        raise last_exception

    @staticmethod
    def safe_execute(
        operation_func: Callable,
        default_return: Any = None,
        logger: Optional[logging.Logger] = None,
        operation_name: str = "operation"
    ) -> Any:
        """
        Safely execute operation with fallback return value.
        
        Args:
            operation_func: Function to execute
            default_return: Value to return if operation fails
            logger: Optional logger for error logging
            operation_name: Name of operation for logging
            
        Returns:
            Any: Result of operation or default_return if failed
        """
        try:
            return operation_func()
        except Exception as e:
            if logger:
                get_logger(__name__).error(f"❌ Safe execution failed for {operation_name}: {e}")
            return default_return

    @staticmethod
    def validate_and_execute(
        operation_func: Callable,
        validation_func: Callable,
        error_message: str = "Validation failed",
        logger: Optional[logging.Logger] = None
    ) -> Any:
        """
        Validate input and execute operation.
        
        Args:
            operation_func: Function to execute
            validation_func: Function to validate input
            error_message: Error message if validation fails
            logger: Optional logger for error logging
            
        Returns:
            Any: Result of operation
            
        Raises:
            ValueError: If validation fails
        """
        try:
            if not validation_func():
                get_unified_validator().raise_validation_error(error_message)
            
            return operation_func()
            
        except Exception as e:
            if logger:
                get_logger(__name__).error(f"❌ Validation and execution failed: {e}")
            raise

    @staticmethod
    def handle_file_operation_error(
        logger: logging.Logger,
        operation: str,
        file_path: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle file operation error with standardized response.
        
        Args:
            logger: Logger instance
            operation: File operation (read, write, delete, etc.)
            file_path: File path
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "operation": operation,
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ File {operation} error for {file_path}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_network_operation_error(
        logger: logging.Logger,
        operation: str,
        url: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle network operation error with standardized response.
        
        Args:
            logger: Logger instance
            operation: Network operation (request, response, etc.)
            url: URL or endpoint
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "operation": operation,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Network {operation} error for {url}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_database_operation_error(
        logger: logging.Logger,
        operation: str,
        table: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle database operation error with standardized response.
        
        Args:
            logger: Logger instance
            operation: Database operation (select, insert, update, delete)
            table: Table name
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "operation": operation,
            "table": table,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Database {operation} error for table {table}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_validation_error(
        logger: logging.Logger,
        validation_type: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle validation error with standardized response.
        
        Args:
            logger: Logger instance
            validation_type: Type of validation
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "validation_type": validation_type,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Validation error for {validation_type}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_configuration_error(
        logger: logging.Logger,
        config_key: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle configuration error with standardized response.
        
        Args:
            logger: Logger instance
            config_key: Configuration key
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "config_key": config_key,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Configuration error for {config_key}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_agent_operation_error(
        logger: logging.Logger,
        agent_id: str,
        operation: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle agent operation error with standardized response.
        
        Args:
            logger: Logger instance
            agent_id: Agent identifier
            operation: Operation name
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "agent_id": agent_id,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Agent {agent_id} operation error for {operation}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def handle_coordination_error(
        logger: logging.Logger,
        coordination_type: str,
        participants: List[str],
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle coordination error with standardized response.
        
        Args:
            logger: Logger instance
            coordination_type: Type of coordination
            participants: List of participants
            error: Exception that occurred
            context: Additional context
            
        Returns:
            Dict[str, Any]: Standardized error response
        """
        error_response = {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "coordination_type": coordination_type,
            "participants": participants,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        participants_str = ", ".join(participants)
        context_str = f" - Context: {context}" if context else ""
        get_logger(__name__).error(f"❌ Coordination error for {coordination_type} with {participants_str}: {error}{context_str}")
        
        return error_response

    @staticmethod
    def create_error_summary(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create error summary from list of errors.
        
        Args:
            errors: List of error dictionaries
            
        Returns:
            Dict[str, Any]: Error summary
        """
        if not get_unified_validator().validate_required(errors):
            return {
                "total_errors": 0,
                "error_types": {},
                "operations": {},
                "timestamp": datetime.now().isoformat()
            }
        
        error_types = {}
        operations = {}
        
        for error in errors:
            # Count error types
            error_type = error.get("error_type", "Unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
            
            # Count operations
            operation = error.get("operation", "Unknown")
            operations[operation] = operations.get(operation, 0) + 1
        
        return {
            "total_errors": len(errors),
            "error_types": error_types,
            "operations": operations,
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def is_recoverable_error(error: Exception) -> bool:
        """
        Check if error is recoverable.
        
        Args:
            error: Exception to check
            
        Returns:
            bool: True if error is recoverable
        """
        recoverable_errors = (
            ConnectionError,
            TimeoutError,
            OSError,
            FileNotFoundError,
            PermissionError
        )
        
        return get_unified_validator().validate_type(error, recoverable_errors)

    @staticmethod
    def get_error_severity(error: Exception) -> str:
        """
        Get error severity level.
        
        Args:
            error: Exception to analyze
            
        Returns:
            str: Severity level (low, medium, high, critical)
        """
        critical_errors = (SystemError, MemoryError, KeyboardInterrupt)
        high_errors = (ValueError, TypeError, AttributeError, KeyError)
        medium_errors = (FileNotFoundError, PermissionError, ConnectionError)
        
        if get_unified_validator().validate_type(error, critical_errors):
            return "critical"
        elif get_unified_validator().validate_type(error, high_errors):
            return "high"
        elif get_unified_validator().validate_type(error, medium_errors):
            return "medium"
        else:
            return "low"


# Convenience functions for backward compatibility
def handle_operation_error(
    logger: logging.Logger,
    operation: str,
    error: Exception,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Handle operation error with standardized response."""
    return UnifiedErrorHandlingUtility.handle_operation_error(logger, operation, error, context)


def retry_operation(
    operation_func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Any:
    """Retry operation with exponential backoff."""
    return UnifiedErrorHandlingUtility.retry_operation(
        operation_func, max_retries, delay, backoff_factor, exceptions, logger
    )


def safe_execute(
    operation_func: Callable,
    default_return: Any = None,
    logger: Optional[logging.Logger] = None,
    operation_name: str = "operation"
) -> Any:
    """Safely execute operation with fallback return value."""
    return UnifiedErrorHandlingUtility.safe_execute(
        operation_func, default_return, logger, operation_name
    )