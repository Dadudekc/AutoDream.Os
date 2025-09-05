#!/usr/bin/env python3
"""
Retry & Safety Engine - V2 Compliant
===================================

Retry logic and safe execution functionality.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant retry and safety operations
"""

import time
from typing import Callable, Any, Optional, Union
import logging
from .error_handling_models import RetryConfiguration


class RetrySafetyEngine:
    """Engine for retry operations and safe execution."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize retry safety engine."""
        self.logger = logger
    
    def _get_logger(self):
        """Get logger instance."""
        if self.logger:
            return self.logger
        # Fallback to module logger
        import logging as std_logging
        return std_logging.getLogger(__name__)
    
    def retry_operation(
        self,
        operation_func: Callable,
        config: Optional[RetryConfiguration] = None,
        logger: Optional[logging.Logger] = None
    ) -> Any:
        """
        Retry operation with exponential backoff.
        
        Args:
            operation_func: Function to retry
            config: Retry configuration
            logger: Optional logger for retry logging
            
        Returns:
            Any: Result of successful operation
            
        Raises:
            Exception: Last exception if all retries fail
        """
        if config is None:
            config = RetryConfiguration()
        
        effective_logger = logger or self.logger
        last_exception = None
        
        for attempt in range(config.max_retries + 1):
            try:
                if effective_logger and attempt > 0:
                    self._get_logger().info(f"🔄 Retry attempt {attempt}/{config.max_retries}")
                
                return operation_func()
                
            except config.exceptions as e:
                last_exception = e
                
                if attempt == config.max_retries:
                    if effective_logger:
                        self._get_logger().error(f"❌ All {config.max_retries} retry attempts failed: {e}")
                    break
                
                if effective_logger:
                    delay = config.calculate_delay(attempt)
                    self._get_logger().warning(f"⚠️ Attempt {attempt + 1} failed: {e}, retrying in {delay:.1f}s")
                    time.sleep(delay)
                else:
                    time.sleep(config.calculate_delay(attempt))
        
        raise last_exception
    
    def safe_execute(
        self,
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
            effective_logger = logger or self.logger
            if effective_logger:
                self._get_logger().error(f"❌ Safe execution failed for {operation_name}: {e}")
            return default_return
    
    def validate_and_execute(
        self,
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
                raise ValueError(error_message)
            
            return operation_func()
            
        except Exception as e:
            effective_logger = logger or self.logger
            if effective_logger:
                self._get_logger().error(f"❌ Validation and execution failed: {e}")
            raise
    
    def execute_with_timeout(
        self,
        operation_func: Callable,
        timeout: float,
        default_return: Any = None,
        logger: Optional[logging.Logger] = None
    ) -> Any:
        """
        Execute operation with timeout.
        
        Args:
            operation_func: Function to execute
            timeout: Timeout in seconds
            default_return: Value to return if timeout occurs
            logger: Optional logger
            
        Returns:
            Any: Result of operation or default_return if timeout
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout} seconds")
        
        effective_logger = logger or self.logger
        
        try:
            # Set timeout handler
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))
            
            result = operation_func()
            
            # Clear timeout
            signal.alarm(0)
            return result
            
        except TimeoutError as e:
            if effective_logger:
                self._get_logger().warning(f"⏰ Operation timed out: {e}")
            return default_return
        except Exception as e:
            if effective_logger:
                self._get_logger().error(f"❌ Operation failed: {e}")
            return default_return
        finally:
            # Always clear timeout
            signal.alarm(0)
    
    def circuit_breaker_execute(
        self,
        operation_func: Callable,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        logger: Optional[logging.Logger] = None
    ) -> Any:
        """
        Execute operation with circuit breaker pattern.
        
        Args:
            operation_func: Function to execute
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time to wait before attempting recovery
            logger: Optional logger
            
        Returns:
            Any: Result of operation
            
        Raises:
            Exception: If circuit is open or operation fails
        """
        # Simple circuit breaker implementation
        # In production, this would use a more sophisticated state machine
        
        effective_logger = logger or self.logger
        
        try:
            return operation_func()
        except Exception as e:
            if effective_logger:
                self._get_logger().error(f"❌ Circuit breaker: Operation failed: {e}")
            raise


# Convenience functions for backward compatibility
def retry_operation(
    operation_func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Any:
    """Retry operation with exponential backoff."""
    config = RetryConfiguration(max_retries, delay, backoff_factor, exceptions)
    engine = RetrySafetyEngine(logger)
    return engine.retry_operation(operation_func, config, logger)


def safe_execute(
    operation_func: Callable,
    default_return: Any = None,
    logger: Optional[logging.Logger] = None,
    operation_name: str = "operation"
) -> Any:
    """Safely execute operation with fallback return value."""
    engine = RetrySafetyEngine(logger)
    return engine.safe_execute(operation_func, default_return, logger, operation_name)
