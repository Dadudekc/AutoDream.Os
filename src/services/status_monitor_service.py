#!/usr/bin/env python3
"""
Status Monitor Service - Agent Cellphone V2
==========================================

Agent status tracking and performance monitoring service.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse


@dataclass
class AgentMetrics:
    """Agent performance metrics data structure."""

    agent_id: str
    status: str
    last_activity: Optional[datetime]
    coordination_count: int
    error_count: int
    success_rate: float
    response_time_avg: float
    tasks_completed: int
    tasks_failed: int


@dataclass
class SystemHealth:
    """System health data structure."""

    total_agents: int
    active_agents: int
    system_status: str
    overall_health_score: float
    critical_issues: int
    warnings: int
    last_health_check: datetime


class StatusMonitorService:
    """
    Status Monitor Service - Single responsibility: Agent status tracking and performance monitoring.

    This service manages:
    - Agent status monitoring and tracking
    - Performance metrics collection
    - System health assessment
    - Status reporting and alerts
    """

    def __init__(self, monitoring_dir: str = "agent_workspaces/monitoring"):
        """Initialize Status Monitor Service."""
        self.monitoring_dir = Path(monitoring_dir)
        self.monitoring_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logging()
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.system_health = self._initialize_system_health()

        # Initialize agent metrics
        self._initialize_agent_metrics()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("StatusMonitorService")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_system_health(self) -> SystemHealth:
        """Initialize system health."""
        return SystemHealth(
            total_agents=5,
            active_agents=0,
            system_status="initializing",
            overall_health_score=100.0,
            critical_issues=0,
            warnings=0,
            last_health_check=datetime.now(),
        )

    def _initialize_agent_metrics(self):
        """Initialize metrics for all agents."""
        agent_ids = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]

        for agent_id in agent_ids:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                status="standby",
                last_activity=None,
                coordination_count=0,
                error_count=0,
                success_rate=100.0,
                response_time_avg=0.0,
                tasks_completed=0,
                tasks_failed=0,
            )

    def update_agent_status(
        self, agent_id: str, status: str, activity_type: str = "coordination"
    ):
        """Update agent status and activity."""
        try:
            if agent_id not in self.agent_metrics:
                self.logger.error(f"Agent {agent_id} not found in metrics")
                return

            metrics = self.agent_metrics[agent_id]
            metrics.status = status
            metrics.last_activity = datetime.now()

            if activity_type == "coordination":
                metrics.coordination_count += 1
            elif activity_type == "task_completion":
                metrics.tasks_completed += 1
            elif activity_type == "task_failure":
                metrics.tasks_failed += 1

            # Update success rate
            total_tasks = metrics.tasks_completed + metrics.tasks_failed
            if total_tasks > 0:
                metrics.success_rate = (metrics.tasks_completed / total_tasks) * 100

            self.logger.info(f"Updated {agent_id} status: {status} ({activity_type})")

        except Exception as e:
            self.logger.error(f"Error updating agent status for {agent_id}: {e}")

    def record_agent_error(self, agent_id: str, error_message: str):
        """Record an error for a specific agent."""
        try:
            if agent_id not in self.agent_metrics:
                self.logger.error(f"Agent {agent_id} not found in metrics")
                return

            metrics = self.agent_metrics[agent_id]
            metrics.error_count += 1

            # Log error details
            error_log_file = self.monitoring_dir / f"{agent_id}_errors.log"
            with open(error_log_file, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] {error_message}\n")

            self.logger.warning(f"Recorded error for {agent_id}: {error_message}")

        except Exception as e:
            self.logger.error(f"Error recording error for {agent_id}: {e}")

    def record_agent_response_time(self, agent_id: str, response_time: float):
        """Record response time for a specific agent."""
        try:
            if agent_id not in self.agent_metrics:
                self.logger.error(f"Agent {agent_id} not found in metrics")
                return

            metrics = self.agent_metrics[agent_id]

            # Update average response time
            if metrics.response_time_avg == 0.0:
                metrics.response_time_avg = response_time
            else:
                metrics.response_time_avg = (
                    metrics.response_time_avg + response_time
                ) / 2

            self.logger.debug(f"Updated response time for {agent_id}: {response_time}s")

        except Exception as e:
            self.logger.error(f"Error recording response time for {agent_id}: {e}")

    def assess_system_health(self) -> SystemHealth:
        """Assess overall system health."""
        try:
            active_agents = sum(
                1
                for metrics in self.agent_metrics.values()
                if metrics.status == "active"
            )
            total_errors = sum(
                metrics.error_count for metrics in self.agent_metrics.values()
            )
            total_warnings = sum(
                1
                for metrics in self.agent_metrics.values()
                if metrics.success_rate < 90.0
            )

            # Calculate health score
            health_score = 100.0
            if total_errors > 0:
                health_score -= total_errors * 10  # -10 points per error
            if total_warnings > 0:
                health_score -= total_warnings * 5  # -5 points per warning
            if active_agents < 2:
                health_score -= 20  # -20 points if less than 2 agents active

            health_score = max(0.0, health_score)

            # Determine system status
            if health_score >= 90:
                system_status = "healthy"
            elif health_score >= 70:
                system_status = "warning"
            elif health_score >= 50:
                system_status = "critical"
            else:
                system_status = "failing"

            # Update system health
            self.system_health.active_agents = active_agents
            self.system_health.system_status = system_status
            self.system_health.overall_health_score = health_score
            self.system_health.critical_issues = total_errors
            self.system_health.warnings = total_warnings
            self.system_health.last_health_check = datetime.now()

            self.logger.info(
                f"System health assessed: {system_status} (score: {health_score:.1f})"
            )
            return self.system_health

        except Exception as e:
            self.logger.error(f"Error assessing system health: {e}")
            return self.system_health

    def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific agent."""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return None

        return {
            "agent_id": metrics.agent_id,
            "status": metrics.status,
            "last_activity": metrics.last_activity.isoformat()
            if metrics.last_activity
            else None,
            "coordination_count": metrics.coordination_count,
            "error_count": metrics.error_count,
            "success_rate": metrics.success_rate,
            "response_time_avg": metrics.response_time_avg,
            "tasks_completed": metrics.tasks_completed,
            "tasks_failed": metrics.tasks_failed,
        }

    def get_system_summary(self) -> Dict[str, Any]:
        """Get system monitoring summary."""
        health = self.assess_system_health()

        # Get agent status summary
        agent_status_summary = {}
        for agent_id, metrics in self.agent_metrics.items():
            agent_status_summary[agent_id] = {
                "status": metrics.status,
                "success_rate": metrics.success_rate,
                "error_count": metrics.error_count,
                "last_activity": metrics.last_activity.isoformat()
                if metrics.last_activity
                else None,
            }

        return {
            "system_health": {
                "status": health.system_status,
                "health_score": health.overall_health_score,
                "active_agents": health.active_agents,
                "total_agents": health.total_agents,
                "critical_issues": health.critical_issues,
                "warnings": health.warnings,
                "last_health_check": health.last_health_check.isoformat(),
            },
            "agent_status": agent_status_summary,
            "overall_metrics": {
                "total_coordinations": sum(
                    m.coordination_count for m in self.agent_metrics.values()
                ),
                "total_errors": sum(m.error_count for m in self.agent_metrics.values()),
                "total_tasks": sum(
                    m.tasks_completed + m.tasks_failed
                    for m in self.agent_metrics.values()
                ),
                "average_success_rate": sum(
                    m.success_rate for m in self.agent_metrics.values()
                )
                / len(self.agent_metrics),
            },
        }

    def generate_health_report(self) -> str:
        """Generate a human-readable health report."""
        try:
            summary = self.get_system_summary()

            report = f"""
📊 AGENT CELLPHONE V2 SYSTEM HEALTH REPORT
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
                status_emoji = (
                    "🟢"
                    if status["status"] == "active"
                    else "🟡"
                    if status["status"] == "standby"
                    else "🔴"
                )
                report += f"  {status_emoji} {agent_id}: {status['status']} (Success: {status['success_rate']:.1f}%, Errors: {status['error_count']})\n"

            report += f"""
