#!/usr/bin/env python3
"""
Performance Reporting Manager - Report Generation and Management
=============================================================

Handles performance report generation, management, and distribution.
Follows V2 standards: ≤400 LOC, SRP, OOP design.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from .performance_models import (
    PerformanceMetric, BenchmarkResult, SystemPerformanceReport, 
    PerformanceLevel, PerformanceAlert
)


class PerformanceReportingManager:
    """
    Performance Reporting Manager - Handles report generation and management
    
    Single Responsibility: Generate comprehensive performance reports,
    manage report history, and distribute performance insights.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceReportingManager")
        
        # Reporting state
        self.reporting_active = False
        self.report_history: List[SystemPerformanceReport] = []
        
        # Report configuration
        self.report_config = {
            "include_metrics": True,
            "include_validation": True,
            "include_benchmarks": True,
            "include_recommendations": True,
            "include_alerts": True,
            "max_history_size": 100
        }
        
        # Statistics
        self.total_reports_generated = 0
        self.last_report_time: Optional[datetime] = None
        
        self.logger.info("Performance Reporting Manager initialized")
    
    def start_reporting(self) -> bool:
        """Start performance reporting"""
        try:
            if self.reporting_active:
                self.logger.warning("Reporting is already active")
                return True
            
            self.reporting_active = True
            self.logger.info("✅ Performance reporting started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start reporting: {e}")
            return False
    
    def stop_reporting(self) -> bool:
        """Stop performance reporting"""
        try:
            if not self.reporting_active:
                self.logger.warning("Reporting is not active")
                return True
            
            self.reporting_active = False
            self.logger.info("✅ Performance reporting stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop reporting: {e}")
            return False
    
    def generate_performance_report(
        self,
        metrics: List[PerformanceMetric],
        validation_results: List[Dict[str, Any]],
        benchmarks: List[BenchmarkResult]
    ) -> SystemPerformanceReport:
        """Generate a comprehensive performance report"""
        try:
            if not self.reporting_active:
                self.logger.warning("Reporting is not active")
                raise RuntimeError("Reporting system is not active")
            
            report_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            # Calculate system health
            system_health = self._calculate_system_health(validation_results)
            
            # Determine overall performance level
            overall_performance = self._calculate_performance_level(validation_results, benchmarks)
            
            # Generate metrics summary
            metrics_summary = self._generate_metrics_summary(metrics)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(validation_results, benchmarks)
            
            # Generate alerts
            alerts = self._generate_alerts(validation_results)
            
            # Create report
            report = SystemPerformanceReport(
                report_id=report_id,
                timestamp=timestamp,
                system_health=system_health,
                overall_performance_level=overall_performance,
                metrics_summary=metrics_summary,
                validation_results=validation_results,
                benchmarks=benchmarks,
                recommendations=recommendations,
                alerts=alerts
            )
            
            # Add to history
            self.report_history.append(report)
            self.total_reports_generated += 1
            self.last_report_time = timestamp
            
            # Maintain history size
            if len(self.report_history) > self.report_config["max_history_size"]:
                self.report_history.pop(0)
            
            self.logger.info(f"Performance report generated: {report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            raise
    
    def _calculate_system_health(self, validation_results: List[Dict[str, Any]]) -> str:
        """Calculate overall system health based on validation results"""
        try:
            if not validation_results:
                return "unknown"
            
            total_checks = len(validation_results)
            passed_checks = sum(1 for result in validation_results if result.get("status") == "pass")
            failed_checks = total_checks - passed_checks
            
            # Calculate health percentage
            health_percentage = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
            
            # Determine health status
            if health_percentage >= 95:
                return "excellent"
            elif health_percentage >= 85:
                return "good"
            elif health_percentage >= 70:
                return "fair"
            elif health_percentage >= 50:
                return "poor"
            else:
                return "critical"
                
        except Exception as e:
            self.logger.error(f"Failed to calculate system health: {e}")
            return "unknown"
    
    def _calculate_performance_level(self, validation_results: List[Dict[str, Any]], benchmarks: List[BenchmarkResult]) -> PerformanceLevel:
        """Calculate overall performance level"""
        try:
            # Check validation results
            critical_failures = sum(
                1 for result in validation_results 
                if result.get("status") == "fail" and result.get("severity") == "critical"
            )
            
            warning_failures = sum(
                1 for result in validation_results 
                if result.get("status") == "fail" and result.get("severity") == "warning"
            )
            
            # Check benchmark results
            failed_benchmarks = sum(1 for bench in benchmarks if not bench.success)
            total_benchmarks = len(benchmarks)
            
            # Determine performance level
            if critical_failures > 0:
                return PerformanceLevel.NOT_READY
            elif warning_failures > 3 or (total_benchmarks > 0 and failed_benchmarks > total_benchmarks * 0.2):
                return PerformanceLevel.BASIC
            elif warning_failures > 1 or (total_benchmarks > 0 and failed_benchmarks > total_benchmarks * 0.1):
                return PerformanceLevel.STANDARD
            elif warning_failures == 0 and failed_benchmarks == 0:
                return PerformanceLevel.EXCELLENT
            else:
                return PerformanceLevel.GOOD
                
        except Exception as e:
            self.logger.error(f"Failed to calculate performance level: {e}")
            return PerformanceLevel.BASIC
    
    def _generate_metrics_summary(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Generate metrics summary"""
        try:
            if not metrics:
                return {"total_metrics": 0, "metric_types": {}, "latest_values": {}}
            
            summary = {
                "total_metrics": len(metrics),
                "metric_types": {},
                "latest_values": {},
                "timestamp_range": {
                    "earliest": None,
                    "latest": None
                }
            }
            
            # Group by metric type
            for metric in metrics:
                metric_type = metric.metric_type.value
                if metric_type not in summary["metric_types"]:
                    summary["metric_types"][metric_type] = 0
                summary["metric_types"][metric_type] += 1
                
                # Store latest value for each metric name
                summary["latest_values"][metric.name] = {
                    "value": metric.value,
                    "unit": metric.unit,
                    "timestamp": metric.timestamp.isoformat()
                }
                
                # Track timestamp range
                if summary["timestamp_range"]["earliest"] is None or metric.timestamp < summary["timestamp_range"]["earliest"]:
                    summary["timestamp_range"]["earliest"] = metric.timestamp
                if summary["timestamp_range"]["latest"] is None or metric.timestamp > summary["timestamp_range"]["latest"]:
                    summary["timestamp_range"]["latest"] = metric.timestamp
            
            # Convert timestamps to ISO format
            if summary["timestamp_range"]["earliest"]:
                summary["timestamp_range"]["earliest"] = summary["timestamp_range"]["earliest"].isoformat()
            if summary["timestamp_range"]["latest"]:
                summary["timestamp_range"]["latest"] = summary["timestamp_range"]["latest"].isoformat()
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate metrics summary: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, validation_results: List[Dict[str, Any]], benchmarks: List[BenchmarkResult]) -> List[str]:
        """Generate performance optimization recommendations"""
        try:
            recommendations = []
            
            # Check validation failures
            for result in validation_results:
                if result.get("status") == "fail":
                    metric_name = result.get("metric_name", "unknown")
                    severity = result.get("severity", "info")
                    
                    if metric_name == "cpu_usage_percent":
                        recommendations.append("Consider optimizing CPU-intensive operations or scaling CPU resources")
                    elif metric_name == "memory_usage_percent":
                        recommendations.append("Review memory allocation patterns and consider memory optimization")
                    elif metric_name == "disk_usage_percent":
                        recommendations.append("Clean up unnecessary files and consider disk space expansion")
                    elif metric_name == "response_time_ms":
                        recommendations.append("Optimize database queries and reduce computational complexity")
            
            # Check benchmark results
            failed_benchmarks = [b for b in benchmarks if not b.success]
            if failed_benchmarks:
                recommendations.append(f"Review {len(failed_benchmarks)} failed benchmarks for performance issues")
            
            # Add general recommendations if none specific
            if not recommendations:
                recommendations.append("Performance meets all targets - maintain current configuration")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            return ["Unable to generate recommendations due to error"]
    
    def _generate_alerts(self, validation_results: List[Dict[str, Any]]) -> List[str]:
        """Generate performance alerts"""
        try:
            alerts = []
            
            for result in validation_results:
                if result.get("status") == "fail":
                    severity = result.get("severity", "info")
                    metric_name = result.get("metric_name", "unknown")
                    metric_value = result.get("metric_value", 0)
                    threshold = result.get("threshold", 0)
                    
                    if severity in ["warning", "critical"]:
                        alert_msg = f"{severity.upper()}: {metric_name} = {metric_value} exceeds threshold {threshold}"
                        alerts.append(alert_msg)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to generate alerts: {e}")
            return []
    
    def get_report(self, report_id: str) -> Optional[SystemPerformanceReport]:
        """Get a specific performance report by ID"""
        try:
            for report in self.report_history:
                if report.report_id == report_id:
                    return report
            return None
        except Exception as e:
            self.logger.error(f"Failed to get report: {e}")
            return None
    
    def get_latest_report(self) -> Optional[SystemPerformanceReport]:
        """Get the most recent performance report"""
        try:
            if self.report_history:
                return self.report_history[-1]
            return None
        except Exception as e:
            self.logger.error(f"Failed to get latest report: {e}")
            return None
    
    def get_report_history(self, limit: Optional[int] = None) -> List[SystemPerformanceReport]:
        """Get report history with optional limit"""
        try:
            if limit is None:
                return self.report_history.copy()
            else:
                return self.report_history[-limit:] if self.report_history else []
        except Exception as e:
            self.logger.error(f"Failed to get report history: {e}")
            return []
    
    def export_report(self, report_id: str, format: str = "json") -> Optional[str]:
        """Export a performance report in specified format"""
        try:
            report = self.get_report(report_id)
            if not report:
                self.logger.warning(f"Report not found: {report_id}")
                return None
            
            if format.lower() == "json":
                import json
                from dataclasses import asdict
                return json.dumps(asdict(report), indent=2, default=str)
            elif format.lower() == "text":
                return self._format_report_as_text(report)
            else:
                self.logger.warning(f"Unsupported export format: {format}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            return None
    
    def _format_report_as_text(self, report: SystemPerformanceReport) -> str:
        """Format report as human-readable text"""
        try:
            text = f"""
Performance Report: {report.report_id}
Generated: {report.timestamp}
System Health: {report.system_health}
Performance Level: {report.overall_performance_level.value}

Metrics Summary:
- Total Metrics: {report.metrics_summary.get('total_metrics', 0)}
- Metric Types: {', '.join(report.metrics_summary.get('metric_types', {}).keys())}

Validation Results:
- Total Checks: {len(report.validation_results)}
- Passed: {sum(1 for r in report.validation_results if r.get('status') == 'pass')}
- Failed: {sum(1 for r in report.validation_results if r.get('status') == 'fail')}

Benchmarks:
- Total: {len(report.benchmarks)}
- Successful: {sum(1 for b in report.benchmarks if b.success)}
- Failed: {sum(1 for b in report.benchmarks if not b.success)}

Recommendations:
{chr(10).join(f"- {rec}" for rec in report.recommendations)}

Alerts:
{chr(10).join(f"- {alert}" for alert in report.alerts) if report.alerts else "- No active alerts"}
"""
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Failed to format report as text: {e}")
            return f"Error formatting report: {str(e)}"
    
    def get_reporting_status(self) -> Dict[str, Any]:
        """Get reporting system status"""
        return {
            "reporting_active": self.reporting_active,
            "total_reports_generated": self.total_reports_generated,
            "report_history_size": len(self.report_history),
            "last_report_time": self.last_report_time.isoformat() if self.last_report_time else None,
            "max_history_size": self.report_config["max_history_size"]
        }
    
    def clear_report_history(self) -> bool:
        """Clear report history"""
        try:
            self.report_history.clear()
            self.logger.info("Report history cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear report history: {e}")
            return False
    
    def update_report_config(self, config_updates: Dict[str, Any]) -> bool:
        """Update reporting configuration"""
        try:
            for key, value in config_updates.items():
                if key in self.report_config:
                    self.report_config[key] = value
                    self.logger.info(f"Report config updated: {key} = {value}")
                else:
                    self.logger.warning(f"Unknown config key: {key}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update report config: {e}")
            return False
