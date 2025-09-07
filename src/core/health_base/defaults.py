#!/usr/bin/env python3
"""
Health Threshold Defaults - Agent_Cellphone_V2

Extracted default thresholds configuration for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

from datetime import datetime
from typing import List

from .models import HealthThreshold


class HealthThresholdDefaults:
    """Service for managing default health thresholds"""

    @staticmethod
    def get_default_thresholds() -> List[HealthThreshold]:
        """Get list of default health thresholds"""
        return [
            HealthThreshold(
                "response_time",
                warning_threshold=1000.0,  # 1 second
                critical_threshold=5000.0,  # 5 seconds
                unit="ms",
                description="Response time threshold",
            ),
            HealthThreshold(
                "memory_usage",
                warning_threshold=80.0,  # 80%
                critical_threshold=95.0,  # 95%
                unit="%",
                description="Memory usage threshold",
            ),
            HealthThreshold(
                "cpu_usage",
                warning_threshold=85.0,  # 85%
                critical_threshold=95.0,  # 95%
                unit="%",
                description="CPU usage threshold",
            ),
            HealthThreshold(
                "error_rate",
                warning_threshold=5.0,  # 5%
                critical_threshold=15.0,  # 15%
                unit="%",
                description="Error rate threshold",
            ),
            HealthThreshold(
                "task_completion_rate",
                warning_threshold=90.0,  # 90%
                critical_threshold=75.0,  # 75%
                unit="%",
                description="Task completion rate threshold",
            ),
            HealthThreshold(
                "heartbeat_frequency",
                warning_threshold=120.0,  # 2 minutes
                critical_threshold=300.0,  # 5 minutes
                unit="seconds",
                description="Heartbeat frequency threshold",
            ),
            HealthThreshold(
                "contract_success_rate",
                warning_threshold=85.0,  # 85%
                critical_threshold=70.0,  # 70%
                unit="%",
                description="Contract success rate threshold",
            ),
            HealthThreshold(
                "communication_latency",
                warning_threshold=500.0,  # 500ms
                critical_threshold=2000.0,  # 2 seconds
                unit="ms",
                description="Communication latency threshold",
            ),
        ]

    @staticmethod
    def get_threshold_by_type(metric_type: str) -> HealthThreshold:
        """Get default threshold for a specific metric type"""
        for threshold in HealthThresholdDefaults.get_default_thresholds():
            if threshold.metric_type == metric_type:
                return threshold
        raise ValueError(f"No default threshold found for metric type: {metric_type}")

    @staticmethod
    def get_metric_types() -> List[str]:
        """Get list of all supported metric types"""
        return [
            threshold.metric_type
            for threshold in HealthThresholdDefaults.get_default_thresholds()
        ]

    @staticmethod
    def is_valid_metric_type(metric_type: str) -> bool:
        """Check if a metric type is supported"""
        return metric_type in HealthThresholdDefaults.get_metric_types()
