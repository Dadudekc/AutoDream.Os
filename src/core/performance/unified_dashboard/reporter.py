"""
Dashboard Reporter - KISS Simplified
===================================

Simplified dashboard reporting for V2 compliance.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined reporting logic.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from .engine import DashboardEngine
from .models import AlertLevel, MetricType, PerformanceReport


class DashboardReporter:
    """Simplified dashboard reporting functionality."""

    def __init__(self, engine: DashboardEngine):
        """Initialize dashboard reporter."""
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False

    def initialize(self) -> bool:
        """Initialize the reporter - simplified."""
        try:
            if not self.engine.is_initialized:
                raise Exception("Engine not initialized")

            self.is_initialized = True
            self.logger.info("Dashboard Reporter initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Dashboard Reporter: {e}")
            return False

    def generate_metrics_report(
        self, metric_type: MetricType = None, hours: int = 24
    ) -> dict[str, Any]:
        """Generate metrics report - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Reporter not initialized")

            # Get metrics from engine
            metrics = self.engine.get_metrics(metric_type, hours)

            # Calculate summary statistics
            total_metrics = len(metrics)
            if total_metrics == 0:
                return {
                    "report_id": f"metrics_{int(datetime.now().timestamp())}",
                    "metric_type": metric_type.value if metric_type else "all",
                    "time_range_hours": hours,
                    "total_metrics": 0,
                    "summary": "No metrics available",
                    "generated_at": datetime.now().isoformat(),
                }

            # Calculate basic statistics
            values = [m.value for m in metrics if m.value is not None]
            avg_value = sum(values) / len(values) if values else 0
            max_value = max(values) if values else 0
            min_value = min(values) if values else 0

            return {
                "report_id": f"metrics_{int(datetime.now().timestamp())}",
                "metric_type": metric_type.value if metric_type else "all",
                "time_range_hours": hours,
                "total_metrics": total_metrics,
                "average_value": avg_value,
                "max_value": max_value,
                "min_value": min_value,
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error generating metrics report: {e}")
            return {
                "report_id": f"metrics_{int(datetime.now().timestamp())}",
                "error": str(e),
                "generated_at": datetime.now().isoformat(),
            }

    def generate_alerts_report(
        self, alert_level: AlertLevel = None, hours: int = 24
    ) -> dict[str, Any]:
        """Generate alerts report - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Reporter not initialized")

            # Get alerts from engine
            alerts = self.engine.get_alerts(alert_level, hours)

            # Calculate summary statistics
            total_alerts = len(alerts)
            critical_alerts = len([a for a in alerts if a.level == AlertLevel.CRITICAL])
            warning_alerts = len([a for a in alerts if a.level == AlertLevel.WARNING])
            info_alerts = len([a for a in alerts if a.level == AlertLevel.INFO])

            return {
                "report_id": f"alerts_{int(datetime.now().timestamp())}",
                "alert_level": alert_level.value if alert_level else "all",
                "time_range_hours": hours,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "warning_alerts": warning_alerts,
                "info_alerts": info_alerts,
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error generating alerts report: {e}")
            return {
                "report_id": f"alerts_{int(datetime.now().timestamp())}",
                "error": str(e),
                "generated_at": datetime.now().isoformat(),
            }

    def generate_performance_report(self, hours: int = 24) -> PerformanceReport:
        """Generate comprehensive performance report - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Reporter not initialized")

            # Generate metrics and alerts reports
            metrics_report = self.generate_metrics_report(hours=hours)
            alerts_report = self.generate_alerts_report(hours=hours)

            # Create performance report
            report = PerformanceReport(
                report_id=f"performance_{int(datetime.now().timestamp())}",
                generated_at=datetime.now(),
                time_range_hours=hours,
                metrics_summary=metrics_report,
                alerts_summary=alerts_report,
                system_health=self._calculate_system_health(metrics_report, alerts_report),
            )

            return report

        except Exception as e:
            self.logger.error(f"Error generating performance report: {e}")
            return PerformanceReport(
                report_id=f"performance_{int(datetime.now().timestamp())}",
                generated_at=datetime.now(),
                time_range_hours=hours,
                metrics_summary={"error": str(e)},
                alerts_summary={"error": str(e)},
                system_health="error",
            )

    def _calculate_system_health(
        self, metrics_report: dict[str, Any], alerts_report: dict[str, Any]
    ) -> str:
        """Calculate system health - simplified."""
        try:
            critical_alerts = alerts_report.get("critical_alerts", 0)
            warning_alerts = alerts_report.get("warning_alerts", 0)

            if critical_alerts > 0:
                return "critical"
            elif warning_alerts > 5:
                return "warning"
            elif warning_alerts > 0:
                return "degraded"
            else:
                return "healthy"

        except Exception:
            return "unknown"

    def export_report(self, report: PerformanceReport, format: str = "json") -> str:
        """Export report - simplified."""
        try:
            if format.lower() == "json":
                return json.dumps(report.to_dict(), indent=2, default=str)
            else:
                return str(report)

        except Exception as e:
            self.logger.error(f"Error exporting report: {e}")
            return f"Export error: {str(e)}"

    def get_report_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get report history - simplified."""
        try:
            if not self.is_initialized:
                return []

            # Get recent reports from engine
            reports = self.engine.get_recent_reports(limit)

            return [
                {
                    "report_id": report.report_id,
                    "generated_at": report.generated_at.isoformat(),
                    "time_range_hours": report.time_range_hours,
                    "system_health": report.system_health,
                }
                for report in reports
            ]

        except Exception as e:
            self.logger.error(f"Error getting report history: {e}")
            return []

    def cleanup_old_reports(self, max_age_hours: int = 168) -> int:
        """Cleanup old reports - simplified."""
        try:
            if not self.is_initialized:
                return 0

            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned = self.engine.cleanup_old_reports(cutoff_time)

            if cleaned > 0:
                self.logger.info(f"Cleaned up {cleaned} old reports")

            return cleaned

        except Exception as e:
            self.logger.error(f"Error cleaning up reports: {e}")
            return 0

    def get_reporter_stats(self) -> dict[str, Any]:
        """Get reporter statistics - simplified."""
        return {
            "is_initialized": self.is_initialized,
            "engine_initialized": self.engine.is_initialized if self.engine else False,
            "reporter_type": "dashboard",
        }

    def shutdown(self) -> bool:
        """Shutdown reporter - simplified."""
        try:
            self.is_initialized = False
            self.logger.info("Dashboard Reporter shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False
