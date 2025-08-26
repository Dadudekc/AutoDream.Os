#!/usr/bin/env python3
"""
Performance Report Generator - V2 Core Performance System
=========================================================

Handles performance report generation and formatting.
Follows Single Responsibility Principle - report generation only.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from src.utils.stability_improvements import stability_manager, safe_import
from ..metrics.collector import PerformanceBenchmark, PerformanceLevel, BenchmarkType


@dataclass
class SystemPerformanceReport:
    """System performance report"""
    report_id: str
    timestamp: str
    overall_performance_level: PerformanceLevel
    benchmark_results: List[PerformanceBenchmark]
    enterprise_readiness_score: float
    recommendations: List[str]


class ReportGenerator:
    """
    Performance report generation and formatting system
    
    Responsibilities:
    - Generate comprehensive performance reports
    - Format reports in various formats (JSON, text, HTML)
    - Calculate enterprise readiness scores
    - Aggregate benchmark data for reporting
    """
    
    def __init__(self):
        self.reports: List[SystemPerformanceReport] = []
        self.logger = logging.getLogger(f"{__name__}.ReportGenerator")
    
    def generate_performance_report(self, benchmarks: List[PerformanceBenchmark], 
                                  overall_level: PerformanceLevel,
                                  recommendations: List[str]) -> SystemPerformanceReport:
        """Generate a comprehensive performance report"""
        try:
            report_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Calculate enterprise readiness score
            enterprise_score = self._calculate_enterprise_readiness_score(benchmarks)
            
            report = SystemPerformanceReport(
                report_id=report_id,
                timestamp=timestamp,
                overall_performance_level=overall_level,
                benchmark_results=benchmarks,
                enterprise_readiness_score=enterprise_score,
                recommendations=recommendations
            )
            
            self.reports.append(report)
            self.logger.info(f"Generated performance report: {report_id}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            # Return a minimal error report
            return SystemPerformanceReport(
                report_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                overall_performance_level=PerformanceLevel.NOT_READY,
                benchmark_results=[],
                enterprise_readiness_score=0.0,
                recommendations=[f"Report generation failed: {str(e)}"]
            )
    
    def format_report_as_json(self, report: SystemPerformanceReport) -> str:
        """Format report as JSON string"""
        try:
            # Convert dataclass to dict with enum handling
            report_dict = self._report_to_dict(report)
            return json.dumps(report_dict, indent=2, default=str)
            
        except Exception as e:
            self.logger.error(f"Failed to format report as JSON: {e}")
            return json.dumps({"error": f"Failed to format report: {str(e)}"})
    
    def format_report_as_text(self, report: SystemPerformanceReport) -> str:
        """Format report as human-readable text"""
        try:
            lines = []
            lines.append("=" * 60)
            lines.append("PERFORMANCE VALIDATION REPORT")
            lines.append("=" * 60)
            lines.append(f"Report ID: {report.report_id}")
            lines.append(f"Generated: {report.timestamp}")
            lines.append(f"Overall Performance Level: {report.overall_performance_level.value.upper()}")
            lines.append(f"Enterprise Readiness Score: {report.enterprise_readiness_score:.1f}%")
            lines.append("")
            
            # Benchmark Results Section
            lines.append("BENCHMARK RESULTS")
            lines.append("-" * 30)
            
            if not report.benchmark_results:
                lines.append("No benchmark results available")
            else:
                for benchmark in report.benchmark_results:
                    lines.append(f"\n{benchmark.test_name}")
                    lines.append(f"  Type: {benchmark.benchmark_type.value}")
                    lines.append(f"  Performance Level: {benchmark.performance_level.value}")
                    lines.append(f"  Duration: {benchmark.duration:.2f}s")
                    
                    # Key metrics
                    lines.append("  Key Metrics:")
                    for metric, value in benchmark.metrics.items():
                        if isinstance(value, float):
                            lines.append(f"    {metric}: {value:.2f}")
                        else:
                            lines.append(f"    {metric}: {value}")
            
            # Recommendations Section
            lines.append("\n\nRECOMMENDATIONS")
            lines.append("-" * 30)
            
            if not report.recommendations:
                lines.append("No recommendations available")
            else:
                for i, recommendation in enumerate(report.recommendations, 1):
                    lines.append(f"{i}. {recommendation}")
            
            lines.append("\n" + "=" * 60)
            
            return "\n".join(lines)
            
        except Exception as e:
            self.logger.error(f"Failed to format report as text: {e}")
            return f"Error formatting report: {str(e)}"
    
    def format_report_as_html(self, report: SystemPerformanceReport) -> str:
        """Format report as HTML"""
        try:
            html_parts = []
            
            # HTML header
            html_parts.append("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Performance Validation Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .header { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
                    .section { margin: 20px 0; }
                    .benchmark { border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 3px; }
                    .metric { margin: 5px 0; }
                    .recommendations { background-color: #fff3cd; padding: 15px; border-radius: 5px; }
                    .enterprise-ready { color: #28a745; }
                    .production-ready { color: #ffc107; }
                    .development-ready { color: #fd7e14; }
                    .not-ready { color: #dc3545; }
                </style>
            </head>
            <body>
            """)
            
            # Report header
            performance_class = report.overall_performance_level.value.replace('_', '-')
            html_parts.append(f"""
            <div class="header">
                <h1>Performance Validation Report</h1>
                <p><strong>Report ID:</strong> {report.report_id}</p>
                <p><strong>Generated:</strong> {report.timestamp}</p>
                <p><strong>Overall Performance Level:</strong> 
                   <span class="{performance_class}">{report.overall_performance_level.value.upper()}</span></p>
                <p><strong>Enterprise Readiness Score:</strong> {report.enterprise_readiness_score:.1f}%</p>
            </div>
            """)
            
            # Benchmarks section
            html_parts.append('<div class="section"><h2>Benchmark Results</h2>')
            
            if not report.benchmark_results:
                html_parts.append('<p>No benchmark results available</p>')
            else:
                for benchmark in report.benchmark_results:
                    benchmark_class = benchmark.performance_level.value.replace('_', '-')
                    html_parts.append(f"""
                    <div class="benchmark">
                        <h3>{benchmark.test_name}</h3>
                        <p><strong>Type:</strong> {benchmark.benchmark_type.value}</p>
                        <p><strong>Performance Level:</strong> 
                           <span class="{benchmark_class}">{benchmark.performance_level.value}</span></p>
                        <p><strong>Duration:</strong> {benchmark.duration:.2f}s</p>
                        <h4>Metrics:</h4>
                    """)
                    
                    for metric, value in benchmark.metrics.items():
                        if isinstance(value, float):
                            html_parts.append(f'<div class="metric">{metric}: {value:.2f}</div>')
                        else:
                            html_parts.append(f'<div class="metric">{metric}: {value}</div>')
                    
                    html_parts.append('</div>')
            
            html_parts.append('</div>')
            
            # Recommendations section
            html_parts.append('<div class="section recommendations"><h2>Recommendations</h2>')
            
            if not report.recommendations:
                html_parts.append('<p>No recommendations available</p>')
            else:
                html_parts.append('<ol>')
                for recommendation in report.recommendations:
                    html_parts.append(f'<li>{recommendation}</li>')
                html_parts.append('</ol>')
            
            html_parts.append('</div>')
            
            # HTML footer
            html_parts.append('</body></html>')
            
            return ''.join(html_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to format report as HTML: {e}")
            return f"<html><body><h1>Error</h1><p>Failed to format report: {str(e)}</p></body></html>"
    
    def get_latest_report(self) -> Optional[SystemPerformanceReport]:
        """Get the most recent performance report"""
        if not self.reports:
            return None
        
        return max(self.reports, key=lambda r: r.timestamp)
    
    def get_report_by_id(self, report_id: str) -> Optional[SystemPerformanceReport]:
        """Get a specific report by ID"""
        for report in self.reports:
            if report.report_id == report_id:
                return report
        return None
    
    def get_all_reports(self) -> List[SystemPerformanceReport]:
        """Get all stored reports"""
        return self.reports.copy()
    
    def generate_summary_report(self, reports: List[SystemPerformanceReport]) -> Dict[str, Any]:
        """Generate a summary across multiple reports"""
        try:
            if not reports:
                return {"error": "No reports provided"}
            
            # Calculate trends
            enterprise_scores = [r.enterprise_readiness_score for r in reports]
            performance_levels = [r.overall_performance_level for r in reports]
            
            # Count performance levels
            level_counts = {}
            for level in performance_levels:
                level_counts[level.value] = level_counts.get(level.value, 0) + 1
            
            # Calculate average enterprise score
            avg_enterprise_score = sum(enterprise_scores) / len(enterprise_scores)
            
            # Get most common recommendations
            all_recommendations = []
            for report in reports:
                all_recommendations.extend(report.recommendations)
            
            recommendation_counts = {}
            for rec in all_recommendations:
                recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
            
            top_recommendations = sorted(
                recommendation_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            
            summary = {
                "total_reports": len(reports),
                "date_range": {
                    "earliest": min(r.timestamp for r in reports),
                    "latest": max(r.timestamp for r in reports),
                },
                "performance_level_distribution": level_counts,
                "average_enterprise_readiness_score": avg_enterprise_score,
                "enterprise_score_trend": {
                    "min": min(enterprise_scores),
                    "max": max(enterprise_scores),
                    "latest": enterprise_scores[-1] if enterprise_scores else 0,
                },
                "top_recommendations": [rec for rec, count in top_recommendations],
                "total_benchmarks": sum(len(r.benchmark_results) for r in reports),
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate summary report: {e}")
            return {"error": f"Failed to generate summary: {str(e)}"}
    
    def _calculate_enterprise_readiness_score(self, benchmarks: List[PerformanceBenchmark]) -> float:
        """Calculate enterprise readiness score based on benchmarks"""
        try:
            if not benchmarks:
                return 0.0
            
            # Weight different performance levels
            level_scores = {
                PerformanceLevel.ENTERPRISE_READY: 100.0,
                PerformanceLevel.PRODUCTION_READY: 75.0,
                PerformanceLevel.DEVELOPMENT_READY: 50.0,
                PerformanceLevel.NOT_READY: 0.0,
            }
            
            total_score = sum(level_scores[benchmark.performance_level] for benchmark in benchmarks)
            max_possible_score = len(benchmarks) * 100.0
            
            return (total_score / max_possible_score) * 100.0 if max_possible_score > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate enterprise readiness score: {e}")
            return 0.0
    
    def _report_to_dict(self, report: SystemPerformanceReport) -> Dict[str, Any]:
        """Convert report to dictionary with proper enum handling"""
        try:
            report_dict = asdict(report)
            
            # Convert enums to strings
            report_dict["overall_performance_level"] = report.overall_performance_level.value
            
            # Convert benchmark enums
            for benchmark_dict in report_dict["benchmark_results"]:
                benchmark_dict["benchmark_type"] = benchmark_dict["benchmark_type"].value
                benchmark_dict["performance_level"] = benchmark_dict["performance_level"].value
            
            return report_dict
            
        except Exception as e:
            self.logger.error(f"Failed to convert report to dict: {e}")
            return {"error": f"Failed to convert report: {str(e)}"}
    
    def clear_reports(self) -> None:
        """Clear all stored reports"""
        self.reports.clear()
        self.logger.info("Cleared all reports")
    
    def export_report_to_file(self, report: SystemPerformanceReport, 
                            file_path: str, format_type: str = "json") -> bool:
        """Export report to file"""
        try:
            if format_type.lower() == "json":
                content = self.format_report_as_json(report)
            elif format_type.lower() == "html":
                content = self.format_report_as_html(report)
            elif format_type.lower() == "txt":
                content = self.format_report_as_text(report)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Exported report {report.report_id} to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export report to file: {e}")
            return False
