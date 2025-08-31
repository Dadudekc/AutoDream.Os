#!/usr/bin/env python3
"""
Base Manager System - Agent Cellphone V2
========================================

CONSOLIDATED base manager system to eliminate duplication across all manager classes.
This provides common functionality that was previously duplicated in 15+ manager files.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
import threading
import time
from .base import ManagerConfig


class ManagerStatus(Enum):
    """Unified manager status states"""

    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    INITIALIZING = "initializing"
    SHUTTING_DOWN = "shutting_down"


class ManagerPriority(Enum):
    """Unified manager priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class ManagerMetrics:
    """Unified manager performance metrics"""

    manager_id: str
    uptime_seconds: float = 0.0
    operations_processed: int = 0
    errors_count: int = 0
    last_operation: Optional[datetime] = None
    performance_score: float = 0.0
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class BaseManager(ABC):
    """
    CONSOLIDATED base manager class that eliminates duplication

    Common functionality previously duplicated across manager classes:
    - Lifecycle management (start/stop/restart)
    - Status tracking and monitoring
    - Performance metrics collection
    - Heartbeat monitoring
    - Error handling and recovery
    - Resource management

    Additional responsibilities such as configuration, logging, and validation
    are provided via mixins.
    """

    def __init__(self, manager_id: str, name: str, description: str = ""):
        # Core identification
        self.manager_id = manager_id
        self.name = name
        self.description = description

        # Status and lifecycle
        self.status = ManagerStatus.OFFLINE
        self.priority = ManagerPriority.NORMAL
        self.running = False
        self.startup_time: Optional[datetime] = None
        self.shutdown_time: Optional[datetime] = None

        # Performance tracking
        self.metrics = ManagerMetrics(manager_id=manager_id)
        self.operations_history: List[Dict[str, Any]] = []

        # Heartbeat monitoring
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.heartbeat_interval = 30
        self.last_heartbeat = datetime.now()

        # Error handling
        self.error_count = 0
        self.last_error: Optional[str] = None
        self.recovery_attempts = 0

        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}

        # Resource management
        self.resources: Dict[str, Any] = {}
        self.resource_locks: Dict[str, threading.Lock] = {}

        if hasattr(self, "logger"):
            self.logger.info(f"BaseManager initialized: {manager_id} ({name})")

    # ============================================================================
    # LIFECYCLE MANAGEMENT - Previously duplicated across all managers
    # ============================================================================

    def start(self) -> bool:
        """Start the manager - common lifecycle method"""
        try:
            if self.running:
                self.logger.warning(f"Manager {self.manager_id} is already running")
                return True

            self.logger.info(f"Starting manager: {self.manager_id}")
            self.status = ManagerStatus.INITIALIZING

            # Initialize resources
            if not self._initialize_resources():
                raise RuntimeError("Failed to initialize resources")

            # Start heartbeat monitoring
            self._start_heartbeat_monitoring()

            # Call subclass-specific startup
            if not self._on_start():
                raise RuntimeError("Subclass startup failed")

            self.running = True
            self.status = ManagerStatus.ONLINE
            self.startup_time = datetime.now()
            self.metrics.uptime_seconds = 0.0

            self.logger.info(f"Manager {self.manager_id} started successfully")
            self._emit_event("manager_started", {"manager_id": self.manager_id})
            return True

        except Exception as e:
            self.logger.error(f"Failed to start manager {self.manager_id}: {e}")
            self.status = ManagerStatus.ERROR
            self.last_error = str(e)
            self.error_count += 1
            return False

    def stop(self) -> bool:
        """Stop the manager - common lifecycle method"""
        try:
            if not self.running:
                self.logger.warning(f"Manager {self.manager_id} is not running")
                return True

            self.logger.info(f"Stopping manager: {self.manager_id}")
            self.status = ManagerStatus.SHUTTING_DOWN

            # Stop heartbeat monitoring
            self._stop_heartbeat_monitoring()

            # Call subclass-specific shutdown
            self._on_stop()

            # Cleanup resources
            self._cleanup_resources()

            self.running = False
            self.status = ManagerStatus.OFFLINE
            self.shutdown_time = datetime.now()

            self.logger.info(f"Manager {self.manager_id} stopped successfully")
            self._emit_event("manager_stopped", {"manager_id": self.manager_id})
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop manager {self.manager_id}: {e}")
            self.status = ManagerStatus.ERROR
            self.last_error = str(e)
            self.error_count += 1
            return False

    def restart(self) -> bool:
        """Restart the manager - common lifecycle method"""
        try:
            self.logger.info(f"Restarting manager: {self.manager_id}")

            if not self.stop():
                return False

            # Wait a moment for cleanup
            time.sleep(1)

            if not self.start():
                return False

            self.logger.info(f"Manager {self.manager_id} restarted successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to restart manager {self.manager_id}: {e}")
            return False

    # ============================================================================
    # STATUS AND MONITORING - Previously duplicated across all managers
    # ============================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status - common monitoring method"""
        return {
            "manager_id": self.manager_id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority.value,
            "running": self.running,
            "startup_time": self.startup_time.isoformat()
            if self.startup_time
            else None,
            "shutdown_time": self.shutdown_time.isoformat()
            if self.shutdown_time
            else None,
            "uptime_seconds": self.metrics.uptime_seconds,
            "operations_processed": self.metrics.operations_processed,
            "errors_count": self.metrics.errors_count,
            "last_operation": self.metrics.last_operation.isoformat()
            if self.metrics.last_operation
            else None,
            "performance_score": self.metrics.performance_score,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "recovery_attempts": self.recovery_attempts,
            "last_error": self.last_error,
        }

    def is_healthy(self) -> bool:
        """Check if manager is healthy - common health check method"""
        if not self.running:
            return False

        # Check heartbeat
        if (
            datetime.now() - self.last_heartbeat
        ).total_seconds() > self.heartbeat_interval * 2:
            return False

        config = getattr(self, "config", None)
        if config and self.error_count > config.max_retries:
            return False

        return True

    # ============================================================================
    # CONFIGURATION MANAGEMENT - Provided via ConfigMixin
    # ============================================================================

    # ============================================================================
    # PERFORMANCE METRICS - Previously duplicated across all managers
    # ============================================================================

    def record_operation(
        self, operation_type: str, success: bool, duration_ms: float = 0.0
    ):
        """Record operation metrics - common metrics method"""
        try:
            self.metrics.operations_processed += 1
            self.metrics.last_operation = datetime.now()

            if not success:
                self.metrics.errors_count += 1

            # Update performance score
            if success:
                # Simple scoring: successful operations improve score
                self.metrics.performance_score = min(
                    100.0, self.metrics.performance_score + 0.1
                )
            else:
                # Failed operations decrease score
                self.metrics.performance_score = max(
                    0.0, self.metrics.performance_score - 1.0
                )

            # Store operation history
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "type": operation_type,
                "success": success,
                "duration_ms": duration_ms,
                "error_count": self.error_count,
            }
            self.operations_history.append(operation_record)

            # Keep only recent history
            if len(self.operations_history) > 100:
                self.operations_history = self.operations_history[-100:]

            self.metrics.updated_at = datetime.now()

        except Exception as e:
            self.logger.error(f"Failed to record operation: {e}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary - common metrics method"""
        return {
            "manager_id": self.manager_id,
            "uptime_seconds": self.metrics.uptime_seconds,
            "operations_processed": self.metrics.operations_processed,
            "success_rate": self._calculate_success_rate(),
            "performance_score": self.metrics.performance_score,
            "error_rate": self._calculate_error_rate(),
            "average_operation_time": self._calculate_avg_operation_time(),
        }

    # ============================================================================
    # EVENT SYSTEM - Previously duplicated across all managers
    # ============================================================================

    def register_event_handler(self, event_type: str, handler: Callable):
        """Register event handler - common event method"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        self.logger.debug(f"Registered event handler for {event_type}")

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered handlers - common event method"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    self.logger.error(f"Event handler error for {event_type}: {e}")

    # ============================================================================
    # RESOURCE MANAGEMENT - Previously duplicated across all managers
    # ============================================================================

    def _initialize_resources(self) -> bool:
        """Initialize manager resources - common resource method"""
        try:
            # Create resource locks
            self.resource_locks = {
                "config": threading.Lock(),
                "metrics": threading.Lock(),
                "status": threading.Lock(),
            }

            # Initialize subclass-specific resources
            return self._on_initialize_resources()

        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _cleanup_resources(self):
        """Cleanup manager resources - common resource method"""
        try:
            # Cleanup subclass-specific resources
            self._on_cleanup_resources()

            # Clear resource locks
            self.resource_locks.clear()

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def acquire_resource_lock(self, resource_name: str) -> Optional[threading.Lock]:
        """Acquire resource lock - common resource method"""
        return self.resource_locks.get(resource_name)

    # ============================================================================
    # HEARTBEAT MONITORING - Previously duplicated across all managers
    # ============================================================================

    def _start_heartbeat_monitoring(self):
        """Start heartbeat monitoring - common monitoring method"""
        try:
            self.heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop,
                daemon=True,
                name=f"heartbeat-{self.manager_id}",
            )
            self.heartbeat_thread.start()
            self.logger.debug(f"Started heartbeat monitoring for {self.manager_id}")

        except Exception as e:
            self.logger.error(f"Failed to start heartbeat monitoring: {e}")

    def _stop_heartbeat_monitoring(self):
        """Stop heartbeat monitoring - common monitoring method"""
        try:
            if self.heartbeat_thread and self.heartbeat_thread.is_alive():
                self.heartbeat_thread.join(timeout=5.0)
                self.logger.debug(f"Stopped heartbeat monitoring for {self.manager_id}")

        except Exception as e:
            self.logger.error(f"Failed to stop heartbeat monitoring: {e}")

    def _heartbeat_loop(self):
        """Heartbeat monitoring loop - common monitoring method"""
        while self.running:
            try:
                self.last_heartbeat = datetime.now()

                # Update uptime
                if self.startup_time:
                    self.metrics.uptime_seconds = (
                        datetime.now() - self.startup_time
                    ).total_seconds()

                # Call subclass-specific heartbeat
                self._on_heartbeat()

                # Sleep until next heartbeat
                time.sleep(self.heartbeat_interval)

            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                time.sleep(5.0)  # Shorter sleep on error

    # ============================================================================
    # ERROR HANDLING AND RECOVERY - Previously duplicated across all managers
    # ============================================================================

    def handle_error(self, error: Exception, context: str = "") -> bool:
        """Handle manager error - common error method"""
        try:
            self.error_count += 1
            self.last_error = f"{context}: {str(error)}" if context else str(error)
            self.logger.error(f"Manager error: {self.last_error}")

            # Emit error event
            self._emit_event(
                "manager_error",
                {
                    "manager_id": self.manager_id,
                    "error": str(error),
                    "context": context,
                    "error_count": self.error_count,
                },
            )

            # Attempt recovery if possible
            if self.error_count <= self.config.max_retries:
                return self._attempt_recovery(error, context)

            # Mark as unrecoverable
            self.status = ManagerStatus.ERROR
            self.logger.critical(f"Manager {self.manager_id} marked as unrecoverable")
            return False

        except Exception as e:
            self.logger.error(f"Failed to handle error: {e}")
            return False

    def _attempt_recovery(self, error: Exception, context: str) -> bool:
        """Attempt error recovery - common recovery method"""
        try:
            self.recovery_attempts += 1
            self.logger.info(
                f"Attempting recovery #{self.recovery_attempts} for {self.manager_id}"
            )

            # Call subclass-specific recovery
            if self._on_recovery_attempt(error, context):
                self.status = ManagerStatus.RECOVERING
                self.logger.info(f"Recovery successful for {self.manager_id}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Recovery attempt failed: {e}")
            return False

    # ============================================================================
    # ABSTRACT METHODS - Subclasses must implement these
    # ============================================================================

    @abstractmethod
    def _on_start(self) -> bool:
        """Perform subclass-specific startup logic.

        Returns:
            bool: ``True`` if the manager started successfully, ``False`` otherwise.
        """
        raise NotImplementedError("_on_start must be implemented by subclasses")

    @abstractmethod
    def _on_stop(self):
        """Perform subclass-specific shutdown logic."""
        raise NotImplementedError("_on_stop must be implemented by subclasses")

    @abstractmethod
    def _on_heartbeat(self):
        """Execute subclass-specific heartbeat logic."""
        raise NotImplementedError("_on_heartbeat must be implemented by subclasses")

    @abstractmethod
    def _on_initialize_resources(self) -> bool:
        """Initialize subclass-specific resources.

        Returns:
            bool: ``True`` if resources were initialized successfully, ``False`` otherwise.
        """
        raise NotImplementedError(
            "_on_initialize_resources must be implemented by subclasses"
        )

    @abstractmethod
    def _on_cleanup_resources(self):
        """Clean up subclass-specific resources."""
        raise NotImplementedError(
            "_on_cleanup_resources must be implemented by subclasses"
        )

    @abstractmethod
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Handle subclass-specific recovery logic.

        Args:
            error (Exception): The exception that triggered recovery.
            context (str): Additional context for the recovery attempt.

        Returns:
            bool: ``True`` if recovery succeeded, ``False`` otherwise.
        """
        raise NotImplementedError(
            "_on_recovery_attempt must be implemented by subclasses"
        )

    # ============================================================================
    # UTILITY METHODS - Previously duplicated across all managers
    # ============================================================================

    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        if self.metrics.operations_processed == 0:
            return 100.0
        return (
            (self.metrics.operations_processed - self.metrics.errors_count)
            / self.metrics.operations_processed
        ) * 100.0

    def _calculate_error_rate(self) -> float:
        """Calculate operation error rate"""
        if self.metrics.operations_processed == 0:
            return 0.0
        return (self.metrics.errors_count / self.metrics.operations_processed) * 100.0

    def _calculate_avg_operation_time(self) -> float:
        """Calculate average operation time"""
        if not self.operations_history:
            return 0.0

        total_time = sum(op.get("duration_ms", 0) for op in self.operations_history)
        return total_time / len(self.operations_history)

    def _get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        return datetime.now().isoformat()

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.manager_id}, status={self.status.value})"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(manager_id='{self.manager_id}', name='{self.name}', status={self.status.value})"
