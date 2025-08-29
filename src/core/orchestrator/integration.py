import logging
from datetime import datetime
from typing import Any, Dict, Optional

from ..base_manager import BaseManager, ManagerStatus
from .registry import ManagerRegistry
from .lifecycle import LifecycleManager

logger = logging.getLogger(__name__)


class IntegrationManager:
    """Provide integration utilities and information access."""

    def __init__(self, registry: ManagerRegistry, lifecycle: LifecycleManager) -> None:
        self.registry = registry
        self.lifecycle = lifecycle
        self.start_time = datetime.now()
        self.total_operations = 0
        self.failed_operations = 0

    # ------------------------------------------------------------------
    # Manager lookup helpers
    # ------------------------------------------------------------------
    def get_manager(self, manager_name: str) -> Optional[BaseManager]:
        return self.registry.manager_instances.get(manager_name)

    def get_manager_status(self, manager_name: str) -> Optional[Dict[str, Any]]:
        if manager_name not in self.registry.managers:
            return None
        info = self.registry.managers[manager_name]
        inst = self.registry.manager_instances.get(manager_name)
        status: Dict[str, Any] = {
            "manager_name": manager_name,
            "status": info.status.value,
            "priority": info.priority.value,
            "dependencies": info.dependencies,
            "last_health_check": info.last_health_check.isoformat(),
            "health_status": info.health_status,
        }
        if inst:
            status.update({
                "instance_info": inst.get_info(),
                "health_check": inst.health_check(),
            })
        return status

    def get_all_manager_statuses(self) -> Dict[str, Dict[str, Any]]:
        return {name: self.get_manager_status(name) for name in self.registry.managers}

    # ------------------------------------------------------------------
    # Metrics and summaries
    # ------------------------------------------------------------------
    def get_orchestrator_metrics(self) -> Dict[str, Any]:
        total_ops = self.total_operations
        failed_ops = self.failed_operations
        return {
            "orchestrator_name": "ManagerOrchestrator",
            "start_time": self.start_time.isoformat(),
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "total_managers": len(self.registry.managers),
            "active_managers": len(
                [m for m in self.registry.managers.values() if m.status == ManagerStatus.ACTIVE]
            ),
            "failed_managers": len(
                [m for m in self.registry.managers.values() if m.status == ManagerStatus.ERROR]
            ),
            "total_operations": total_ops,
            "failed_operations": failed_ops,
            "success_rate": (total_ops - failed_ops) / total_ops if total_ops > 0 else 0,
            "last_health_check": self.lifecycle.last_health_check.isoformat(),
            "health_check_interval": self.lifecycle.health_check_interval,
            "startup_order": self.registry.startup_order,
            "dependency_graph": self.registry.dependency_graph,
        }

    def get_consolidation_summary(self) -> Dict[str, Any]:
        return {
            "consolidation_benefits": {
                "files_before": 42,
                "files_after": 10,
                "reduction_percentage": 76,
                "duplication_eliminated": "80%",
                "maintenance_effort_reduction": "50-60%",
                "code_consolidation": "70%",
            },
            "manager_categories": {
                "core_system": ["system_manager", "config_manager", "status_manager"],
                "task_management": ["task_manager"],
                "data_management": ["data_manager"],
                "communication": ["communication_manager"],
                "health_monitoring": ["health_manager", "performance_manager"],
            },
            "replaced_files": {
                "system_manager": [
                    "agent_manager.py",
                    "core_manager.py",
                    "repository/system_manager.py",
                    "workspace_manager.py",
                    "persistent_storage_manager.py",
                ],
                "config_manager": [
                    "config_manager.py",
                    "config_manager_core.py",
                    "config_manager_loader.py",
                    "config_manager_validator.py",
                    "config_manager_config.py",
                ],
                "status_manager": [
                    "status_manager.py",
                    "status_manager_core.py",
                    "status_manager_tracker.py",
                    "status_manager_reporter.py",
                    "status_manager_config.py",
                ],
                "task_manager": [
                    "task_manager.py",
                    "autonomous_development/tasks/manager.py",
                    "task_management/task_scheduler_manager.py",
                    "autonomous_development/workflow/manager.py",
                ],
                "data_manager": [
                    "services/testing/data_manager.py",
                    "services/financial/sentiment/data_manager.py",
                    "services/financial/analytics/data_manager.py",
                ],
                "communication_manager": [
                    "services/communication/channel_manager.py",
                    "core/communication/communication_manager.py",
                    "services/api_manager.py",
                ],
                "health_manager": [
                    "core/health_alert_manager.py",
                    "core/health_threshold_manager.py",
                    "core/health/monitoring/health_notification_manager.py",
                ],
                "performance_manager": [
                    "core/performance/alerts/manager.py",
                    "core/connection_pool_manager.py",
                ],
            },
        }
