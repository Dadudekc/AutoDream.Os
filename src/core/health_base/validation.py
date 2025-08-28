#!/usr/bin/env python3
"""
Health Threshold Validation - Agent_Cellphone_V2

Extracted validation service for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

from .models import HealthThreshold, ValidationOperation


class HealthThresholdValidation:
    """Service for validating health thresholds"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.validation_operations: List[ValidationOperation] = []

    def validate_threshold(self, threshold: HealthThreshold, value: float) -> str:
        """Validate a metric value against its threshold"""
        try:
            if value >= threshold.critical_threshold:
                status = "critical"
            elif value >= threshold.warning_threshold:
                status = "warning"
            else:
                status = "good"

            # Record validation operation
            validation_record = ValidationOperation(
                timestamp=datetime.now().isoformat(),
                metric_type=threshold.metric_type,
                value=value,
                status=status,
                threshold={
                    "warning": threshold.warning_threshold,
                    "critical": threshold.critical_threshold,
                    "unit": threshold.unit,
                },
            )
            self.validation_operations.append(validation_record)

            return status

        except Exception as e:
            self.logger.error(
                f"Failed to validate threshold for {threshold.metric_type}: {e}"
            )
            return "unknown"

    def get_validation_history(
        self, metric_type: str = None
    ) -> List[ValidationOperation]:
        """Get validation operation history, optionally filtered by metric type"""
        if metric_type:
            return [
                op for op in self.validation_operations if op.metric_type == metric_type
            ]
        return self.validation_operations.copy()

    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        if not self.validation_operations:
            return {"total_validations": 0, "status_counts": {}}

        status_counts = {}
        for op in self.validation_operations:
            status_counts[op.status] = status_counts.get(op.status, 0) + 1

        return {
            "total_validations": len(self.validation_operations),
            "status_counts": status_counts,
            "last_validation": self.validation_operations[-1].timestamp
            if self.validation_operations
            else None,
        }

    def clear_validation_history(self):
        """Clear validation operation history"""
        self.validation_operations.clear()

    def get_validation_count(self) -> int:
        """Get total number of validation operations"""
        return len(self.validation_operations)
