"""
Automated Recovery Procedures
============================

Intelligent system recovery with health checks, auto-healing,
and proactive maintenance procedures.

V2 Compliance: <400 lines, single responsibility, automated recovery.
"""

import logging
import subprocess
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class RecoveryStrategy(Enum):
    """Types of recovery strategies."""

    RESTART = "restart"  # Restart failed component
    FAILOVER = "failover"  # Switch to backup component
    SCALE_UP = "scale_up"  # Increase resources
    SCALE_DOWN = "scale_down"  # Reduce resources
    CIRCUIT_BREAK = "circuit_break"  # Temporarily isolate component
    HEALTH_CHECK = "health_check"  # Verify component health
    ROLLBACK = "rollback"  # Revert to previous version
    NOTIFICATION = "notification"  # Alert administrators


class RecoveryState(Enum):
    """States of the recovery process."""

    IDLE = "idle"  # No recovery needed
    ANALYZING = "analyzing"  # Analyzing failure
    RECOVERING = "recovering"  # Executing recovery
    VERIFYING = "verifying"  # Verifying recovery success
    COMPLETED = "completed"  # Recovery successful
    FAILED = "failed"  # Recovery failed


@dataclass
class RecoveryConfig:
    """Configuration for automated recovery."""

    name: str = "default_recovery"
    max_recovery_attempts: int = 3
    recovery_timeout: float = 300.0  # 5 minutes
    health_check_interval: float = 30.0  # 30 seconds
    enable_auto_recovery: bool = True
    enable_proactive_monitoring: bool = True

    # Recovery strategies to attempt (in order)
    recovery_strategies: List[RecoveryStrategy] = field(
        default_factory=lambda: [
            RecoveryStrategy.HEALTH_CHECK,
            RecoveryStrategy.RESTART,
            RecoveryStrategy.FAILOVER,
            RecoveryStrategy.NOTIFICATION,
        ]
    )


@dataclass
class RecoveryMetrics:
    """Metrics for recovery operations."""

    total_recoveries: int = 0
    successful_recoveries: int = 0
    failed_recoveries: int = 0
    average_recovery_time: float = 0.0
    last_recovery_time: Optional[float] = None
    consecutive_failures: int = 0

    recovery_attempts_by_strategy: Dict[RecoveryStrategy, int] = field(
        default_factory=lambda: {strategy: 0 for strategy in RecoveryStrategy}
    )


class HealthChecker:
    """Component health monitoring and verification."""

    def __init__(self, config: RecoveryConfig):
        self.config = config
        self._health_checks: Dict[str, Callable[[], bool]] = {}
        self._lock = threading.RLock()

    def register_health_check(self, component: str, check_func: Callable[[], bool]) -> None:
        """Register a health check function for a component."""
        with self._lock:
            self._health_checks[component] = check_func

    def check_health(self, component: str) -> bool:
        """Check health of a specific component."""
        with self._lock:
            if component in self._health_checks:
                try:
                    return self._health_checks[component]()
                except Exception as e:
                    logging.error(f"Health check failed for {component}: {e}")
                    return False
            return False

    def check_all_health(self) -> Dict[str, bool]:
        """Check health of all registered components."""
        with self._lock:
            results = {}
            for component, check_func in self._health_checks.items():
                try:
                    results[component] = check_func()
                except Exception as e:
                    logging.error(f"Health check failed for {component}: {e}")
                    results[component] = False
            return results


class RecoveryExecutor:
    """Executes recovery strategies for failed components."""

    def __init__(self, config: RecoveryConfig):
        self.config = config
        self._recovery_actions: Dict[RecoveryStrategy, Callable[[str], bool]] = {}
        self._lock = threading.RLock()

    def register_recovery_action(
        self, strategy: RecoveryStrategy, action_func: Callable[[str], bool]
    ) -> None:
        """Register a recovery action for a strategy."""
        with self._lock:
            self._recovery_actions[strategy] = action_func

    def execute_strategy(self, strategy: RecoveryStrategy, component: str) -> bool:
        """Execute a specific recovery strategy."""
        with self._lock:
            if strategy in self._recovery_actions:
                try:
                    logging.info(f"Executing {strategy.value} recovery for {component}")
                    return self._recovery_actions[strategy](component)
                except Exception as e:
                    logging.error(f"Recovery strategy {strategy.value} failed for {component}: {e}")
                    return False
            else:
                logging.warning(f"No recovery action registered for {strategy.value}")
                return False

    def _default_restart_action(self, component: str) -> bool:
        """Default restart recovery action."""
        try:
            # This would typically restart a service or process
            logging.info(f"Restarting component: {component}")
            # Simulate restart
            time.sleep(2)  # Simulate restart time
            return True
        except Exception as e:
            logging.error(f"Restart failed for {component}: {e}")
            return False

    def _default_failover_action(self, component: str) -> bool:
        """Default failover recovery action."""
        try:
            # This would typically switch to a backup component
            logging.info(f"Executing failover for component: {component}")
            # Simulate failover
            time.sleep(1)
            return True
        except Exception as e:
            logging.error(f"Failover failed for {component}: {e}")
            return False

    def _default_notification_action(self, component: str) -> bool:
        """Default notification recovery action."""
        try:
            # This would send notifications to administrators
            logging.warning(f"Sending notification for failed component: {component}")
            # Simulate notification
            return True
        except Exception as e:
            logging.error(f"Notification failed for {component}: {e}")
            return False


