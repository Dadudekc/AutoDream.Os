#!/usr/bin/env python3
"""
Error Report Generator - V2 Error Report Generation
==================================================
Specialized module for generating comprehensive error analytics reports
in multiple formats. Follows V2 standards with advanced reporting
and visualization capabilities.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum

# ──────────────────────────── Logging
log = logging.getLogger("error_report_generator")


class ReportFormat(str, Enum):
    """Report output formats"""
    
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    CONSOLE = "console"


@dataclass
class AnalyticsReport:
    """Comprehensive analytics report"""
    
    report_id: str
    timestamp: str
    time_range: str
    summary: Dict[str, Any]
    patterns: List[Dict[str, Any]]
    trends: List[Dict[str, Any]]
    correlations: List[Dict[str, Any]]
    recommendations: List[str]
    metadata: Dict[str, Any]


class ErrorReportGenerator:
    """Advanced error analytics report generation"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.reports_directory = Path(self.config.get("reports_directory", "reports"))
        self.reports_directory.mkdir(exist_ok=True)
        
        # Report configuration
        self.default_format = ReportFormat.JSON
        self.include_metadata = self.config.get("include_metadata", True)
        self.include_recommendations = self.config.get("include_recommendations", True)
        
    def generate_comprehensive_report(
        self,
        patterns: List[Dict[str, Any]],
        trends: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]],
        format_type: ReportFormat = None
    ) -> AnalyticsReport:
        """Generate a comprehensive analytics report"""
        try:
            # Generate report ID and timestamp
            report_id = f"error_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            timestamp = datetime.now().isoformat()
            time_range = f"Last 24 hours (generated at {timestamp})"
            
            # Create summary
            summary = self._create_report_summary(patterns, trends, correlations)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(patterns, trends, correlations)
            
            # Create metadata
            metadata = self._create_report_metadata(patterns, trends, correlations)
            
            # Create report object
            report = AnalyticsReport(
                report_id=report_id,
                timestamp=timestamp,
                time_range=time_range,
                summary=summary,
                patterns=patterns,
                trends=trends,
                correlations=correlations,
                recommendations=recommendations,
                metadata=metadata
            )
            
            # Generate output in specified format
            if format_type:
                self._output_report(report, format_type)
            
            log.info(f"Generated comprehensive report: {report_id}")
            return report
            
        except Exception as e:
            log.error(f"Error generating comprehensive report: {e}")
            return None
    
    def _create_report_summary(
        self,
        patterns: List[Dict[str, Any]],
        trends: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a summary of the analytics data"""
        try:
            summary = {
                "total_patterns": len(patterns),
                "total_trends": len(trends),
                "total_correlations": len(correlations),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            # Pattern summary
            if patterns:
                high_frequency_patterns = [p for p in patterns if p.get("occurrences", 0) >= 10]
                summary["high_frequency_patterns"] = len(high_frequency_patterns)
                summary["average_pattern_occurrences"] = sum(
                    p.get("occurrences", 0) for p in patterns
                ) / len(patterns)
            
            # Trend summary
            if trends:
                increasing_trends = [t for t in trends if t.get("trend_direction") == "increasing"]
                decreasing_trends = [t for t in trends if t.get("trend_direction") == "decreasing"]
                summary["increasing_trends"] = len(increasing_trends)
                summary["decreasing_trends"] = len(decreasing_trends)
                summary["trend_confidence"] = sum(
                    t.get("trend_confidence", 0) for t in trends
                ) / len(trends)
            
            # Correlation summary
            if correlations:
                strong_correlations = [c for c in correlations if c.get("correlation_strength", 0) >= 0.8]
                summary["strong_correlations"] = len(strong_correlations)
                summary["average_correlation_strength"] = sum(
                    c.get("correlation_strength", 0) for c in correlations
                ) / len(correlations)
            
            return summary
            
        except Exception as e:
            log.error(f"Error creating report summary: {e}")
            return {"error": "Failed to create summary"}
    
    def _generate_recommendations(
        self,
        patterns: List[Dict[str, Any]],
        trends: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations based on analytics"""
        try:
            recommendations = []
            
            # Pattern-based recommendations
            high_frequency_patterns = [p for p in patterns if p.get("occurrences", 0) >= 10]
            if high_frequency_patterns:
                recommendations.append(
                    f"Investigate {len(high_frequency_patterns)} high-frequency error patterns "
                    "for potential systemic issues"
                )
            
            # Trend-based recommendations
            increasing_trends = [t for t in trends if t.get("trend_direction") == "increasing"]
            if increasing_trends:
                recommendations.append(
                    f"Address {len(increasing_trends)} increasing error trends "
                    "before they become critical"
                )
            
            # Correlation-based recommendations
            strong_correlations = [c for c in correlations if c.get("correlation_strength", 0) >= 0.8]
            if strong_correlations:
                recommendations.append(
                    f"Investigate {len(strong_correlations)} strong error correlations "
                    "for root cause analysis"
                )
            
            # General recommendations
            if not recommendations:
                recommendations.append("Monitor error patterns for emerging issues")
                recommendations.append("Continue collecting error data for trend analysis")
            
            return recommendations
            
        except Exception as e:
            log.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _create_report_metadata(
        self,
        patterns: List[Dict[str, Any]],
        trends: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create metadata for the report"""
        try:
            metadata = {
                "generator_version": "2.0.0",
                "generation_timestamp": datetime.now().isoformat(),
                "data_sources": ["error_handler", "pattern_detector", "trend_analyzer", "correlation_analyzer"],
                "report_configuration": {
                    "include_metadata": self.include_metadata,
                    "include_recommendations": self.include_recommendations,
                    "reports_directory": str(self.reports_directory)
                }
            }
            
            # Add data quality metrics
            if patterns:
                metadata["pattern_data_quality"] = {
                    "total_patterns": len(patterns),
                    "patterns_with_timestamps": len([p for p in patterns if p.get("first_seen") and p.get("last_seen")]),
                    "patterns_with_severity": len([p for p in patterns if p.get("severity_distribution")])
                }
            
            if trends:
                metadata["trend_data_quality"] = {
                    "total_trends": len(trends),
                    "trends_with_direction": len([t for t in trends if t.get("trend_direction")]),
                    "trends_with_confidence": len([t for t in trends if t.get("trend_confidence")])
                }
            
            if correlations:
                metadata["correlation_data_quality"] = {
                    "total_correlations": len(correlations),
                    "correlations_with_strength": len([c for c in correlations if c.get("correlation_strength")]),
                    "correlations_with_type": len([c for c in correlations if c.get("correlation_type")])
                }
            
            return metadata
            
        except Exception as e:
            log.error(f"Error creating report metadata: {e}")
            return {"error": "Failed to create metadata"}
    
    def _output_report(self, report: AnalyticsReport, format_type: ReportFormat):
        """Output the report in the specified format"""
        try:
            if format_type == ReportFormat.JSON:
                self._output_json_report(report)
            elif format_type == ReportFormat.MARKDOWN:
                self._output_markdown_report(report)
            elif format_type == ReportFormat.HTML:
                self._output_html_report(report)
            elif format_type == ReportFormat.CSV:
                self._output_csv_report(report)
            elif format_type == ReportFormat.CONSOLE:
                self._output_console_report(report)
            else:
                log.warning(f"Unknown report format: {format_type}, using JSON")
                self._output_json_report(report)
                
        except Exception as e:
            log.error(f"Error outputting report: {e}")
    
    def _output_json_report(self, report: AnalyticsReport):
        """Output report in JSON format"""
        try:
            report_path = self.reports_directory / f"error_analytics_{report.report_id}.json"
            
            # Convert report to dictionary
            report_dict = asdict(report)
            
            with open(report_path, "w") as f:
                json.dump(report_dict, f, indent=2, default=str)
            
            log.info(f"JSON report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving JSON report: {e}")
    
    def _output_markdown_report(self, report: AnalyticsReport):
        """Output report in Markdown format"""
        try:
            report_path = self.reports_directory / f"error_analytics_{report.report_id}.md"
            
            markdown_content = f"""# Error Analytics Report

**Generated:** {report.timestamp}  
**Time Range:** {report.time_range}  
**Report ID:** {report.report_id}

## Summary

"""
            
            # Add summary items
            for key, value in report.summary.items():
                markdown_content += f"- **{key.replace('_', ' ').title()}:** {value}\n"
            
            markdown_content += "\n## Patterns\n\n"
            
            # Add patterns
            if report.patterns:
                for pattern in report.patterns:
                    markdown_content += f"- **{pattern.get('error_signature', 'Unknown')}** "
                    markdown_content += f"({pattern.get('occurrences', 0)} occurrences)\n"
            else:
                markdown_content += "No patterns detected\n"
            
            markdown_content += "\n## Trends\n\n"
            
            # Add trends
            if report.trends:
                for trend in report.trends:
                    markdown_content += f"- **{trend.get('time_period', 'Unknown')}**: "
                    markdown_content += f"{trend.get('error_count', 0)} errors, "
                    markdown_content += f"{trend.get('trend_direction', 'unknown')} trend\n"
            else:
                markdown_content += "No trends detected\n"
            
            markdown_content += "\n## Correlations\n\n"
            
            # Add correlations
            if report.correlations:
                for correlation in report.correlations:
                    markdown_content += f"- **{correlation.get('primary_error', 'Unknown')}** "
                    markdown_content += f"↔ {', '.join(correlation.get('correlated_errors', []))} "
                    markdown_content += f"(strength: {correlation.get('correlation_strength', 0):.2f})\n"
            else:
                markdown_content += "No correlations detected\n"
            
            # Add recommendations
            if report.recommendations:
                markdown_content += "\n## Recommendations\n\n"
                for rec in report.recommendations:
                    markdown_content += f"- {rec}\n"
            
            with open(report_path, "w") as f:
                f.write(markdown_content)
            
            log.info(f"Markdown report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving Markdown report: {e}")
    
    def _output_html_report(self, report: AnalyticsReport):
        """Output report in HTML format"""
        try:
            report_path = self.reports_directory / f"error_analytics_{report.report_id}.html"
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Error Analytics Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
        .summary-item {{ background-color: #f9f9f9; padding: 10px; border-radius: 3px; }}
        h1, h2 {{ color: #333; }}
        ul {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Error Analytics Report</h1>
        <p><strong>Generated:</strong> {report.timestamp}</p>
        <p><strong>Time Range:</strong> {report.time_range}</p>
        <p><strong>Report ID:</strong> {report.report_id}</p>
    </div>

    <div class="section">
        <h2>Summary</h2>
        <div class="summary">
"""
            
            for key, value in report.summary.items():
                html_content += f"""
            <div class="summary-item">
                <strong>{key.replace('_', ' ').title()}</strong><br>
                {value}
            </div>
"""
            
            html_content += """
        </div>
    </div>

    <div class="section">
        <h2>Recommendations</h2>
        <ul>
"""
            
            for rec in report.recommendations:
                html_content += f"<li>{rec}</li>"
            
            html_content += """
        </ul>
    </div>
</body>
</html>
"""
            
            with open(report_path, "w") as f:
                f.write(html_content)
            
            log.info(f"HTML report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving HTML report: {e}")
    
    def _output_csv_report(self, report: AnalyticsReport):
        """Output report in CSV format"""
        try:
            report_path = self.reports_directory / f"error_analytics_{report.report_id}.csv"
            
            with open(report_path, "w") as f:
                # Summary
                f.write("Category,Value\n")
                for key, value in report.summary.items():
                    f.write(f"{key.replace('_', ' ').title()},{value}\n")
                
                # Patterns
                if report.patterns:
                    f.write("\nPattern,Occurrences,First Seen,Last Seen\n")
                    for pattern in report.patterns:
                        f.write(
                            f"{pattern.get('error_signature', 'Unknown')},"
                            f"{pattern.get('occurrences', 0)},"
                            f"{pattern.get('first_seen', 'Unknown')},"
                            f"{pattern.get('last_seen', 'Unknown')}\n"
                        )
                
                # Trends
                if report.trends:
                    f.write("\nTime Period,Error Count,Trend Direction\n")
                    for trend in report.trends:
                        f.write(
                            f"{trend.get('time_period', 'Unknown')},"
                            f"{trend.get('error_count', 0)},"
                            f"{trend.get('trend_direction', 'unknown')}\n"
                        )
                
                # Correlations
                if report.correlations:
                    f.write("\nPrimary Error,Correlated Errors,Strength,Type\n")
                    for correlation in report.correlations:
                        f.write(
                            f"{correlation.get('primary_error', 'Unknown')},"
                            f"{','.join(correlation.get('correlated_errors', []))},"
                            f"{correlation.get('correlation_strength', 0):.2f},"
                            f"{correlation.get('correlation_type', 'unknown')}\n"
                        )
            
            log.info(f"CSV report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving CSV report: {e}")
    
    def _output_console_report(self, report: AnalyticsReport):
        """Output report to console"""
        try:
            print(f"\n{'='*60}")
            print(f"ERROR ANALYTICS REPORT")
            print(f"{'='*60}")
            print(f"Generated: {report.timestamp}")
            print(f"Time Range: {report.time_range}")
            print(f"Report ID: {report.report_id}")
            print(f"{'='*60}")
            
            print(f"\nSUMMARY:")
            for key, value in report.summary.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            
            if report.recommendations:
                print(f"\nRECOMMENDATIONS:")
                for rec in report.recommendations:
                    print(f"  • {rec}")
            
            print(f"\n{'='*60}")
            
        except Exception as e:
            log.error(f"Error outputting console report: {e}")
    
    def get_report_statistics(self) -> Dict[str, Any]:
        """Get report generation statistics"""
        try:
            report_files = list(self.reports_directory.glob("error_analytics_*.json"))
            
            return {
                "total_reports_generated": len(report_files),
                "reports_directory": str(self.reports_directory),
                "latest_report": max(report_files).name if report_files else None,
                "report_formats_supported": [fmt.value for fmt in ReportFormat]
            }
            
        except Exception as e:
            log.error(f"Error getting report statistics: {e}")
            return {}
    
    def cleanup_old_reports(self, days_to_keep: int = 30):
        """Clean up old report files"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0
            
            for report_file in self.reports_directory.glob("error_analytics_*"):
                if report_file.stat().st_mtime < cutoff_date:
                    report_file.unlink()
                    deleted_count += 1
            
            log.info(f"Cleaned up {deleted_count} old report files")
            
        except Exception as e:
            log.error(f"Error cleaning up old reports: {e}")
    
    def shutdown(self):
        """Shutdown the report generator"""
        log.info("Error Report Generator shutdown complete")
