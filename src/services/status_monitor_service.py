#!/usr/bin/env python3
"""
Status Monitor Service - Agent Cellphone V2
==========================================

Agent status tracking and performance monitoring service.
Follows V2 standards: \u2264 200 LOC, SRP, OOP design, CLI interface.
"""

import argparse
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from src.services.status_monitor.calculations import (
    SystemHealth,
    assess_system_health,
    get_system_summary,
)
from src.services.status_monitor.constants import DEFAULT_AGENT_IDS
from src.services.status_monitor.metrics import MetricsCollector
from src.services.status_monitor.visualization import generate_health_report


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
        self.collector = MetricsCollector()
        self.system_health = SystemHealth(total_agents=len(DEFAULT_AGENT_IDS))

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

    def update_agent_status(
        self, agent_id: str, status: str, activity_type: str = "coordination"
    ) -> None:
        """Update agent status and activity."""
        try:
            self.collector.update_agent_status(agent_id, status, activity_type)
            self.logger.info(f"Updated {agent_id} status: {status} ({activity_type})")
        except Exception as e:
            self.logger.error(f"Error updating agent status for {agent_id}: {e}")

    def record_agent_error(self, agent_id: str, error_message: str) -> None:
        """Record an error for a specific agent."""
        try:
            self.collector.record_agent_error(
                agent_id, error_message, self.monitoring_dir
            )
            self.logger.warning(f"Recorded error for {agent_id}: {error_message}")
        except Exception as e:
            self.logger.error(f"Error recording error for {agent_id}: {e}")

    def record_agent_response_time(self, agent_id: str, response_time: float) -> None:
        """Record response time for a specific agent."""
        try:
            self.collector.record_agent_response_time(agent_id, response_time)
            self.logger.debug(f"Updated response time for {agent_id}: {response_time}s")
        except Exception as e:
            self.logger.error(f"Error recording response time for {agent_id}: {e}")

    def assess_system_health(self) -> SystemHealth:
        """Assess overall system health."""
        try:
            self.system_health = assess_system_health(
                self.collector.agent_metrics.values(), self.system_health
            )
            self.logger.info(
                f"System health assessed: {self.system_health.system_status} "
                f"(score: {self.system_health.overall_health_score:.1f})"
            )
            return self.system_health
        except Exception as e:
            self.logger.error(f"Error assessing system health: {e}")
            return self.system_health

    def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific agent."""
        return self.collector.get_agent_metrics(agent_id)

    def get_system_summary(self) -> Dict[str, Any]:
        """Get system monitoring summary."""
        health = self.assess_system_health()
        return get_system_summary(self.collector.agent_metrics, health)

    def generate_health_report(self) -> str:
        """Generate a human-readable health report."""
        try:
            summary = self.get_system_summary()
            return generate_health_report(summary)
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return f"Error generating health report: {e}"


def main() -> None:
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
