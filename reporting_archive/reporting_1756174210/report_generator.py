#!/usr/bin/env python3
"""
Performance Report Generator - V2 Modular Architecture
=====================================================

Handles all performance report generation operations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from .report_types import PerformanceReport, ReportSection, ReportMetric, ReportFormat, ReportStatus


logger = logging.getLogger(__name__)


class PerformanceReportGenerator:
    """
    Performance Report Generator - Single responsibility: Generate performance reports
    
    Handles all report generation operations including:
    - Report creation and formatting
    - Data aggregation and analysis
    - Multiple output formats
    - Report customization
    """

    def __init__(self):
        """Initialize report generator"""
        self.logger = logging.getLogger(f"{__name__}.PerformanceReportGenerator")
        
        # Report templates
        self.report_templates: Dict[str, Dict[str, Any]] = {}
        
        # Default template
        self._setup_default_template()
        
        self.logger.info("✅ Performance Report Generator initialized successfully")

    def _setup_default_template(self) -> None:
        """Setup default report template"""
        self.report_templates["default"] = {
            "title": "Performance Report",
            "sections": [
                "executive_summary",
                "system_overview",
                "performance_metrics",
                "benchmark_results",
                "alerts_and_issues",
                "recommendations",
                "appendix"
            ],
            "include_charts": True,
            "include_metrics": True,
            "include_benchmarks": True,
            "include_alerts": True
        }

    def generate_report(self, data: Dict[str, Any], template: str = "default") -> PerformanceReport:
        """Generate a comprehensive performance report"""
        try:
            self.logger.info("📊 Generating performance report...")
            
            # Get template
            template_config = self.report_templates.get(template, self.report_templates["default"])
            
            # Create report sections
            sections = []
            
            # Executive Summary
            if "executive_summary" in template_config["sections"]:
                sections.append(self._create_executive_summary(data))
            
            # System Overview
            if "system_overview" in template_config["sections"]:
                sections.append(self._create_system_overview(data))
            
            # Performance Metrics
            if "performance_metrics" in template_config["sections"]:
                sections.append(self._create_performance_metrics(data))
            
            # Benchmark Results
            if "benchmark_results" in template_config["sections"]:
                sections.append(self._create_benchmark_results(data))
            
            # Alerts and Issues
            if "include_alerts" in template_config and "alerts_and_issues" in template_config["sections"]:
                sections.append(self._create_alerts_section(data))
            
            # Recommendations
            if "recommendations" in template_config["sections"]:
                sections.append(self._create_recommendations_section(data))
            
            # Appendix
            if "appendix" in template_config["sections"]:
                sections.append(self._create_appendix_section(data))
            
            # Create report
            report = PerformanceReport(
                id=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title=template_config["title"],
                generated_at=datetime.now().isoformat(),
                sections=sections,
                status=ReportStatus.COMPLETED,
                format=ReportFormat.STRUCTURED
            )
            
            self.logger.info("✅ Performance report generated successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return self._create_error_report(str(e))

    def _create_executive_summary(self, data: Dict[str, Any]) -> ReportSection:
        """Create executive summary section"""
        try:
            # Extract key information
            system_health = data.get("system_health", "unknown")
            overall_performance = data.get("overall_performance_level", "unknown")
            total_alerts = len(data.get("alerts", []))
            recommendations = data.get("recommendations", [])
            
            # Create summary metrics
            summary_metrics = [
                ReportMetric(
                    name="System Health",
                    value=system_health,
                    unit="status",
                    category="overview"
                ),
                ReportMetric(
                    name="Performance Level",
                    value=overall_performance,
                    unit="level",
                    category="overview"
                ),
                ReportMetric(
                    name="Active Alerts",
                    value=total_alerts,
                    unit="count",
                    category="overview"
                ),
                ReportMetric(
                    name="Recommendations",
                    value=len(recommendations),
                    unit="count",
                    category="overview"
                )
            ]
            
            return ReportSection(
                title="Executive Summary",
                content=f"System performance report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. "
                        f"Current system health: {system_health}. Overall performance level: {overall_performance}. "
                        f"Active alerts: {total_alerts}. Recommendations: {len(recommendations)}.",
                metrics=summary_metrics,
                subsections=[],
                order=1
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create executive summary: {e}")
            return ReportSection(
                title="Executive Summary",
                content="Failed to generate executive summary",
                metrics=[],
                subsections=[],
                order=1
            )

    def _create_system_overview(self, data: Dict[str, Any]) -> ReportSection:
        """Create system overview section"""
        try:
            # Extract system information
            metrics_summary = data.get("metrics_summary", {})
            system_health = data.get("system_health", "unknown")
            
            # Create system metrics
            system_metrics = []
            for metric_name, metric_data in metrics_summary.items():
                if isinstance(metric_data, dict) and "latest" in metric_data:
                    system_metrics.append(ReportMetric(
                        name=metric_name.replace("_", " ").title(),
                        value=metric_data["latest"],
                        unit="value",
                        category="system"
                    ))
            
            # Add system health metric
            system_metrics.append(ReportMetric(
                name="System Health Status",
                value=system_health,
                unit="status",
                category="system"
            ))
            
            return ReportSection(
                title="System Overview",
                content=f"System overview showing current performance metrics and health status. "
                        f"Total metrics tracked: {len(metrics_summary)}. "
                        f"Current system health: {system_health}.",
                metrics=system_metrics,
                subsections=[],
                order=2
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create system overview: {e}")
            return ReportSection(
                title="System Overview",
                content="Failed to generate system overview",
                metrics=[],
                subsections=[],
                order=2
            )

    def _create_performance_metrics(self, data: Dict[str, Any]) -> ReportSection:
        """Create performance metrics section"""
        try:
            # Extract metrics data
            metrics_summary = data.get("metrics_summary", {})
            
            # Create performance metrics
            performance_metrics = []
            for metric_name, metric_data in metrics_summary.items():
                if isinstance(metric_data, dict):
                    # Add latest value
                    if "latest" in metric_data:
                        performance_metrics.append(ReportMetric(
                            name=f"{metric_name.replace('_', ' ').title()} (Latest)",
                            value=metric_data["latest"],
                            unit="value",
                            category="performance"
                        ))
                    
                    # Add average value
                    if "avg" in metric_data:
                        performance_metrics.append(ReportMetric(
                            name=f"{metric_name.replace('_', ' ').title()} (Average)",
                            value=round(metric_data["avg"], 2),
                            unit="value",
                            category="performance"
                        ))
                    
                    # Add min/max values
                    if "min" in metric_data and "max" in metric_data:
                        performance_metrics.append(ReportMetric(
                            name=f"{metric_name.replace('_', ' ').title()} (Range)",
                            value=f"{metric_data['min']} - {metric_data['max']}",
                            unit="range",
                            category="performance"
                        ))
            
            return ReportSection(
                title="Performance Metrics",
                content=f"Detailed performance metrics analysis. "
                        f"Total metrics analyzed: {len(metrics_summary)}. "
                        f"Metrics include current values, averages, and ranges.",
                metrics=performance_metrics,
                subsections=[],
                order=3
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create performance metrics: {e}")
            return ReportSection(
                title="Performance Metrics",
                content="Failed to generate performance metrics",
                metrics=[],
                subsections=[],
                order=3
            )

    def _create_benchmark_results(self, data: Dict[str, Any]) -> ReportSection:
        """Create benchmark results section"""
        try:
            # Extract benchmark data
            benchmarks = data.get("benchmarks", [])
            
            # Create benchmark metrics
            benchmark_metrics = []
            if benchmarks:
                # Overall benchmark statistics
                total_benchmarks = len(benchmarks)
                successful_benchmarks = len([b for b in benchmarks if getattr(b, 'success', False)])
                success_rate = (successful_benchmarks / total_benchmarks) * 100 if total_benchmarks > 0 else 0
                
                benchmark_metrics.extend([
                    ReportMetric(
                        name="Total Benchmarks",
                        value=total_benchmarks,
                        unit="count",
                        category="benchmark"
                    ),
                    ReportMetric(
                        name="Successful Benchmarks",
                        value=successful_benchmarks,
                        unit="count",
                        category="benchmark"
                    ),
                    ReportMetric(
                        name="Success Rate",
                        value=round(success_rate, 1),
                        unit="percent",
                        category="benchmark"
                    )
                ])
                
                # Recent benchmark results
                recent_benchmarks = benchmarks[-5:] if len(benchmarks) > 5 else benchmarks
                for benchmark in recent_benchmarks:
                    if hasattr(benchmark, 'name') and hasattr(benchmark, 'success'):
                        benchmark_metrics.append(ReportMetric(
                            name=f"Recent: {benchmark.name}",
                            value="✅ Passed" if benchmark.success else "❌ Failed",
                            unit="status",
                            category="benchmark"
                        ))
            
            return ReportSection(
                title="Benchmark Results",
                content=f"Performance benchmark execution results. "
                        f"Total benchmarks: {len(benchmarks)}. "
                        f"Success rate: {round(success_rate, 1)}% if benchmarks exist.",
                metrics=benchmark_metrics,
                subsections=[],
                order=4
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create benchmark results: {e}")
            return ReportSection(
                title="Benchmark Results",
                content="Failed to generate benchmark results",
                metrics=[],
                subsections=[],
                order=4
            )

    def _create_alerts_section(self, data: Dict[str, Any]) -> ReportSection:
        """Create alerts and issues section"""
        try:
            # Extract alerts data
            alerts = data.get("alerts", [])
            
            # Create alert metrics
            alert_metrics = [
                ReportMetric(
                    name="Total Alerts",
                    value=len(alerts),
                    unit="count",
                    category="alert"
                )
            ]
            
            # Categorize alerts by severity
            critical_alerts = [a for a in alerts if "CRITICAL:" in a]
            warning_alerts = [a for a in alerts if "WARNING:" in a]
            
            alert_metrics.extend([
                ReportMetric(
                    name="Critical Alerts",
                    value=len(critical_alerts),
                    unit="count",
                    category="alert"
                ),
                ReportMetric(
                    name="Warning Alerts",
                    value=len(warning_alerts),
                    unit="count",
                    category="alert"
                )
            ])
            
            return ReportSection(
                title="Alerts and Issues",
                content=f"System alerts and performance issues. "
                        f"Total alerts: {len(alerts)}. "
                        f"Critical: {len(critical_alerts)}, Warnings: {len(warning_alerts)}.",
                metrics=alert_metrics,
                subsections=[],
                order=5
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create alerts section: {e}")
            return ReportSection(
                title="Alerts and Issues",
                content="Failed to generate alerts section",
                metrics=[],
                subsections=[],
                order=5
            )

    def _create_recommendations_section(self, data: Dict[str, Any]) -> ReportSection:
        """Create recommendations section"""
        try:
            # Extract recommendations data
            recommendations = data.get("recommendations", [])
            
            # Create recommendation metrics
            recommendation_metrics = [
                ReportMetric(
                    name="Total Recommendations",
                    value=len(recommendations),
                    unit="count",
                    category="recommendation"
                )
            ]
            
            # Add specific recommendations as metrics
            for i, recommendation in enumerate(recommendations[:5]):  # Limit to 5
                recommendation_metrics.append(ReportMetric(
                    name=f"Recommendation {i+1}",
                    value=recommendation[:50] + "..." if len(recommendation) > 50 else recommendation,
                    unit="text",
                    category="recommendation"
                ))
            
            return ReportSection(
                title="Recommendations",
                content=f"Performance optimization recommendations. "
                        f"Total recommendations: {len(recommendations)}. "
                        f"Focus on high-impact optimizations first.",
                metrics=recommendation_metrics,
                subsections=[],
                order=6
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create recommendations section: {e}")
            return ReportSection(
                title="Recommendations",
                content="Failed to generate recommendations section",
                metrics=[],
                subsections=[],
                order=6
            )

    def _create_appendix_section(self, data: Dict[str, Any]) -> ReportSection:
        """Create appendix section"""
        try:
            # Create appendix metrics
            appendix_metrics = [
                ReportMetric(
                    name="Report Generated",
                    value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    unit="timestamp",
                    category="metadata"
                ),
                ReportMetric(
                    name="Data Source",
                    value="Performance Monitoring System",
                    unit="text",
                    category="metadata"
                ),
                ReportMetric(
                    name="Report Version",
                    value="2.0",
                    unit="version",
                    category="metadata"
                )
            ]
            
            return ReportSection(
                title="Appendix",
                content="Report metadata and additional information. "
                        f"Generated by V2 Performance System. "
                        f"Report ID: {data.get('id', 'unknown')}.",
                metrics=appendix_metrics,
                subsections=[],
                order=7
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create appendix section: {e}")
            return ReportSection(
                title="Appendix",
                content="Failed to generate appendix section",
                metrics=[],
                subsections=[],
                order=7
            )

    def _create_error_report(self, error_message: str) -> PerformanceReport:
        """Create error report when generation fails"""
        error_section = ReportSection(
            title="Error",
            content=f"Failed to generate performance report: {error_message}",
            metrics=[],
            subsections=[],
            order=1
        )
        
        return PerformanceReport(
            id=f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title="Performance Report - Error",
            generated_at=datetime.now().isoformat(),
            sections=[error_section],
            status=ReportStatus.FAILED,
            format=ReportFormat.STRUCTURED
        )

    def export_report(self, report: PerformanceReport, format: str = "json") -> str:
        """Export report in specified format"""
        try:
            if format.lower() == "json":
                return json.dumps(report.__dict__, indent=2, default=str)
            elif format.lower() == "text":
                return self._export_as_text(report)
            elif format.lower() == "html":
                return self._export_as_html(report)
            else:
                return f"Export format {format} not supported"
                
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            return f"Export failed: {e}"

    def _export_as_text(self, report: PerformanceReport) -> str:
        """Export report as plain text"""
        try:
            text_lines = []
            text_lines.append(f"Performance Report: {report.title}")
            text_lines.append(f"Generated: {report.generated_at}")
            text_lines.append(f"Status: {report.status.value}")
            text_lines.append("=" * 50)
            
            for section in report.sections:
                text_lines.append(f"\n{section.title}")
                text_lines.append("-" * 30)
                text_lines.append(section.content)
                
                if section.metrics:
                    text_lines.append("\nMetrics:")
                    for metric in section.metrics:
                        text_lines.append(f"  {metric.name}: {metric.value} {metric.unit}")
            
            return "\n".join(text_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to export as text: {e}")
            return f"Text export failed: {e}"

    def _export_as_html(self, report: PerformanceReport) -> str:
        """Export report as HTML"""
        try:
            html_lines = []
            html_lines.append("<!DOCTYPE html>")
            html_lines.append("<html>")
            html_lines.append("<head>")
            html_lines.append(f"<title>{report.title}</title>")
            html_lines.append("<style>")
            html_lines.append("body { font-family: Arial, sans-serif; margin: 20px; }")
            html_lines.append("h1 { color: #333; }")
            html_lines.append("h2 { color: #666; border-bottom: 1px solid #ccc; }")
            html_lines.append("table { border-collapse: collapse; width: 100%; }")
            html_lines.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
            html_lines.append("th { background-color: #f2f2f2; }")
            html_lines.append("</style>")
            html_lines.append("</head>")
            html_lines.append("<body>")
            
            html_lines.append(f"<h1>{report.title}</h1>")
            html_lines.append(f"<p><strong>Generated:</strong> {report.generated_at}</p>")
            html_lines.append(f"<p><strong>Status:</strong> {report.status.value}</p>")
            
            for section in report.sections:
                html_lines.append(f"<h2>{section.title}</h2>")
                html_lines.append(f"<p>{section.content}</p>")
                
                if section.metrics:
                    html_lines.append("<table>")
                    html_lines.append("<tr><th>Metric</th><th>Value</th><th>Unit</th><th>Category</th></tr>")
                    for metric in section.metrics:
                        html_lines.append(f"<tr><td>{metric.name}</td><td>{metric.value}</td><td>{metric.unit}</td><td>{metric.category}</td></tr>")
                    html_lines.append("</table>")
            
            html_lines.append("</body>")
            html_lines.append("</html>")
            
            return "\n".join(html_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to export as HTML: {e}")
            return f"HTML export failed: {e}"

    def add_template(self, name: str, template: Dict[str, Any]) -> None:
        """Add a new report template"""
        try:
            self.report_templates[name] = template
            self.logger.info(f"✅ Added report template: {name}")
            
        except Exception as e:
            self.logger.error(f"Failed to add template {name}: {e}")

    def get_templates(self) -> List[str]:
        """Get available template names"""
        return list(self.report_templates.keys())

    def remove_template(self, name: str) -> bool:
        """Remove a report template"""
        try:
            if name in self.report_templates and name != "default":
                del self.report_templates[name]
                self.logger.info(f"✅ Removed template: {name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove template {name}: {e}")
            return False
