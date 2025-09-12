"""
Advanced Error Handling & Recovery Orchestrator
==============================================

Comprehensive error handling system with circuit breakers, retry logic,
graceful degradation, and automated recovery procedures.

V2 Compliance: <400 lines, single responsibility, error handling orchestration.
"""

import threading
import time
import logging
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum

from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from .retry_mechanisms import RetryMechanism, RetryConfig
from .error_recovery import RecoveryManager, RecoveryConfig


class DegradationLevel(Enum):
    """Levels of system degradation."""
    NORMAL = "normal"           # Full functionality
    DEGRADED = "degraded"       # Reduced functionality
    MINIMAL = "minimal"         # Critical functions only
    EMERGENCY = "emergency"     # Emergency mode


@dataclass
class ResilienceConfig:
    """Configuration for resilient error handling."""
    name: str = "default"
    enable_circuit_breaker: bool = True
    enable_retry: bool = True
    enable_graceful_degradation: bool = True
    enable_automated_recovery: bool = True

    circuit_breaker_config: Optional[CircuitBreakerConfig] = None
    retry_config: Optional[RetryConfig] = None
    recovery_config: Optional[RecoveryConfig] = None

    degradation_thresholds: Dict[str, int] = field(default_factory=lambda: {
        "error_rate": 0.1,      # 10% error rate triggers degradation
        "response_time": 5.0,   # 5 seconds triggers degradation
        "consecutive_failures": 3
    })


@dataclass
class ResilienceMetrics:
    """Metrics for system resilience."""
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    degraded_operations: int = 0
    recovered_operations: int = 0

    current_degradation_level: DegradationLevel = DegradationLevel.NORMAL
    last_degradation_time: Optional[float] = None
    last_recovery_time: Optional[float] = None

    circuit_breaker_trips: int = 0
    retry_attempts: int = 0
    recovery_attempts: int = 0


