#!/usr/bin/env python3
"""Core Status Manager orchestrating tracking and reporting."""

import logging
import threading
from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, List

from .agent_manager import AgentManager
from .config_manager import ConfigManager
from .status_manager_config import Alert, HealthCheck, StatusEvent
from .status_manager_tracker import StatusTrackerMixin
from .status_manager_reporter import StatusReporterMixin


class StatusManager(StatusTrackerMixin, StatusReporterMixin):
    """Manages real-time status monitoring, health checks, and alert systems."""

    def __init__(self, agent_manager: AgentManager, config_manager: ConfigManager):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.health_checks: Dict[str, HealthCheck] = {}
        self.alerts: Dict[str, Alert] = {}
        self.status_events: Dict[str, StatusEvent] = {}
        self.monitoring_thread = None
        self.health_check_thread = None
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.StatusManager")

        self.status_callbacks: Dict[str, List[Callable]] = defaultdict(list)

        self._start_monitoring_threads()

    def _start_monitoring_threads(self) -> None:
        """Start status monitoring and health check threads."""
        self.running = True
        self.monitoring_thread = threading.Thread(
            target=self._status_monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()
        self.health_check_thread = threading.Thread(
            target=self._health_check_loop, daemon=True
        )
        self.health_check_thread.start()
        self.logger.info("Status monitoring threads started")

    def shutdown(self) -> None:
        """Shutdown the status manager."""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5)


def run_smoke_test() -> bool:
    """Run basic functionality test for StatusManager."""
    print("🧪 Running StatusManager Smoke Test...")
    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir = Path(temp_dir) / "config"
            agent_dir.mkdir()
            config_dir.mkdir()

            test_agent_dir = agent_dir / "Agent-1"
            test_agent_dir.mkdir()

            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            status_manager = StatusManager(agent_manager, config_manager)

            summary = status_manager.get_status_summary()
            assert "total_agents" in summary
            health_status = status_manager.get_health_status("Agent-1")
            assert health_status is not None
            alerts = status_manager.get_active_alerts()
            assert isinstance(alerts, list)

            status_manager.shutdown()
            agent_manager.shutdown()
            config_manager.shutdown()

        print("✅ StatusManager Smoke Test PASSED")
        return True
    except Exception as e:  # pragma: no cover - diagnostic output
        print(f"❌ StatusManager Smoke Test FAILED: {e}")
        return False


def main() -> None:
    """CLI interface for StatusManager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Status Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--health", help="Get health status for agent")
    parser.add_argument("--alerts", action="store_true", help="Show active alerts")
    parser.add_argument("--summary", action="store_true", help="Show status summary")
    parser.add_argument("--acknowledge", help="Acknowledge alert by ID")
    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    config_manager = ConfigManager()
    agent_manager = AgentManager()
    status_manager = StatusManager(agent_manager, config_manager)

    if args.health:
        health_status = status_manager.get_health_status(args.health)
        if health_status:
            print(f"Health status for {args.health}: {health_status.value}")
        else:
            print(f"No health status found for {args.health}")
    elif args.alerts:
        alerts = status_manager.get_active_alerts()
        print("Active Alerts:")
        for alert in alerts:
            print(f"  {alert.alert_id}: {alert.level.value} - {alert.message}")
    elif args.summary:
        summary = status_manager.get_status_summary()
        print("Status Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    elif args.acknowledge:
        success = status_manager.acknowledge_alert(args.acknowledge)
        print(f"Alert acknowledgment: {'✅ Success' if success else '❌ Failed'}")
    else:
        parser.print_help()

    status_manager.shutdown()
    agent_manager.shutdown()
    config_manager.shutdown()


__all__ = ["StatusManager", "run_smoke_test", "main"]
