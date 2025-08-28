"""Visualization utilities for the status monitor service."""

from datetime import datetime
from typing import Any, Dict

from .constants import STATUS_EMOJIS


def generate_health_report(summary: Dict[str, Any]) -> str:
    """Generate a human-readable health report from the summary."""
    report = f"""📊 AGENT CELLPHONE V2 SYSTEM HEALTH REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

🏥 SYSTEM HEALTH STATUS
  Status: {summary['system_health']['status'].upper()}
  Health Score: {summary['system_health']['health_score']:.1f}/100
  Active Agents: {summary['system_health']['active_agents']}/{summary['system_health']['total_agents']}
  Critical Issues: {summary['system_health']['critical_issues']}
  Warnings: {summary['system_health']['warnings']}

🤖 AGENT STATUS SUMMARY
"""
    for agent_id, status in summary["agent_status"].items():
        status_emoji = STATUS_EMOJIS.get(status["status"], "🔴")
        report += (
            f"  {status_emoji} {agent_id}: {status['status']} (Success: {status['success_rate']:.1f}%, "
            f"Errors: {status['error_count']})\n"
        )

    report += f"""📈 OVERALL METRICS
  Total Coordinations: {summary['overall_metrics']['total_coordinations']}
  Total Errors: {summary['overall_metrics']['total_errors']}
  Total Tasks: {summary['overall_metrics']['total_tasks']}
  Average Success Rate: {summary['overall_metrics']['average_success_rate']:.1f}%

{'=' * 60}"""
    return report.strip()