class GracefulDegradationManager:
    """Manages graceful degradation of system functionality."""

    def __init__(self, config: ResilienceConfig):
        self.config = config
        self._degradation_level = DegradationLevel.NORMAL
        self._degraded_features: Dict[str, bool] = {}
        self._lock = threading.RLock()

    def should_degrade(self, metrics: ResilienceMetrics) -> bool:
        """Determine if system should degrade based on metrics."""
        if metrics.total_operations == 0:
            return False

        error_rate = metrics.failed_operations / metrics.total_operations

        # Check degradation thresholds
        if error_rate > self.config.degradation_thresholds["error_rate"]:
            return True

        if metrics.failed_operations > self.config.degradation_thresholds["consecutive_failures"]:
            return True

        return False

    def degrade_to_level(self, level: DegradationLevel) -> None:
        """Degrade system to specified level."""
        with self._lock:
            if level != self._degradation_level:
                self._degradation_level = level
                self._configure_degraded_features(level)

    def _configure_degraded_features(self, level: DegradationLevel) -> None:
        """Configure which features to disable at each degradation level."""
        if level == DegradationLevel.DEGRADED:
            # Disable non-critical features
            self._degraded_features.update({
                "caching": False,
                "analytics": False,
                "background_processing": False,
                "real_time_updates": False
            })
        elif level == DegradationLevel.MINIMAL:
            # Keep only critical features
            self._degraded_features.update({
                "basic_operations": True,
                "error_handling": True,
                "monitoring": True,
                "emergency_recovery": True
            })
        elif level == DegradationLevel.EMERGENCY:
            # Emergency mode - minimal functionality
            self._degraded_features.update({
                "all_optional": False,
                "critical_only": True,
                "maintenance_mode": True
            })

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled given current degradation level."""
        with self._lock:
            if self._degradation_level == DegradationLevel.NORMAL:
                return True

            return self._degraded_features.get(feature, True)

    def get_degradation_status(self) -> Dict[str, Any]:
        """Get current degradation status."""
        with self._lock:
            return {
                "level": self._degradation_level.value,
                "degraded_features": self._degraded_features.copy(),
                "timestamp": time.time()
            }


class AdvancedErrorHandler:
    """
    Advanced error handling orchestrator with comprehensive resilience features.

    Features:
    - Circuit breaker integration
    - Retry logic with exponential backoff
    - Graceful degradation management
    - Automated recovery procedures
    - Comprehensive metrics and monitoring
    """

    def __init__(self, config: ResilienceConfig = None):
        self.config = config or ResilienceConfig()

        # Initialize components
        self.circuit_breaker = None
        self.retry_mechanism = None
        self.recovery_manager = None
        self.degradation_manager = GracefulDegradationManager(self.config)

        self._setup_components()

        # Metrics and monitoring
        self.metrics = ResilienceMetrics()
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"{__name__}.{self.config.name}")

    def _setup_components(self) -> None:
        """Initialize error handling components."""
        if self.config.enable_circuit_breaker:
            cb_config = self.config.circuit_breaker_config or CircuitBreakerConfig(
                name=f"{self.config.name}_circuit_breaker"
            )
            self.circuit_breaker = CircuitBreaker(cb_config)

        if self.config.enable_retry:
            retry_config = self.config.retry_config or RetryConfig()
            self.retry_mechanism = RetryMechanism(retry_config)

        if self.config.enable_automated_recovery:
            recovery_config = self.config.recovery_config or RecoveryConfig()
            self.recovery_manager = RecoveryManager(recovery_config)

    def execute_with_resilience(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with comprehensive error handling and resilience.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all recovery mechanisms fail
        """
        with self._lock:
            self.metrics.total_operations += 1

        try:
            # Check if we should degrade
            if self.config.enable_graceful_degradation:
                if self.degradation_manager.should_degrade(self.metrics):
                    self._handle_degradation()

            # Execute with circuit breaker protection
            if self.circuit_breaker and self.config.enable_circuit_breaker:
                result = self.circuit_breaker.call(func, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Record success
            with self._lock:
                self.metrics.successful_operations += 1

            # Check if we should recover from degradation
            if self.config.enable_graceful_degradation:
                self._attempt_recovery()

            return result

        except Exception as e:
            # Record failure
            with self._lock:
                self.metrics.failed_operations += 1

            # Attempt recovery strategies
            if self._should_attempt_recovery(e):
                return self._execute_recovery_strategy(func, e, *args, **kwargs)

            # If all recovery fails, raise original exception
            raise e

    def _handle_degradation(self) -> None:
        """Handle system degradation."""
        if self.metrics.current_degradation_level == DegradationLevel.NORMAL:
            # Degrade to first level
            self.degradation_manager.degrade_to_level(DegradationLevel.DEGRADED)
            self.metrics.current_degradation_level = DegradationLevel.DEGRADED
            self.metrics.last_degradation_time = time.time()

            self._logger.warning(f"System degraded to {DegradationLevel.DEGRADED.value} mode")

    def _attempt_recovery(self) -> None:
        """Attempt to recover from degradation."""
        if (self.metrics.current_degradation_level != DegradationLevel.NORMAL and
            self.metrics.successful_operations > 10 and
            self.metrics.failed_operations < 2):

            # Recover to normal operation
            self.degradation_manager.degrade_to_level(DegradationLevel.NORMAL)
            self.metrics.current_degradation_level = DegradationLevel.NORMAL
            self.metrics.last_recovery_time = time.time()

            self._logger.info("System recovered to normal operation")

    def _should_attempt_recovery(self, exception: Exception) -> bool:
        """Determine if recovery should be attempted for given exception."""
        # Don't retry certain types of exceptions
        non_retryable = (
            KeyboardInterrupt,
            SystemExit,
            MemoryError,
            ImportError,
            SyntaxError
        )

        if isinstance(exception, non_retryable):
            return False

        # Check if we have recovery mechanisms available
        return (self.retry_mechanism or self.recovery_manager) is not None

    def _execute_recovery_strategy(self, func: Callable, original_exception: Exception,
                                 *args, **kwargs) -> Any:
        """Execute recovery strategy based on available mechanisms."""

        # Try retry mechanism first
        if self.retry_mechanism and self.config.enable_retry:
            try:
                with self._lock:
                    self.metrics.retry_attempts += 1

                self._logger.info("Attempting retry recovery")
                return self.retry_mechanism.call(func, *args, **kwargs)

            except Exception as retry_exception:
                self._logger.warning(f"Retry recovery failed: {retry_exception}")

        # Try automated recovery
        if self.recovery_manager and self.config.enable_automated_recovery:
            try:
                with self._lock:
                    self.metrics.recovery_attempts += 1

                self._logger.info("Attempting automated recovery")
                return self.recovery_manager.recover_and_retry(
                    func, original_exception, *args, **kwargs
                )

            except Exception as recovery_exception:
                self._logger.error(f"Automated recovery failed: {recovery_exception}")

        # If all recovery mechanisms fail, record degraded operation
        with self._lock:
            self.metrics.degraded_operations += 1

        # Return fallback response or re-raise
        raise original_exception

    def get_resilience_status(self) -> Dict[str, Any]:
        """Get comprehensive resilience status."""
        with self._lock:
            return {
                "config": {
                    "name": self.config.name,
                    "circuit_breaker_enabled": self.config.enable_circuit_breaker,
                    "retry_enabled": self.config.enable_retry,
                    "degradation_enabled": self.config.enable_graceful_degradation,
                    "recovery_enabled": self.config.enable_automated_recovery,
                },
                "metrics": {
                    "total_operations": self.metrics.total_operations,
                    "successful_operations": self.metrics.successful_operations,
                    "failed_operations": self.metrics.failed_operations,
                    "degraded_operations": self.metrics.degraded_operations,
                    "recovered_operations": self.metrics.recovered_operations,
                    "current_degradation_level": self.metrics.current_degradation_level.value,
                    "circuit_breaker_trips": self.metrics.circuit_breaker_trips,
                    "retry_attempts": self.metrics.retry_attempts,
                    "recovery_attempts": self.metrics.recovery_attempts,
                },
                "degradation_status": self.degradation_manager.get_degradation_status(),
                "circuit_breaker_status": (
                    self.circuit_breaker.get_stats() if self.circuit_breaker else None
                ),
                "last_degradation_time": self.metrics.last_degradation_time,
                "last_recovery_time": self.metrics.last_recovery_time,
                "health_percentage": (
                    (self.metrics.successful_operations / self.metrics.total_operations * 100)
                    if self.metrics.total_operations > 0 else 100
                ),
            }

    def reset(self) -> None:
        """Reset all error handling components."""
        with self._lock:
            if self.circuit_breaker:
                self.circuit_breaker.reset()
            if self.recovery_manager:
                self.recovery_manager.reset()

            self.metrics = ResilienceMetrics()
            self.degradation_manager.degrade_to_level(DegradationLevel.NORMAL)

            self._logger.info(f"Advanced error handler '{self.config.name}' reset")


# Global registry for managing multiple error handlers
_advanced_error_handlers: Dict[str, AdvancedErrorHandler] = {}
_handlers_lock = threading.RLock()

def get_advanced_error_handler(name: str = "default") -> AdvancedErrorHandler:
    """Get or create advanced error handler by name."""
    with _handlers_lock:
        if name not in _advanced_error_handlers:
            config = ResilienceConfig(name=name)
            _advanced_error_handlers[name] = AdvancedErrorHandler(config)
        return _advanced_error_handlers[name]

def create_advanced_error_handler(config: ResilienceConfig) -> AdvancedErrorHandler:
    """Create and register a new advanced error handler."""
    with _handlers_lock:
        handler = AdvancedErrorHandler(config)
        _advanced_error_handlers[config.name] = handler
        return handler

def get_all_error_handlers() -> Dict[str, AdvancedErrorHandler]:
    """Get all registered error handlers."""
    with _handlers_lock:
        return _advanced_error_handlers.copy()

def reset_all_error_handlers() -> None:
    """Reset all error handlers."""
    with _handlers_lock:
        for handler in _advanced_error_handlers.values():
            handler.reset()
