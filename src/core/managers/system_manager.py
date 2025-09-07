#!/usr/bin/env python3
"""System Manager coordinating user, resource and process managers."""

import logging
from typing import Any, Dict, List, Optional

from ..base_manager import BaseManager
from .user_manager import (
    AgentStatus,
    AgentCapability,
    AgentInfo,
    UserManager,
)
from .resource_manager import WorkspaceInfo, ResourceManager
from .process_manager import ProcessManager

logger = logging.getLogger(__name__)


class SystemManager(BaseManager):
    """Coordinate agents, workspaces and system processes."""

    def __init__(self, config_path: str = "config/system_manager.json"):
        super().__init__(manager_id="system_manager", name="SystemManager")
        self.config_path = config_path
        self.user_manager = UserManager()
        self.resource_manager = ResourceManager()
        self.process_manager = ProcessManager(self.user_manager, self.resource_manager)
        logger.info("SystemManager initialized successfully")

    @property
    def agents(self) -> Dict[str, AgentInfo]:
        """Expose registered agents (backwards compatibility)."""
        return self.user_manager.agents

    @property
    def workspaces(self) -> Dict[str, WorkspaceInfo]:
        """Expose tracked workspaces (backwards compatibility)."""
        return self.resource_manager.workspaces

    # ------------------------------------------------------------------
    # BaseManager abstract method implementations
    # ------------------------------------------------------------------
    def _on_start(self) -> bool:  # pragma: no cover - simple delegation
        return True

    def _on_stop(self) -> None:  # pragma: no cover - simple delegation
        return None

    def _on_heartbeat(self) -> None:  # pragma: no cover - simple delegation
        return None

    def _on_initialize_resources(self) -> bool:  # pragma: no cover - simple delegation
        return True

    def _on_cleanup_resources(self) -> None:  # pragma: no cover - simple delegation
        return None

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:  # pragma: no cover
        logger.error("Recovery attempt failed for %s: %s", context, error)
        return False

    # ------------------------------------------------------------------
    # Agent management wrappers
    # ------------------------------------------------------------------
    def register_agent(self, agent_id: str, name: str, capabilities: List[str]) -> bool:
        return self.user_manager.register_agent(agent_id, name, capabilities)

    def unregister_agent(self, agent_id: str) -> bool:
        return self.user_manager.unregister_agent(agent_id)

    def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        return self.user_manager.update_agent_status(agent_id, status)

    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        return self.user_manager.get_agent(agent_id)

    def get_all_agents(self) -> List[AgentInfo]:
        return self.user_manager.get_all_agents()

    def get_agents_by_status(self, status: AgentStatus) -> List[AgentInfo]:
        return self.user_manager.get_agents_by_status(status)

    def get_agents_by_capability(self, capability: AgentCapability) -> List[AgentInfo]:
        return self.user_manager.get_agents_by_capability(capability)

    def assign_contract_to_agent(self, agent_id: str, contract_id: str) -> bool:
        return self.user_manager.assign_contract(agent_id, contract_id)

    def complete_contract_for_agent(self, agent_id: str, contract_id: str) -> bool:
        return self.user_manager.complete_contract(agent_id, contract_id)

    def get_agent_summary(self) -> Dict[str, Any]:
        return self.user_manager.get_summary()

    # ------------------------------------------------------------------
    # Workspace management wrappers
    # ------------------------------------------------------------------
    def create_workspace(
        self, workspace_id: str, name: str, path: str, agent_id: Optional[str] = None
    ) -> bool:
        return self.resource_manager.create_workspace(workspace_id, name, path, agent_id)

    def delete_workspace(self, workspace_id: str) -> bool:
        return self.resource_manager.delete_workspace(workspace_id)

    def get_workspace(self, workspace_id: str) -> Optional[WorkspaceInfo]:
        return self.resource_manager.get_workspace(workspace_id)

    def get_all_workspaces(self) -> List[WorkspaceInfo]:
        return self.resource_manager.get_all_workspaces()

    def get_workspaces_by_agent(self, agent_id: str) -> List[WorkspaceInfo]:
        return self.resource_manager.get_workspaces_by_agent(agent_id)

    def assign_workspace_to_agent(self, workspace_id: str, agent_id: str) -> bool:
        return self.resource_manager.assign_workspace(workspace_id, agent_id)

    def get_workspace_summary(self) -> Dict[str, Any]:
        return self.resource_manager.get_summary()

    # ------------------------------------------------------------------
    # Process management wrappers
    # ------------------------------------------------------------------
    def get_system_status(self) -> Dict[str, Any]:
        metrics = self.get_metrics() if self.enable_metrics else None
        return self.process_manager.get_system_status(metrics)

    def perform_system_health_check(self) -> Dict[str, Any]:
        return self.process_manager.perform_system_health_check()

    def backup_system_data(self) -> bool:
        return self.process_manager.backup_system_data()
