#!/usr/bin/env python3
"""Process management module for system operations."""

import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .manager_utils import current_timestamp
from .user_manager import UserManager, AgentStatus
from .resource_manager import ResourceManager


class ProcessManager:
    """Handle system-level operations and monitoring."""

    def __init__(self, users: UserManager, resources: ResourceManager) -> None:
        self.logger = logging.getLogger(__name__ + ".ProcessManager")
        self.users = users
        self.resources = resources
        self.system_status = "operational"
        self.startup_time = datetime.now()

    # ------------------------------------------------------------------
    # System status and health
    # ------------------------------------------------------------------
    def get_system_status(self, metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return a snapshot of current system status."""
        status = {
            "system_status": self.system_status,
            "startup_time": self.startup_time.isoformat(),
            "uptime": (datetime.now() - self.startup_time).total_seconds(),
            "total_agents": len(self.users.agents),
            "active_agents": len([a for a in self.users.agents.values() if a.status == AgentStatus.ONLINE]),
            "total_workspaces": len(self.resources.workspaces),
            "active_workspaces": len([w for w in self.resources.workspaces.values() if w.status == "active"]),
        }
        if metrics is not None:
            status["manager_metrics"] = metrics
        return status

    def perform_system_health_check(self) -> Dict[str, Any]:
        """Evaluate basic system health metrics."""
        health = {"timestamp": current_timestamp(), "overall_health": "healthy", "issues": []}

        offline_agents = [a for a in self.users.agents.values() if a.status == AgentStatus.OFFLINE]
        if offline_agents:
            health["issues"].append(f"{len(offline_agents)} agents offline")

        inactive_workspaces = [w for w in self.resources.workspaces.values() if w.status != "active"]
        if inactive_workspaces:
            health["issues"].append(f"{len(inactive_workspaces)} inactive workspaces")

        if health["issues"]:
            health["overall_health"] = "degraded"
        return health

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def backup_system_data(self, backup_dir: str = "backups") -> bool:
        """Persist a backup of current system data to disk."""
        try:
            path = Path(backup_dir)
            path.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file = path / f"system_backup_{timestamp}.json"
            data = {
                "timestamp": timestamp,
                "agents": {aid: asdict(agent) for aid, agent in self.users.agents.items()},
                "workspaces": {wid: asdict(ws) for wid, ws in self.resources.workspaces.items()},
                "system_status": self.get_system_status(),
            }
            with open(file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to backup system data: %s", exc)
            return False
