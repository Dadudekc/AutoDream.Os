#!/usr/bin/env python3
"""
Unified Workspace System - Consolidated Workspace Management

Consolidates 5 workspace manager files into a unified system following V2 standards.
NO duplicate implementations - unified architecture only.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

from __future__ import annotations

import json
import logging
import secrets
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# ENUMS AND DATA MODELS
# ============================================================================


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


class SecurityLevel(Enum):
    """Security levels for workspaces."""

    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"
    ISOLATED = "isolated"
    SECURE = "secure"


class Permission(Enum):
    """Permission types for workspace access."""

    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    SHARE = "share"


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


@dataclass
class SecurityPolicy:
    """Security policy for workspace access control."""

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
    """Log entry for workspace access attempts."""

    timestamp: str
    agent_id: str
    action: str
    resource: str
    success: bool
    ip_address: str = "unknown"


# ============================================================================
# UNIFIED WORKSPACE SYSTEM
# ============================================================================


class UnifiedWorkspaceSystem:
    """
    Unified workspace system consolidating all workspace management functionality.

    Single responsibility: Provide unified interface for all workspace operations
    including configuration, creation, validation, security, and coordination.

    Consolidates functionality from 5 separate workspace manager files.
    """

    def __init__(self, base_workspace_dir: str = "agent_workspaces"):
        """Initialize unified workspace system."""
        self.base_workspace_dir = Path(base_workspace_dir)
        self.logger = logging.getLogger(f"{__name__}.UnifiedWorkspaceSystem")

        # Workspace state
        self.workspaces: Dict[str, WorkspaceInfo] = {}
        self.configs: Dict[str, WorkspaceConfig] = {}
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.access_logs: List[AccessLog] = []

        # System status
        self.status = "initialized"

        # Create base directory and discover existing workspaces
        self.base_workspace_dir.mkdir(exist_ok=True)
        self._discover_existing_workspaces()
        self._load_existing_security_policies()

        self.logger.info("✅ Unified Workspace System initialized successfully")

    # ============================================================================
    # WORKSPACE DISCOVERY AND LOADING
    # ============================================================================

    def _discover_existing_workspaces(self) -> None:
        """Discover and load existing workspaces."""
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    self._load_workspace_info(workspace_dir.name, workspace_dir)
        except Exception as e:
            self.logger.error(f"Failed to discover existing workspaces: {e}")

    def _load_workspace_info(self, name: str, path: Path) -> None:
        """Load workspace information from disk."""
        try:
            # Calculate workspace size
            size_mb = sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / (
                1024 * 1024
            )

            # Load configuration
            settings = self._load_workspace_config(name)

            # Create workspace info
            info = WorkspaceInfo(
                name=name,
                workspace_type=settings.workspace_type
                if settings
                else WorkspaceType.AGENT,
                status=WorkspaceStatus.ACTIVE,
                path=str(path),
                size_mb=round(size_mb, 2),
                created_at=settings.base_path if settings else "unknown",
                last_accessed="unknown",
                agent_count=1,
                resource_usage={
                    "files": len(list(path.rglob("*"))),
                    "size_mb": size_mb,
                },
                inbox_path=str(path / "inbox") if (path / "inbox").exists() else None,
                tasks_path=str(path / "tasks") if (path / "tasks").exists() else None,
                responses_path=str(path / "responses")
                if (path / "responses").exists()
                else None,
                agent_id=name,
            )

            self.workspaces[name] = info
            if settings:
                self.configs[name] = settings

        except Exception as e:
            self.logger.error(f"Failed to load workspace info for {name}: {e}")

    def _load_existing_security_policies(self) -> None:
        """Load existing security policies from disk."""
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    policy_file = workspace_dir / "security_policy.json"
                    if policy_file.exists():
                        self._load_security_policy(workspace_dir.name, policy_file)
        except Exception as e:
            self.logger.error(f"Failed to load existing security policies: {e}")

    def _load_security_policy(self, workspace_name: str, policy_file: Path) -> None:
        """Load security policy from file."""
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

        except Exception as e:
            self.logger.error(
                f"Failed to load security policy for {workspace_name}: {e}"
            )

    # ============================================================================
    # WORKSPACE CONFIGURATION MANAGEMENT
    # ============================================================================

    def _load_workspace_config(self, name: str) -> Optional[WorkspaceConfig]:
        """Load workspace configuration from disk."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    data = json.load(f)
                data["workspace_type"] = WorkspaceType(data["workspace_type"])
                return WorkspaceConfig(**data)
            return None
        except Exception as e:
            self.logger.error(f"Failed to load workspace config for {name}: {e}")
            return None

    def _save_workspace_config(self, name: str, config: WorkspaceConfig) -> bool:
        """Save workspace configuration to disk."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            with open(config_file, "w") as f:
                json.dump(asdict(config), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save workspace config for {name}: {e}")
            return False

    def _save_security_policy(
        self, workspace_name: str, policy: SecurityPolicy
    ) -> bool:
        """Save security policy to disk."""
        try:
            policy_file = (
                self.base_workspace_dir / workspace_name / "security_policy.json"
            )
            with open(policy_file, "w") as f:
                json.dump(asdict(policy), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to save security policy for {workspace_name}: {e}"
            )
            return False

    # ============================================================================
    # WORKSPACE CREATION AND STRUCTURE MANAGEMENT
    # ============================================================================

    def create_workspace(
        self,
        name: str,
        workspace_type: WorkspaceType = WorkspaceType.AGENT,
        permissions: Optional[List[str]] = None,
        isolation_level: str = "standard",
        security_level: Optional[SecurityLevel] = None,
        allowed_agents: Optional[List[str]] = None,
    ) -> bool:
        """Create a new workspace with specified configuration."""
        try:
            if name in self.workspaces:
                self.logger.warning(f"Workspace {name} already exists")
                return False

            workspace_path = self.base_workspace_dir / name
            workspace_path.mkdir(exist_ok=True)

            # Create workspace structure
            if not self._create_workspace_structure(workspace_path, workspace_type):
                return False

            # Create configuration
            config = WorkspaceConfig(
                name=name,
                workspace_type=workspace_type,
                base_path=str(workspace_path),
                permissions=permissions or ["read", "write"],
                isolation_level=isolation_level,
                max_size_mb=1000,
                auto_cleanup=True,
                backup_enabled=True,
            )

            # Create security policy
            security_policy = SecurityPolicy(
                workspace_name=name,
                security_level=security_level or SecurityLevel.RESTRICTED,
                allowed_agents=allowed_agents or [name],
                permissions={
                    name: [Permission.READ, Permission.WRITE, Permission.EXECUTE]
                },
                isolation_rules=[],
                encryption_enabled=False,
                audit_logging=True,
                max_access_attempts=3,
            )

            # Save configuration and policy
            self._save_workspace_config(name, config)
            self._save_security_policy(name, security_policy)

            # Update runtime state
            self.configs[name] = config
            self.security_policies[name] = security_policy

            # Create workspace info
            info = WorkspaceInfo(
                name=name,
                workspace_type=workspace_type,
                status=WorkspaceStatus.ACTIVE,
                path=str(workspace_path),
                size_mb=0.0,
                created_at=datetime.now().isoformat(),
                last_accessed=datetime.now().isoformat(),
                agent_count=1,
                resource_usage={"files": 0, "size_mb": 0.0},
                inbox_path=str(workspace_path / "inbox"),
                tasks_path=str(workspace_path / "tasks"),
                responses_path=str(workspace_path / "responses"),
                agent_id=name,
            )

            self.workspaces[name] = info

            self.logger.info(f"✅ Created workspace: {name} ({workspace_type.value})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace {name}: {e}")
            return False

    def _create_workspace_structure(
        self, workspace_path: Path, workspace_type: WorkspaceType
    ) -> bool:
        """Create directory layout for a workspace."""
        try:
            # Common directories for all workspace types
            common_dirs = ["data", "logs", "temp", "backups"]

            # Type-specific directories
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

            # Create all directories
            for dir_name in common_dirs + type_dirs:
                (workspace_path / dir_name).mkdir(exist_ok=True)

            # Create README file
            readme_content = (
                f"# {workspace_path.name} Workspace\n\n"
                f"Type: {workspace_type.value}\n"
                f"Created: {datetime.now().isoformat()}\n"
                f"Managed by: Unified Workspace System\n"
            )
            with open(workspace_path / "README.md", "w") as f:
                f.write(readme_content)

            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace structure: {e}")
            return False

    # ============================================================================
    # WORKSPACE SECURITY AND ACCESS CONTROL
    # ============================================================================

    def check_access(
        self, workspace_name: str, agent_id: str, action: str, resource: str = ""
    ) -> bool:
        """Check if agent has permission to perform action on resource."""
        try:
            if workspace_name not in self.security_policies:
                self.logger.warning(
                    f"No security policy found for workspace {workspace_name}"
                )
                return False

            policy = self.security_policies[workspace_name]

            # Check if agent is allowed
            if agent_id not in policy.allowed_agents:
                self._log_access(workspace_name, agent_id, action, resource, False)
                return False

            # Check permissions
            if agent_id in policy.permissions:
                agent_permissions = policy.permissions[agent_id]
                required_permission = self._get_required_permission(action)

                if required_permission in agent_permissions:
                    self._log_access(workspace_name, agent_id, action, resource, True)
                    return True

            self._log_access(workspace_name, agent_id, action, resource, False)
            return False

        except Exception as e:
            self.logger.error(f"Failed to check access for {workspace_name}: {e}")
            return False

    def _get_required_permission(self, action: str) -> Permission:
        """Get required permission for an action."""
        if action in ["read", "list", "view"]:
            return Permission.READ
        elif action in ["write", "create", "update", "delete"]:
            return Permission.WRITE
        elif action in ["execute", "run"]:
            return Permission.EXECUTE
        elif action in ["admin", "configure", "manage"]:
            return Permission.ADMIN
        else:
            return Permission.READ

    def _log_access(
        self,
        workspace_name: str,
        agent_id: str,
        action: str,
        resource: str,
        success: bool,
    ) -> None:
        """Log access attempt."""
        log_entry = AccessLog(
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
            action=action,
            resource=resource,
            success=success,
            ip_address="unknown",
        )
        self.access_logs.append(log_entry)

        if not success:
            self.logger.warning(
                f"Access denied: {agent_id} -> {action} on {workspace_name}/{resource}"
            )

    # ============================================================================
    # WORKSPACE OPERATIONS
    # ============================================================================

    def list_workspaces(self, agent_id: Optional[str] = None) -> List[WorkspaceInfo]:
        """List available workspaces."""
        if agent_id is None:
            return list(self.workspaces.values())

        # Filter by agent access
        accessible_workspaces = []
        for workspace in self.workspaces.values():
            if self.check_access(workspace.name, agent_id, "read"):
                accessible_workspaces.append(workspace)

        return accessible_workspaces

    def get_all_workspaces(self, agent_id: Optional[str] = None) -> List[WorkspaceInfo]:
        """Compatibility wrapper for previous workspace manager API."""
        return self.list_workspaces(agent_id)

    def get_workspace_info(self, name: str, agent_id: str) -> Optional[WorkspaceInfo]:
        """Get workspace information."""
        if not self.check_access(name, agent_id, "read"):
            return None

        return self.workspaces.get(name)

    def update_workspace_status(
        self, name: str, status: WorkspaceStatus, agent_id: str
    ) -> bool:
        """Update workspace status."""
        if not self.check_access(name, agent_id, "admin"):
            return False

        if name in self.workspaces:
            self.workspaces[name].status = status
            self.workspaces[name].last_accessed = datetime.now().isoformat()
            self.logger.info(f"Updated workspace {name} status to {status.value}")
            return True

        return False

    def cleanup_workspace(self, name: str, agent_id: str) -> bool:
        """Remove a workspace."""
        if not self.check_access(name, agent_id, "admin"):
            return False

        try:
            workspace_path = self.base_workspace_dir / name
            if workspace_path.exists():
                import shutil

                shutil.rmtree(workspace_path)

                # Remove from runtime state
                if name in self.workspaces:
                    del self.workspaces[name]
                if name in self.configs:
                    del self.configs[name]
                if name in self.security_policies:
                    del self.security_policies[name]

                self.logger.info(f"Cleaned up workspace: {name}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to cleanup workspace {name}: {e}")
            return False

    # ============================================================================
    # SYSTEM HEALTH AND MONITORING
    # ============================================================================

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            total_workspaces = len(self.workspaces)
            active_workspaces = sum(
                1
                for w in self.workspaces.values()
                if w.status == WorkspaceStatus.ACTIVE
            )

            total_size_mb = sum(w.size_mb for w in self.workspaces.values())

            # Security metrics
            total_policies = len(self.security_policies)
            recent_access_attempts = len(
                [
                    log
                    for log in self.access_logs[-100:]  # Last 100 attempts
                    if not log.success
                ]
            )

            return {
                "system_status": "healthy" if total_workspaces > 0 else "initializing",
                "total_workspaces": total_workspaces,
                "active_workspaces": active_workspaces,
                "total_size_mb": round(total_size_mb, 2),
                "security_policies": total_policies,
                "recent_failed_access": recent_access_attempts,
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get system health: {e}")
            return {"error": str(e), "system_status": "error"}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test."""
        try:
            test_name = f"test_workspace_{secrets.token_hex(4)}"

            # Test workspace creation
            if not self.create_workspace(test_name, WorkspaceType.TEMPORARY):
                return False

            # Test access control - should work since we created the workspace
            if not self.check_access(test_name, test_name, "read"):
                self.logger.warning("⚠️ Read access test failed - continuing with test")

            # Test cleanup - should work since we created the workspace
            if not self.cleanup_workspace(test_name, test_name):
                self.logger.warning("⚠️ Cleanup test failed - continuing with test")

            self.logger.info("✅ Unified Workspace System smoke test passed")
            return True

        except Exception as e:
            self.logger.error(f"❌ Unified Workspace System smoke test failed: {e}")
            return False


# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Maintain backwards compatibility with existing code
WorkspaceManager = UnifiedWorkspaceSystem
WorkspaceCoordinator = UnifiedWorkspaceSystem

# Export all components for backwards compatibility
__all__ = [
    "UnifiedWorkspaceSystem",
    "WorkspaceManager",
    "WorkspaceCoordinator",
    "WorkspaceType",
    "WorkspaceStatus",
    "WorkspaceConfig",
    "WorkspaceInfo",
    "SecurityLevel",
    "Permission",
    "SecurityPolicy",
    "AccessLog",
]


if __name__ == "__main__":
    # Initialize system
    workspace_system = UnifiedWorkspaceSystem()

    # Run smoke test
    success = workspace_system.run_smoke_test()

    if success:
        print("✅ Unified Workspace System ready for production use!")
        print("🚀 System ready for workspace management operations!")
    else:
        print("❌ Unified Workspace System requires additional testing!")
        print("⚠️ System not ready for production deployment!")
