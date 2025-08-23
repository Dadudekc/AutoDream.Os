#!/usr/bin/env python3
"""
⚖️ Health Threshold Manager - Agent_Cellphone_V2

This component is responsible for managing health thresholds and configurations.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class HealthMetricType(Enum):
    """Types of health metrics"""

    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


@dataclass
class HealthThreshold:
    """Health threshold configuration"""

    metric_type: str
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


class HealthThresholdManager:
    """
    Health Threshold Manager - Single responsibility: Manage health thresholds and configurations.

    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """

    def __init__(self):
        """Initialize the threshold manager"""
        self.thresholds: Dict[str, HealthThreshold] = {}
        self._initialize_default_thresholds()
        logger.info("HealthThresholdManager initialized with default thresholds")

    def _initialize_default_thresholds(self):
        """Initialize default health thresholds"""
        default_thresholds = [
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

        for threshold in default_thresholds:
            self.thresholds[threshold.metric_type] = threshold

    def set_threshold(
        self,
        metric_type: str,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ):
        """Set custom health threshold for a metric type"""
        threshold = HealthThreshold(
            metric_type=metric_type,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            unit=unit,
            description=description,
        )

        self.thresholds[metric_type] = threshold
        logger.info(f"Health threshold updated for {metric_type}")

    def get_threshold(self, metric_type: str) -> Optional[HealthThreshold]:
        """Get health threshold for a specific metric type"""
        return self.thresholds.get(metric_type)

    def get_all_thresholds(self) -> Dict[str, HealthThreshold]:
        """Get all health thresholds"""
        return self.thresholds.copy()

    def remove_threshold(self, metric_type: str):
        """Remove a health threshold"""
        if metric_type in self.thresholds:
            del self.thresholds[metric_type]
            logger.info(f"Health threshold removed for {metric_type}")

    def has_threshold(self, metric_type: str) -> bool:
        """Check if a threshold exists for a metric type"""
        return metric_type in self.thresholds

    def get_threshold_count(self) -> int:
        """Get the total number of thresholds"""
        return len(self.thresholds)

    def validate_threshold(self, metric_type: str, value: float) -> str:
        """Validate a metric value against its threshold"""
        threshold = self.get_threshold(metric_type)
        if not threshold:
            return "unknown"

        if value >= threshold.critical_threshold:
            return "critical"
        elif value >= threshold.warning_threshold:
            return "warning"
        else:
            return "good"

    def get_threshold_summary(self) -> Dict[str, Dict[str, float]]:
        """Get a summary of all thresholds"""
        summary = {}
        for metric_type, threshold in self.thresholds.items():
            summary[metric_type] = {
                "warning": threshold.warning_threshold,
                "critical": threshold.critical_threshold,
                "unit": threshold.unit,
            }
        return summary

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthThresholdManager smoke test...")

            # Test basic initialization
            assert len(self.thresholds) > 0
            assert self.get_threshold_count() > 0
            logger.info("Basic initialization passed")

            # Test default thresholds
            response_threshold = self.get_threshold("response_time")
            assert response_threshold is not None
            assert response_threshold.unit == "ms"
            assert response_threshold.warning_threshold == 1000.0
            logger.info("Default thresholds passed")

            # Test custom threshold
            self.set_threshold(
                "custom_metric",
                warning_threshold=50.0,
                critical_threshold=100.0,
                unit="count",
                description="Custom metric threshold",
            )

            custom_threshold = self.get_threshold("custom_metric")
            assert custom_threshold is not None
            assert custom_threshold.warning_threshold == 50.0
            assert custom_threshold.critical_threshold == 100.0
            logger.info("Custom threshold passed")

            # Test threshold validation
            assert self.validate_threshold("response_time", 500.0) == "good"
            assert self.validate_threshold("response_time", 1500.0) == "warning"
            assert self.validate_threshold("response_time", 6000.0) == "critical"
            logger.info("Threshold validation passed")

            # Test threshold summary
            summary = self.get_threshold_summary()
            assert "response_time" in summary
            assert "custom_metric" in summary
            logger.info("Threshold summary passed")

            # Test threshold removal
            self.remove_threshold("custom_metric")
            assert not self.has_threshold("custom_metric")
            logger.info("Threshold removal passed")

            logger.info("✅ HealthThresholdManager smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthThresholdManager smoke test FAILED: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return False


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Threshold Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.test:
        manager = HealthThresholdManager()
        success = manager.run_smoke_test()
        exit(0 if success else 1)

    elif args.demo:
        print("🚀 Starting Health Threshold Manager Demo...")
        manager = HealthThresholdManager()

        # Show default thresholds
        print(f"\n📊 Default Thresholds ({manager.get_threshold_count()} total):")
        for metric_type, threshold in manager.thresholds.items():
            print(
                f"  {metric_type}: {threshold.warning_threshold}{threshold.unit} (warning) / {threshold.critical_threshold}{threshold.unit} (critical)"
            )

        # Add custom threshold
        print("\n⚙️ Adding custom threshold...")
        manager.set_threshold("custom_metric", 50.0, 100.0, "count", "Custom metric")

        # Test validation
        print("\n🧪 Testing threshold validation:")
        test_values = [25.0, 75.0, 125.0]
        for value in test_values:
            status = manager.validate_threshold("custom_metric", value)
            print(f"  Value {value}: {status}")

        # Show summary
        print("\n📋 Threshold Summary:")
        summary = manager.get_threshold_summary()
        for metric, details in summary.items():
            print(
                f"  {metric}: {details['warning']}{details['unit']} / {details['critical']}{details['unit']}"
            )

        print("\n✅ Demo completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
