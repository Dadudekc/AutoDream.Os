#!/usr/bin/env python3
"""
Performance Validator Module - Agent Cellphone V2
===============================================

Performance metrics validation functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""




class PerformanceValidator:
    """Handles performance metrics validation."""

    def validate_performance_metrics(
        self, metrics_data: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate performance metrics and thresholds."""
        issues = []

        # Check response time thresholds
        if "response_time" in metrics_data:
            response_time = metrics_data["response_time"]
            if get_unified_validator().validate_type(response_time, (int, float)) and response_time > 5.0:
                issues.append(
                    ValidationIssue(
                        rule_id="performance_threshold",
                        rule_name="Performance Threshold",
                        severity=ValidationSeverity.WARNING,
                        message=f"Response time exceeds threshold: {response_time}s",
                        details={"threshold": 5.0, "actual": response_time},
                        timestamp=datetime.now(),
                        component="performance_metrics",
                    )
                )

        # Check throughput metrics
        if "throughput" in metrics_data:
            throughput = metrics_data["throughput"]
            if get_unified_validator().validate_type(throughput, (int, float)) and throughput < 100:
                issues.append(
                    ValidationIssue(
                        rule_id="performance_threshold",
                        rule_name="Performance Threshold",
                        severity=ValidationSeverity.WARNING,
                        message=f"Throughput below threshold: {throughput}",
                        details={"threshold": 100, "actual": throughput},
                        timestamp=datetime.now(),
                        component="performance_metrics",
                    )
                )

        return issues
