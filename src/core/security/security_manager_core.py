from __future__ import annotations

from dataclasses import asdict
import json
import logging
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..workspace_config import WorkspaceConfigManager
from .security_auth import SecurityLevel, Permission, SecurityPolicy, AccessLog
from .security_config import get_default_isolation_rules

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
                isolation_rules=get_default_isolation_rules(security_level),
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


__all__ = ["WorkspaceSecurityManager"]
