#!/usr/bin/env python3
"""Unified Workspace Manager
=================================

This module consolidates workspace architecture, configuration, structure and
security management into a single file. Each concern is handled by a dedicated
component while :class:`WorkspaceManager` orchestrates their interaction.

The design maintains clear separation of responsibilities:

* ``WorkspaceConfigManager`` – persistence of workspace configuration
* ``WorkspaceStructureManager`` – directory creation and cleanup
* ``WorkspaceSecurityManager`` – security policies and access control
* ``WorkspaceManager`` – high level orchestration and architecture

The file folds logic previously split across ``workspace_architecture_manager``,
``workspace_security_manager``, ``workspace_config`` and ``workspace_structure``
modules.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Any, Dict, List, Optional
import secrets


# ---------------------------------------------------------------------------
# Configuration models
# ---------------------------------------------------------------------------


class WorkspaceType(Enum):
    """Types of agent workspaces."""

    AGENT = "agent"
    COORDINATION = "coordination"
    SHARED = "shared"
    ISOLATED = "isolated"
    TEMPORARY = "temporary"


class WorkspaceStatus(Enum):
    """Workspace lifecycle states."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"
    ERROR = "error"


@dataclass
class WorkspaceConfig:
    """Configuration persisted for a workspace."""

    name: str
    workspace_type: WorkspaceType
    base_path: str
    permissions: List[str]
    isolation_level: str
    max_size_mb: int
    auto_cleanup: bool
    backup_enabled: bool


@dataclass
class WorkspaceInfo:
    """Runtime information about a workspace."""

    name: str
    workspace_type: WorkspaceType
    status: WorkspaceStatus
    path: str
    size_mb: float
    created_at: str
    last_accessed: str
    agent_count: int
    resource_usage: Dict[str, Any]
    # Agent specific paths for backwards compatibility
    inbox_path: Optional[str] = None
    tasks_path: Optional[str] = None
    responses_path: Optional[str] = None
    agent_id: Optional[str] = None


class WorkspaceConfigManager:
    """Handles persistence of workspace configuration."""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceConfigManager")

    def save_workspace_config(self, name: str, config: WorkspaceConfig) -> bool:
        """Persist workspace configuration to disk."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            with open(config_file, "w") as f:
                json.dump(asdict(config), f, indent=2, default=str)
            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to save workspace config for {name}: {e}")
            return False

    def load_workspace_config(self, name: str) -> Optional[WorkspaceConfig]:
        """Load configuration from disk if available."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    data = json.load(f)
                data["workspace_type"] = WorkspaceType(data["workspace_type"])
                return WorkspaceConfig(**data)
            return None
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to load workspace config for {name}: {e}")
            return None

    @staticmethod
    def get_current_timestamp() -> str:
        """Return current timestamp string."""
        from datetime import datetime

        return datetime.now().isoformat()


# ---------------------------------------------------------------------------
# Structure management
# ---------------------------------------------------------------------------


class WorkspaceStructureManager:
    """Manages creation and cleanup of workspace directories."""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceStructureManager")

    def create_workspace_structure(
        self, workspace_path: Path, workspace_type: WorkspaceType
    ) -> bool:
        """Create directory layout for a workspace."""
        try:
            common_dirs = ["data", "logs", "temp", "backups"]
            if workspace_type == WorkspaceType.AGENT:
                type_dirs = [
                    "personal",
                    "shared",
                    "work",
                    "archive",
                    "inbox",
                    "tasks",
                    "responses",
                ]
            elif workspace_type == WorkspaceType.COORDINATION:
                type_dirs = ["coordination", "shared", "monitoring", "reports"]
            elif workspace_type == WorkspaceType.SHARED:
                type_dirs = ["public", "restricted", "templates", "examples"]
            else:
                type_dirs = ["general"]

            for dir_name in common_dirs + type_dirs:
                (workspace_path / dir_name).mkdir(exist_ok=True)

            readme_content = (
                f"# {workspace_path.name} Workspace\n\n"
                f"Type: {workspace_type.value}\n"
                f"Created: {self._get_current_timestamp()}\n"
            )
            with open(workspace_path / "README.md", "w") as f:
                f.write(readme_content)

            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to create workspace structure: {e}")
            return False

    def cleanup_workspace_structure(self, workspace_path: Path) -> bool:
        """Remove a workspace directory tree."""
        try:
            if workspace_path.exists():
                import shutil

                shutil.rmtree(workspace_path)
                return True
            return False
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to cleanup workspace structure: {e}")
            return False

    @staticmethod
    def _get_current_timestamp() -> str:
        from datetime import datetime

        return datetime.now().isoformat()


