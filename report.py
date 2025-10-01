#!/usr/bin/env python3
"""
Reporting System - Comprehensive Report Generation
==================================================

Multi-format report generation system for V2_SWARM monitoring and analysis.
Supports JSON, Markdown, and HTML output formats.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ReportConfig:
    """Report configuration data class"""
    title: str
    format: str
    output_path: str
    include_timestamp: bool = True
    include_summary: bool = True


class ReportGenerator:
    """Generate reports in multiple formats"""
    
    def __init__(self, config: Optional[ReportConfig] = None):
        """Initialize report generator"""
        self.config = config or ReportConfig(
            title="V2_SWARM System Report",
            format="markdown",
            output_path="reports/system_report.md"
        )
    
    def generate_json_report(self, data: Dict[str, Any]) -> str:
        """Generate JSON format report"""
        report = {
            "title": self.config.title,
            "timestamp": datetime.now().isoformat() if self.config.include_timestamp else None,
            "data": data
        }
        return json.dumps(report, indent=2)
    
    def generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """Generate Markdown format report"""
        lines = []
        
        # Header
        lines.append(f"# {self.config.title}")
        lines.append("")
        
        # Timestamp
        if self.config.include_timestamp:
            lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
        
        # System Health Section
        if "system_health" in data:
            health = data["system_health"]
            lines.append("## System Health")
            lines.append("")
            lines.append(f"- **Status**: {health.get('overall_status', 'UNKNOWN')}")
            lines.append(f"- **Health Score**: {health.get('health_score', 0):.1f}/100")
            lines.append(f"- **Active Agents**: {health.get('active_agents', 0)}/{health.get('total_agents', 0)}")
            lines.append("")
            
            # Alerts
            alerts = health.get('alerts', [])
            if alerts:
                lines.append("### Alerts")
                lines.append("")
                for alert in alerts:
                    lines.append(f"- ⚠️  {alert}")
                lines.append("")
        
        # Agent Details Section
        if "agent_details" in data:
            agent_data = data["agent_details"]
            lines.append("## Agent Status")
            lines.append("")
            lines.append("| Agent | Status | Role | Tasks | Health |")
            lines.append("|-------|--------|------|-------|--------|")
            
            for agent in agent_data.get('agents', []):
                status_emoji = "✅" if agent['status'] == 'ACTIVE' else "❌"
                lines.append(
                    f"| {status_emoji} {agent['agent_id']} | "
                    f"{agent['status']} | "
                    f"{agent['role']} | "
                    f"{agent['task_count']} | "
                    f"{agent['health_score']:.1f} |"
                )
            lines.append("")
        
        # Summary Section
        if self.config.include_summary and "agent_details" in data:
            summary = data["agent_details"].get('summary', {})
            lines.append("## Summary")
            lines.append("")
            lines.append(f"- **Total Agents**: {summary.get('total_agents', 0)}")
            lines.append(f"- **Active Agents**: {summary.get('active_agents', 0)}")
            lines.append(f"- **Average Health**: {summary.get('average_health', 0):.1f}/100")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML format report"""
        html = []
        
        # HTML Header
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append(f"<title>{self.config.title}</title>")
        html.append("<style>")
        html.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html.append("h1 { color: #333; }")
        html.append("h2 { color: #666; border-bottom: 2px solid #ccc; padding-bottom: 5px; }")
        html.append("table { border-collapse: collapse; width: 100%; }")
        html.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
        html.append("th { background-color: #4CAF50; color: white; }")
        html.append(".alert { background-color: #ffebee; padding: 10px; margin: 5px 0; border-left: 4px solid #f44336; }")
        html.append(".good { color: green; }")
        html.append(".bad { color: red; }")
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        # Title
        html.append(f"<h1>{self.config.title}</h1>")
        
        # Timestamp
        if self.config.include_timestamp:
            html.append(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # System Health
        if "system_health" in data:
            health = data["system_health"]
            html.append("<h2>System Health</h2>")
            html.append("<ul>")
            html.append(f"<li><strong>Status:</strong> {health.get('overall_status', 'UNKNOWN')}</li>")
            html.append(f"<li><strong>Health Score:</strong> {health.get('health_score', 0):.1f}/100</li>")
            html.append(f"<li><strong>Active Agents:</strong> {health.get('active_agents', 0)}/{health.get('total_agents', 0)}</li>")
            html.append("</ul>")
            
            # Alerts
            alerts = health.get('alerts', [])
            if alerts:
                html.append("<h3>Alerts</h3>")
                for alert in alerts:
                    html.append(f'<div class="alert">⚠️  {alert}</div>')
        
        # Agent Status Table
        if "agent_details" in data:
            agent_data = data["agent_details"]
            html.append("<h2>Agent Status</h2>")
            html.append("<table>")
            html.append("<tr><th>Agent</th><th>Status</th><th>Role</th><th>Tasks</th><th>Health</th></tr>")
            
            for agent in agent_data.get('agents', []):
                status_class = "good" if agent['status'] == 'ACTIVE' else "bad"
                html.append("<tr>")
                html.append(f"<td>{agent['agent_id']}</td>")
                html.append(f'<td class="{status_class}">{agent["status"]}</td>')
                html.append(f"<td>{agent['role']}</td>")
                html.append(f"<td>{agent['task_count']}</td>")
                html.append(f"<td>{agent['health_score']:.1f}</td>")
                html.append("</tr>")
            
            html.append("</table>")
        
        # Summary
        if self.config.include_summary and "agent_details" in data:
            summary = data["agent_details"].get('summary', {})
            html.append("<h2>Summary</h2>")
            html.append("<ul>")
            html.append(f"<li><strong>Total Agents:</strong> {summary.get('total_agents', 0)}</li>")
            html.append(f"<li><strong>Active Agents:</strong> {summary.get('active_agents', 0)}</li>")
            html.append(f"<li><strong>Average Health:</strong> {summary.get('average_health', 0):.1f}/100</li>")
            html.append("</ul>")
        
        # HTML Footer
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
    
    def generate_report(self, data: Dict[str, Any]) -> str:
        """Generate report in configured format"""
        if self.config.format == "json":
            return self.generate_json_report(data)
        elif self.config.format == "markdown":
            return self.generate_markdown_report(data)
        elif self.config.format == "html":
            return self.generate_html_report(data)
        else:
            raise ValueError(f"Unsupported format: {self.config.format}")
    
    def save_report(self, data: Dict[str, Any]) -> Path:
        """Generate and save report to file"""
        report_content = self.generate_report(data)
        
        output_path = Path(self.config.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Report saved: {output_path}")
        return output_path


class ReportService:
    """Main reporting service"""
    
    def __init__(self):
        """Initialize reporting service"""
        self.generators = {}
    
    def create_health_report(self, health_data: Dict[str, Any], format: str = "markdown") -> Path:
        """Create system health report"""
        config = ReportConfig(
            title="V2_SWARM System Health Report",
            format=format,
            output_path=f"reports/health_report.{format}"
        )
        
        generator = ReportGenerator(config)
        return generator.save_report(health_data)
    
    def create_agent_report(self, agent_data: Dict[str, Any], format: str = "markdown") -> Path:
        """Create agent status report"""
        config = ReportConfig(
            title="V2_SWARM Agent Status Report",
            format=format,
            output_path=f"reports/agent_report.{format}"
        )
        
        generator = ReportGenerator(config)
        return generator.save_report(agent_data)
    
    def create_full_report(self, health_data: Dict[str, Any], formats: List[str] = None) -> List[Path]:
        """Create full report in multiple formats"""
        if formats is None:
            formats = ["json", "markdown", "html"]
        
        reports = []
        for format in formats:
            try:
                report_path = self.create_health_report(health_data, format)
                reports.append(report_path)
            except Exception as e:
                logger.error(f"Error generating {format} report: {e}")
        
        return reports


def main():
    """Main execution function"""
    print("📊 REPORTING SYSTEM - V2_SWARM Report Generation")
    print("=" * 60)
    
    # Load health data
    health_report_path = Path("reports/health_report.json")
    if not health_report_path.exists():
        print("❌ No health data found. Run watchdog.py first.")
        return
    
    with open(health_report_path, 'r') as f:
        health_data = json.load(f)
    
    # Initialize reporting service
    report_service = ReportService()
    
    # Generate reports in all formats
    print("\n📝 Generating reports...")
    report_paths = report_service.create_full_report(health_data)
    
    print(f"\n✅ Reports generated ({len(report_paths)}):")
    for path in report_paths:
        print(f"  - {path}")
    
    print("\n📊 Reporting system complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

