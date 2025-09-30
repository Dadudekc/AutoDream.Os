#!/usr/bin/env python3
"""
Operational Dashboard Tool Main
===============================

Main operational dashboard class and CLI interface.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .operational_dashboard_tool_core import (
    AlertLevel,
    MetricType,
    OperationalAlert,
)
from .operational_dashboard_tool_utils import (
    calculate_quality_score,
    count_completed_tasks,
    count_total_tasks,
    extract_metric,
    generate_recommendations,
    load_agent_performance_data,
    load_project_progress_data,
    load_quality_gate_data,
    load_v3_coordination_data,
)

logger = logging.getLogger(__name__)


class OperationalDashboard:
    """Operational Dashboard for Team Alpha coordination."""

    def __init__(self):
        """Initialize operational dashboard."""
        self.project_root = Path.cwd()
        self.alerts: list[OperationalAlert] = []

    def generate_operational_report(self) -> dict[str, Any]:
        """Generate comprehensive operational report."""
        logger.info("Generating operational report...")

        # Load all data sources
        v3_data = load_v3_coordination_data()
        quality_data = load_quality_gate_data()
        agent_performance = load_agent_performance_data()
        project_progress = load_project_progress_data()

        # Calculate metrics
        total_tasks = count_total_tasks()
        completed_tasks = count_completed_tasks()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Generate recommendations
        recommendations = generate_recommendations(
            quality_data.quality_score,
            quality_data.violations,
            quality_data.critical_issues,
            agent_performance,
        )

        # Compile report
        report = {
            "timestamp": datetime.now().isoformat(),
            "v3_coordination": v3_data,
            "quality_gates": {
                "total_files": quality_data.total_files,
                "compliant_files": quality_data.compliant_files,
                "violations": quality_data.violations,
                "quality_score": quality_data.quality_score,
                "critical_issues": quality_data.critical_issues,
                "recommendations": quality_data.recommendations,
            },
            "agent_performance": [
                {
                    "agent_id": agent.agent_id,
                    "tasks_completed": agent.tasks_completed,
                    "tasks_failed": agent.tasks_failed,
                    "average_cycle_time": agent.average_cycle_time,
                    "quality_score": agent.quality_score,
                    "last_active": agent.last_active,
                    "current_status": agent.current_status,
                }
                for agent in agent_performance
            ],
            "project_progress": [
                {
                    "project_name": project.project_name,
                    "completion_percentage": project.completion_percentage,
                    "tasks_completed": project.tasks_completed,
                    "tasks_total": project.tasks_total,
                    "last_update": project.last_update,
                    "status": project.status,
                }
                for project in project_progress
            ],
            "operational_metrics": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": completion_rate,
                "active_agents": len([agent for agent in agent_performance if agent.current_status == "active"]),
                "inactive_agents": len([agent for agent in agent_performance if agent.current_status == "inactive"]),
            },
            "recommendations": recommendations,
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp,
                    "agent_id": alert.agent_id,
                    "project_name": alert.project_name,
                    "resolved": alert.resolved,
                }
                for alert in self.alerts
            ],
        }

        logger.info("Operational report generated successfully")
        return report

    def create_operational_alert(
        self,
        level: AlertLevel,
        message: str,
        agent_id: str | None = None,
        project_name: str | None = None,
    ) -> OperationalAlert:
        """Create a new operational alert."""
        alert = OperationalAlert(
            alert_id=f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            level=level,
            message=message,
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
            project_name=project_name,
            resolved=False,
        )
        
        self.alerts.append(alert)
        logger.info(f"Created {level.value} alert: {message}")
        return alert

    def generate_dashboard_html(self) -> str:
        """Generate HTML dashboard."""
        report = self.generate_operational_report()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V2_SWARM Operational Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #ecf0f1; border-radius: 5px; text-align: center; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .metric-label {{ font-size: 14px; color: #7f8c8d; }}
        .alert {{ padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .alert-info {{ background-color: #d1ecf1; border-left: 4px solid #17a2b8; }}
        .alert-warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; }}
        .alert-error {{ background-color: #f8d7da; border-left: 4px solid #dc3545; }}
        .alert-critical {{ background-color: #f5c6cb; border-left: 4px solid #721c24; }}
        .agent-status {{ display: inline-block; padding: 5px 10px; border-radius: 15px; font-size: 12px; }}
        .status-active {{ background-color: #d4edda; color: #155724; }}
        .status-inactive {{ background-color: #f8d7da; color: #721c24; }}
        .progress-bar {{ width: 100%; background-color: #e9ecef; border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 20px; background-color: #28a745; transition: width 0.3s ease; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>V2_SWARM Operational Dashboard</h1>
            <p>Last Updated: {report['timestamp']}</p>
        </div>

        <div class="section">
            <h2>Operational Metrics</h2>
            <div class="metric">
                <div class="metric-value">{report['operational_metrics']['total_tasks']}</div>
                <div class="metric-label">Total Tasks</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['operational_metrics']['completed_tasks']}</div>
                <div class="metric-label">Completed Tasks</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['operational_metrics']['completion_rate']:.1f}%</div>
                <div class="metric-label">Completion Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['operational_metrics']['active_agents']}</div>
                <div class="metric-label">Active Agents</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['operational_metrics']['inactive_agents']}</div>
                <div class="metric-label">Inactive Agents</div>
            </div>
        </div>

        <div class="section">
            <h2>Quality Gates</h2>
            <div class="metric">
                <div class="metric-value">{report['quality_gates']['total_files']}</div>
                <div class="metric-label">Total Files</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['quality_gates']['compliant_files']}</div>
                <div class="metric-label">Compliant Files</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['quality_gates']['violations']}</div>
                <div class="metric-label">Violations</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report['quality_gates']['quality_score']:.1f}</div>
                <div class="metric-label">Quality Score</div>
            </div>
        </div>

        <div class="section">
            <h2>Agent Performance</h2>
            {"".join([
                f"""
                <div style="margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                    <h3>{agent['agent_id']}</h3>
                    <p>Tasks Completed: {agent['tasks_completed']} | Failed: {agent['tasks_failed']}</p>
                    <p>Quality Score: {agent['quality_score']:.1f} | Cycle Time: {agent['average_cycle_time']:.1f}s</p>
                    <p>Last Active: {agent['last_active']}</p>
                    <span class="agent-status status-{agent['current_status']}">{agent['current_status'].upper()}</span>
                </div>
                """
                for agent in report['agent_performance']
            ])}
        </div>

        <div class="section">
            <h2>Project Progress</h2>
            {"".join([
                f"""
                <div style="margin: 10px 0;">
                    <h3>{project['project_name']}</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {project['completion_percentage']:.1f}%"></div>
                    </div>
                    <p>{project['tasks_completed']}/{project['tasks_total']} tasks completed ({project['completion_percentage']:.1f}%)</p>
                    <p>Status: {project['status']} | Last Update: {project['last_update']}</p>
                </div>
                """
                for project in report['project_progress']
            ])}
        </div>

        <div class="section">
            <h2>Recommendations</h2>
            <ul>
                {"".join([f"<li>{rec}</li>" for rec in report['recommendations']])}
            </ul>
        </div>

        <div class="section">
            <h2>Alerts</h2>
            {"".join([
                f"""
                <div class="alert alert-{alert['level']}">
                    <strong>{alert['level'].upper()}</strong>: {alert['message']}
                    <br><small>Agent: {alert['agent_id'] or 'N/A'} | Project: {alert['project_name'] or 'N/A'} | {alert['timestamp']}</small>
                </div>
                """
                for alert in report['alerts']
            ])}
        </div>
    </div>
</body>
</html>
        """
        
        return html


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Operational Dashboard & Analytics Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python operational_dashboard_tool.py --report
  python operational_dashboard_tool.py --html --output dashboard.html
  python operational_dashboard_tool.py --alert --level warning --message "High CPU usage"
        """,
    )

    parser.add_argument("--report", action="store_true", help="Generate operational report")
    parser.add_argument("--html", action="store_true", help="Generate HTML dashboard")
    parser.add_argument("--output", help="Output file for report/dashboard")
    parser.add_argument("--alert", action="store_true", help="Create operational alert")
    parser.add_argument("--level", choices=["info", "warning", "error", "critical"], help="Alert level")
    parser.add_argument("--message", help="Alert message")
    parser.add_argument("--agent", help="Agent ID for alert")
    parser.add_argument("--project", help="Project name for alert")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    try:
        dashboard = OperationalDashboard()

        if args.alert:
            if not args.level or not args.message:
                print("Error: --level and --message are required for alerts")
                return

            level = AlertLevel(args.level)
            alert = dashboard.create_operational_alert(
                level=level,
                message=args.message,
                agent_id=args.agent,
                project_name=args.project,
            )
            print(f"Alert created: {alert.alert_id}")

        elif args.html:
            html_content = dashboard.generate_dashboard_html()
            
            if args.output:
                with open(args.output, "w") as f:
                    f.write(html_content)
                print(f"HTML dashboard saved to {args.output}")
            else:
                print(html_content)

        else:  # Default to report
            report = dashboard.generate_operational_report()
            
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(report, f, indent=2)
                print(f"Operational report saved to {args.output}")
            else:
                print(json.dumps(report, indent=2))

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


# For direct execution
if __name__ == "__main__":
    main()
