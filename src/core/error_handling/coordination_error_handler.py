from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Coordination & Communication Error Handler - Agent Cellphone V2
============================================================

Comprehensive error handling with retry mechanisms and circuit breaker patterns.

Author: Agent-6 (Gaming & Entertainment Specialist)
License: MIT
"""

import time
import logging
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps

# Type variable for generic return types
T = TypeVar('T')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Circuit is open, requests fail fast
    HALF_OPEN = "HALF_OPEN"  # Testing if service is recovered


@dataclass
class ErrorContext:
    """Context information for error handling."""
    operation: str
    component: str
    timestamp: datetime
    severity: ErrorSeverity
    retry_count: int = 0
    max_retries: int = 3
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.details is None:
            self.details = {}


class RetryHandler:
    """Handles retry logic for failed operations."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, 
                 max_delay: float = 60.0, exponential_backoff: bool = True):
        """Initialize retry handler."""
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_backoff = exponential_backoff
        self.retry_history: List[ErrorContext] = []
    
    def execute_with_retry(self, operation: Callable[[], T], 
                          operation_name: str = "operation",
                          component: str = "unknown") -> T:
        """Execute operation with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = operation()
                
                # Log successful execution
                if attempt > 0:
                    logger.info(f"✅ Operation '{operation_name}' succeeded on attempt {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Create error context
                error_context = ErrorContext(
                    operation=operation_name,
                    component=component,
                    timestamp=datetime.now(),
                    severity=self._determine_severity(e, attempt),
                    retry_count=attempt,
                    max_retries=self.max_retries,
                    details={"exception": str(e), "exception_type": type(e).__name__}
                )
                
                self.retry_history.append(error_context)
                
                # Log the error
                logger.warning(f"⚠️ Operation '{operation_name}' failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                
                # If this was the last attempt, don't retry
                if attempt >= self.max_retries:
                    logger.error(f"❌ Operation '{operation_name}' failed after {self.max_retries + 1} attempts")
                    break
                
                # Calculate delay before retry
                delay = self._calculate_retry_delay(attempt)
                logger.info(f"⏳ Retrying '{operation_name}' in {delay:.2f} seconds...")
                time.sleep(delay)
        
        # If we get here, all retries failed
        raise last_exception
    
    def _determine_severity(self, exception: Exception, attempt: int) -> ErrorSeverity:
        """Determine error severity based on exception and attempt count."""
        if attempt >= self.max_retries:
            return ErrorSeverity.CRITICAL
        elif attempt >= self.max_retries // 2:
            return ErrorSeverity.HIGH
        else:
            return ErrorSeverity.MEDIUM
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate delay before retry."""
        if self.exponential_backoff:
            delay = self.base_delay * (2 ** attempt)
        else:
            delay = self.base_delay * (attempt + 1)
        
        # Add jitter to prevent thundering herd
        jitter = delay * 0.1 * (time.time() % 1)
        delay += jitter
        
        return min(delay, self.max_delay)
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get retry statistics."""
        if not self.retry_history:
            return {"total_operations": 0, "successful_retries": 0, "failed_operations": 0}
        
        total_operations = len(self.retry_history)
        successful_retries = len([ctx for ctx in self.retry_history if ctx.retry_count > 0])
        failed_operations = len([ctx for ctx in self.retry_history if ctx.retry_count >= ctx.max_retries])
        
        return {
            "total_operations": total_operations,
            "successful_retries": successful_retries,
            "failed_operations": failed_operations,
            "success_rate": (total_operations - failed_operations) / total_operations * 100
        }


class CircuitBreaker:
    """Implements circuit breaker pattern for fault tolerance."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0,
                 expected_exception: type = Exception):
        """Initialize circuit breaker."""
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.state = CircuitState.CLOSED
        self.failure_count = get_config('failure_count', 0)
        self.last_failure_time = None
        self.success_count = get_config('success_count', 0)
    
    def call(self, operation: Callable[[], T], operation_name: str = "operation") -> T:
        """Execute operation with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"🔄 Circuit breaker for '{operation_name}' moved to HALF_OPEN state")
            else:
                raise Exception(f"Circuit breaker is OPEN for '{operation_name}'")
        
        try:
            result = operation()
            self._on_success(operation_name)
            return result
            
        except self.expected_exception as e:
            self._on_failure(operation_name)
            raise e
    
    def _on_success(self, operation_name: str):
        """Handle successful operation."""
        self.failure_count = get_config('failure_count', 0)
        self.success_count += 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            logger.info(f"✅ Circuit breaker for '{operation_name}' reset to CLOSED state")
    
    def _on_failure(self, operation_name: str):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error(f"🚨 Circuit breaker for '{operation_name}' opened after {self.failure_count} failures")
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset."""
        if self.last_failure_time is None:
            return False
        
        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout
    
    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status."""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout
        }


class CoordinationErrorHandler:
    """Main error handler for coordination and communication systems."""
    
    def __init__(self):
        """Initialize the error handler."""
        self.retry_handler = RetryHandler()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.error_history: List[ErrorContext] = []
    
    def register_circuit_breaker(self, component: str, failure_threshold: int = 5,
                                recovery_timeout: float = 60.0) -> None:
        """Register a circuit breaker for a component."""
        self.circuit_breakers[component] = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout
        )
        logger.info(f"🔧 Registered circuit breaker for component: {component}")
    
    def execute_with_error_handling(self, operation: Callable[[], T],
                                   operation_name: str = "operation",
                                   component: str = "unknown",
                                   use_retry: bool = True,
                                   use_circuit_breaker: bool = True) -> T:
        """Execute operation with comprehensive error handling."""
        try:
            if use_circuit_breaker and component in self.circuit_breakers:
                # Use circuit breaker
                return self.circuit_breakers[component].call(
                    lambda: self._execute_operation(operation, operation_name, component, use_retry),
                    operation_name
                )
            else:
                # Execute directly
                return self._execute_operation(operation, operation_name, component, use_retry)
                
        except Exception as e:
            # Log and store error context
            error_context = ErrorContext(
                operation=operation_name,
                component=component,
                timestamp=datetime.now(),
                severity=ErrorSeverity.HIGH,
                details={"exception": str(e), "exception_type": type(e).__name__}
            )
            self.error_history.append(error_context)
            
            logger.error(f"❌ Operation '{operation_name}' failed in component '{component}': {e}")
            raise e
    
    def _execute_operation(self, operation: Callable[[], T], operation_name: str,
                          component: str, use_retry: bool) -> T:
        """Execute operation with optional retry."""
        if use_retry:
            return self.retry_handler.execute_with_retry(operation, operation_name, component)
        else:
            return operation()
    
    def get_error_report(self) -> Dict[str, Any]:
        """Generate comprehensive error report."""
        return {
            "error_summary": {
                "total_errors": len(self.error_history),
                "retry_statistics": self.retry_handler.get_retry_statistics(),
                "circuit_breaker_status": {
                    component: cb.get_status() 
                    for component, cb in self.circuit_breakers.items()
                }
            },
            "recent_errors": self.error_history[-10:] if self.error_history else [],
            "system_health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> str:
        """Assess overall system health."""
        if not self.error_history:
            return "HEALTHY"
        
        recent_errors = [e for e in self.error_history 
                        if (datetime.now() - e.timestamp).total_seconds() < 3600]  # Last hour
        
        if len(recent_errors) == 0:
            return "HEALTHY"
        elif len(recent_errors) < 5:
            return "DEGRADED"
        else:
            return "UNHEALTHY"


# Decorator for easy error handling
def handle_errors(component: str = "unknown", use_retry: bool = True, 
                  use_circuit_breaker: bool = True):
    """Decorator for automatic error handling."""
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Get global error handler instance
            error_handler = getattr(wrapper, '_error_handler', None)
            if error_handler is None:
                error_handler = CoordinationErrorHandler()
                wrapper._error_handler = error_handler
            
            operation_name = f"{func.__module__}.{func.__name__}"
            
            def operation():
                return func(*args, **kwargs)
            
            return error_handler.execute_with_error_handling(
                operation, operation_name, component, use_retry, use_circuit_breaker
            )
        return wrapper
    return decorator
