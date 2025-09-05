"""
Circuit Breaker Executor - V2 Compliance Module
==============================================

Circuit breaker execution functionality.

V2 Compliance: < 300 lines, single responsibility, circuit breaker executor.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from typing import Optional, Callable, Any
from datetime import datetime

from .core import CircuitState, CircuitBreakerCore

logger = logging.getLogger(__name__)


class CircuitBreakerOpenException(Exception):
    """Exception raised when circuit breaker is open."""
    
    def __init__(self, message: str, retry_after: Optional[datetime] = None):
        super().__init__(message)
        self.retry_after = retry_after


class CircuitBreakerExecutor:
    """Circuit breaker execution functionality."""
    
    def __init__(self, core: CircuitBreakerCore):
        """Initialize circuit breaker executor."""
        self.core = core
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.core.state == CircuitState.OPEN:
            if not self.core._should_attempt_reset():
                raise CircuitBreakerOpenException(
                    f"Circuit breaker '{self.core.config.name}' is OPEN",
                    retry_after=self.core.next_attempt_time,
                )
            
            self.core.state = CircuitState.HALF_OPEN
            logger.info(
                f"Circuit breaker '{self.core.config.name}' testing recovery (HALF_OPEN)"
            )
        
        try:
            result = func(*args, **kwargs)
            self.core._record_success()
            return result
        
        except Exception as e:
            self.core._record_failure(e)
            raise
    
    def call_with_fallback(self, func: Callable, fallback_func: Callable, *args, **kwargs) -> Any:
        """Execute function with fallback if circuit breaker is open."""
        try:
            return self.call(func, *args, **kwargs)
        except CircuitBreakerOpenException:
            logger.warning(
                f"Circuit breaker '{self.core.config.name}' is open, using fallback"
            )
            return fallback_func(*args, **kwargs)
    
    def call_with_retry(self, func: Callable, max_retries: int = 3, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return self.call(func, *args, **kwargs)
            except CircuitBreakerOpenException as e:
                last_exception = e
                if attempt < max_retries:
                    logger.info(
                        f"Circuit breaker '{self.core.config.name}' is open, retrying in {attempt + 1} seconds"
                    )
                    import time
                    time.sleep(attempt + 1)
                else:
                    break
            except Exception as e:
                last_exception = e
                break
        
        if last_exception:
            raise last_exception
        
        raise RuntimeError("Max retries exceeded")
    
    def is_available(self) -> bool:
        """Check if circuit breaker is available for calls."""
        return self.core.state != CircuitState.OPEN or self.core._should_attempt_reset()
    
    def get_retry_after(self) -> Optional[datetime]:
        """Get the time when the circuit breaker will be available again."""
        if self.core.state == CircuitState.OPEN:
            return self.core.next_attempt_time
        return None
