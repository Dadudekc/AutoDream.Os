from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json
import logging

    from .performance_core import PerformanceMetric, MetricType
from .performance_core import (
from __future__ import annotations

#!/usr/bin/env python3
"""
Performance Reporter - Performance Reporting and Analytics

Extracted from unified_performance_system.py to achieve V2 compliance.
Contains reporting, analytics, and visualization functionality.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""



    PerformanceMetric, PerformanceResult, PerformanceLevel,
    ValidationSeverity
)


class PerformanceReporter:
    """
    Performance reporting and analytics engine.
    
    Generates comprehensive performance reports, analytics,
    and visualizations for system performance monitoring.
    """
    
    def __init__(self):
        """Initialize the performance reporter."""
        self.logger = logging.getLogger(__name__)
        
        # Reporting components
        self.report_templates: Dict[str, Dict[str, Any]] = {}
        self.report_history: List[Dict[str, Any]] = []
        
        # Analytics
        self.performance_trends: Dict[str, List[float]] = {}
        self.benchmark_history: List[PerformanceResult] = []
        
        # Output configuration
        self.output_formats = ["json", "text", "html"]
        self.default_output_format = "json"
        
        self.logger.info("Performance Reporter initialized")
    
    def generate_performance_report(
        self,
        metrics: List[PerformanceMetric],
        validation_results: List[Dict[str, Any]],
        benchmark_results: Optional[List[PerformanceResult]] = None,
        report_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Generate a performance report."""
        try:
            self.logger.info(f"Generating {report_type} performance report...")
            
            # Generate report based on type
            if report_type == "comprehensive":
                report = self._generate_comprehensive_report(metrics, validation_results, benchmark_results)
            elif report_type == "summary":
                report = self._generate_summary_report(metrics, validation_results)
            elif report_type == "alerts":
                report = self._generate_alerts_report(validation_results)
            else:
                report = self._generate_custom_report(metrics, validation_results, report_type)
            
            # Add metadata
            report["metadata"] = {
                "report_id": self._generate_report_id(),
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "metrics_count": len(metrics),
                "validation_count": len(validation_results)
            }
            
            # Store report
            self.report_history.append(report)
            
            self.logger.info(f"Performance report generated: {report['metadata']['report_id']}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return {
                "error": str(e),
                "metadata": {
                    "report_id": "error",
                    "generated_at": datetime.now().isoformat(),
                    "report_type": report_type
                }
            }
    
    def _generate_comprehensive_report(
        self,
        metrics: List[PerformanceMetric],
        validation_results: List[Dict[str, Any]],
        benchmark_results: Optional[List[PerformanceResult]]
    ) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        report = {
            "summary": self._generate_summary_section(metrics, validation_results),
            "metrics": self._generate_metrics_section(metrics),
            "validation": self._generate_validation_section(validation_results),
            "trends": self._generate_trends_section(metrics),
            "recommendations": self._generate_recommendations_section(validation_results)
        }
        
        if benchmark_results:
            report["benchmarks"] = self._generate_benchmarks_section(benchmark_results)
        
        return report
    
    def _generate_summary_section(
        self,
        metrics: List[PerformanceMetric],
        validation_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summary section of the report."""
        # Calculate overall performance score
        if metrics:
            avg_values = {}
            for metric in metrics:
                if metric.name not in avg_values:
                    avg_values[metric.name] = []
                avg_values[metric.name].append(metric.value)
            
            # Calculate averages
            for metric_name, values in avg_values.items():
                if values:
                    avg_values[metric_name] = sum(values) / len(values)
        else:
            avg_values = {}
        
        # Calculate validation summary
        total_validations = len(validation_results)
        pass_count = len([r for r in validation_results if r.get("overall_status") == "pass"])
        warn_count = len([r for r in validation_results if r.get("overall_status") == "warn"])
        fail_count = len([r for r in validation_results if r.get("overall_status") == "fail"])
        
        pass_rate = (pass_count / total_validations * 100) if total_validations > 0 else 0
        
        # Determine overall performance level
        if pass_rate >= 95:
            overall_level = PerformanceLevel.EXCELLENT
        elif pass_rate >= 85:
            overall_level = PerformanceLevel.GOOD
        elif pass_rate >= 70:
            overall_level = PerformanceLevel.STANDARD
        elif pass_rate >= 50:
            overall_level = PerformanceLevel.BASIC
        else:
            overall_level = PerformanceLevel.NOT_READY
        
        return {
            "overall_performance_level": overall_level.value,
            "overall_score": pass_rate,
            "total_metrics": len(metrics),
            "total_validations": total_validations,
            "validation_summary": {
                "pass": pass_count,
                "warn": warn_count,
                "fail": fail_count,
                "pass_rate": pass_rate
            },
            "key_metrics_averages": avg_values
        }
    
    def _generate_metrics_section(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Generate metrics section of the report."""
        if not metrics:
            return {"message": "No metrics available"}
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in metrics:
            metric_type = metric.metric_type.value
            if metric_type not in metrics_by_type:
                metrics_by_type[metric_type] = []
            metrics_by_type[metric_type].append({
                "name": metric.name,
                "value": metric.value,
                "unit": metric.unit,
                "timestamp": metric.timestamp.isoformat(),
                "labels": metric.labels,
                "description": metric.description
            })
        
        return {
            "total_metrics": len(metrics),
            "metrics_by_type": metrics_by_type,
            "recent_metrics": sorted(
                [m for m in metrics],
                key=lambda x: x.timestamp,
                reverse=True
            )[:10]  # Last 10 metrics
        }
    
    def _generate_validation_section(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate validation section of the report."""
        if not validation_results:
            return {"message": "No validation results available"}
        
        # Group by status
        by_status = {}
        for result in validation_results:
            status = result.get("overall_status", "unknown")
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(result)
        
        # Group by severity
        by_severity = {}
        for result in validation_results:
            for validation in result.get("validations", []):
                severity = validation.get("severity", ValidationSeverity.INFO).value
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(validation)
        
        return {
            "total_validations": len(validation_results),
            "by_status": by_status,
            "by_severity": by_severity,
            "recent_validations": validation_results[-10:]  # Last 10 validations
        }
    
    def _generate_trends_section(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Generate trends section of the report."""
        if not metrics:
            return {"message": "No metrics available for trend analysis"}
        
        return {
            "trends_available": 0,
            "trend_analysis": {}
        }
    
    def _generate_recommendations_section(self, validation_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        # Analyze validation results for recommendations
        for result in validation_results:
            if result.get("overall_status") == "fail":
                recommendations.append({
                    "type": "critical",
                    "metric": result.get("metric_name"),
                    "message": f"Critical validation failure detected for {result.get('metric_name')}",
                    "action": "Immediate investigation required"
                })
            elif result.get("overall_status") == "warn":
                recommendations.append({
                    "type": "warning",
                    "metric": result.get("metric_name"),
                    "message": f"Warning validation detected for {result.get('metric_name')}",
                    "action": "Monitor closely and consider optimization"
                })
        
        # Add general recommendations based on patterns
        if len([r for r in validation_results if r.get("overall_status") == "fail"]) > 0:
            recommendations.append({
                "type": "general",
                "message": "Multiple critical failures detected",
                "action": "System-wide performance review recommended"
            })
        
        return recommendations
    
    def _generate_benchmarks_section(self, benchmark_results: List[PerformanceResult]) -> Dict[str, Any]:
        """Generate benchmarks section of the report."""
        if not benchmark_results:
            return {"message": "No benchmark results available"}
        
        return {
            "total_benchmarks": len(benchmark_results),
            "by_benchmark": {},
            "recent_benchmarks": []
        }
    
    def _generate_report_id(self) -> str:
        """Generate a unique report ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"perf_report_{timestamp}"
    
    def export_report(self, report: Dict[str, Any], format: str = "json", filepath: Optional[str] = None) -> str:
        """Export a report to the specified format."""
        try:
            if format == "json":
                content = json.dumps(report, indent=2, default=str)
                extension = "json"
            elif format == "text":
                content = self._format_report_as_text(report)
                extension = "txt"
            elif format == "html":
                content = self._format_report_as_html(report)
                extension = "html"
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Determine filepath
            if not filepath:
                report_id = report.get("metadata", {}).get("report_id", "report")
                filepath = f"performance_report_{report_id}.{extension}"
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Report exported to: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            raise
    
    def _format_report_as_text(self, report: Dict[str, Any]) -> str:
        """Format report as plain text."""
        lines = []
        lines.append("=" * 80)
        lines.append("PERFORMANCE REPORT")
        lines.append("=" * 80)
        
        # Summary
        summary = report.get("summary", {})
        lines.append(f"\nOverall Performance Level: {summary.get('overall_performance_level', 'Unknown')}")
        lines.append(f"Overall Score: {summary.get('overall_score', 0):.1f}%")
        lines.append(f"Total Metrics: {summary.get('total_metrics', 0)}")
        lines.append(f"Total Validations: {summary.get('total_validations', 0)}")
        
        # Validation summary
        val_summary = summary.get("validation_summary", {})
        lines.append(f"\nValidation Summary:")
        lines.append(f"  Pass: {val_summary.get('pass', 0)}")
        lines.append(f"  Warn: {val_summary.get('warn', 0)}")
        lines.append(f"  Fail: {val_summary.get('fail', 0)}")
        lines.append(f"  Pass Rate: {val_summary.get('pass_rate', 0):.1f}%")
        
        # Recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            lines.append(f"\nRecommendations:")
            for rec in recommendations:
                lines.append(f"  [{rec.get('type', 'info').upper()}] {rec.get('message', '')}")
                lines.append(f"    Action: {rec.get('action', '')}")
        
        return "\n".join(lines)
    
    def _format_report_as_html(self, report: Dict[str, Any]) -> str:
        """Format report as HTML."""
        return f"<html><body><h1>Performance Report</h1><p>Generated: {report.get('metadata', {}).get('generated_at', 'Unknown')}</p></body></html>"
    
    def get_report_history(self) -> List[Dict[str, Any]]:
        """Get report generation history."""
        return self.report_history.copy()
    
    def clear_report_history(self):
        """Clear report history."""
        self.report_history.clear()
        self.logger.info("Report history cleared")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test performance reporter
    reporter = PerformanceReporter()
    
    # Create sample metrics
    sample_metrics = [
        PerformanceMetric(
            name="cpu_usage",
            value=75.5,
            unit="percent",
            metric_type=MetricType.GAUGE,
            timestamp=datetime.now(),
            labels={"system": "main"},
            description="CPU usage percentage"
        )
    ]
    
    # Create sample validation results
    sample_validations = [
        {
            "metric_name": "cpu_usage",
            "overall_status": "warn",
            "validations": [
                {
                    "severity": ValidationSeverity.WARNING,
                    "message": "CPU usage is high"
                }
            ]
        }
    ]
    
    # Generate report
    report = reporter.generate_performance_report(
        sample_metrics,
        sample_validations,
        report_type="summary"
    )
    
    print("✅ Performance reporter initialized successfully")
    print(f"📊 Report generated: {report['metadata']['report_id']}")
    print(f"📈 Overall score: {report['summary']['overall_score']:.1f}%")
