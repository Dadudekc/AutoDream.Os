#!/usr/bin/env python3
"""
Monitor Health - Agent Cellphone V2
===================================

Health monitoring and diagnostics functionality.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from .monitor_types import AgentInfo, AgentStatus


class HealthMonitor:
    """
    Health monitoring and diagnostics for agents.

    Responsibilities:
    - Monitor system resources
    - Check agent health metrics
    - Provide health diagnostics
    - Alert on health issues
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.HealthMonitor")
        self.health_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 5.0,
        }
        self.health_history: List[Dict[str, Any]] = []

    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            health_data = {
                "timestamp": time.time(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "memory_available": memory.available,
                "disk_free": disk.free,
                "status": "healthy",
            }

            # Check thresholds
            if cpu_percent > self.health_thresholds["cpu_usage"]:
                health_data["status"] = "warning"
                health_data[
                    "cpu_warning"
                ] = f"CPU usage {cpu_percent}% exceeds threshold"

            if memory.percent > self.health_thresholds["memory_usage"]:
                health_data["status"] = "warning"
                health_data[
                    "memory_warning"
                ] = f"Memory usage {memory.percent}% exceeds threshold"

            if disk.percent > self.health_thresholds["disk_usage"]:
                health_data["status"] = "critical"
                health_data[
                    "disk_warning"
                ] = f"Disk usage {disk.percent}% exceeds threshold"

            self.health_history.append(health_data)
            if len(self.health_history) > 100:
                self.health_history.pop(0)

            return health_data

        except Exception as e:
            self.logger.error(f"System health check error: {e}")
            return {"timestamp": time.time(), "status": "error", "error": str(e)}

    def check_agent_health(self, agent_info: AgentInfo) -> Dict[str, Any]:
        """Check health for specific agent"""
        try:
            health_data = {
                "agent_id": agent_info.agent_id,
                "timestamp": time.time(),
                "status": agent_info.status.value,
                "performance_score": agent_info.performance_score,
                "uptime": agent_info.uptime,
                "health_score": 100.0,
                "warnings": [],
                "recommendations": [],
            }

            # Performance health check
            if agent_info.performance_score < 0.5:
                health_data["health_score"] -= 30
                health_data["warnings"].append("Low performance detected")
                health_data["recommendations"].append(
                    "Check agent workload and resources"
                )

            if agent_info.performance_score < 0.3:
                health_data["health_score"] -= 40
                health_data["warnings"].append("Critical performance issues")
                health_data["recommendations"].append("Immediate intervention required")

            # Uptime health check
            if agent_info.uptime < 300:  # Less than 5 minutes
                health_data["health_score"] -= 20
                health_data["warnings"].append("Recent restart detected")
                health_data["recommendations"].append("Monitor for stability issues")

            # Status health check
            if agent_info.status == AgentStatus.ERROR:
                health_data["health_score"] -= 50
                health_data["warnings"].append("Agent in error state")
                health_data["recommendations"].append("Investigate error logs")

            elif agent_info.status == AgentStatus.OFFLINE:
                health_data["health_score"] -= 100
                health_data["warnings"].append("Agent offline")
                health_data["recommendations"].append("Check agent connectivity")

            # Ensure health score doesn't go below 0
            health_data["health_score"] = max(0.0, health_data["health_score"])

            return health_data

        except Exception as e:
            self.logger.error(
                f"Agent health check error for {agent_info.agent_id}: {e}"
            )
            return {
                "agent_id": agent_info.agent_id,
                "timestamp": time.time(),
                "status": "error",
                "error": str(e),
                "health_score": 0.0,
            }

    def check_workspace_health(self, workspace_path: Path) -> Dict[str, Any]:
        """Check workspace directory health"""
        try:
            if not workspace_path.exists():
                return {
                    "timestamp": time.time(),
                    "status": "critical",
                    "error": "Workspace directory does not exist",
                    "recommendation": "Create workspace directory",
                }

            # Check directory permissions
            try:
                test_file = workspace_path / ".health_check"
                test_file.touch()
                test_file.unlink()
                permissions_ok = True
            except Exception:
                permissions_ok = False

            # Check disk space
            disk_usage = psutil.disk_usage(str(workspace_path))

            health_data = {
                "timestamp": time.time(),
                "workspace_path": str(workspace_path),
                "exists": True,
                "permissions_ok": permissions_ok,
                "disk_free": disk_usage.free,
                "disk_usage_percent": disk_usage.percent,
                "status": "healthy",
            }

            if not permissions_ok:
                health_data["status"] = "critical"
                health_data["warnings"] = ["Permission issues detected"]
                health_data["recommendations"] = ["Check directory permissions"]

            if disk_usage.percent > self.health_thresholds["disk_usage"]:
                health_data["status"] = "warning"
                if "warnings" not in health_data:
                    health_data["warnings"] = []
                health_data["warnings"].append(
                    f"Disk usage {disk_usage.percent}% is high"
                )
                health_data["recommendations"] = ["Consider cleanup or expansion"]

            return health_data

        except Exception as e:
            self.logger.error(f"Workspace health check error: {e}")
            return {"timestamp": time.time(), "status": "error", "error": str(e)}

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        if not self.health_history:
            return {"status": "no_data", "message": "No health data available"}

        latest_system = self.health_history[-1] if self.health_history else {}

        # Calculate health trends
        recent_health = (
            self.health_history[-10:]
            if len(self.health_history) >= 10
            else self.health_history
        )

        avg_cpu = (
            sum(h.get("cpu_usage", 0) for h in recent_health) / len(recent_health)
            if recent_health
            else 0
        )
        avg_memory = (
            sum(h.get("memory_usage", 0) for h in recent_health) / len(recent_health)
            if recent_health
            else 0
        )

        return {
            "timestamp": time.time(),
            "system_status": latest_system.get("status", "unknown"),
            "average_cpu_usage": round(avg_cpu, 2),
            "average_memory_usage": round(avg_memory, 2),
            "health_history_count": len(self.health_history),
            "recent_health_status": [h.get("status", "unknown") for h in recent_health],
            "overall_health": self._calculate_overall_health(recent_health),
        }

    def _calculate_overall_health(self, recent_health: List[Dict[str, Any]]) -> str:
        """Calculate overall health status from recent data"""
        if not recent_health:
            return "unknown"

        critical_count = sum(1 for h in recent_health if h.get("status") == "critical")
        warning_count = sum(1 for h in recent_health if h.get("status") == "warning")
        healthy_count = sum(1 for h in recent_health if h.get("status") == "healthy")

        if critical_count > 0:
            return "critical"
        elif warning_count > len(recent_health) * 0.3:  # More than 30% warnings
            return "warning"
        elif healthy_count > len(recent_health) * 0.7:  # More than 70% healthy
            return "healthy"
        else:
            return "degraded"

    def set_health_thresholds(self, thresholds: Dict[str, float]):
        """Update health monitoring thresholds"""
        for key, value in thresholds.items():
            if key in self.health_thresholds:
                self.health_thresholds[key] = value
                self.logger.info(f"Updated health threshold {key}: {value}")

    def get_health_thresholds(self) -> Dict[str, float]:
        """Get current health thresholds"""
        return self.health_thresholds.copy()
