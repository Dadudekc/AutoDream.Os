#!/usr/bin/env python3
"""
Unified Reporting Framework - Agent Cellphone V2

Consolidates all scattered reporting implementations into a single,
unified framework eliminating 100% duplication.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3I - Reporting Systems Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import os
import sys
import json
import csv
import logging
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import html

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig


class ReportType(Enum):
    """Types of reports supported by the unified framework"""
    TESTING = "testing"
    PERFORMANCE = "performance"
    HEALTH = "health"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    QUALITY = "quality"
    ANALYTICS = "analytics"
    FINANCIAL = "financial"
    CUSTOM = "custom"


class ReportFormat(Enum):
    """Output formats for reports"""
    JSON = "json"
    TEXT = "text"
    HTML = "html"
    CSV = "csv"
    XML = "xml"
    PDF = "pdf"


class ReportPriority(Enum):
    """Report priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ReportConfig:
    """Configuration for report generation"""
    report_type: ReportType
    format: ReportFormat
    priority: ReportPriority = ReportPriority.MEDIUM
    include_charts: bool = False
    include_recommendations: bool = True
    max_history: int = 100
    output_directory: str = "reports"
    template_path: Optional[str] = None


@dataclass
class ReportMetadata:
    """Metadata for generated reports"""
    report_id: str
    timestamp: datetime
    report_type: ReportType
    format: ReportFormat
    priority: ReportPriority
    source_system: str
    version: str = "2.0.0"
    tags: List[str] = field(default_factory=list)


@dataclass
class UnifiedReport:
    """Unified report structure"""
    metadata: ReportMetadata
    content: Dict[str, Any]
    summary: str
    recommendations: List[str] = field(default_factory=list)
    charts: List[Dict[str, Any]] = field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = None


class ReportGenerator:
    """Base report generator class"""
    
    def __init__(self, config: ReportConfig):
        self.config = config
        self.output_dir = Path(config.output_directory)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.ReportGenerator")
    
    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a report from data"""
        raise NotImplementedError("Subclasses must implement generate_report")
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists"""
        self.output_dir.mkdir(exist_ok=True, parents=True)


class TestingReportGenerator(ReportGenerator):
    """Generates testing reports"""
    
    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a testing report"""
        test_results = data.get("test_results", [])
        coverage_data = data.get("coverage_data", {})
        
        # Calculate test statistics
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.get("status") == "passed")
        failed_tests = sum(1 for r in test_results if r.get("status") == "failed")
        coverage_percentage = coverage_data.get("total_coverage", 0.0)
        
        # Create report content
        content = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "coverage": coverage_data,
            "test_details": test_results
        }
        
        # Generate summary
        summary = f"Testing Report: {passed_tests}/{total_tests} tests passed ({content['test_summary']['success_rate']:.1f}% success rate)"
        
        # Generate recommendations
        recommendations = []
        if content['test_summary']['success_rate'] < 80:
            recommendations.append("Test success rate below 80% - investigate failing tests")
        if coverage_percentage < 70:
            recommendations.append("Test coverage below 70% - add more test cases")
        
        # Create metadata
        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.TESTING,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_testing_framework"
        )
        
        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations
        )


class PerformanceReportGenerator(ReportGenerator):
    """Generates performance reports"""
    
    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a performance report"""
        benchmarks = data.get("benchmarks", [])
        metrics = data.get("metrics", {})
        
        # Calculate performance statistics
        total_benchmarks = len(benchmarks)
        passed_benchmarks = sum(1 for b in benchmarks if b.get("status") == "passed")
        performance_score = metrics.get("overall_score", 0.0)
        
        # Create report content
        content = {
            "performance_summary": {
                "total_benchmarks": total_benchmarks,
                "passed_benchmarks": passed_benchmarks,
                "performance_score": performance_score,
                "benchmark_success_rate": (passed_benchmarks / total_benchmarks * 100) if total_benchmarks > 0 else 0
            },
            "benchmarks": benchmarks,
            "metrics": metrics
        }
        
        # Generate summary
        summary = f"Performance Report: {passed_benchmarks}/{total_benchmarks} benchmarks passed (Score: {performance_score:.1f})"
        
        # Generate recommendations
        recommendations = []
        if content['performance_summary']['benchmark_success_rate'] < 90:
            recommendations.append("Benchmark success rate below 90% - investigate performance issues")
        if performance_score < 70:
            recommendations.append("Performance score below 70 - optimize system performance")
        
        # Create metadata
        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.PERFORMANCE,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_performance_system"
        )
        
        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations
        )