# ---------------------------------------------------------------------------
# Security management
# ---------------------------------------------------------------------------


class SecurityLevel(Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"
    ISOLATED = "isolated"
    SECURE = "secure"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    SHARE = "share"


@dataclass
class SecurityPolicy:
    workspace_name: str
    security_level: SecurityLevel
    allowed_agents: List[str]
    permissions: Dict[str, List[Permission]]
    isolation_rules: List[str]
    encryption_enabled: bool
    audit_logging: bool
    max_access_attempts: int


@dataclass
class AccessLog:
    timestamp: str
    agent_id: str
    action: str
    resource: str
    success: bool
    ip_address: str = "unknown"


class WorkspaceSecurityManager:
    """Handles security policy enforcement and access control."""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.access_logs: List[AccessLog] = []
        self.logger = logging.getLogger(f"{__name__}.WorkspaceSecurityManager")

        self._load_existing_policies()

    # -- policy management -------------------------------------------------
    def _load_existing_policies(self) -> None:
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    policy_file = workspace_dir / "security_policy.json"
                    if policy_file.exists():
                        self._load_security_policy(workspace_dir.name, policy_file)
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to load existing security policies: {e}")

    def _load_security_policy(self, workspace_name: str, policy_file: Path) -> None:
        try:
            with open(policy_file, "r") as f:
                data = json.load(f)

            level = SecurityLevel(data.get("security_level", "restricted"))
            permissions: Dict[str, List[Permission]] = {}
            for agent, perms in data.get("permissions", {}).items():
                permissions[agent] = [Permission(p) for p in perms]

            policy = SecurityPolicy(
                workspace_name=workspace_name,
                security_level=level,
                allowed_agents=data.get("allowed_agents", []),
                permissions=permissions,
                isolation_rules=data.get("isolation_rules", []),
                encryption_enabled=data.get("encryption_enabled", False),
                audit_logging=data.get("audit_logging", True),
                max_access_attempts=data.get("max_access_attempts", 3),
            )

            self.security_policies[workspace_name] = policy
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(
                f"Failed to load security policy for {workspace_name}: {e}"
            )

    def create_security_policy(
        self,
        workspace_name: str,
        security_level: SecurityLevel,
        allowed_agents: Optional[List[str]] = None,
        permissions: Optional[Dict[str, List[Permission]]] = None,
    ) -> bool:
        try:
            if workspace_name in self.security_policies:
                return False

            if permissions is None:
                permissions = {
                    agent: [Permission.READ, Permission.WRITE]
                    for agent in (allowed_agents or [])
                }

            policy = SecurityPolicy(
                workspace_name=workspace_name,
                security_level=security_level,
                allowed_agents=allowed_agents or [],
                permissions=permissions,
                isolation_rules=self._get_default_isolation_rules(security_level),
                encryption_enabled=security_level
                in [SecurityLevel.ISOLATED, SecurityLevel.SECURE],
                audit_logging=True,
                max_access_attempts=3,
            )

            self.security_policies[workspace_name] = policy
            self._save_security_policy(workspace_name, policy)

            if security_level in [SecurityLevel.ISOLATED, SecurityLevel.SECURE]:
                self._create_isolated_structure(workspace_name)
            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(
                f"Failed to create security policy for {workspace_name}: {e}"
            )
            return False

    # -- helpers -----------------------------------------------------------
    def _get_default_isolation_rules(self, level: SecurityLevel) -> List[str]:
        if level == SecurityLevel.PUBLIC:
            return ["allow_all_agents"]
        if level == SecurityLevel.RESTRICTED:
            return ["allow_authenticated_agents", "log_all_access"]
        if level == SecurityLevel.PRIVATE:
            return ["allow_owner_only", "encrypt_data", "log_all_access"]
        if level == SecurityLevel.ISOLATED:
            return [
                "strict_isolation",
                "encrypt_all_data",
                "audit_everything",
                "no_shared_resources",
            ]
        if level == SecurityLevel.SECURE:
            return [
                "maximum_isolation",
                "encrypt_everything",
                "full_audit_trail",
                "no_external_access",
            ]
        return ["default_isolation"]

    def _create_isolated_structure(self, workspace_name: str) -> None:
        try:
            workspace_path = self.base_workspace_dir / workspace_name
            for dir_name in ["secure", "encrypted", "audit", "backup"]:
                (workspace_path / dir_name).mkdir(exist_ok=True)

            security_meta = {
                "isolation_level": "high",
                "created_at": WorkspaceConfigManager.get_current_timestamp(),
                "encryption_key": secrets.token_hex(32),
            }
            with open(workspace_path / "security_metadata.json", "w") as f:
                json.dump(security_meta, f, indent=2)
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(
                f"Failed to create isolated structure for {workspace_name}: {e}"
            )

    def _save_security_policy(self, name: str, policy: SecurityPolicy) -> None:
        try:
            policy_file = self.base_workspace_dir / name / "security_policy.json"
            data = asdict(policy)
            data["security_level"] = policy.security_level.value
            data["permissions"] = {
                agent: [p.value for p in perms]
                for agent, perms in policy.permissions.items()
            }
            with open(policy_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to save security policy for {name}: {e}")

    # -- access control ----------------------------------------------------
    def check_access_permission(
        self, workspace_name: str, agent_id: str, permission: Permission
    ) -> bool:
        try:
            policy = self.security_policies.get(workspace_name)
            if not policy or agent_id not in policy.allowed_agents:
                self._log_access_attempt(workspace_name, agent_id, permission, False)
                return False
            if permission in policy.permissions.get(agent_id, []):
                self._log_access_attempt(workspace_name, agent_id, permission, True)
                return True
            self._log_access_attempt(workspace_name, agent_id, permission, False)
            return False
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to check access permission: {e}")
            return False

    def _log_access_attempt(
        self, workspace: str, agent_id: str, permission: Permission, success: bool
    ) -> None:
        log_entry = AccessLog(
            timestamp=WorkspaceConfigManager.get_current_timestamp(),
            agent_id=agent_id,
            action=f"check_{permission.value}",
            resource=workspace,
            success=success,
        )
        self.access_logs.append(log_entry)
        if len(self.access_logs) > 1000:
            self.access_logs = self.access_logs[-1000:]

    def get_security_summary(self) -> Dict[str, Any]:
        try:
            security_levels: Dict[str, int] = {}
            for policy in self.security_policies.values():
                level = policy.security_level.value
                security_levels[level] = security_levels.get(level, 0) + 1
            recent_failures = len([log for log in self.access_logs[-100:] if not log.success])
            return {
                "total_policies": len(self.security_policies),
                "total_access_logs": len(self.access_logs),
                "security_levels": security_levels,
                "recent_failures": recent_failures,
                "encrypted_workspaces": len(
                    [p for p in self.security_policies.values() if p.encryption_enabled]
                ),
            }
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to get security summary: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run a basic self-test of the security subsystem."""
        try:
            test_workspace = "smoke_test_security"
            success = self.create_security_policy(
                test_workspace, SecurityLevel.PRIVATE, ["test_agent"]
            )
            if not success:
                return False
            if not self.check_access_permission(
                test_workspace, "test_agent", Permission.READ
            ):
                return False
            if self.check_access_permission(
                test_workspace, "unauthorized", Permission.READ
            ):
                return False
            summary = self.get_security_summary()
            if "total_policies" not in summary:
                return False
            self.security_policies.pop(test_workspace, None)
            test_path = self.base_workspace_dir / test_workspace
            if test_path.exists():
                import shutil

                shutil.rmtree(test_path)
            return True
        except Exception:  # pragma: no cover - safety net
            return False


# ---------------------------------------------------------------------------
# Unified manager
# ---------------------------------------------------------------------------


class WorkspaceManager:
    """High level workspace orchestration combining all concerns."""

    def __init__(self, base_workspace_dir: str = "agent_workspaces"):
        self.base_workspace_dir = Path(base_workspace_dir)
        self.logger = logging.getLogger(f"{__name__}.WorkspaceManager")
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


# ---------------------------------------------------------------------------
# Smoke test ---------------------------------------------------------------


def run_smoke_test() -> bool:
    """Basic functionality test for the unified manager."""

    print("🧪 Running WorkspaceManager smoke test...")
    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            manager = WorkspaceManager(tmp)
            assert manager.create_workspace("test_agent")
            assert manager.get_workspace_info("test_agent") is not None
            assert manager.update_workspace_status("test_agent", WorkspaceStatus.ACTIVE)
            assert len(manager.list_workspaces()) == 1
            summary = manager.get_architecture_summary()
            assert "total_workspaces" in summary
            sec = manager.get_security_summary()
            assert "total_policies" in sec
    except Exception as e:
        print(f"❌ WorkspaceManager smoke test FAILED: {e}")
        return False
    print("✅ WorkspaceManager smoke test PASSED")
    return True


if __name__ == "__main__":
    run_smoke_test()

