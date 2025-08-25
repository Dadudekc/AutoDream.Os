from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .workspace_config import (
    WorkspaceType,
    WorkspaceStatus,
    WorkspaceConfig,
    WorkspaceInfo,
    WorkspaceConfigManager,
)
from .workspace_creator import WorkspaceStructureManager
from .security.security_manager import (
    SecurityLevel,
    Permission,
    WorkspaceSecurityManager,
)


class WorkspaceCoordinator:
    """High level workspace orchestration combining all concerns."""

    def __init__(self, base_workspace_dir: str = "agent_workspaces"):
        self.base_workspace_dir = Path(base_workspace_dir)
        self.logger = logging.getLogger(f"{__name__}.WorkspaceCoordinator")
        self.workspaces: Dict[str, WorkspaceInfo] = {}
        self.configs: Dict[str, WorkspaceConfig] = {}
        self.status = "initialized"

        self.config_manager = WorkspaceConfigManager(self.base_workspace_dir)
        self.structure_manager = WorkspaceStructureManager(self.base_workspace_dir)
        self.security_manager = WorkspaceSecurityManager(self.base_workspace_dir)

        self.base_workspace_dir.mkdir(exist_ok=True)
        self._discover_existing_workspaces()

    # -- workspace discovery ----------------------------------------------
    def _discover_existing_workspaces(self) -> None:
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    self._load_workspace_info(workspace_dir.name, workspace_dir)
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to discover existing workspaces: {e}")

    def _load_workspace_info(self, name: str, path: Path) -> None:
        try:
            size_mb = sum(
                f.stat().st_size for f in path.rglob("*") if f.is_file()
            ) / (1024 * 1024)

            settings = self.config_manager.load_workspace_config(name)
            info = WorkspaceInfo(
                name=name,
                workspace_type=settings.workspace_type if settings else WorkspaceType.AGENT,
                status=WorkspaceStatus.ACTIVE,
                path=str(path),
                size_mb=round(size_mb, 2),
                created_at=settings.base_path if settings else "unknown",
                last_accessed="unknown",
                agent_count=1,
                resource_usage={"files": len(list(path.rglob("*"))), "size_mb": size_mb},
                inbox_path=str(path / "inbox") if (path / "inbox").exists() else None,
                tasks_path=str(path / "tasks") if (path / "tasks").exists() else None,
                responses_path=str(path / "responses") if (path / "responses").exists() else None,
                agent_id=name,
            )

            self.workspaces[name] = info
            if settings:
                self.configs[name] = settings
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to load workspace info for {name}: {e}")

    # -- creation ---------------------------------------------------------
    def create_workspace(
        self,
        name: str,
        workspace_type: WorkspaceType = WorkspaceType.AGENT,
        permissions: Optional[List[str]] = None,
        isolation_level: str = "standard",
        security_level: Optional[SecurityLevel] = None,
        allowed_agents: Optional[List[str]] = None,
    ) -> bool:
        try:
            if name in self.workspaces:
                return False

            workspace_path = self.base_workspace_dir / name
            workspace_path.mkdir(exist_ok=True)

            if not self.structure_manager.create_workspace_structure(
                workspace_path, workspace_type
            ):
                return False

            settings = WorkspaceConfig(
                name=name,
                workspace_type=workspace_type,
                base_path=str(workspace_path),
                permissions=permissions or ["read", "write"],
                isolation_level=isolation_level,
                max_size_mb=100,
                auto_cleanup=True,
                backup_enabled=True,
            )

            info = WorkspaceInfo(
                name=name,
                workspace_type=workspace_type,
                status=WorkspaceStatus.ACTIVE,
                path=str(workspace_path),
                size_mb=0.0,
                created_at=self.config_manager.get_current_timestamp(),
                last_accessed=self.config_manager.get_current_timestamp(),
                agent_count=0,
                resource_usage={"files": 0, "size_mb": 0.0},
                inbox_path=str(workspace_path / "inbox"),
                tasks_path=str(workspace_path / "tasks"),
                responses_path=str(workspace_path / "responses"),
                agent_id=name,
            )

            self.workspaces[name] = info
            self.configs[name] = settings
            self.config_manager.save_workspace_config(name, settings)

            if security_level:
                self.security_manager.create_security_policy(
                    name, security_level, allowed_agents, None
                )
            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to create workspace {name}: {e}")
            return False

    # -- query operations -------------------------------------------------
    def get_workspace_info(self, name: str) -> Optional[WorkspaceInfo]:
        return self.workspaces.get(name)

    def list_workspaces(self) -> List[WorkspaceInfo]:
        return list(self.workspaces.values())

    def get_all_workspaces(self) -> List[WorkspaceInfo]:
        """Alias maintained for backwards compatibility."""
        return self.list_workspaces()

    def update_workspace_status(self, name: str, status: WorkspaceStatus) -> bool:
        try:
            if name in self.workspaces:
                self.workspaces[name].status = status
                self.workspaces[name].last_accessed = (
                    self.config_manager.get_current_timestamp()
                )
                return True
            return False
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to update workspace status: {e}")
            return False

    def get_architecture_summary(self) -> Dict[str, Any]:
        try:
            total_workspaces = len(self.workspaces)
            active_workspaces = len(
                [w for w in self.workspaces.values() if w.status == WorkspaceStatus.ACTIVE]
            )
            total_size_mb = sum(w.size_mb for w in self.workspaces.values())
            return {
                "total_workspaces": total_workspaces,
                "active_workspaces": active_workspaces,
                "total_size_mb": round(total_size_mb, 2),
                "workspace_types": {
                    wt.value: len(
                        [w for w in self.workspaces.values() if w.workspace_type == wt]
                    )
                    for wt in WorkspaceType
                },
                "isolation_levels": list(
                    set(c.isolation_level for c in self.configs.values())
                ),
            }
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to get architecture summary: {e}")
            return {"error": str(e)}

    def get_workspace_status(self) -> Dict[str, Any]:
        try:
            total = len(self.workspaces)
            active = sum(1 for w in self.workspaces.values() if Path(w.path).exists())
            details: Dict[str, Any] = {}
            for name, info in self.workspaces.items():
                workspace_path = Path(info.path)
                details[name] = {
                    "exists": workspace_path.exists(),
                    "inbox_files": len(list((workspace_path / "inbox").glob("*"))),
                    "task_files": len(list((workspace_path / "tasks").glob("*"))),
                    "response_files": len(
                        list((workspace_path / "responses").glob("*"))
                    ),
                    "last_accessed": info.last_accessed,
                }
            return {
                "status": self.status,
                "total_workspaces": total,
                "active_workspaces": active,
                "base_path": str(self.base_workspace_dir),
                "workspace_details": details,
            }
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to get workspace status: {e}")
            return {"status": "error", "error": str(e)}

    # -- cleanup ----------------------------------------------------------
    def cleanup_workspace(self, name: str) -> bool:
        try:
            info = self.workspaces.get(name)
            if not info:
                return False
            success = self.structure_manager.cleanup_workspace_structure(Path(info.path))
            if success:
                self.workspaces.pop(name, None)
                self.configs.pop(name, None)
            return success
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to cleanup workspace {name}: {e}")
            return False

    # -- security wrappers ------------------------------------------------
    def create_security_policy(
        self,
        workspace_name: str,
        security_level: SecurityLevel,
        allowed_agents: Optional[List[str]] = None,
        permissions: Optional[Dict[str, List[Permission]]] = None,
    ) -> bool:
        return self.security_manager.create_security_policy(
            workspace_name, security_level, allowed_agents, permissions
        )

    def check_access_permission(
        self, workspace_name: str, agent_id: str, permission: Permission
    ) -> bool:
        return self.security_manager.check_access_permission(
            workspace_name, agent_id, permission
        )

    def get_security_summary(self) -> Dict[str, Any]:
        return self.security_manager.get_security_summary()


def run_smoke_test() -> bool:
    """Basic functionality test for the workspace coordinator."""

    print("🧪 Running WorkspaceCoordinator smoke test...")
    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            manager = WorkspaceCoordinator(tmp)
            assert manager.create_workspace("test_agent")
            assert manager.get_workspace_info("test_agent") is not None
            assert manager.update_workspace_status("test_agent", WorkspaceStatus.ACTIVE)
            assert len(manager.list_workspaces()) == 1
            summary = manager.get_architecture_summary()
            assert "total_workspaces" in summary
            sec = manager.get_security_summary()
            assert "total_policies" in sec
    except Exception as e:
        print(f"❌ WorkspaceCoordinator smoke test FAILED: {e}")
        return False
    print("✅ WorkspaceCoordinator smoke test PASSED")
    return True


__all__ = [
    "WorkspaceCoordinator",
    "run_smoke_test",
]