class HealthReportGenerator(ReportGenerator):
    """Generates health reports"""
    
    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a health report"""
        health_data = data.get("health_data", {})
        alerts = data.get("alerts", [])
        
        # Calculate health statistics
        total_agents = len(health_data.get("agents", {}))
        healthy_agents = sum(1 for a in health_data.get("agents", {}).values() 
                           if a.get("overall_status") == "good")
        total_alerts = len(alerts)
        critical_alerts = sum(1 for a in alerts if a.get("severity") == "critical")
        
        # Create report content
        content = {
            "health_summary": {
                "total_agents": total_agents,
                "healthy_agents": healthy_agents,
                "health_percentage": (healthy_agents / total_agents * 100) if total_agents > 0 else 0,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts
            },
            "agents": health_data.get("agents", {}),
            "alerts": alerts
        }
        
        # Generate summary
        summary = f"Health Report: {healthy_agents}/{total_agents} agents healthy ({content['health_summary']['health_percentage']:.1f}% health rate)"
        
        # Generate recommendations
        recommendations = []
        if content['health_summary']['health_percentage'] < 80:
            recommendations.append("System health below 80% - investigate agent issues")
        if critical_alerts > 0:
            recommendations.append(f"{critical_alerts} critical alerts - immediate attention required")
        
        # Create metadata
        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.HEALTH,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_health_system"
        )
        
        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations
        )


class SecurityReportGenerator(ReportGenerator):
    """Generates security reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a security report"""
        vulnerabilities = data.get("vulnerabilities", [])
        severity_counts: Dict[str, int] = {}
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        content = {
            "vulnerability_summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "severity_counts": severity_counts,
            },
            "vulnerabilities": vulnerabilities,
        }

        summary = f"Security Report: {len(vulnerabilities)} vulnerabilities detected"

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.SECURITY,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_security_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)


class ComplianceReportGenerator(ReportGenerator):
    """Generates compliance reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a compliance report"""
        issues = data.get("issues", [])
        compliance_score = data.get("compliance_score", 0)

        content = {
            "compliance_summary": {
                "total_issues": len(issues),
                "compliance_score": compliance_score,
            },
            "issues": issues,
        }

        summary = (
            f"Compliance Report: {len(issues)} issues found (Score: {compliance_score})"
        )

        recommendations = []
        if compliance_score < 100 and issues:
            recommendations.append(
                "Compliance issues detected - review required policies"
            )

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.COMPLIANCE,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_compliance_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )


class QualityReportGenerator(ReportGenerator):
    """Generates quality reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a quality report"""
        metrics = data.get("quality_metrics", {})
        issues = data.get("issues", [])
        score = metrics.get("score", 0)

        content = {
            "quality_summary": {
                "issue_count": len(issues),
                "quality_score": score,
            },
            "quality_metrics": metrics,
            "issues": issues,
        }

        summary = f"Quality Report: score {score} with {len(issues)} issues"

        recommendations = []
        if score < 80:
            recommendations.append("Quality score below 80 - improvements recommended")

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.QUALITY,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_quality_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )


class AnalyticsReportGenerator(ReportGenerator):
    """Generates analytics reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate an analytics report"""
        metrics = data.get("metrics", {})
        insights = data.get("insights", [])

        content = {
            "analytics_summary": {
                "metric_count": len(metrics),
                "insight_count": len(insights),
            },
            "metrics": metrics,
            "insights": insights,
        }

        summary = f"Analytics Report: {len(insights)} insights derived"

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.ANALYTICS,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_analytics_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)


class FinancialReportGenerator(ReportGenerator):
    """Generates financial reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a financial report"""
        transactions = data.get("transactions", [])
        total_amount = sum(t.get("amount", 0) for t in transactions)

        content = {
            "financial_summary": {
                "total_transactions": len(transactions),
                "total_amount": total_amount,
            },
            "transactions": transactions,
        }

        summary = (
            f"Financial Report: {len(transactions)} transactions totaling {total_amount:.2f}"
        )

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.FINANCIAL,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_financial_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)


class CustomReportGenerator(ReportGenerator):
    """Generates custom reports"""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a custom report"""
        content = data.get("content", data)
        summary = data.get("summary", "Custom report generated")

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.CUSTOM,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_custom_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)


