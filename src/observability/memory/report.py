"""
Memory Reporting System - V2_SWARM
==================================

Comprehensive memory reporting and analysis.
Generates reports for monitoring and CI/CD integration.

Author: Agent-5 (Coordinator)
License: MIT
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MemoryReport:
    """Comprehensive memory report"""
    
    timestamp: float
    report_type: str  # summary, detailed, alert, trend
    services: Dict[str, Any]
    global_stats: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    recommendations: List[str]


class ReportGenerator:
    """Generate memory reports"""
    
    def __init__(self):
        """Initialize report generator"""
        self.reports = []
    
    def generate_summary_report(self, watchdog_data: Dict[str, Any]) -> MemoryReport:
        """Generate summary report"""
        import time
        
        snapshot = watchdog_data.get('snapshot', {})
        budget_checks = watchdog_data.get('budget_checks', {})
        alerts = watchdog_data.get('alerts', [])
        
        # Calculate global stats
        global_stats = {
            'current_mb': snapshot.get('current_mb', 0),
            'peak_mb': snapshot.get('peak_mb', 0),
            'object_count': snapshot.get('object_count', 0),
            'services_ok': sum(1 for svc in budget_checks.values() if svc.get('status') == 'ok'),
            'services_warning': sum(1 for svc in budget_checks.values() if svc.get('status') == 'warning'),
            'services_critical': sum(1 for svc in budget_checks.values() if svc.get('status') == 'critical')
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(global_stats, budget_checks, alerts)
        
        report = MemoryReport(
            timestamp=time.time(),
            report_type='summary',
            services=budget_checks,
            global_stats=global_stats,
            alerts=alerts,
            recommendations=recommendations
        )
        
        self.reports.append(report)
        return report
    
    def _generate_recommendations(self, global_stats: Dict, budget_checks: Dict,
                                 alerts: List) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if global_stats['services_critical'] > 0:
            recommendations.append("CRITICAL: Immediate action required for services exceeding budget")
        
        if global_stats['services_warning'] > 0:
            recommendations.append("WARNING: Monitor services approaching budget limits")
        
        if len(alerts) > 5:
            recommendations.append("HIGH: Multiple alerts detected - investigate memory patterns")
        
        if not recommendations:
            recommendations.append("GOOD: All services within budget")
        
        return recommendations
    
    def save_report(self, report: MemoryReport, output_path: str) -> bool:
        """Save report to file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(asdict(report), f, indent=2)
            
            logger.info(f"Report saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False


class ReportFormatter:
    """Format reports for different outputs"""
    
    @staticmethod
    def format_text(report: MemoryReport) -> str:
        """Format report as text"""
        lines = [
            "=" * 60,
            "MEMORY REPORT",
            "=" * 60,
            f"Type: {report.report_type}",
            f"Timestamp: {datetime.fromtimestamp(report.timestamp)}",
            "",
            "GLOBAL STATISTICS:",
            f"  Current Memory: {report.global_stats['current_mb']:.2f} MB",
            f"  Peak Memory: {report.global_stats['peak_mb']:.2f} MB",
            f"  Object Count: {report.global_stats['object_count']:,}",
            "",
            "SERVICE STATUS:",
            f"  OK: {report.global_stats['services_ok']}",
            f"  Warning: {report.global_stats['services_warning']}",
            f"  Critical: {report.global_stats['services_critical']}",
            "",
            "RECOMMENDATIONS:",
        ]
        
        for rec in report.recommendations:
            lines.append(f"  • {rec}")
        
        if report.alerts:
            lines.append("")
            lines.append("RECENT ALERTS:")
            for alert in report.alerts[:5]:
                lines.append(f"  • {alert['service']}: {alert['type']} - {alert['memory_mb']:.2f} MB")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    @staticmethod
    def format_markdown(report: MemoryReport) -> str:
        """Format report as markdown"""
        lines = [
            "# Memory Report",
            "",
            f"**Type**: {report.report_type}  ",
            f"**Timestamp**: {datetime.fromtimestamp(report.timestamp)}  ",
            "",
            "## Global Statistics",
            "",
            f"- **Current Memory**: {report.global_stats['current_mb']:.2f} MB",
            f"- **Peak Memory**: {report.global_stats['peak_mb']:.2f} MB",
            f"- **Object Count**: {report.global_stats['object_count']:,}",
            "",
            "## Service Status",
            "",
            f"- ✅ OK: {report.global_stats['services_ok']}",
            f"- ⚠️ Warning: {report.global_stats['services_warning']}",
            f"- 🚨 Critical: {report.global_stats['services_critical']}",
            "",
            "## Recommendations",
            "",
        ]
        
        for rec in report.recommendations:
            lines.append(f"- {rec}")
        
        if report.alerts:
            lines.append("")
            lines.append("## Recent Alerts")
            lines.append("")
            for alert in report.alerts[:5]:
                lines.append(f"- **{alert['service']}**: {alert['type']} - {alert['memory_mb']:.2f} MB")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_html(report: MemoryReport) -> str:
        """Format report as HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Memory Report - {datetime.fromtimestamp(report.timestamp)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .stats {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .ok {{ color: green; }}
        .warning {{ color: orange; }}
        .critical {{ color: red; }}
    </style>
</head>
<body>
    <h1>Memory Report</h1>
    <p><strong>Type:</strong> {report.report_type}</p>
    <p><strong>Timestamp:</strong> {datetime.fromtimestamp(report.timestamp)}</p>
    
    <h2>Global Statistics</h2>
    <div class="stats">
        <p>Current Memory: {report.global_stats['current_mb']:.2f} MB</p>
        <p>Peak Memory: {report.global_stats['peak_mb']:.2f} MB</p>
        <p>Object Count: {report.global_stats['object_count']:,}</p>
    </div>
    
    <h2>Service Status</h2>
    <ul>
        <li class="ok">OK: {report.global_stats['services_ok']}</li>
        <li class="warning">Warning: {report.global_stats['services_warning']}</li>
        <li class="critical">Critical: {report.global_stats['services_critical']}</li>
    </ul>
    
    <h2>Recommendations</h2>
    <ul>
"""
        for rec in report.recommendations:
            html += f"        <li>{rec}</li>\n"
        
        html += """    </ul>
</body>
</html>
"""
        return html


class PerformanceReporter:
    """Report on performance metrics"""
    
    def __init__(self, ledger_manager):
        """Initialize performance reporter"""
        self.ledger_manager = ledger_manager
    
    def generate_service_report(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Generate performance report for service"""
        analysis = self.ledger_manager.get_service_analysis(service_name)
        
        if not analysis or not analysis.get('summary'):
            return None
        
        summary = analysis['summary']
        growth = analysis.get('growth_analysis')
        
        return {
            'service': service_name,
            'memory_stats': summary['memory_stats'],
            'object_stats': summary['object_stats'],
            'time_range': summary['time_range'],
            'growth_analysis': growth,
            'health_status': self._assess_health(summary, growth)
        }
    
    def _assess_health(self, summary: Dict, growth: Optional[Dict]) -> str:
        """Assess service health"""
        if not growth:
            return "insufficient_data"
        
        growth_rate = growth.get('growth_rate_mb_per_hour', 0)
        
        if growth_rate > 10:
            return "unhealthy"
        elif growth_rate > 5:
            return "concerning"
        elif growth_rate > 1:
            return "watch"
        else:
            return "healthy"