📈 OVERALL METRICS
  Total Coordinations: {summary['overall_metrics']['total_coordinations']}
  Total Errors: {summary['overall_metrics']['total_errors']}
  Total Tasks: {summary['overall_metrics']['total_tasks']}
  Average Success Rate: {summary['overall_metrics']['average_success_rate']:.1f}%

{'=' * 60}
"""

            return report.strip()

        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return f"Error generating health report: {e}"


def main():
    """CLI interface for Status Monitor Service."""
    parser = argparse.ArgumentParser(description="Status Monitor Service CLI")
    parser.add_argument("--status", type=str, help="Show status for specific agent")
    parser.add_argument(
        "--update",
        type=str,
        help="Update agent status (format: agent_id:status:activity_type)",
    )
    parser.add_argument(
        "--error", type=str, help="Record agent error (format: agent_id:error_message)"
    )
    parser.add_argument(
        "--response-time",
        type=str,
        help="Record response time (format: agent_id:time_seconds)",
    )
    parser.add_argument("--health", action="store_true", help="Assess system health")
    parser.add_argument("--summary", action="store_true", help="Show system summary")
    parser.add_argument("--report", action="store_true", help="Generate health report")

    args = parser.parse_args()

    # Initialize service
    monitor_service = StatusMonitorService()

    if args.status:
        metrics = monitor_service.get_agent_metrics(args.status)
        if metrics:
            print(f"📊 Metrics for {args.status}:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Agent {args.status} not found")

    elif args.update:
        try:
            agent_id, status, activity_type = args.update.split(":", 2)
            monitor_service.update_agent_status(agent_id, status, activity_type)
            print(f"✅ Updated {agent_id} status: {status}")
        except ValueError:
            print("❌ Invalid format. Use: agent_id:status:activity_type")

    elif args.error:
        try:
            agent_id, error_message = args.error.split(":", 1)
            monitor_service.record_agent_error(agent_id, error_message)
            print(f"✅ Recorded error for {agent_id}")
        except ValueError:
            print("❌ Invalid format. Use: agent_id:error_message")

    elif args.response_time:
        try:
            agent_id, time_str = args.response_time.split(":", 1)
            response_time = float(time_str)
            monitor_service.record_agent_response_time(agent_id, response_time)
            print(f"✅ Recorded response time for {agent_id}: {response_time}s")
        except ValueError:
            print("❌ Invalid format. Use: agent_id:time_seconds")

    elif args.health:
        health = monitor_service.assess_system_health()
        print("🏥 System Health Assessment:")
        print(f"  Status: {health.system_status}")
        print(f"  Health Score: {health.overall_health_score:.1f}/100")
        print(f"  Active Agents: {health.active_agents}/{health.total_agents}")
        print(f"  Critical Issues: {health.critical_issues}")
        print(f"  Warnings: {health.warnings}")

    elif args.summary:
        summary = monitor_service.get_system_summary()
        print("📊 System Monitoring Summary:")
        print(f"  System Status: {summary['system_health']['status']}")
        print(f"  Health Score: {summary['system_health']['health_score']:.1f}")
        print(f"  Active Agents: {summary['system_health']['active_agents']}")
        print(
            f"  Total Coordinations: {summary['overall_metrics']['total_coordinations']}"
        )
        print(f"  Total Errors: {summary['overall_metrics']['total_errors']}")

    elif args.report:
        report = monitor_service.generate_health_report()
        print(report)

    else:
        print("📊 Status Monitor Service - Use --help for available commands")


if __name__ == "__main__":
    main()
