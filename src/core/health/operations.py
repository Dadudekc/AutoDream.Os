#!/usr/bin/env python3
"""
Health Threshold Operations - Agent_Cellphone_V2

Extracted operations service for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, Optional, List, Any

from .models import HealthThreshold, ThresholdOperation, ConfigurationChange


class HealthThresholdOperations:
    """Service for managing health threshold operations"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.thresholds: Dict[str, HealthThreshold] = {}
        self.threshold_operations: List[ThresholdOperation] = []
        self.configuration_changes: List[ConfigurationChange] = []
    
    def set_threshold(
        self,
        metric_type: str,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ) -> bool:
        """Set custom health threshold for a metric type"""
        try:
            threshold = HealthThreshold(
                metric_type=metric_type,
                warning_threshold=warning_threshold,
                critical_threshold=critical_threshold,
                unit=unit,
                description=description,
            )

            self.thresholds[metric_type] = threshold
            
            # Record threshold operation
            operation_record = ThresholdOperation(
                timestamp=datetime.now().isoformat(),
                operation="set_threshold",
                metric_type=metric_type,
                success=True,
                warning_threshold=warning_threshold,
                critical_threshold=critical_threshold,
                unit=unit
            )
            self.threshold_operations.append(operation_record)
            
            # Record configuration change
            config_record = ConfigurationChange(
                timestamp=datetime.now().isoformat(),
                operation="set_threshold",
                metric_type=metric_type,
                success=True
            )
            self.configuration_changes.append(config_record)
            
            self.logger.info(f"Health threshold updated for {metric_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set threshold for {metric_type}: {e}")
            return False

    def get_threshold(self, metric_type: str) -> Optional[HealthThreshold]:
        """Get health threshold for a specific metric type"""
        return self.thresholds.get(metric_type)

    def get_all_thresholds(self) -> Dict[str, HealthThreshold]:
        """Get all health thresholds"""
        return self.thresholds.copy()

    def remove_threshold(self, metric_type: str) -> bool:
        """Remove a health threshold"""
        try:
            if metric_type in self.thresholds:
                del self.thresholds[metric_type]
                
                # Record threshold operation
                operation_record = ThresholdOperation(
                    timestamp=datetime.now().isoformat(),
                    operation="remove_threshold",
                    metric_type=metric_type,
                    success=True
                )
                self.threshold_operations.append(operation_record)
                
                # Record configuration change
                config_record = ConfigurationChange(
                    timestamp=datetime.now().isoformat(),
                    operation="remove_threshold",
                    metric_type=metric_type,
                    success=True
                )
                self.configuration_changes.append(config_record)
                
                self.logger.info(f"Health threshold removed for {metric_type}")
                return True
            return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove threshold for {metric_type}: {e}")
            return False

    def has_threshold(self, metric_type: str) -> bool:
        """Check if a threshold exists for a metric type"""
        return metric_type in self.thresholds

    def get_threshold_count(self) -> int:
        """Get the total number of thresholds"""
        return len(self.thresholds)

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

    def clear_operations(self):
        """Clear operation tracking data"""
        self.threshold_operations.clear()
        self.configuration_changes.clear()

    def get_operations_stats(self) -> Dict[str, int]:
        """Get operations statistics"""
        return {
            "threshold_operations_count": len(self.threshold_operations),
            "configuration_changes_count": len(self.configuration_changes),
        }
