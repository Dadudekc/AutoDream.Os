import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


@dataclass
class ManagerInfo:
    """Information about a registered manager."""

    manager_name: str
    manager_class: Type[BaseManager]
    instance: Optional[BaseManager]
    status: ManagerStatus
    priority: ManagerPriority
    dependencies: List[str]
    config_path: Optional[str]
    last_health_check: datetime
    health_status: Dict[str, Any]


class ManagerRegistry:
    """Maintain registration and ordering of managers."""

    def __init__(self) -> None:
        self.managers: Dict[str, ManagerInfo] = {}
        self.manager_instances: Dict[str, BaseManager] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.startup_order: List[str] = []

    # ------------------------------------------------------------------
    # Registration utilities
    # ------------------------------------------------------------------
    def register_default_managers(self) -> None:
        """Register the eight consolidated managers with placeholders."""
        self.register_manager(
            "system_manager",
            "SystemManager",
            priority=ManagerPriority.CRITICAL,
            dependencies=[],
            config_path="config/system_manager.json",
        )
        self.register_manager(
            "config_manager",
            "ConfigManager",
            priority=ManagerPriority.HIGH,
            dependencies=["system_manager"],
            config_path="config/config_manager.json",
        )
        self.register_manager(
            "status_manager",
            "StatusManager",
            priority=ManagerPriority.HIGH,
            dependencies=["system_manager"],
            config_path="config/status_manager.json",
        )
        self.register_manager(
            "task_manager",
            "TaskManager",
            priority=ManagerPriority.HIGH,
            dependencies=["system_manager", "status_manager"],
            config_path="config/task_manager.json",
        )
        self.register_manager(
            "data_manager",
            "DataManager",
            priority=ManagerPriority.MEDIUM,
            dependencies=["system_manager", "config_manager"],
            config_path="config/data_manager.json",
        )
        self.register_manager(
            "communication_manager",
            "CommunicationManager",
            priority=ManagerPriority.MEDIUM,
            dependencies=["system_manager", "config_manager"],
            config_path="config/communication_manager.json",
        )
        self.register_manager(
            "health_manager",
            "HealthManager",
            priority=ManagerPriority.MEDIUM,
            dependencies=["system_manager", "status_manager"],
            config_path="config/health_manager.json",
        )
        self.register_manager(
            "performance_manager",
            "PerformanceManager",
            priority=ManagerPriority.LOW,
            dependencies=["system_manager", "health_manager"],
            config_path="config/performance_manager.json",
        )
        logger.info("Registered %s specialized managers", len(self.managers))

    def register_manager(
        self,
        manager_name: str,
        manager_class_name: str,
        priority: ManagerPriority = ManagerPriority.NORMAL,
        dependencies: Optional[List[str]] = None,
        config_path: Optional[str] = None,
    ) -> None:
        """Register a manager using placeholder classes."""
        if dependencies is None:
            dependencies = []

        class PlaceholderManager(BaseManager):
            def _validate_data(self, data: Any) -> bool:  # pragma: no cover - simple stub
                return True

        info = ManagerInfo(
            manager_name=manager_name,
            manager_class=PlaceholderManager,
            instance=None,
            status=ManagerStatus.INACTIVE,
            priority=priority,
            dependencies=dependencies,
            config_path=config_path,
            last_health_check=datetime.now(),
            health_status={},
        )
        self.managers[manager_name] = info
        logger.debug("Registered manager: %s", manager_name)

    # ------------------------------------------------------------------
    # Dependency ordering
    # ------------------------------------------------------------------
    def build_dependency_graph(self) -> None:
        self.dependency_graph = {
            name: info.dependencies.copy() for name, info in self.managers.items()
        }
        logger.debug("Dependency graph built")

    def calculate_startup_order(self) -> None:
        visited = set()
        temp_visited = set()
        order: List[str] = []

        def dfs(node: str) -> None:
            if node in temp_visited:
                raise ValueError(f"Circular dependency detected: {node}")
            if node in visited:
                return
            temp_visited.add(node)
            for dep in self.dependency_graph.get(node, []):
                if dep not in self.managers:
                    logger.warning(
                        "Manager %s depends on unknown manager: %s", node, dep
                    )
                else:
                    dfs(dep)
            temp_visited.remove(node)
            visited.add(node)
            order.append(node)

        priority_order = sorted(
            self.managers.keys(),
            key=lambda x: self.managers[x].priority.value,
            reverse=True,
        )
        for name in priority_order:
            if name not in visited:
                dfs(name)
        self.startup_order = order
        logger.info("Startup order calculated: %s", self.startup_order)