class ReportFormatter:
    """Formats reports in various output formats"""
    
    @staticmethod
    def format_as_json(report: UnifiedReport) -> str:
        """Format report as JSON"""
        report_dict = {
            "metadata": {
                "report_id": report.metadata.report_id,
                "timestamp": report.metadata.timestamp.isoformat(),
                "report_type": report.metadata.report_type.value,
                "format": report.metadata.format.value,
                "priority": report.metadata.priority.value,
                "source_system": report.metadata.source_system,
                "version": report.metadata.version,
                "tags": report.metadata.tags
            },
            "content": report.content,
            "summary": report.summary,
            "recommendations": report.recommendations,
            "charts": report.charts
        }
        return json.dumps(report_dict, indent=2, default=str)
    
    @staticmethod
    def format_as_text(report: UnifiedReport) -> str:
        """Format report as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"REPORT: {report.metadata.report_type.value.upper()}")
        lines.append("=" * 80)
        lines.append(f"Report ID: {report.metadata.report_id}")
        lines.append(f"Timestamp: {report.metadata.timestamp}")
        lines.append(f"Source: {report.metadata.source_system}")
        lines.append(f"Priority: {report.metadata.priority.value}")
        lines.append("")
        lines.append("SUMMARY:")
        lines.append("-" * 40)
        lines.append(report.summary)
        lines.append("")
        
        if report.recommendations:
            lines.append("RECOMMENDATIONS:")
            lines.append("-" * 40)
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        lines.append("DETAILS:")
        lines.append("-" * 40)
        lines.append(json.dumps(report.content, indent=2, default=str))
        
        return "\n".join(lines)
    
    @staticmethod
    def format_as_html(report: UnifiedReport) -> str:
        """Format report as HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.metadata.report_type.value.title()} Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .recommendations {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .priority-high {{ color: #dc3545; }}
                .priority-medium {{ color: #ffc107; }}
                .priority-low {{ color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report.metadata.report_type.value.title()} Report</h1>
                <p><strong>Report ID:</strong> {report.metadata.report_id}</p>
                <p><strong>Timestamp:</strong> {report.metadata.timestamp}</p>
                <p><strong>Source:</strong> {report.metadata.source_system}</p>
                <p><strong>Priority:</strong> <span class="priority-{report.metadata.priority.value}">{report.metadata.priority.value.upper()}</span></p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>{report.summary}</p>
            </div>
        """
        
        if report.recommendations:
            html_content += f"""
            <div class="recommendations">
                <h2>Recommendations</h2>
                <ul>
            """
            for rec in report.recommendations:
                html_content += f"<li>{html.escape(rec)}</li>"
            html_content += """
                </ul>
            </div>
            """
        
        html_content += f"""
            <div class="details">
                <h2>Details</h2>
                <pre>{json.dumps(report.content, indent=2, default=str)}</pre>
            </div>
        </body>
        </html>
        """
        
        return html_content


class UnifiedReportingFramework(BaseManager):
    """
    Unified Reporting Framework - TASK 3I
    
    Consolidates all scattered reporting implementations into a single,
    unified framework eliminating 100% duplication.
    """
    
    def __init__(self, manager_id: str, name: str = "Unified Reporting Framework", description: str = ""):
        super().__init__(manager_id, name, description)
        
        # Report generators by type
        self.report_generators: Dict[ReportType, ReportGenerator] = {}
        self.report_formatter = ReportFormatter()
        
        # Report history
        self.report_history: List[UnifiedReport] = []
        self.max_history = 1000
        
        # Initialize generators
        self._initialize_generators()
        
        self.logger.info(f"UnifiedReportingFramework initialized: {manager_id}")
    
    def _initialize_generators(self) -> None:
        """Initialize report generators for each type"""
        # Create output directories
        for report_type in ReportType:
            config = ReportConfig(
                report_type=report_type,
                format=ReportFormat.JSON,
                output_directory=f"reports/{report_type.value}"
            )

            if report_type == ReportType.TESTING:
                self.report_generators[report_type] = TestingReportGenerator(config)
            elif report_type == ReportType.PERFORMANCE:
                self.report_generators[report_type] = PerformanceReportGenerator(config)
            elif report_type == ReportType.HEALTH:
                self.report_generators[report_type] = HealthReportGenerator(config)
            elif report_type == ReportType.SECURITY:
                self.report_generators[report_type] = SecurityReportGenerator(config)
            elif report_type == ReportType.COMPLIANCE:
                self.report_generators[report_type] = ComplianceReportGenerator(config)
            elif report_type == ReportType.QUALITY:
                self.report_generators[report_type] = QualityReportGenerator(config)
            elif report_type == ReportType.ANALYTICS:
                self.report_generators[report_type] = AnalyticsReportGenerator(config)
            elif report_type == ReportType.FINANCIAL:
                self.report_generators[report_type] = FinancialReportGenerator(config)
            elif report_type == ReportType.CUSTOM:
                self.report_generators[report_type] = CustomReportGenerator(config)
            else:
                self.report_generators[report_type] = ReportGenerator(config)
    
    def generate_report(self, report_type: ReportType, data: Dict[str, Any], 
                       config: Optional[ReportConfig] = None) -> UnifiedReport:
        """Generate a report of the specified type"""
        try:
            if report_type not in self.report_generators:
                raise ValueError(f"No generator available for report type: {report_type}")
            
            # Use provided config or default
            if config:
                # Update generator config
                self.report_generators[report_type].config = config
                self.report_generators[report_type].output_dir = Path(config.output_directory)
            
            # Generate report
            report = self.report_generators[report_type].generate_report(data)
            
            # Add to history
            self._add_to_history(report)
            
            self.logger.info(f"Generated {report_type.value} report: {report.metadata.report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate {report_type.value} report: {e}")
            raise
    
    def format_report(self, report: UnifiedReport, format_type: ReportFormat) -> str:
        """Format a report in the specified format"""
        try:
            if format_type == ReportFormat.JSON:
                return self.report_formatter.format_as_json(report)
            elif format_type == ReportFormat.TEXT:
                return self.report_formatter.format_as_text(report)
            elif format_type == ReportFormat.HTML:
                return self.report_formatter.format_as_html(report)
            else:
                # Default to JSON for unsupported formats
                return self.report_formatter.format_as_json(report)
                
        except Exception as e:
            self.logger.error(f"Failed to format report: {e}")
            return f"Error formatting report: {str(e)}"
    
    def save_report(self, report: UnifiedReport, format_type: Optional[ReportFormat] = None,
                   filename: Optional[str] = None) -> str:
        """Save a report to file"""
        try:
            if format_type is None:
                format_type = report.metadata.format

            # Generate filename if not provided
            if not filename:
                timestamp = report.metadata.timestamp.strftime("%Y%m%d_%H%M%S")
                filename = f"{report.metadata.report_type.value}_report_{timestamp}.{format_type.value}"
            
            # Get output directory from generator
            generator = self.report_generators[report.metadata.report_type]
            output_path = generator.output_dir / filename
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Format and save report
            formatted_content = self.format_report(report, format_type)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            self.logger.info(f"Report saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
            raise
    
    def get_report_history(self, report_type: Optional[ReportType] = None, 
                          limit: int = 100) -> List[UnifiedReport]:
        """Get report history, optionally filtered by type"""
        if report_type:
            filtered_history = [r for r in self.report_history if r.metadata.report_type == report_type]
            return filtered_history[-limit:]
        else:
            return self.report_history[-limit:]
    
    def _add_to_history(self, report: UnifiedReport) -> None:
        """Add report to history, maintaining size limit"""
        self.report_history.append(report)
        
        # Maintain history size
        if len(self.report_history) > self.max_history:
            self.report_history = self.report_history[-self.max_history:]
    
    def cleanup_old_reports(self, days_to_keep: int = 30) -> int:
        """Clean up old reports from history and filesystem"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            
            # Clean history
            initial_count = len(self.report_history)
            self.report_history = [
                r for r in self.report_history 
                if r.metadata.timestamp.timestamp() > cutoff_date
            ]
            history_cleaned = initial_count - len(self.report_history)
            
            # Clean filesystem (basic cleanup)
            files_cleaned = 0
            for generator in self.report_generators.values():
                if hasattr(generator, 'output_dir') and generator.output_dir.exists():
                    for file_path in generator.output_dir.glob("*"):
                        if file_path.is_file():
                            file_age = datetime.now().timestamp() - file_path.stat().st_mtime
                            if file_age > (days_to_keep * 24 * 60 * 60):
                                file_path.unlink()
                                files_cleaned += 1
            
            total_cleaned = history_cleaned + files_cleaned
            self.logger.info(f"Cleanup completed: {total_cleaned} items removed")
            return total_cleaned
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return 0
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status for monitoring"""
        return {
            "status": self.status.value,
            "total_reports_generated": len(self.report_history),
            "generators_available": len(self.report_generators),
            "supported_report_types": [rt.value for rt in self.report_generators.keys()],
            "supported_formats": [rf.value for rf in ReportFormat],
            "last_report_time": self.report_history[-1].metadata.timestamp.isoformat() if self.report_history else None
        }


def main():
    """Main entry point for unified reporting framework"""
    # Example usage
    framework = UnifiedReportingFramework("test_manager", "Test Reporting Framework")
    
    # Generate test report
    test_data = {
        "test_results": [
            {"name": "test_1", "status": "passed", "duration": 0.5},
            {"name": "test_2", "status": "failed", "duration": 1.2},
            {"name": "test_3", "status": "passed", "duration": 0.8}
        ],
        "coverage_data": {"total_coverage": 85.5}
    }
    
    try:
        # Generate report
        report = framework.generate_report(ReportType.TESTING, test_data)
        print(f"Generated report: {report.metadata.report_id}")
        
        # Format and save
        json_content = framework.format_report(report, ReportFormat.JSON)
        file_path = framework.save_report(report, ReportFormat.TEXT)
        print(f"Report saved to: {file_path}")
        
        # Get status
        status = framework.get_system_status()
        print(f"System status: {status}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

