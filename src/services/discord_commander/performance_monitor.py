#!/usr/bin/env python3
"""
Performance Monitor - Discord Commander performance monitoring
==========================================================

Performance monitoring extracted from optimization.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import threading
import time
from collections import deque
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from .performance_metrics import (
    DiscordPerformanceMetrics,
    PerformanceAlert,
    PerformanceMetricsCalculator,
    PerformanceThresholds,
)

logger = logging.getLogger(__name__)


class DiscordPerformanceMonitor:
    """Monitor Discord Commander performance metrics."""

    def __init__(self, max_history: int = 1000):
        """Initialize performance monitor."""
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.thresholds = PerformanceThresholds()
        self.calculator = PerformanceMetricsCalculator(self.thresholds)

        # Performance tracking
        self.start_time = time.time()
        self.message_count = 0
        self.command_count = 0
        self.error_count = 0
        self.last_message_time = 0.0
        self.last_command_time = 0.0

        # Callbacks
        self.alert_callbacks: list[Callable[[PerformanceAlert], None]] = []

        # Thread safety
        self._lock = threading.Lock()

    def start_monitoring(self, interval: float = 30.0):
        """Start periodic performance monitoring."""

        def monitor_loop():
            while True:
                try:
                    self._collect_metrics()
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in performance monitoring: {e}")
                    time.sleep(interval)

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True, daemon=True, daemon=True)
        monitor_thread.start()
        logger.info("Performance monitoring started")

    def record_message_processed(self, processing_time: float):
        """Record a message processing event."""
        with self._lock:
            self.message_count += 1
            self.last_message_time = processing_time

    def record_command_executed(self, execution_time: float):
        """Record a command execution event."""
        with self._lock:
            self.command_count += 1
            self.last_command_time = execution_time

    def record_error(self):
        """Record an error event."""
        with self._lock:
            self.error_count += 1

    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]):
        """Add alert callback function."""
        self.alert_callbacks.append(callback)

    def get_current_metrics(self) -> DiscordPerformanceMetrics:
        """Get current performance metrics."""
        with self._lock:
            uptime = time.time() - self.start_time

            # Calculate rates
            messages_per_second = self.message_count / uptime if uptime > 0 else 0
            commands_per_second = self.command_count / uptime if uptime > 0 else 0
            error_rate = self.error_count / max(self.message_count + self.command_count, 1)

            # Get memory usage (simplified)
            memory_usage = self._get_memory_usage()

            return DiscordPerformanceMetrics(
                message_processing_time=self.last_message_time,
                command_execution_time=self.last_command_time,
                event_handling_time=0.0,  # TODO: Implement event timing
                memory_usage=memory_usage,
                messages_per_second=messages_per_second,
                commands_per_second=commands_per_second,
                error_rate=error_rate,
                uptime_seconds=uptime,
                timestamp=datetime.now().isoformat(),
            )

    def _collect_metrics(self):
        """Collect and store current metrics."""
        try:
            metrics = self.get_current_metrics()
            self.metrics_history.append(metrics)

            # Check for alerts
            alerts = self.calculator.check_for_alerts(metrics)
            for alert in alerts:
                self._trigger_alert(alert)

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

    def _trigger_alert(self, alert: PerformanceAlert):
        """Trigger performance alert."""
        logger.warning(f"Performance Alert: {alert.message}")

        # Call all registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            # Fallback: return 0 if psutil not available
            return 0.0
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return 0.0

    def get_metrics_history(self, minutes: int = 60) -> list[DiscordPerformanceMetrics]:
        """Get metrics history for specified time period."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)

        with self._lock:
            recent_metrics = []
            for metrics in self.metrics_history:
                if datetime.fromisoformat(metrics.timestamp) >= cutoff_time:
                    recent_metrics.append(metrics)

            return recent_metrics

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance summary."""
        current_metrics = self.get_current_metrics()

        return {
            "current_metrics": current_metrics.to_dict(),
            "performance_score": current_metrics.get_performance_score(),
            "is_healthy": current_metrics.is_healthy(),
            "uptime_hours": current_metrics.uptime_seconds / 3600,
            "total_messages": self.message_count,
            "total_commands": self.command_count,
            "total_errors": self.error_count,
            "metrics_in_history": len(self.metrics_history),
        }

    def reset_metrics(self):
        """Reset performance metrics."""
        with self._lock:
            self.start_time = time.time()
            self.message_count = 0
            self.command_count = 0
            self.error_count = 0
            self.last_message_time = 0.0
            self.last_command_time = 0.0
            self.metrics_history.clear()

        logger.info("Performance metrics reset")

    def update_thresholds(self, new_thresholds: PerformanceThresholds):
        """Update performance thresholds."""
        self.thresholds = new_thresholds
        self.calculator.thresholds = new_thresholds
        logger.info("Performance thresholds updated")
