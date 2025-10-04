#!/usr/bin/env python3
"""
GitHub Protocol Database - Database Operations
=============================================

Database operations for GitHub protocol management.
Handles permissions, operations, audit logs, and configurations.

V2 Compliance: ≤400 lines, focused database operations module
Author: Agent-6 (Quality Assurance Specialist)
"""

from datetime import datetime
from typing import Any

from .github_protocol_data_models import (
    GitHubAgentPermission,
    GitHubAuditLog,
    GitHubOperation,
    GitHubOperationStatus,
    GitHubPermissionLevel,
    GitHubRepositoryConfig,
    GitHubWorkflowTemplate,
)


class GitHubProtocolDatabase:
    """
    GitHub protocol database operations.

    Manages GitHub operations, permissions, and audit logs.
    """

    def __init__(self, db_path: str = "github_protocol.db"):
        """Initialize GitHub protocol database."""
        self.db_path = db_path
        self.permissions: dict[str, GitHubAgentPermission] = {}
        self.operations: dict[str, GitHubOperation] = {}
        self.audit_logs: list[GitHubAuditLog] = []
        self.repository_configs: dict[str, GitHubRepositoryConfig] = {}
        self.workflow_templates: dict[str, GitHubWorkflowTemplate] = {}

    def grant_permission(self, permission: GitHubAgentPermission) -> bool:
        """Grant GitHub permission to agent."""
        try:
            key = f"{permission.agent_id}:{permission.repository}"
            self.permissions[key] = permission

            # Log permission grant
            self._log_audit(
                permission.agent_id,
                "permission_granted",
                permission.repository,
                {"permission_level": permission.permission_level.value},
            )

            return True
        except Exception:
            return False

    def revoke_permission(self, agent_id: str, repository: str) -> bool:
        """Revoke GitHub permission from agent."""
        try:
            key = f"{agent_id}:{repository}"
            if key in self.permissions:
                permission = self.permissions[key]
                # Note: GitHubAgentPermission doesn't have is_active field in our model
                del self.permissions[key]

                # Log permission revocation
                self._log_audit(
                    agent_id,
                    "permission_revoked",
                    repository,
                    {"permission_level": permission.permission_level.value},
                )

                return True
            return False
        except Exception:
            return False

    def check_permission(
        self, agent_id: str, repository: str, required_level: GitHubPermissionLevel
    ) -> bool:
        """Check if agent has required permission level."""
        key = f"{agent_id}:{repository}"

        if key not in self.permissions:
            return False

        permission = self.permissions[key]

        if permission.expires_at and permission.expires_at < datetime.utcnow():
            return False

        # Check permission level hierarchy
        level_hierarchy = {
            GitHubPermissionLevel.READ: 1,
            GitHubPermissionLevel.WRITE: 2,
            GitHubPermissionLevel.ADMIN: 3,
            GitHubPermissionLevel.OWNER: 4,
        }

        return level_hierarchy[permission.permission_level] >= level_hierarchy[required_level]

    def create_operation(self, operation: GitHubOperation) -> bool:
        """Create new GitHub operation."""
        try:
            self.operations[operation.operation_id] = operation

            # Log operation creation
            self._log_audit(
                operation.agent_id,
                "operation_created",
                operation.repository,
                {
                    "operation_type": operation.operation_type,
                    "operation_id": operation.operation_id,
                },
            )

            return True
        except Exception:
            return False

    def update_operation_status(
        self,
        operation_id: str,
        status: GitHubOperationStatus,
        error_message: str = None,
        result_data: dict[str, Any] = None,
    ) -> bool:
        """Update operation status."""
        try:
            if operation_id not in self.operations:
                return False

            operation = self.operations[operation_id]
            operation.status = status

            if status in [GitHubOperationStatus.COMPLETED, GitHubOperationStatus.FAILED]:
                operation.completed_at = datetime.utcnow()

            if error_message:
                operation.error_message = error_message

            if result_data:
                operation.metadata = result_data

            # Log status update
            self._log_audit(
                operation.agent_id,
                "operation_status_updated",
                operation.repository,
                {
                    "operation_id": operation_id,
                    "status": status.value,
                    "error_message": error_message,
                },
            )

            return True
        except Exception:
            return False

    def get_agent_operations(
        self, agent_id: str, status: GitHubOperationStatus = None
    ) -> list[GitHubOperation]:
        """Get operations for specific agent."""
        operations = [op for op in self.operations.values() if op.agent_id == agent_id]

        if status:
            operations = [op for op in operations if op.status == status]

        return sorted(operations, key=lambda x: x.created_at, reverse=True)

    def get_repository_config(self, repository: str) -> GitHubRepositoryConfig | None:
        """Get repository configuration."""
        return self.repository_configs.get(repository)

    def set_repository_config(self, config: GitHubRepositoryConfig) -> bool:
        """Set repository configuration."""
        try:
            self.repository_configs[config.repository] = config

            # Log config update
            self._log_audit(
                "system",
                "repository_config_updated",
                config.repository,
                {"config_keys": list(config.__dict__.keys())},
            )

            return True
        except Exception:
            return False

    def create_workflow_template(self, template: GitHubWorkflowTemplate) -> bool:
        """Create workflow template."""
        try:
            self.workflow_templates[template.template_id] = template

            # Log template creation
            self._log_audit(
                template.created_by,
                "workflow_template_created",
                "system",
                {"template_id": template.template_id, "template_name": template.name},
            )

            return True
        except Exception:
            return False

    def get_workflow_template(self, template_id: str) -> GitHubWorkflowTemplate | None:
        """Get workflow template."""
        return self.workflow_templates.get(template_id)

    def _log_audit(
        self, agent_id: str, action: str, repository: str, details: dict[str, Any]
    ) -> None:
        """Log audit event."""
        log_entry = GitHubAuditLog(
            log_id=f"log_{len(self.audit_logs) + 1}",
            agent_id=agent_id,
            operation_id="",
            action=action,
            repository=repository,
            details=details,
            timestamp=datetime.utcnow(),
        )

        self.audit_logs.append(log_entry)

    def get_audit_logs(
        self, agent_id: str = None, repository: str = None, limit: int = 100
    ) -> list[GitHubAuditLog]:
        """Get audit logs with filters."""
        logs = self.audit_logs

        if agent_id:
            logs = [log for log in logs if log.agent_id == agent_id]

        if repository:
            logs = [log for log in logs if log.repository == repository]

        return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]

    def export_data(self) -> dict[str, Any]:
        """Export all database data."""
        return {
            "permissions": {k: v.to_dict() for k, v in self.permissions.items()},
            "operations": {k: v.to_dict() for k, v in self.operations.items()},
            "audit_logs": [log.to_dict() for log in self.audit_logs],
            "repository_configs": {k: v.to_dict() for k, v in self.repository_configs.items()},
            "workflow_templates": {k: v.to_dict() for k, v in self.workflow_templates.items()},
        }

    def import_data(self, data: dict[str, Any]) -> bool:
        """Import database data."""
        try:
            # Import permissions
            for k, v in data.get("permissions", {}).items():
                v["permission_level"] = GitHubPermissionLevel(v["permission_level"])
                v["granted_at"] = datetime.fromisoformat(v["granted_at"])
                if v.get("expires_at"):
                    v["expires_at"] = datetime.fromisoformat(v["expires_at"])
                self.permissions[k] = GitHubAgentPermission(**v)

            # Import operations
            for k, v in data.get("operations", {}).items():
                v["status"] = GitHubOperationStatus(v["status"])
                v["created_at"] = datetime.fromisoformat(v["created_at"])
                if v.get("completed_at"):
                    v["completed_at"] = datetime.fromisoformat(v["completed_at"])
                self.operations[k] = GitHubOperation(**v)

            # Import audit logs
            for log_data in data.get("audit_logs", []):
                log_data["timestamp"] = datetime.fromisoformat(log_data["timestamp"])
                self.audit_logs.append(GitHubAuditLog(**log_data))

            # Import repository configs
            for k, v in data.get("repository_configs", {}).items():
                self.repository_configs[k] = GitHubRepositoryConfig(**v)

            # Import workflow templates
            for k, v in data.get("workflow_templates", {}).items():
                v["created_at"] = datetime.fromisoformat(v["created_at"])
                self.workflow_templates[k] = GitHubWorkflowTemplate(**v)

            return True
        except Exception:
            return False


def create_github_protocol_db() -> GitHubProtocolDatabase:
    """Create GitHub protocol database instance."""
    return GitHubProtocolDatabase()


__all__ = ["GitHubProtocolDatabase", "create_github_protocol_db"]

