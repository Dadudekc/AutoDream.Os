from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Unit tests for Coordination Error Handler - Agent Cellphone V2
============================================================

Comprehensive testing for the error handling system.

Author: Agent-6 (Gaming & Entertainment Specialist)
License: MIT
"""

import pytest
import time
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.core.error_handling.coordination_error_handler import (
    CoordinationErrorHandler,
    RetryHandler,
    CircuitBreaker,
    ErrorSeverity,
    CircuitState,
    ErrorContext,
    handle_errors
)


class TestErrorSeverity:
    """Test error severity enum."""
    
    def test_error_severity_values(self):
        """Test error severity enum values."""
        assert ErrorSeverity.LOW.value == "LOW"
        assert ErrorSeverity.MEDIUM.value == "MEDIUM"
        assert ErrorSeverity.HIGH.value == "HIGH"
        assert ErrorSeverity.CRITICAL.value == "CRITICAL"


class TestCircuitState:
    """Test circuit state enum."""
    
    def test_circuit_state_values(self):
        """Test circuit state enum values."""
        assert CircuitState.CLOSED.value == "CLOSED"
        assert CircuitState.OPEN.value == "OPEN"
        assert CircuitState.HALF_OPEN.value == "HALF_OPEN"


class TestErrorContext:
    """Test error context dataclass."""
    
    def test_error_context_creation(self):
        """Test error context creation with all fields."""
        context = ErrorContext(
            operation="test_operation",
            component="test_component",
            timestamp=datetime.now(),
            severity=ErrorSeverity.HIGH,
            retry_count=2,
            max_retries=3,
            details={"test": "data"}
        )
        
        assert context.operation == "test_operation"
        assert context.component == "test_component"
        assert context.severity == ErrorSeverity.HIGH
        assert context.retry_count == 2
        assert context.max_retries == 3
        assert context.details == {"test": "data"}
    
    def test_error_context_defaults(self):
        """Test error context creation with default values."""
        context = ErrorContext(
            operation="test_operation",
            component="test_component",
            timestamp=datetime.now(),
            severity=ErrorSeverity.MEDIUM
        )
        
        assert context.retry_count == 0
        assert context.max_retries == 3
        assert context.details == {}


class TestRetryHandler:
    """Test retry handler class."""
    
    @pytest.fixture
    def retry_handler(self):
        """Create retry handler instance for testing."""
        return RetryHandler(max_retries=2, base_delay=0.1)
    
    def test_retry_handler_initialization(self, retry_handler):
        """Test retry handler initialization."""
        assert retry_handler.max_retries == 2
        assert retry_handler.base_delay == 0.1
        assert retry_handler.max_delay == 60.0
        assert retry_handler.exponential_backoff is True
        assert isinstance(retry_handler.retry_history, list)
    
    def test_execute_with_retry_success_first_attempt(self, retry_handler):
        """Test retry handler with successful first attempt."""
        def successful_operation():
            return "success"
        
        result = retry_handler.execute_with_retry(
            successful_operation, "test_operation", "test_component"
        )
        
        assert result == "success"
        assert len(retry_handler.retry_history) == 0
    
    def test_execute_with_retry_success_after_retry(self, retry_handler):
        """Test retry handler with success after retry."""
        attempt_count = get_config('attempt_count', 0)
        
        def failing_then_successful_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count == 1:
                raise ValueError("First attempt fails")
            return "success"
        
        result = retry_handler.execute_with_retry(
            failing_then_successful_operation, "test_operation", "test_component"
        )
        
        assert result == "success"
        assert len(retry_handler.retry_history) == 1
        assert retry_handler.retry_history[0].retry_count == 0
    
    def test_execute_with_retry_all_attempts_fail(self, retry_handler):
        """Test retry handler with all attempts failing."""
        def always_failing_operation():
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            retry_handler.execute_with_retry(
                always_failing_operation, "test_operation", "test_component"
            )
        
        assert len(retry_handler.retry_history) == 3  # 3 attempts total
        assert retry_handler.retry_history[-1].retry_count == 2
    
    def test_determine_severity(self, retry_handler):
        """Test error severity determination."""
        error = ValueError("Test error")
        
        # First attempt
        severity = retry_handler._determine_severity(error, 0)
        assert severity == ErrorSeverity.MEDIUM
        
        # Middle attempt
        severity = retry_handler._determine_severity(error, 1)
        assert severity == ErrorSeverity.HIGH
        
        # Last attempt
        severity = retry_handler._determine_severity(error, 2)
        assert severity == ErrorSeverity.CRITICAL
    
    def test_calculate_retry_delay_exponential(self, retry_handler):
        """Test retry delay calculation with exponential backoff."""
        delay1 = retry_handler._calculate_retry_delay(0)
        delay2 = retry_handler._calculate_retry_delay(1)
        delay3 = retry_handler._calculate_retry_delay(2)
        
        assert delay1 < delay2 < delay3
        assert delay1 >= 0.1  # Base delay
        assert delay2 >= 0.2  # 2^1 * base
        assert delay3 >= 0.4  # 2^2 * base
    
    def test_calculate_retry_delay_linear(self):
        """Test retry delay calculation with linear backoff."""
        retry_handler = RetryHandler(exponential_backoff=False, base_delay=0.1)
        
        delay1 = retry_handler._calculate_retry_delay(0)
        delay2 = retry_handler._calculate_retry_delay(1)
        delay3 = retry_handler._calculate_retry_delay(2)
        
        assert delay1 >= 0.1  # Base delay
        assert delay2 >= 0.2  # 2 * base
        assert delay3 >= 0.3  # 3 * base
    
    def test_calculate_retry_delay_max_delay(self):
        """Test retry delay calculation respects max delay."""
        retry_handler = RetryHandler(max_delay=0.1, base_delay=0.5)
        
        delay = retry_handler._calculate_retry_delay(5)  # Should exceed max_delay
        assert delay <= 0.1
    
    def test_get_retry_statistics_no_history(self, retry_handler):
        """Test retry statistics with no history."""
        stats = retry_handler.get_retry_statistics()
        
        assert stats["total_operations"] == 0
        assert stats["successful_retries"] == 0
        assert stats["failed_operations"] == 0
        # Note: success_rate is not calculated when total_operations is 0
        assert "success_rate" not in stats
    
    def test_get_retry_statistics_with_history(self, retry_handler):
        """Test retry statistics with history."""
        # Simulate some retry history
        retry_handler.retry_history = [
            ErrorContext(
                operation="op1",
                component="comp1",
                timestamp=datetime.now(),
                severity=ErrorSeverity.MEDIUM,
                retry_count=1,
                max_retries=2
            ),
            ErrorContext(
                operation="op2",
                component="comp2",
                timestamp=datetime.now(),
                severity=ErrorSeverity.CRITICAL,
                retry_count=2,
                max_retries=2
            )
        ]
        
        stats = retry_handler.get_retry_statistics()
        
        assert stats["total_operations"] == 2
        # Note: successful_retries counts operations that had retries, not successful outcomes
        assert stats["successful_retries"] == 2  # Both had retries
        assert stats["failed_operations"] == 1  # One failed after max retries
        assert stats["success_rate"] == 50.0


class TestCircuitBreaker:
    """Test circuit breaker class."""
    
    @pytest.fixture
    def circuit_breaker(self):
        """Create circuit breaker instance for testing."""
        return CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
    
    def test_circuit_breaker_initialization(self, circuit_breaker):
        """Test circuit breaker initialization."""
        assert circuit_breaker.failure_threshold == 2
        assert circuit_breaker.recovery_timeout == 0.1
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.failure_count == 0
        assert circuit_breaker.success_count == 0
    
    def test_circuit_breaker_closed_state_success(self, circuit_breaker):
        """Test circuit breaker in closed state with success."""
        def successful_operation():
            return "success"
        
        result = circuit_breaker.call(successful_operation, "test_operation")
        
        assert result == "success"
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.failure_count == 0
        assert circuit_breaker.success_count == 1
    
    def test_circuit_breaker_closed_state_failure(self, circuit_breaker):
        """Test circuit breaker in closed state with failure."""
        def failing_operation():
            raise ValueError("Operation fails")
        
        with pytest.raises(ValueError):
            circuit_breaker.call(failing_operation, "test_operation")
        
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.failure_count == 1
        assert circuit_breaker.success_count == 0
    
    def test_circuit_breaker_opens_after_threshold(self, circuit_breaker):
        """Test circuit breaker opens after failure threshold."""
        def failing_operation():
            raise ValueError("Operation fails")
        
        # First failure
        with pytest.raises(ValueError):
            circuit_breaker.call(failing_operation, "test_operation")
        
        # Second failure - should open circuit
        with pytest.raises(ValueError):
            circuit_breaker.call(failing_operation, "test_operation")
        
        assert circuit_breaker.state == CircuitState.OPEN
        assert circuit_breaker.failure_count == 2
    
    def test_circuit_breaker_half_open_recovery(self, circuit_breaker):
        """Test circuit breaker recovery from open to half-open to closed."""
        def failing_operation():
            raise ValueError("Operation fails")
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                circuit_breaker.call(failing_operation, "test_operation")
        
        assert circuit_breaker.state == CircuitState.OPEN
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Should move to half-open
        def successful_operation():
            return "success"
        
        result = circuit_breaker.call(successful_operation, "test_operation")
        
        assert result == "success"
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.failure_count == 0
    
    def test_circuit_breaker_half_open_failure(self, circuit_breaker):
        """Test circuit breaker stays open after half-open failure."""
        def failing_operation():
            raise ValueError("Operation fails")
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                circuit_breaker.call(failing_operation, "test_operation")
        
        assert circuit_breaker.state == CircuitState.OPEN
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Should move to half-open, but fail again
        with pytest.raises(ValueError):
            circuit_breaker.call(failing_operation, "test_operation")
        
        assert circuit_breaker.state == CircuitState.OPEN
    
    def test_get_status(self, circuit_breaker):
        """Test circuit breaker status reporting."""
        status = circuit_breaker.get_status()
        
        assert "state" in status
        assert "failure_count" in status
        assert "success_count" in status
        assert "last_failure_time" in status
        assert "threshold" in status
        assert "recovery_timeout" in status
        
        assert status["state"] == CircuitState.CLOSED.value
        assert status["failure_count"] == 0
        assert status["success_count"] == 0


class TestCoordinationErrorHandler:
    """Test coordination error handler main class."""
    
    @pytest.fixture
    def error_handler(self):
        """Create error handler instance for testing."""
        return CoordinationErrorHandler()
    
    def test_error_handler_initialization(self, error_handler):
        """Test error handler initialization."""
        assert isinstance(error_handler.retry_handler, RetryHandler)
        assert isinstance(error_handler.circuit_breakers, dict)
        assert isinstance(error_handler.error_history, list)
    
    def test_register_circuit_breaker(self, error_handler):
        """Test circuit breaker registration."""
        error_handler.register_circuit_breaker("test_component", 3, 0.1)
        
        assert "test_component" in error_handler.circuit_breakers
        circuit_breaker = error_handler.circuit_breakers["test_component"]
        assert circuit_breaker.failure_threshold == 3
        assert circuit_breaker.recovery_timeout == 0.1
    
    def test_execute_with_error_handling_success(self, error_handler):
        """Test error handler execution with success."""
        def successful_operation():
            return "success"
        
        result = error_handler.execute_with_error_handling(
            successful_operation, "test_operation", "test_component"
        )
        
        assert result == "success"
        assert len(error_handler.error_history) == 0
    
    def test_execute_with_error_handling_failure(self, error_handler):
        """Test error handler execution with failure."""
        def failing_operation():
            raise ValueError("Operation fails")
        
        with pytest.raises(ValueError):
            error_handler.execute_with_error_handling(
                failing_operation, "test_operation", "test_component"
            )
        
        assert len(error_handler.error_history) == 1
        assert error_handler.error_history[0].operation == "test_operation"
        assert error_handler.error_history[0].component == "test_component"
        assert error_handler.error_history[0].severity == ErrorSeverity.HIGH
    
    def test_execute_with_error_handling_with_circuit_breaker(self, error_handler):
        """Test error handler execution with circuit breaker."""
        error_handler.register_circuit_breaker("test_component", 1, 0.1)
        
        def failing_operation():
            raise ValueError("Operation fails")
        
        # First failure should open circuit
        with pytest.raises(ValueError):
            error_handler.execute_with_error_handling(
                failing_operation, "test_operation", "test_component"
            )
        
        # Second call should fail fast due to open circuit
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            error_handler.execute_with_error_handling(
                failing_operation, "test_operation", "test_component"
            )
    
    def test_get_error_report(self, error_handler):
        """Test error report generation."""
        # Generate some error history
        def failing_operation():
            raise ValueError("Operation fails")
        
        with pytest.raises(ValueError):
            error_handler.execute_with_error_handling(
                failing_operation, "test_operation", "test_component"
            )
        
        report = error_handler.get_error_report()
        
        assert "error_summary" in report
        assert "recent_errors" in report
        assert "system_health" in report
        
        assert report["error_summary"]["total_errors"] == 1
        # Note: The retry mechanism creates multiple error contexts, so system health is DEGRADED
        assert report["system_health"] == "DEGRADED"  # Multiple error contexts from retries
    
    def test_assess_system_health(self, error_handler):
        """Test system health assessment."""
        # No errors - should be healthy
        assert error_handler._assess_system_health() == "HEALTHY"
        
        # Add some errors
        for i in range(3):
            error_context = ErrorContext(
                operation=f"op{i}",
                component=f"comp{i}",
                timestamp=datetime.now(),
                severity=ErrorSeverity.MEDIUM
            )
            error_handler.error_history.append(error_context)
        
        # 3 errors in last hour - should be degraded
        assert error_handler._assess_system_health() == "DEGRADED"
        
        # Add more errors
        for i in range(5):
            error_context = ErrorContext(
                operation=f"op{i+3}",
                component=f"comp{i+3}",
                timestamp=datetime.now(),
                severity=ErrorSeverity.HIGH
            )
            error_handler.error_history.append(error_context)
        
        # 8 errors in last hour - should be unhealthy
        assert error_handler._assess_system_health() == "UNHEALTHY"


class TestErrorHandlerDecorator:
    """Test error handler decorator."""
    
    def test_handle_errors_decorator_success(self):
        """Test error handler decorator with success."""
        @handle_errors(component="test_component")
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"
    
    def test_handle_errors_decorator_failure(self):
        """Test error handler decorator with failure."""
        @handle_errors(component="test_component")
        def failing_function():
            raise ValueError("Function fails")
        
        with pytest.raises(ValueError):
            failing_function()
    
    def test_handle_errors_decorator_with_parameters(self):
        """Test error handler decorator with function parameters."""
        @handle_errors(component="test_component")
        def function_with_params(param1, param2):
            return f"{param1}_{param2}"
        
        result = function_with_params("hello", "world")
        assert result == "hello_world"


if __name__ == "__main__":
    pytest.main([__file__])
