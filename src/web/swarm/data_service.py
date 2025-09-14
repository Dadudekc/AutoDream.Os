"""Data service for swarm monitoring dashboard."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from .models import AgentStatus, Alert, SystemMetrics, ConsolidationProgress

logger = logging.getLogger(__name__)


class SwarmDataService:
    """Service for collecting and managing swarm monitoring data."""

    def __init__(self, project_root: Path):
        """Initialize the data service."""
        self.project_root = project_root
        self.agent_workspaces = project_root / "agent_workspaces"
        self.alerts: list[Alert] = []
        self.last_system_metrics: SystemMetrics | None = None

    def get_agent_statuses(self) -> list[AgentStatus]:
        """Get status of all agents."""
        agent_statuses = []
        
        if not self.agent_workspaces.exists():
            logger.warning("Agent workspaces directory not found")
            return agent_statuses

        for agent_dir in self.agent_workspaces.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, 'r', encoding='utf-8') as f:
                            status_data = json.load(f)
                        
                        agent_status = AgentStatus(
                            agent_id=status_data.get('agent_id', agent_dir.name),
                            status=status_data.get('status', 'unknown'),
                            current_phase=status_data.get('current_phase', 'unknown'),
                            last_updated=datetime.fromisoformat(
                                status_data.get('last_updated', datetime.now().isoformat())
                            ),
                            current_mission=status_data.get('current_mission'),
                            mission_priority=status_data.get('mission_priority'),
                            progress_percentage=status_data.get('progress_percentage'),
                            active_tasks=status_data.get('current_tasks', []),
                            completed_tasks=status_data.get('completed_tasks', []),
                            coordination_status=status_data.get('coordination_status', {})
                        )
                        agent_statuses.append(agent_status)
                        
                    except Exception as e:
                        logger.error(f"Error reading status for {agent_dir.name}: {e}")
                        # Create a default status for failed reads
                        agent_statuses.append(AgentStatus(
                            agent_id=agent_dir.name,
                            status="error",
                            current_phase="unknown",
                            last_updated=datetime.now()
                        ))

        return agent_statuses

    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available - returning default metrics")
            return SystemMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={"bytes_sent": 0, "bytes_recv": 0},
                timestamp=datetime.now()
            )

        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv
            }
            
            metrics = SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                timestamp=datetime.now()
            )
            
            self.last_system_metrics = metrics
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            # Return last known metrics or default
            if self.last_system_metrics:
                return self.last_system_metrics
            return SystemMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={"bytes_sent": 0, "bytes_recv": 0},
                timestamp=datetime.now()
            )

    def get_consolidation_progress(self) -> ConsolidationProgress:
        """Get consolidation progress information."""
        # This would typically read from consolidation status files
        # For now, return a default progress
        return ConsolidationProgress(
            phase="Phase 2",
            progress_percentage=75.0,
            files_processed=150,
            total_files=200,
            estimated_completion=datetime.now(),
            current_task="Refactoring large files"
        )

    def get_alerts(self) -> list[Alert]:
        """Get current alerts."""
        return self.alerts

    def add_alert(self, level: str, message: str, component: str) -> None:
        """Add a new alert."""
        alert = Alert(
            alert_id=f"alert_{len(self.alerts) + 1}",
            level=level,
            message=message,
            component=component,
            timestamp=datetime.now()
        )
        self.alerts.append(alert)
        logger.info(f"Alert added: {level} - {message}")

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert by ID."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Alert resolved: {alert_id}")
                return True
        return False

    def get_dashboard_summary(self) -> dict[str, Any]:
        """Get a summary of all dashboard data."""
        agent_statuses = self.get_agent_statuses()
        system_metrics = self.get_system_metrics()
        consolidation_progress = self.get_consolidation_progress()
        alerts = self.get_alerts()

        return {
            "agents": {
                "total": len(agent_statuses),
                "active": len([a for a in agent_statuses if a.status == "active"]),
                "statuses": [{"id": a.agent_id, "status": a.status} for a in agent_statuses]
            },
            "system": {
                "cpu_usage": system_metrics.cpu_usage,
                "memory_usage": system_metrics.memory_usage,
                "disk_usage": system_metrics.disk_usage
            },
            "consolidation": {
                "phase": consolidation_progress.phase,
                "progress": consolidation_progress.progress_percentage,
                "files_processed": consolidation_progress.files_processed,
                "total_files": consolidation_progress.total_files
            },
            "alerts": {
                "total": len(alerts),
                "unresolved": len([a for a in alerts if not a.resolved]),
                "critical": len([a for a in alerts if a.level == "critical" and not a.resolved])
            },
            "timestamp": datetime.now().isoformat()
        }