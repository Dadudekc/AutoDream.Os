#!/usr/bin/env python3
"""
Performance Metrics - Discord Commander performance tracking
=========================================================

Performance metrics extracted from optimization.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DiscordPerformanceMetrics:
    """Performance metrics for Discord Commander."""

    message_processing_time: float
    command_execution_time: float
    event_handling_time: float
    memory_usage: float
    messages_per_second: float
    commands_per_second: float
    error_rate: float
    uptime_seconds: float
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "message_processing_time": self.message_processing_time,
            "command_execution_time": self.command_execution_time,
            "event_handling_time": self.event_handling_time,
            "memory_usage": self.memory_usage,
            "messages_per_second": self.messages_per_second,
            "commands_per_second": self.commands_per_second,
            "error_rate": self.error_rate,
            "uptime_seconds": self.uptime_seconds,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DiscordPerformanceMetrics":
        """Create metrics from dictionary."""
        return cls(
            message_processing_time=data.get("message_processing_time", 0.0),
            command_execution_time=data.get("command_execution_time", 0.0),
            event_handling_time=data.get("event_handling_time", 0.0),
            memory_usage=data.get("memory_usage", 0.0),
            messages_per_second=data.get("messages_per_second", 0.0),
            commands_per_second=data.get("commands_per_second", 0.0),
            error_rate=data.get("error_rate", 0.0),
            uptime_seconds=data.get("uptime_seconds", 0.0),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )

    def is_healthy(self) -> bool:
        """Check if performance metrics indicate healthy system."""
        return (
            self.message_processing_time < 1.0
            and self.command_execution_time < 2.0
            and self.event_handling_time < 0.5
            and self.memory_usage < 1000.0
            and self.error_rate < 0.05  # MB
            and self.uptime_seconds > 0  # 5%
        )

    def get_performance_score(self) -> float:
        """Calculate overall performance score (0-100)."""
        scores = []

        # Message processing score
        if self.message_processing_time < 0.1:
            scores.append(100)
        elif self.message_processing_time < 0.5:
            scores.append(80)
        elif self.message_processing_time < 1.0:
            scores.append(60)
        else:
            scores.append(40)

        # Command execution score
        if self.command_execution_time < 0.5:
            scores.append(100)
        elif self.command_execution_time < 1.0:
            scores.append(80)
        elif self.command_execution_time < 2.0:
            scores.append(60)
        else:
            scores.append(40)

        # Memory usage score
        if self.memory_usage < 100:
            scores.append(100)
        elif self.memory_usage < 500:
            scores.append(80)
        elif self.memory_usage < 1000:
            scores.append(60)
        else:
            scores.append(40)

        # Error rate score
        if self.error_rate < 0.01:
            scores.append(100)
        elif self.error_rate < 0.05:
            scores.append(80)
        elif self.error_rate < 0.1:
            scores.append(60)
        else:
            scores.append(40)

        return sum(scores) / len(scores) if scores else 0.0


@dataclass
class PerformanceThresholds:
    """Performance thresholds for monitoring."""

    max_message_processing_time: float = 1.0
    max_command_execution_time: float = 2.0
    max_event_handling_time: float = 0.5
    max_memory_usage: float = 1000.0
    max_error_rate: float = 0.05
    min_messages_per_second: float = 1.0
    min_commands_per_second: float = 0.5

    def check_metrics(self, metrics: DiscordPerformanceMetrics) -> dict[str, bool]:
        """Check metrics against thresholds."""
        return {
            "message_processing_ok": metrics.message_processing_time
            <= self.max_message_processing_time,
            "command_execution_ok": metrics.command_execution_time
            <= self.max_command_execution_time,
            "event_handling_ok": metrics.event_handling_time <= self.max_event_handling_time,
            "memory_usage_ok": metrics.memory_usage <= self.max_memory_usage,
            "error_rate_ok": metrics.error_rate <= self.max_error_rate,
            "messages_per_second_ok": metrics.messages_per_second >= self.min_messages_per_second,
            "commands_per_second_ok": metrics.commands_per_second >= self.min_commands_per_second,
        }


@dataclass
class PerformanceAlert:
    """Performance alert data."""

    alert_type: str
    metric_name: str
    current_value: float
    threshold_value: float
    severity: str
    timestamp: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "alert_type": self.alert_type,
            "metric_name": self.metric_name,
            "current_value": self.current_value,
            "threshold_value": self.threshold_value,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "message": self.message,
        }


class PerformanceMetricsCalculator:
    """Calculate performance metrics from raw data."""

    def __init__(self, thresholds: PerformanceThresholds = None):
        """Initialize calculator."""
        self.thresholds = thresholds or PerformanceThresholds()

    def calculate_metrics(self, raw_data: dict[str, Any]) -> DiscordPerformanceMetrics:
        """Calculate performance metrics from raw data."""
        return DiscordPerformanceMetrics(
            message_processing_time=raw_data.get("message_processing_time", 0.0),
            command_execution_time=raw_data.get("command_execution_time", 0.0),
            event_handling_time=raw_data.get("event_handling_time", 0.0),
            memory_usage=raw_data.get("memory_usage", 0.0),
            messages_per_second=raw_data.get("messages_per_second", 0.0),
            commands_per_second=raw_data.get("commands_per_second", 0.0),
            error_rate=raw_data.get("error_rate", 0.0),
            uptime_seconds=raw_data.get("uptime_seconds", 0.0),
            timestamp=datetime.now().isoformat(),
        )

    def check_for_alerts(self, metrics: DiscordPerformanceMetrics) -> list[PerformanceAlert]:
        """Check metrics for alerts."""
        alerts = []
        checks = self.thresholds.check_metrics(metrics)

        if not checks["message_processing_ok"]:
            alerts.append(
                PerformanceAlert(
                    alert_type="threshold_exceeded",
                    metric_name="message_processing_time",
                    current_value=metrics.message_processing_time,
                    threshold_value=self.thresholds.max_message_processing_time,
                    severity="warning",
                    timestamp=metrics.timestamp,
                    message=f"Message processing time {metrics.message_processing_time:.2f}s exceeds threshold {self.thresholds.max_message_processing_time}s",
                )
            )

        if not checks["command_execution_ok"]:
            alerts.append(
                PerformanceAlert(
                    alert_type="threshold_exceeded",
                    metric_name="command_execution_time",
                    current_value=metrics.command_execution_time,
                    threshold_value=self.thresholds.max_command_execution_time,
                    severity="warning",
                    timestamp=metrics.timestamp,
                    message=f"Command execution time {metrics.command_execution_time:.2f}s exceeds threshold {self.thresholds.max_command_execution_time}s",
                )
            )

        if not checks["memory_usage_ok"]:
            alerts.append(
                PerformanceAlert(
                    alert_type="threshold_exceeded",
                    metric_name="memory_usage",
                    current_value=metrics.memory_usage,
                    threshold_value=self.thresholds.max_memory_usage,
                    severity="critical",
                    timestamp=metrics.timestamp,
                    message=f"Memory usage {metrics.memory_usage:.2f}MB exceeds threshold {self.thresholds.max_memory_usage}MB",
                )
            )

        if not checks["error_rate_ok"]:
            alerts.append(
                PerformanceAlert(
                    alert_type="threshold_exceeded",
                    metric_name="error_rate",
                    current_value=metrics.error_rate,
                    threshold_value=self.thresholds.max_error_rate,
                    severity="critical",
                    timestamp=metrics.timestamp,
                    message=f"Error rate {metrics.error_rate:.2%} exceeds threshold {self.thresholds.max_error_rate:.2%}",
                )
            )

        return alerts
