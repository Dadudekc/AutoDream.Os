"""
Manager Metrics - Base Manager Metrics Tracking
===============================================
Extracted from base_manager.py for V2 compliance.
Handles operation tracking, metrics calculation, and performance monitoring.

Author: Agent-5 (refactored from Agent-2's base_manager.py)
License: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class ManagerMetricsTracker:
    """Tracks manager operation metrics and performance."""

    def __init__(self):
        """Initialize metrics tracker."""
        # Operation tracking
        self.operation_count = 0
        self.success_count = 0
        self.error_count = 0

        # Timing
        self.initialized_at: datetime | None = None

    def record_operation_start(self) -> None:
        """Record start of an operation."""
        self.operation_count += 1

    def record_success(self) -> None:
        """Record successful operation."""
        self.success_count += 1

    def record_error(self) -> None:
        """Record failed operation."""
        self.error_count += 1

    def set_initialized_at(self, timestamp: datetime) -> None:
        """Set initialization timestamp."""
        self.initialized_at = timestamp

    def get_metrics(self) -> dict[str, Any]:
        """
        Get manager metrics.

        Returns:
            Dict containing performance metrics
        """
        return {
            "operation_count": self.operation_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": self._calculate_success_rate(),
            "average_operations_per_hour": self._calculate_ops_per_hour(),
            "uptime_seconds": self._calculate_uptime(),
            "error_rate": self._calculate_error_rate(),
        }

    def get_metrics_for_status(self) -> dict[str, Any]:
        """Get metrics suitable for status reporting."""
        return {
            "operation_count": self.operation_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": self._calculate_success_rate(),
        }

    def reset(self) -> bool:
        """
        Reset manager metrics.

        Returns:
            bool: True if reset successful
        """
        try:
            self.operation_count = 0
            self.success_count = 0
            self.error_count = 0
            return True
        except Exception:
            return False

    def _calculate_success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.operation_count == 0:
            return 0.0
        return (self.success_count / self.operation_count) * 100

    def _calculate_error_rate(self) -> float:
        """Calculate error rate percentage."""
        if self.operation_count == 0:
            return 0.0
        return (self.error_count / self.operation_count) * 100

    def _calculate_ops_per_hour(self) -> float:
        """Calculate average operations per hour."""
        if not self.initialized_at:
            return 0.0

        uptime_hours = (datetime.now() - self.initialized_at).total_seconds() / 3600
        if uptime_hours < 0.01:
            return 0.0

        return self.operation_count / uptime_hours

    def _calculate_uptime(self) -> float:
        """Calculate uptime in seconds."""
        if not self.initialized_at:
            return 0.0

        return (datetime.now() - self.initialized_at).total_seconds()
