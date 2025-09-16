#!/usr/bin/env python3
"""
Metrics Collector - System and Swarm Metrics Collection
======================================================

Collects system and swarm metrics for the monitoring dashboard.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from .models import AgentStatus, SwarmMetrics, SystemMetrics

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects system and swarm metrics."""

    def __init__(self):
        """Initialize the metrics collector."""
        self.agent_workspaces = Path("agent_workspaces")
        self.coordinates_file = Path("cursor_agent_coords.json")

    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        if not PSUTIL_AVAILABLE:
            return SystemMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={"bytes_sent": 0, "bytes_recv": 0},
                timestamp=datetime.now(),
            )

        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            network = psutil.net_io_counters()

            return SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_io={"bytes_sent": network.bytes_sent, "bytes_recv": network.bytes_recv},
                timestamp=datetime.now(),
            )
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={"bytes_sent": 0, "bytes_recv": 0},
                timestamp=datetime.now(),
            )

    def get_agent_statuses(self) -> list[AgentStatus]:
        """Get status of all agents."""
        agents = []

        if not self.agent_workspaces.exists():
            return agents

        try:
            # Load coordinates
            coordinates = {}
            if self.coordinates_file.exists():
                with open(self.coordinates_file) as f:
                    coord_data = json.load(f)
                    coordinates = coord_data.get("agents", {})

            # Check each agent workspace
            for agent_dir in self.agent_workspaces.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name
                    status_file = agent_dir / "status.json"

                    status = "unknown"
                    last_activity = datetime.now()
                    performance_metrics = {}

                    if status_file.exists():
                        try:
                            with open(status_file) as f:
                                status_data = json.load(f)
                                status = status_data.get("status", "unknown")
                                last_activity_str = status_data.get("last_updated", "")
                                if last_activity_str:
                                    last_activity = datetime.fromisoformat(
                                        last_activity_str.replace("Z", "+00:00")
                                    )
                                performance_metrics = status_data.get("performance_metrics", {})
                        except Exception as e:
                            logger.error(f"Error reading status for {agent_id}: {e}")

                    agent_coords = coordinates.get(agent_id, {})

                    agents.append(
                        AgentStatus(
                            agent_id=agent_id,
                            status=status,
                            last_activity=last_activity,
                            coordinates=agent_coords,
                            performance_metrics=performance_metrics,
                        )
                    )

        except Exception as e:
            logger.error(f"Error collecting agent statuses: {e}")

        return agents

    def get_swarm_metrics(self) -> SwarmMetrics:
        """Get swarm-level metrics."""
        agents = self.get_agent_statuses()
        active_agents = len(
            [a for a in agents if a.status in ["active", "operational", "onboarded"]]
        )

        # Calculate coordination efficiency (simplified)
        total_agents = len(agents)
        coordination_efficiency = (active_agents / total_agents * 100) if total_agents > 0 else 0

        # Determine system health
        if coordination_efficiency >= 90:
            system_health = "excellent"
        elif coordination_efficiency >= 75:
            system_health = "good"
        elif coordination_efficiency >= 50:
            system_health = "fair"
        else:
            system_health = "poor"

        return SwarmMetrics(
            total_agents=total_agents,
            active_agents=active_agents,
            total_messages=0,  # Would need to track from messaging system
            coordination_efficiency=coordination_efficiency,
            system_health=system_health,
            timestamp=datetime.now(),
        )

