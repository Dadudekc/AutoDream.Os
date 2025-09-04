#!/usr/bin/env python3
"""
Error Recovery Module - Agent Cellphone V2
=======================================

Error recovery strategies and automatic remediation.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""



logger = logging.getLogger(__name__)


class RecoveryStrategy:
    """Base class for error recovery strategies."""

    def __init__(self, name: str, description: str):
        """Initialize recovery strategy."""
        self.name = name
        self.description = description

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if this strategy can recover from the error."""
        raise NotImplementedError

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute the recovery strategy."""
        raise NotImplementedError


class ServiceRestartStrategy(RecoveryStrategy):
    """Strategy for restarting failed services."""

    def __init__(self, service_manager: Callable):
        """Initialize service restart strategy."""
        super().__init__("service_restart", "Restart failed service components")
        self.service_manager = service_manager
        self.last_restart = None
        self.restart_cooldown = timedelta(minutes=5)

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if service restart is appropriate."""
        if (
            self.last_restart
            and datetime.now() - self.last_restart < self.restart_cooldown
        ):
            return False
        return error_context.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute service restart."""
        try:
            get_logger(__name__).info(f"Executing service restart for {error_context.component}")
            success = self.service_manager()
            if success:
                self.last_restart = datetime.now()
                get_logger(__name__).info(f"Service restart successful for {error_context.component}")
            return success
        except Exception as e:
            get_logger(__name__).error(f"Service restart failed: {e}")
            return False


class ConfigurationResetStrategy(RecoveryStrategy):
    """Strategy for resetting configuration to defaults."""

    def __init__(self, config_reset_func: Callable):
        """Initialize configuration reset strategy."""
        super().__init__("config_reset", "Reset configuration to safe defaults")
        self.config_reset_func = config_reset_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if configuration reset is appropriate."""
        return (
            "config" in error_context.operation.lower()
            or error_context.severity == ErrorSeverity.CRITICAL
        )

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute configuration reset."""
        try:
            get_logger(__name__).info(f"Executing configuration reset for {error_context.component}")
            success = self.config_reset_func()
            if success:
                get_logger(__name__).info(
                    f"Configuration reset successful for {error_context.component}"
                )
            return success
        except Exception as e:
            get_logger(__name__).error(f"Configuration reset failed: {e}")
            return False


class ResourceCleanupStrategy(RecoveryStrategy):
    """Strategy for cleaning up stuck resources."""

    def __init__(self, cleanup_func: Callable):
        """Initialize resource cleanup strategy."""
        super().__init__("resource_cleanup", "Clean up stuck resources and locks")
        self.cleanup_func = cleanup_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if resource cleanup is appropriate."""
        return (
            "resource" in str(error_context.details).lower()
            or "lock" in str(error_context.details).lower()
        )

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute resource cleanup."""
        try:
            get_logger(__name__).info(f"Executing resource cleanup for {error_context.component}")
            success = self.cleanup_func()
            if success:
                get_logger(__name__).info(
                    f"Resource cleanup successful for {error_context.component}"
                )
            return success
        except Exception as e:
            get_logger(__name__).error(f"Resource cleanup failed: {e}")
            return False


class ErrorRecoveryManager:
    """Manages error recovery strategies."""

    def __init__(self):
        """Initialize error recovery manager."""
        self.strategies: List[RecoveryStrategy] = []
        self.recovery_history: List[Dict[str, Any]] = []

    def add_strategy(self, strategy: RecoveryStrategy):
        """Add a recovery strategy."""
        self.strategies.append(strategy)
        get_logger(__name__).info(f"Added recovery strategy: {strategy.name}")

    def attempt_recovery(self, error_context: ErrorContext) -> bool:
        """Attempt to recover from an error using available strategies."""
        recovery_attempt = {
            "timestamp": datetime.now(),
            "error_context": error_context,
            "strategies_attempted": [],
            "successful_strategy": None,
            "recovery_success": False,
        }

        for strategy in self.strategies:
            if strategy.can_recover(error_context):
                recovery_attempt["strategies_attempted"].append(strategy.name)

                get_logger(__name__).info(f"Attempting recovery with strategy: {strategy.name}")
                success = strategy.execute_recovery(error_context)

                if success:
                    recovery_attempt["successful_strategy"] = strategy.name
                    recovery_attempt["recovery_success"] = True
                    get_logger(__name__).info(f"Recovery successful using strategy: {strategy.name}")
                    break
                else:
                    get_logger(__name__).warning(f"Recovery failed with strategy: {strategy.name}")

        self.recovery_history.append(recovery_attempt)
        return recovery_attempt["recovery_success"]

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery statistics."""
        if not self.recovery_history:
            return {"total_attempts": 0, "successful_recoveries": 0, "success_rate": 0}

        total_attempts = len(self.recovery_history)
        successful_recoveries = len(
            [r for r in self.recovery_history if r["recovery_success"]]
        )

        return {
            "total_attempts": total_attempts,
            "successful_recoveries": successful_recoveries,
            "success_rate": (
                (successful_recoveries / total_attempts) * 100
                if total_attempts > 0
                else 0
            ),
        }


def with_error_recovery(recovery_manager: ErrorRecoveryManager):
    """Decorator for automatic error recovery."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Create error context
                error_context = ErrorContext(
                    operation=f"{func.__module__}.{func.__name__}",
                    component=func.__module__,
                    timestamp=datetime.now(),
                    severity=ErrorSeverity.HIGH,
                    details={"exception": str(e), "exception_type": type(e).__name__},
                )

                # Attempt recovery
                if recovery_manager.attempt_recovery(error_context):
                    # Retry the operation once after successful recovery
                    try:
                        return func(*args, **kwargs)
                    except Exception as retry_error:
                        get_logger(__name__).error(
                            f"Operation failed even after recovery: {retry_error}"
                        )
                        raise retry_error
                else:
                    get_logger(__name__).error(f"No recovery strategy succeeded for: {e}")
                    raise e

        return wrapper

    return decorator
