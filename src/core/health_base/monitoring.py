#!/usr/bin/env python3
"""
Health Threshold Monitoring - Agent_Cellphone_V2

Extracted monitoring service for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import logging
from typing import Dict, Any


class HealthThresholdMonitoring:
    """Service for monitoring health threshold management health"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def check_health_status(
        self,
        threshold_operations_count: int,
        validation_operations_count: int,
        configuration_changes_count: int,
    ) -> Dict[str, Any]:
        """Check health threshold management health status"""
        try:
            health_status = {
                "status": "healthy",
                "warnings": [],
                "metrics": {
                    "threshold_operations": threshold_operations_count,
                    "validation_operations": validation_operations_count,
                    "configuration_changes": configuration_changes_count,
                },
            }

            # Check for excessive threshold operations
            if threshold_operations_count > 1000:
                health_status["warnings"].append(
                    f"High number of threshold operations: {threshold_operations_count}"
                )
                health_status["status"] = "warning"

            # Check validation operations
            if validation_operations_count > 500:
                health_status["warnings"].append(
                    f"Large validation history: {validation_operations_count} records"
                )
                if validation_operations_count > 1000:
                    health_status["status"] = "warning"

            # Check configuration changes
            if configuration_changes_count > 100:
                health_status["warnings"].append(
                    f"High number of configuration changes: {configuration_changes_count}"
                )
                health_status["status"] = "warning"

            return health_status

        except Exception as e:
            self.logger.error(f"Failed to check health status: {e}")
            return {"status": "error", "error": str(e), "metrics": {}}

    def get_health_summary(
        self,
        total_thresholds: int,
        threshold_operations_count: int,
        validation_operations_count: int,
        configuration_changes_count: int,
        manager_status: str,
        manager_uptime: float,
    ) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        try:
            health_status = self.check_health_status(
                threshold_operations_count,
                validation_operations_count,
                configuration_changes_count,
            )

            summary = {
                "total_thresholds": total_thresholds,
                "threshold_operations_count": threshold_operations_count,
                "validation_operations_count": validation_operations_count,
                "configuration_changes_count": configuration_changes_count,
                "manager_status": manager_status,
                "manager_uptime": manager_uptime,
                "health_status": health_status,
            }

            return summary

        except Exception as e:
            self.logger.error(f"Failed to get health summary: {e}")
            return {"error": str(e)}

    def should_trigger_cleanup(
        self,
        threshold_operations_count: int,
        validation_operations_count: int,
        configuration_changes_count: int,
    ) -> bool:
        """Determine if cleanup should be triggered"""
        return (
            threshold_operations_count > 2000
            or validation_operations_count > 1500
            or configuration_changes_count > 200
        )

    def get_cleanup_recommendations(
        self,
        threshold_operations_count: int,
        validation_operations_count: int,
        configuration_changes_count: int,
    ) -> list:
        """Get cleanup recommendations based on current state"""
        recommendations = []

        if threshold_operations_count > 1000:
            recommendations.append("Consider archiving old threshold operations")

        if validation_operations_count > 500:
            recommendations.append("Consider archiving old validation operations")

        if configuration_changes_count > 100:
            recommendations.append("Consider archiving old configuration changes")

        return recommendations
