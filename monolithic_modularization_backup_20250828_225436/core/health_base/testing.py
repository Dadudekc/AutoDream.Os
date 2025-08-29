#!/usr/bin/env python3
"""
Health Threshold Testing - Agent_Cellphone_V2

Extracted testing service for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, Any

from .models import HealthThreshold


class HealthThresholdTesting:
    """Service for testing health threshold functionality"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def run_smoke_test(
        self,
        get_threshold_count_func,
        get_threshold_func,
        set_threshold_func,
        has_threshold_func,
        remove_threshold_func,
        validate_threshold_func,
        get_threshold_summary_func,
    ) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            start_time = datetime.now()

            self.logger.info("Running HealthThresholdManager smoke test...")

            # Test basic initialization
            threshold_count = get_threshold_count_func()
            assert threshold_count > 0
            self.logger.info("Basic initialization passed")

            # Test default thresholds
            response_threshold = get_threshold_func("response_time")
            assert response_threshold is not None
            assert response_threshold.unit == "ms"
            assert response_threshold.warning_threshold == 1000.0
            self.logger.info("Default thresholds passed")

            # Test custom threshold
            set_threshold_func(
                "custom_metric",
                warning_threshold=50.0,
                critical_threshold=100.0,
                unit="count",
                description="Custom metric threshold",
            )

            custom_threshold = get_threshold_func("custom_metric")
            assert custom_threshold is not None
            assert custom_threshold.warning_threshold == 50.0
            assert custom_threshold.critical_threshold == 100.0
            self.logger.info("Custom threshold passed")

            # Test threshold validation
            assert validate_threshold_func("response_time", 500.0) == "good"
            assert validate_threshold_func("response_time", 1500.0) == "warning"
            assert validate_threshold_func("response_time", 6000.0) == "critical"
            self.logger.info("Threshold validation passed")

            # Test threshold summary
            summary = get_threshold_summary_func()
            assert "response_time" in summary
            assert "custom_metric" in summary
            self.logger.info("Threshold summary passed")

            # Test threshold removal
            remove_threshold_func("custom_metric")
            assert not has_threshold_func("custom_metric")
            self.logger.info("Threshold removal passed")

            self.logger.info("✅ HealthThresholdManager smoke test PASSED")
            return True

        except Exception as e:
            self.logger.error(f"❌ HealthThresholdManager smoke test FAILED: {e}")
            import traceback

            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def run_validation_test(self, get_threshold_func, validate_threshold_func) -> bool:
        """Run validation-specific tests"""
        try:
            self.logger.info("Running validation tests...")

            # Test various threshold values
            test_cases = [
                ("response_time", 500.0, "good"),
                ("response_time", 1500.0, "warning"),
                ("response_time", 6000.0, "critical"),
                ("memory_usage", 50.0, "good"),
                ("memory_usage", 85.0, "warning"),
                ("memory_usage", 98.0, "critical"),
            ]

            for metric_type, value, expected_status in test_cases:
                threshold = get_threshold_func(metric_type)
                if threshold:
                    actual_status = validate_threshold_func(metric_type, value)
                    assert (
                        actual_status == expected_status
                    ), f"Expected {expected_status}, got {actual_status} for {metric_type}={value}"

            self.logger.info("✅ Validation tests PASSED")
            return True

        except Exception as e:
            self.logger.error(f"❌ Validation tests FAILED: {e}")
            return False

    def run_performance_test(
        self, set_threshold_func, get_threshold_func, iterations: int = 1000
    ) -> bool:
        """Run performance tests"""
        try:
            self.logger.info(
                f"Running performance tests with {iterations} iterations..."
            )

            start_time = datetime.now()

            # Test bulk operations
            for i in range(iterations):
                metric_name = f"perf_test_{i}"
                set_threshold_func(
                    metric_name, 50.0, 100.0, "count", f"Performance test {i}"
                )
                threshold = get_threshold_func(metric_name)
                assert threshold is not None

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            ops_per_second = iterations / duration

            self.logger.info(f"✅ Performance test PASSED: {ops_per_second:.2f} ops/sec")
            return True

        except Exception as e:
            self.logger.error(f"❌ Performance test FAILED: {e}")
            return False