class AutomatedRecoveryManager:
    """
    Automated recovery manager with intelligent failure detection and recovery.

    Features:
    - Proactive health monitoring
    - Multi-strategy recovery execution
    - Recovery success verification
    - Comprehensive metrics collection
    - Configurable recovery policies
    """

    def __init__(self, config: RecoveryConfig = None):
        self.config = config or RecoveryConfig()

        # Initialize components
        self.health_checker = HealthChecker(self.config)
        self.recovery_executor = RecoveryExecutor(self.config)

        # Setup default recovery actions
        self._setup_default_actions()

        # Monitoring and metrics
        self.metrics = RecoveryMetrics()
        self._current_recovery_state = RecoveryState.IDLE
        self._recovery_lock = threading.RLock()
        self._logger = logging.getLogger(f"{__name__}.{self.config.name}")

        # Proactive monitoring
        if self.config.enable_proactive_monitoring:
            self._start_proactive_monitoring()

    def _setup_default_actions(self) -> None:
        """Setup default recovery actions."""
        self.recovery_executor.register_recovery_action(
            RecoveryStrategy.RESTART, self.recovery_executor._default_restart_action
        )
        self.recovery_executor.register_recovery_action(
            RecoveryStrategy.FAILOVER, self.recovery_executor._default_failover_action
        )
        self.recovery_executor.register_recovery_action(
            RecoveryStrategy.NOTIFICATION, self.recovery_executor._default_notification_action
        )

    def _start_proactive_monitoring(self) -> None:
        """Start proactive health monitoring."""

        def monitor_worker():
            while True:
                try:
                    health_status = self.health_checker.check_all_health()

                    # Check for unhealthy components
                    unhealthy_components = [
                        comp for comp, healthy in health_status.items() if not healthy
                    ]

                    if unhealthy_components:
                        for component in unhealthy_components:
                            self._logger.warning(f"Unhealthy component detected: {component}")
                            self.initiate_recovery(component)

                    time.sleep(self.config.health_check_interval)

                except Exception as e:
                    self._logger.error(f"Proactive monitoring error: {e}")
                    time.sleep(self.config.health_check_interval)

        thread = threading.Thread(target=monitor_worker, daemon=True, name="recovery_monitor")
        thread.start()
        self._logger.info("Proactive recovery monitoring started")

    def register_component(
        self,
        component: str,
        health_check: Callable[[], bool],
        recovery_strategies: List[RecoveryStrategy] = None,
    ) -> None:
        """
        Register a component for automated recovery.

        Args:
            component: Component name
            health_check: Function to check component health
            recovery_strategies: List of recovery strategies (uses config default if None)
        """
        self.health_checker.register_health_check(component, health_check)

        if recovery_strategies:
            # Override default strategies for this component
            self._component_strategies = getattr(self, "_component_strategies", {})
            self._component_strategies[component] = recovery_strategies

    def initiate_recovery(self, component: str, exception: Exception = None) -> bool:
        """
        Initiate automated recovery for a failed component.

        Args:
            component: Component to recover
            exception: Original exception that triggered recovery

        Returns:
            True if recovery successful, False otherwise
        """
        with self._recovery_lock:
            if self._current_recovery_state != RecoveryState.IDLE:
                self._logger.warning(f"Recovery already in progress for {component}")
                return False

            self._current_recovery_state = RecoveryState.ANALYZING
            self.metrics.total_recoveries += 1

        start_time = time.time()

        try:
            # Get recovery strategies for this component
            strategies = self._get_recovery_strategies(component)

            for strategy in strategies:
                self._logger.info(f"Attempting {strategy.value} recovery for {component}")

                with self._recovery_lock:
                    self._current_recovery_state = RecoveryState.RECOVERING
                    self.metrics.recovery_attempts_by_strategy[strategy] += 1

                # Execute recovery strategy
                success = self.recovery_executor.execute_strategy(strategy, component)

                if success:
                    # Verify recovery
                    if self._verify_recovery(component):
                        recovery_time = time.time() - start_time

                        with self._recovery_lock:
                            self._current_recovery_state = RecoveryState.COMPLETED
                            self.metrics.successful_recoveries += 1
                            self.metrics.consecutive_failures = 0
                            self.metrics.last_recovery_time = time.time()

                            # Update average recovery time
                            if self.metrics.successful_recoveries == 1:
                                self.metrics.average_recovery_time = recovery_time
                            else:
                                self.metrics.average_recovery_time = (
                                    self.metrics.average_recovery_time
                                    * (self.metrics.successful_recoveries - 1)
                                    + recovery_time
                                ) / self.metrics.successful_recoveries

                        self._logger.info(
                            f"Recovery successful for {component} in {recovery_time:.2f}s"
                        )
                        return True
                    else:
                        self._logger.warning(f"Recovery verification failed for {component}")

            # All strategies failed
            with self._recovery_lock:
                self._current_recovery_state = RecoveryState.FAILED
                self.metrics.failed_recoveries += 1
                self.metrics.consecutive_failures += 1

            self._logger.error(f"All recovery strategies failed for {component}")
            return False

        except Exception as e:
            with self._recovery_lock:
                self._current_recovery_state = RecoveryState.FAILED
                self.metrics.failed_recoveries += 1
                self.metrics.consecutive_failures += 1

            self._logger.error(f"Recovery process failed for {component}: {e}")
            return False

        finally:
            with self._recovery_lock:
                if self._current_recovery_state != RecoveryState.COMPLETED:
                    self._current_recovery_state = RecoveryState.IDLE

    def _get_recovery_strategies(self, component: str) -> List[RecoveryStrategy]:
        """Get recovery strategies for a component."""
        component_strategies = getattr(self, "_component_strategies", {})
        return component_strategies.get(component, self.config.recovery_strategies)

    def _verify_recovery(self, component: str) -> bool:
        """Verify that recovery was successful."""
        try:
            # Wait a moment for component to stabilize
            time.sleep(2)

            # Check health
            return self.health_checker.check_health(component)

        except Exception as e:
            self._logger.error(f"Recovery verification failed for {component}: {e}")
            return False

    def recover_and_retry(self, func: Callable, exception: Exception, *args, **kwargs) -> Any:
        """
        Recover from failure and retry the operation.

        Args:
            func: Function to retry
            exception: Original exception
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result if successful

        Raises:
            Exception: If recovery or retry fails
        """
        # Attempt recovery (component name derived from function)
        component = getattr(func, "__name__", "unknown_component")
        recovery_success = self.initiate_recovery(component, exception)

        if recovery_success:
            try:
                # Retry the operation
                self._logger.info(f"Retrying operation after successful recovery: {component}")
                return func(*args, **kwargs)
            except Exception as retry_exception:
                self._logger.error(
                    f"Retry failed after recovery for {component}: {retry_exception}"
                )
                raise retry_exception
        else:
            self._logger.error(f"Recovery failed for {component}, cannot retry")
            raise exception

    def get_recovery_status(self) -> Dict[str, Any]:
        """Get comprehensive recovery status."""
        with self._recovery_lock:
            return {
                "config": {
                    "name": self.config.name,
                    "max_recovery_attempts": self.config.max_recovery_attempts,
                    "recovery_timeout": self.config.recovery_timeout,
                    "health_check_interval": self.config.health_check_interval,
                    "auto_recovery_enabled": self.config.enable_auto_recovery,
                    "proactive_monitoring_enabled": self.config.enable_proactive_monitoring,
                },
                "metrics": {
                    "total_recoveries": self.metrics.total_recoveries,
                    "successful_recoveries": self.metrics.successful_recoveries,
                    "failed_recoveries": self.metrics.failed_recoveries,
                    "average_recovery_time": self.metrics.average_recovery_time,
                    "last_recovery_time": self.metrics.last_recovery_time,
                    "consecutive_failures": self.metrics.consecutive_failures,
                    "recovery_attempts_by_strategy": dict(
                        self.metrics.recovery_attempts_by_strategy
                    ),
                },
                "current_state": self._current_recovery_state.value,
                "health_status": self.health_checker.check_all_health(),
                "success_rate": (
                    (self.metrics.successful_recoveries / self.metrics.total_recoveries * 100)
                    if self.metrics.total_recoveries > 0
                    else 0
                ),
            }

    def reset(self) -> None:
        """Reset recovery manager to initial state."""
        with self._recovery_lock:
            self.metrics = RecoveryMetrics()
            self._current_recovery_state = RecoveryState.IDLE
            self._logger.info(f"Recovery manager '{self.config.name}' reset")


# Global registry for managing multiple recovery managers
_recovery_managers: Dict[str, AutomatedRecoveryManager] = {}
_managers_lock = threading.RLock()


def get_recovery_manager(name: str = "default") -> AutomatedRecoveryManager:
    """Get or create recovery manager by name."""
    with _managers_lock:
        if name not in _recovery_managers:
            config = RecoveryConfig(name=name)
            _recovery_managers[name] = AutomatedRecoveryManager(config)
        return _recovery_managers[name]


def create_recovery_manager(config: RecoveryConfig) -> AutomatedRecoveryManager:
    """Create and register a new recovery manager."""
    with _managers_lock:
        manager = AutomatedRecoveryManager(config)
        _recovery_managers[config.name] = manager
        return manager


def get_all_recovery_managers() -> Dict[str, AutomatedRecoveryManager]:
    """Get all registered recovery managers."""
    with _managers_lock:
        return _recovery_managers.copy()


def reset_all_recovery_managers() -> None:
    """Reset all recovery managers."""
    with _managers_lock:
        for manager in _recovery_managers.values():
            manager.reset()
