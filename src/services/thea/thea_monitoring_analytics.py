#!/usr/bin/env python3
"""
Thea Monitoring Analytics - Analytics and Reporting
===================================================

Analytics and reporting operations for Thea monitoring system.
Handles performance analysis and data export.

V2 Compliance: ≤400 lines, focused analytics module
Author: Agent-6 (Quality Assurance Specialist)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .thea_monitoring_models import PerformanceMetrics, SystemHealth


class TheaMonitoringAnalytics:
    """
    Analytics and reporting for Thea monitoring system.

    Handles performance analysis and data export.
    """

    def __init__(
        self, performance_data: list[PerformanceMetrics], system_health_data: list[SystemHealth]
    ):
        """Initialize analytics with data."""
        self.performance_data = performance_data
        self.system_health_data = system_health_data

    def get_performance_summary(self, hours: int = 24) -> dict[str, Any]:
        """Get performance summary for specified hours."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            # Filter recent data
            recent_data = [
                data
                for data in self.performance_data
                if datetime.fromisoformat(data.timestamp) > cutoff_time
            ]

            if not recent_data:
                return {
                    "total_operations": 0,
                    "success_rate": 0.0,
                    "average_duration": 0.0,
                    "average_memory_usage": 0.0,
                    "average_cpu_usage": 0.0,
                    "error_count": 0,
                }

            # Calculate metrics
            total_operations = len(recent_data)
            successful_operations = sum(1 for data in recent_data if data.success)
            success_rate = (successful_operations / total_operations) * 100

            average_duration = sum(data.duration for data in recent_data) / total_operations
            average_memory = sum(data.memory_usage for data in recent_data) / total_operations
            average_cpu = sum(data.cpu_usage for data in recent_data) / total_operations

            error_count = sum(1 for data in recent_data if not data.success)

            return {
                "total_operations": total_operations,
                "success_rate": round(success_rate, 2),
                "average_duration": round(average_duration, 2),
                "average_memory_usage": round(average_memory, 2),
                "average_cpu_usage": round(average_cpu, 2),
                "error_count": error_count,
                "time_range_hours": hours,
            }

        except Exception as e:
            return {
                "error": f"Failed to generate performance summary: {e}",
                "total_operations": 0,
                "success_rate": 0.0,
                "average_duration": 0.0,
                "average_memory_usage": 0.0,
                "average_cpu_usage": 0.0,
                "error_count": 0,
            }

    def get_system_health_summary(self, hours: int = 24) -> dict[str, Any]:
        """Get system health summary for specified hours."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            # Filter recent data
            recent_data = [
                data
                for data in self.system_health_data
                if datetime.fromisoformat(data.timestamp) > cutoff_time
            ]

            if not recent_data:
                return {
                    "total_checks": 0,
                    "average_cpu_usage": 0.0,
                    "average_memory_usage": 0.0,
                    "average_disk_usage": 0.0,
                    "network_uptime": 0.0,
                    "browser_uptime": 0.0,
                    "cookies_valid_rate": 0.0,
                    "overall_health": "unknown",
                }

            # Calculate metrics
            total_checks = len(recent_data)
            average_cpu = sum(data.cpu_usage for data in recent_data) / total_checks
            average_memory = sum(data.memory_usage for data in recent_data) / total_checks
            average_disk = sum(data.disk_usage for data in recent_data) / total_checks

            network_uptime = (
                sum(1 for data in recent_data if data.network_connected) / total_checks
            ) * 100
            browser_uptime = (
                sum(1 for data in recent_data if data.browser_running) / total_checks
            ) * 100
            cookies_valid_rate = (
                sum(1 for data in recent_data if data.cookies_valid) / total_checks
            ) * 100

            # Determine overall health
            health_counts = {}
            for data in recent_data:
                health = data.overall_health
                health_counts[health] = health_counts.get(health, 0) + 1

            overall_health = (
                max(health_counts, key=health_counts.get) if health_counts else "unknown"
            )

            return {
                "total_checks": total_checks,
                "average_cpu_usage": round(average_cpu, 2),
                "average_memory_usage": round(average_memory, 2),
                "average_disk_usage": round(average_disk, 2),
                "network_uptime": round(network_uptime, 2),
                "browser_uptime": round(browser_uptime, 2),
                "cookies_valid_rate": round(cookies_valid_rate, 2),
                "overall_health": overall_health,
                "time_range_hours": hours,
            }

        except Exception as e:
            return {
                "error": f"Failed to generate system health summary: {e}",
                "total_checks": 0,
                "average_cpu_usage": 0.0,
                "average_memory_usage": 0.0,
                "average_disk_usage": 0.0,
                "network_uptime": 0.0,
                "browser_uptime": 0.0,
                "cookies_valid_rate": 0.0,
                "overall_health": "error",
            }

    def export_data(self, output_dir: str = "exports/thea_monitoring") -> dict[str, Any]:
        """Export monitoring data to files."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

            # Export performance data
            performance_file = output_path / f"performance_data_{timestamp}.json"
            performance_export = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "data_type": "performance_metrics",
                "total_records": len(self.performance_data),
                "data": [data.to_dict() for data in self.performance_data],
            }

            with open(performance_file, "w") as f:
                json.dump(performance_export, f, indent=2)

            # Export system health data
            health_file = output_path / f"system_health_{timestamp}.json"
            health_export = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "data_type": "system_health",
                "total_records": len(self.system_health_data),
                "data": [data.to_dict() for data in self.system_health_data],
            }

            with open(health_file, "w") as f:
                json.dump(health_export, f, indent=2)

            # Generate summary report
            summary_file = output_path / f"monitoring_summary_{timestamp}.json"
            summary = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "performance_summary": self.get_performance_summary(),
                "system_health_summary": self.get_system_health_summary(),
                "export_files": {
                    "performance_data": str(performance_file),
                    "system_health": str(health_file),
                    "summary": str(summary_file),
                },
            }

            with open(summary_file, "w") as f:
                json.dump(summary, f, indent=2)

            return {
                "success": True,
                "export_directory": str(output_path),
                "files_created": [str(performance_file), str(health_file), str(summary_file)],
                "total_records": {
                    "performance": len(self.performance_data),
                    "system_health": len(self.system_health_data),
                },
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to export data: {e}",
                "export_directory": None,
                "files_created": [],
                "total_records": {"performance": 0, "system_health": 0},
            }


__all__ = ["TheaMonitoringAnalytics"]
