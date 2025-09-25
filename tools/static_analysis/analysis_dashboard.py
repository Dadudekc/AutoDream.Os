#!/usr/bin/env python3
"""
Analysis Dashboard - Interactive Static Analysis Reporting
=========================================================

Interactive dashboard for viewing and analyzing static analysis results
with rich visualizations and detailed reporting.

Author: Agent-2 (Security & Quality Specialist)
License: MIT
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

logger = logging.getLogger(__name__)


class AnalysisDashboard:
    """Interactive static analysis dashboard."""
    
    def __init__(self, project_root: str = "."):
        """Initialize analysis dashboard."""
        self.project_root = Path(project_root).resolve()
        self.console = Console() if RICH_AVAILABLE else None
        self.reports_dir = self.project_root / 'analysis_reports'
    
    def display_security_summary(self, security_data: Dict[str, Any]) -> None:
        """Display security analysis summary."""
        if not self.console:
            self._print_security_summary(security_data)
            return
        
        summary = security_data.get('summary', {})
        
        # Create security summary table
        table = Table(title="🔒 Security Analysis Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        table.add_column("Status", style="green")
        
        total_issues = summary.get('total_issues', 0)
        high_severity = summary.get('high_severity', 0)
        medium_severity = summary.get('medium_severity', 0)
        low_severity = summary.get('low_severity', 0)
        
        table.add_row("Total Issues", str(total_issues), 
                     "🚨 CRITICAL" if high_severity > 0 else "✅ GOOD")
        table.add_row("High Severity", str(high_severity),
                     "🚨 CRITICAL" if high_severity > 0 else "✅ GOOD")
        table.add_row("Medium Severity", str(medium_severity),
                     "⚠️  WARNING" if medium_severity > 5 else "✅ GOOD")
        table.add_row("Low Severity", str(low_severity),
                     "ℹ️  INFO" if low_severity > 0 else "✅ GOOD")
        
        self.console.print(table)
        
        # Display recommendations
        recommendations = summary.get('recommendations', [])
        if recommendations:
            rec_text = "\n".join(f"• {rec}" for rec in recommendations)
            panel = Panel(rec_text, title="📋 Security Recommendations", border_style="yellow")
            self.console.print(panel)
    
    def display_quality_summary(self, quality_data: Dict[str, Any]) -> None:
        """Display code quality analysis summary."""
        if not self.console:
            self._print_quality_summary(quality_data)
            return
        
        metrics = quality_data.get('metrics', {})
        
        # Create quality summary table
        table = Table(title="🔍 Code Quality Analysis Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Score", style="magenta")
        table.add_column("Status", style="green")
        
        overall_score = metrics.get('overall_score', 0)
        code_style = metrics.get('code_style', 0)
        type_safety = metrics.get('type_safety', 0)
        maintainability = metrics.get('maintainability', 0)
        
        table.add_row("Overall Score", f"{overall_score:.1f}/100",
                     self._get_score_status(overall_score))
        table.add_row("Code Style", f"{code_style:.1f}/100",
                     self._get_score_status(code_style))
        table.add_row("Type Safety", f"{type_safety:.1f}/100",
                     self._get_score_status(type_safety))
        table.add_row("Maintainability", f"{maintainability:.1f}/100",
                     self._get_score_status(maintainability))
        
        self.console.print(table)
        
        # Display violation summary
        violations = quality_data.get('violations', {})
        if violations:
            self._display_violation_summary(violations)
    
    def display_dependency_summary(self, dependency_data: Dict[str, Any]) -> None:
        """Display dependency vulnerability summary."""
        if not self.console:
            self._print_dependency_summary(dependency_data)
            return
        
        summary = dependency_data.get('summary', {})
        
        # Create dependency summary table
        table = Table(title="📦 Dependency Vulnerability Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        table.add_column("Status", style="green")
        
        total_vulns = summary.get('total_vulnerabilities', 0)
        high_severity = summary.get('high_severity', 0)
        medium_severity = summary.get('medium_severity', 0)
        low_severity = summary.get('low_severity', 0)
        
        table.add_row("Total Vulnerabilities", str(total_vulns),
                     "🚨 CRITICAL" if high_severity > 0 else "✅ GOOD")
        table.add_row("High Severity", str(high_severity),
                     "🚨 CRITICAL" if high_severity > 0 else "✅ GOOD")
        table.add_row("Medium Severity", str(medium_severity),
                     "⚠️  WARNING" if medium_severity > 5 else "✅ GOOD")
        table.add_row("Low Severity", str(low_severity),
                     "ℹ️  INFO" if low_severity > 0 else "✅ GOOD")
        
        self.console.print(table)
        
        # Display recommendations
        recommendations = summary.get('recommendations', [])
        if recommendations:
            rec_text = "\n".join(f"• {rec}" for rec in recommendations)
            panel = Panel(rec_text, title="📋 Dependency Recommendations", border_style="yellow")
            self.console.print(panel)
    
    def _get_score_status(self, score: float) -> str:
        """Get status emoji for score."""
        if score >= 90:
            return "✅ EXCELLENT"
        elif score >= 80:
            return "✅ GOOD"
        elif score >= 70:
            return "⚠️  FAIR"
        else:
            return "🚨 POOR"
    
    def _display_violation_summary(self, violations: Dict[str, Any]) -> None:
        """Display violation summary."""
        table = Table(title="📊 Violation Summary")
        table.add_column("Tool", style="cyan")
        table.add_column("Violations", style="magenta")
        
        by_tool = violations.get('by_tool', {})
        for tool, count in by_tool.items():
            table.add_row(tool.title(), str(count))
        
        self.console.print(table)
    
    def _print_security_summary(self, security_data: Dict[str, Any]) -> None:
        """Print security summary without rich."""
        summary = security_data.get('summary', {})
        print(f"\n🔒 Security Analysis Summary:")
        print(f"Total Issues: {summary.get('total_issues', 0)}")
        print(f"High Severity: {summary.get('high_severity', 0)}")
        print(f"Medium Severity: {summary.get('medium_severity', 0)}")
        print(f"Low Severity: {summary.get('low_severity', 0)}")
        
        recommendations = summary.get('recommendations', [])
        if recommendations:
            print(f"\n📋 Recommendations:")
            for rec in recommendations:
                print(f"  {rec}")
    
    def _print_quality_summary(self, quality_data: Dict[str, Any]) -> None:
        """Print quality summary without rich."""
        metrics = quality_data.get('metrics', {})
        print(f"\n🔍 Code Quality Analysis Summary:")
        print(f"Overall Score: {metrics.get('overall_score', 0):.1f}/100")
        print(f"Code Style: {metrics.get('code_style', 0):.1f}/100")
        print(f"Type Safety: {metrics.get('type_safety', 0):.1f}/100")
        print(f"Maintainability: {metrics.get('maintainability', 0):.1f}/100")
    
    def _print_dependency_summary(self, dependency_data: Dict[str, Any]) -> None:
        """Print dependency summary without rich."""
        summary = dependency_data.get('summary', {})
        print(f"\n📦 Dependency Vulnerability Summary:")
        print(f"Total Vulnerabilities: {summary.get('total_vulnerabilities', 0)}")
        print(f"High Severity: {summary.get('high_severity', 0)}")
        print(f"Medium Severity: {summary.get('medium_severity', 0)}")
        print(f"Low Severity: {summary.get('low_severity', 0)}")
    
    def load_and_display_reports(self) -> None:
        """Load and display all analysis reports."""
        if not self.reports_dir.exists():
            print("❌ No analysis reports found. Run analysis first.")
            return
        
        # Load security report
        security_file = self.reports_dir / 'security_report.json'
        if security_file.exists():
            with open(security_file, 'r') as f:
                security_data = json.load(f)
            self.display_security_summary(security_data)
        
        # Load quality report
        quality_file = self.reports_dir / 'quality_report.json'
        if quality_file.exists():
            with open(quality_file, 'r') as f:
                quality_data = json.load(f)
            self.display_quality_summary(quality_data)
        
        # Load dependency report
        dependency_file = self.reports_dir / 'dependency_vulnerability_report.json'
        if dependency_file.exists():
            with open(dependency_file, 'r') as f:
                dependency_data = json.load(f)
            self.display_dependency_summary(dependency_data)
    
    def generate_html_report(self, output_file: Optional[str] = None) -> str:
        """Generate HTML report."""
        if not self.reports_dir.exists():
            raise FileNotFoundError("No analysis reports found. Run analysis first.")
        
        html_file = output_file or self.project_root / 'analysis_dashboard.html'
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Analysis Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .section { background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; text-align: center; min-width: 120px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #333; }
        .metric-label { font-size: 14px; color: #666; margin-top: 5px; }
        .status-good { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-critical { color: #dc3545; }
        .recommendations { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-top: 15px; }
        .recommendations h4 { margin-top: 0; color: #856404; }
        .recommendations ul { margin-bottom: 0; }
        .timestamp { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Static Analysis Dashboard</h1>
            <p class="timestamp">Generated: {timestamp}</p>
        </div>
"""
        
        # Add security section
        security_file = self.reports_dir / 'security_report.json'
        if security_file.exists():
            with open(security_file, 'r') as f:
                security_data = json.load(f)
            
            summary = security_data.get('summary', {})
            html_content += f"""
        <div class="section">
            <h2>🔒 Security Analysis</h2>
            <div class="metric">
                <div class="metric-value {'status-critical' if summary.get('high_severity', 0) > 0 else 'status-good'}">{summary.get('total_issues', 0)}</div>
                <div class="metric-label">Total Issues</div>
            </div>
            <div class="metric">
                <div class="metric-value status-critical">{summary.get('high_severity', 0)}</div>
                <div class="metric-label">High Severity</div>
            </div>
            <div class="metric">
                <div class="metric-value status-warning">{summary.get('medium_severity', 0)}</div>
                <div class="metric-label">Medium Severity</div>
            </div>
            <div class="metric">
                <div class="metric-value status-good">{summary.get('low_severity', 0)}</div>
                <div class="metric-label">Low Severity</div>
            </div>
"""
            
            recommendations = summary.get('recommendations', [])
            if recommendations:
                html_content += f"""
            <div class="recommendations">
                <h4>📋 Security Recommendations</h4>
                <ul>
"""
                for rec in recommendations:
                    html_content += f"                    <li>{rec}</li>\n"
                html_content += "                </ul>\n            </div>\n"
            
            html_content += "        </div>\n"
        
        # Add quality section
        quality_file = self.reports_dir / 'quality_report.json'
        if quality_file.exists():
            with open(quality_file, 'r') as f:
                quality_data = json.load(f)
            
            metrics = quality_data.get('metrics', {})
            html_content += f"""
        <div class="section">
            <h2>🔍 Code Quality Analysis</h2>
            <div class="metric">
                <div class="metric-value {'status-critical' if metrics.get('overall_score', 0) < 70 else 'status-good'}">{metrics.get('overall_score', 0):.1f}</div>
                <div class="metric-label">Overall Score</div>
            </div>
            <div class="metric">
                <div class="metric-value status-good">{metrics.get('code_style', 0):.1f}</div>
                <div class="metric-label">Code Style</div>
            </div>
            <div class="metric">
                <div class="metric-value status-good">{metrics.get('type_safety', 0):.1f}</div>
                <div class="metric-label">Type Safety</div>
            </div>
            <div class="metric">
                <div class="metric-value status-good">{metrics.get('maintainability', 0):.1f}</div>
                <div class="metric-label">Maintainability</div>
            </div>
        </div>
"""
        
        # Add dependency section
        dependency_file = self.reports_dir / 'dependency_vulnerability_report.json'
        if dependency_file.exists():
            with open(dependency_file, 'r') as f:
                dependency_data = json.load(f)
            
            summary = dependency_data.get('summary', {})
            html_content += f"""
        <div class="section">
            <h2>📦 Dependency Vulnerabilities</h2>
            <div class="metric">
                <div class="metric-value {'status-critical' if summary.get('high_severity', 0) > 0 else 'status-good'}">{summary.get('total_vulnerabilities', 0)}</div>
                <div class="metric-label">Total Vulnerabilities</div>
            </div>
            <div class="metric">
                <div class="metric-value status-critical">{summary.get('high_severity', 0)}</div>
                <div class="metric-label">High Severity</div>
            </div>
            <div class="metric">
                <div class="metric-value status-warning">{summary.get('medium_severity', 0)}</div>
                <div class="metric-label">Medium Severity</div>
            </div>
            <div class="metric">
                <div class="metric-value status-good">{summary.get('low_severity', 0)}</div>
                <div class="metric-label">Low Severity</div>
            </div>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # Replace timestamp placeholder
        html_content = html_content.replace('{timestamp}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"📄 HTML dashboard generated: {html_file}")
        return str(html_file)


def main():
    """Main entry point for analysis dashboard."""
    parser = argparse.ArgumentParser(description='Static Analysis Dashboard')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--output', help='Output file for HTML report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    dashboard = AnalysisDashboard(args.project_root)
    
    if args.html:
        html_file = dashboard.generate_html_report(args.output)
        print(f"📄 HTML dashboard generated: {html_file}")
    else:
        dashboard.load_and_display_reports()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())






