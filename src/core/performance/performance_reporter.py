#!/usr/bin/env python3
"""
Performance Reporter - Unified Performance Reporting System
=========================================================

Performance report generation and formatting consolidated from multiple files.
Follows Single Responsibility Principle with focused reporting functionality.

Author: Performance Validation Consolidation Team
License: MIT
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# from src.utils.stability_improvements import stability_manager, safe_import

# Import the core performance module
try:
    from .performance_core import BenchmarkResult, ValidationRule
except ImportError:
    # Fallback import for standalone testing
    from performance_core import BenchmarkResult, ValidationRule


@dataclass
class SystemPerformanceReport:
    """Comprehensive system performance report."""
    report_id: str
    timestamp: datetime
    overall_performance_level: str
    benchmark_results: List[BenchmarkResult]
    summary_statistics: Dict[str, Any]
    optimization_recommendations: List[str]
    report_format: str = "json"


class PerformanceReporter:
    """
    Unified performance reporting system consolidated from multiple files.
    
    Responsibilities:
    - Performance report generation
    - Report formatting and output
    - Historical data analysis
    - Trend identification
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceReporter")
        self.report_history: List[SystemPerformanceReport] = []
    
    def generate_performance_report(
        self,
        benchmark_results: List[BenchmarkResult],
        report_format: str = "json"
    ) -> SystemPerformanceReport:
        """
        Generate a comprehensive performance report from benchmark results.
        
        Args:
            benchmark_results: List of benchmark results to include in report
            report_format: Output format for the report
            
        Returns:
            SystemPerformanceReport object
        """
        try:
            self.logger.info(f"Generating performance report for {len(benchmark_results)} benchmarks")
            
            # Calculate overall performance level
            overall_level = self._calculate_overall_performance_level(benchmark_results)
            
            # Generate summary statistics
            summary_stats = self._generate_summary_statistics(benchmark_results)
            
            # Collect optimization recommendations
            optimization_recs = self._collect_optimization_recommendations(benchmark_results)
            
            # Create report
            report = SystemPerformanceReport(
                report_id=f"PERF_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                overall_performance_level=overall_level,
                benchmark_results=benchmark_results,
                summary_statistics=summary_stats,
                optimization_recommendations=optimization_recs,
                report_format=report_format
            )
            
            # Store in history
            self.report_history.append(report)
            
            self.logger.info(f"Generated performance report: {report.report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating performance report: {e}")
            raise
    
    def _calculate_overall_performance_level(
        self, 
        benchmark_results: List[BenchmarkResult]
    ) -> str:
        """Calculate overall performance level across all benchmarks."""
        if not benchmark_results:
            return "unknown"
        
        # Count performance levels
        level_counts = {}
        for result in benchmark_results:
            level = result.performance_level
            level_counts[level] = level_counts.get(level, 0) + 1
        
        # Determine overall level based on worst case
        if "critical" in level_counts:
            return "critical"
        elif "poor" in level_counts:
            return "poor"
        elif "acceptable" in level_counts:
            return "acceptable"
        elif "good" in level_counts:
            return "good"
        else:
            return "excellent"
    
    def _generate_summary_statistics(
        self, 
        benchmark_results: List[BenchmarkResult]
    ) -> Dict[str, Any]:
        """Generate summary statistics from benchmark results."""
        if not benchmark_results:
            return {}
        
        # Calculate total duration
        total_duration = sum(result.duration for result in benchmark_results)
        
        # Count benchmark types
        type_counts = {}
        for result in benchmark_results:
            btype = result.benchmark_type
            type_counts[btype] = type_counts.get(btype, 0) + 1
        
        # Calculate average metrics across all benchmarks
        all_metrics = {}
        for result in benchmark_results:
            for metric_name, metric_value in result.metrics.items():
                if metric_name not in all_metrics:
                    all_metrics[metric_name] = []
                if isinstance(metric_value, (int, float)):
                    all_metrics[metric_name].append(metric_value)
        
        # Calculate averages
        avg_metrics = {}
        for metric_name, values in all_metrics.items():
            if values:
                avg_metrics[f"avg_{metric_name}"] = sum(values) / len(values)
                avg_metrics[f"min_{metric_name}"] = min(values)
                avg_metrics[f"max_{metric_name}"] = max(values)
        
        return {
            "total_benchmarks": len(benchmark_results),
            "total_duration": total_duration,
            "benchmark_type_counts": type_counts,
            "average_metrics": avg_metrics,
            "performance_level_distribution": self._get_performance_level_distribution(benchmark_results)
        }
    
    def _get_performance_level_distribution(
        self, 
        benchmark_results: List[BenchmarkResult]
    ) -> Dict[str, int]:
        """Get distribution of performance levels across benchmarks."""
        distribution = {}
        for result in benchmark_results:
            level = result.performance_level
            distribution[level] = distribution.get(level, 0) + 1
        return distribution
    
    def _collect_optimization_recommendations(
        self, 
        benchmark_results: List[BenchmarkResult]
    ) -> List[str]:
        """Collect and deduplicate optimization recommendations."""
        all_recommendations = []
        for result in benchmark_results:
            all_recommendations.extend(result.optimization_recommendations)
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        seen = set()
        for rec in all_recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        return unique_recommendations
    
    def format_report(
        self, 
        report: SystemPerformanceReport, 
        output_format: Optional[str] = None
    ) -> str:
        """
        Format a performance report for output.
        
        Args:
            report: The performance report to format
            output_format: Output format (overrides report.report_format if specified)
            
        Returns:
            Formatted report as string
        """
        format_type = output_format or report.report_format
        
        if format_type == "json":
            return self._format_json(report)
        elif format_type == "text":
            return self._format_text(report)
        elif format_type == "html":
            return self._format_html(report)
        else:
            self.logger.warning(f"Unknown format type: {format_type}, defaulting to JSON")
            return self._format_json(report)
    
    def _format_json(self, report: SystemPerformanceReport) -> str:
        """Format report as JSON."""
        # Convert datetime objects to ISO strings for JSON serialization
        report_dict = asdict(report)
        report_dict["timestamp"] = report.timestamp.isoformat()
        
        for result in report_dict["benchmark_results"]:
            result["start_time"] = result["start_time"].isoformat()
            result["end_time"] = result["end_time"].isoformat()
        
        return json.dumps(report_dict, indent=2, default=str)
    
    def _format_text(self, report: SystemPerformanceReport) -> str:
        """Format report as human-readable text."""
        lines = []
        lines.append("=" * 60)
        lines.append("PERFORMANCE VALIDATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Report ID: {report.report_id}")
        lines.append(f"Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Overall Performance: {report.overall_performance_level.upper()}")
        lines.append("")
        
        # Summary statistics
        lines.append("SUMMARY STATISTICS:")
        lines.append("-" * 30)
        lines.append(f"Total Benchmarks: {report.summary_statistics.get('total_benchmarks', 0)}")
        lines.append(f"Total Duration: {report.summary_statistics.get('total_duration', 0):.2f}s")
        lines.append("")
        
        # Benchmark results
        lines.append("BENCHMARK RESULTS:")
        lines.append("-" * 30)
        for i, result in enumerate(report.benchmark_results, 1):
            lines.append(f"{i}. {result.benchmark_type.upper()}")
            lines.append(f"   Performance Level: {result.performance_level}")
            lines.append(f"   Duration: {result.duration:.2f}s")
            lines.append(f"   Key Metrics: {', '.join(result.metrics.keys())}")
            lines.append("")
        
        # Optimization recommendations
        if report.optimization_recommendations:
            lines.append("OPTIMIZATION RECOMMENDATIONS:")
            lines.append("-" * 30)
            for i, rec in enumerate(report.optimization_recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def _format_html(self, report: SystemPerformanceReport) -> str:
        """Format report as HTML."""
        html_lines = []
        html_lines.append("<!DOCTYPE html>")
        html_lines.append("<html>")
        html_lines.append("<head>")
        html_lines.append("<title>Performance Validation Report</title>")
        html_lines.append("<style>")
        html_lines.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html_lines.append(".header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }")
        html_lines.append(".section { margin: 20px 0; }")
        html_lines.append(".benchmark { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px; }")
        html_lines.append(".excellent { border-left: 5px solid #4CAF50; }")
        html_lines.append(".good { border-left: 5px solid #8BC34A; }")
        html_lines.append(".acceptable { border-left: 5px solid #FFC107; }")
        html_lines.append(".poor { border-left: 5px solid #FF9800; }")
        html_lines.append(".critical { border-left: 5px solid #F44336; }")
        html_lines.append("</style>")
        html_lines.append("</head>")
        html_lines.append("<body>")
        
        # Header
        html_lines.append('<div class="header">')
        html_lines.append(f'<h1>Performance Validation Report</h1>')
        html_lines.append(f'<p><strong>Report ID:</strong> {report.report_id}</p>')
        html_lines.append(f'<p><strong>Generated:</strong> {report.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>')
        html_lines.append(f'<p><strong>Overall Performance:</strong> {report.overall_performance_level.upper()}</p>')
        html_lines.append('</div>')
        
        # Summary
        html_lines.append('<div class="section">')
        html_lines.append('<h2>Summary Statistics</h2>')
        html_lines.append(f'<p><strong>Total Benchmarks:</strong> {report.summary_statistics.get("total_benchmarks", 0)}</p>')
        html_lines.append(f'<p><strong>Total Duration:</strong> {report.summary_statistics.get("total_duration", 0):.2f}s</p>')
        html_lines.append('</div>')
        
        # Benchmarks
        html_lines.append('<div class="section">')
        html_lines.append('<h2>Benchmark Results</h2>')
        for result in report.benchmark_results:
            css_class = result.performance_level
            html_lines.append(f'<div class="benchmark {css_class}">')
            html_lines.append(f'<h3>{result.benchmark_type.upper()}</h3>')
            html_lines.append(f'<p><strong>Performance Level:</strong> {result.performance_level}</p>')
            html_lines.append(f'<p><strong>Duration:</strong> {result.duration:.2f}s</p>')
            html_lines.append('</div>')
        html_lines.append('</div>')
        
        # Recommendations
        if report.optimization_recommendations:
            html_lines.append('<div class="section">')
            html_lines.append('<h2>Optimization Recommendations</h2>')
            html_lines.append('<ul>')
            for rec in report.optimization_recommendations:
                html_lines.append(f'<li>{rec}</li>')
            html_lines.append('</ul>')
            html_lines.append('</div>')
        
        html_lines.append("</body>")
        html_lines.append("</html>")
        
        return "\n".join(html_lines)
    
    def get_latest_report(self) -> Optional[SystemPerformanceReport]:
        """Get the most recent performance report."""
        if self.report_history:
            return self.report_history[-1]
        return None
    
    def get_report_by_id(self, report_id: str) -> Optional[SystemPerformanceReport]:
        """Get a specific performance report by ID."""
        for report in self.report_history:
            if report.report_id == report_id:
                return report
        return None
    
    def get_reports_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[SystemPerformanceReport]:
        """Get all reports within a date range."""
        reports = []
        for report in self.report_history:
            if start_date <= report.timestamp <= end_date:
                reports.append(report)
        return reports
    
    def export_report_history(self, filepath: str, format_type: str = "json") -> bool:
        """
        Export the complete report history to a file.
        
        Args:
            filepath: Path to the output file
            format_type: Export format (json, text, html)
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if not self.report_history:
                self.logger.warning("No report history to export")
                return False
            
            # Generate a comprehensive report from all history
            all_results = []
            for report in self.report_history:
                all_results.extend(report.benchmark_results)
            
            comprehensive_report = self.generate_performance_report(all_results, format_type)
            formatted_report = self.format_report(comprehensive_report, format_type)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_report)
            
            self.logger.info(f"Exported report history to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting report history: {e}")
            return False
