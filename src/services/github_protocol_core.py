#!/usr/bin/env python3
"""
GitHub Protocol Core - Main Service Class
==========================================

Core GitHub protocol service class with initialization and permission management.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: github_protocol_service.py (485 lines) - Split into 3 modules
"""

import logging
from datetime import datetime
from typing import Any

from tools.github_agent_controller import GitHubAgentController

from .github_protocol_models import (
    GitHubAgentPermission,
    GitHubPermissionLevel,
    GitHubProtocolDatabase,
    GitHubRepositoryConfig,
)


class GitHubProtocolService:
    """
    GitHub Protocol Service for agent operations.

    Integrates GitHub controller with protocol database to provide:
    - Permission-based GitHub operations
    - Operation tracking and audit logging
    - Repository configuration management
    - Workflow template management
    """

    def __init__(self, github_token: str, db_path: str = "github_protocol.db"):
        """Initialize GitHub protocol service."""
        self.controller = GitHubAgentController(github_token)
        self.db = GitHubProtocolDatabase(db_path)
        self.logger = logging.getLogger(f"{__name__}.GitHubProtocolService")

        # Initialize default configurations
        self._initialize_default_configs()

    def _initialize_default_configs(self):
        """Initialize default repository configurations."""
        default_config = GitHubRepositoryConfig(
            repository="default",
            owner="default",
            default_branch="main",
            protected_branches=["main", "develop"],
            required_checks=["tests", "linting"],
            auto_merge_enabled=False,
            auto_delete_branches=True,
        )

        self.db.set_repository_config(default_config)

    def grant_agent_permission(
        self,
        agent_id: str,
        repository: str,
        permission_level: GitHubPermissionLevel,
        granted_by: str = "Agent-4",
        expires_at: datetime = None,
    ) -> bool:
        """Grant GitHub permission to agent."""
        permission = GitHubAgentPermission(
            agent_id=agent_id,
            repository=repository,
            permission_level=permission_level,
            granted_by=granted_by,
            granted_at=datetime.utcnow(),
            expires_at=expires_at,
        )

        return self.db.grant_permission(permission)

    def check_agent_permission(
        self, agent_id: str, repository: str, required_level: GitHubPermissionLevel
    ) -> bool:
        """Check if agent has required permission."""
        return self.db.check_permission(agent_id, repository, required_level)

    def get_agent_operations(self, agent_id: str, status=None):
        """Get operations for specific agent."""
        return self.db.get_agent_operations(agent_id, status)

    def get_audit_logs(
        self, agent_id: str = None, repository: str = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Get audit logs with filters."""
        from dataclasses import asdict

        logs = self.db.get_audit_logs(agent_id, repository, limit)
        return [asdict(log) for log in logs]

    def set_repository_config(self, config: GitHubRepositoryConfig) -> bool:
        """Set repository configuration."""
        return self.db.set_repository_config(config)

    def get_repository_config(self, repository: str) -> GitHubRepositoryConfig | None:
        """Get repository configuration."""
        return self.db.get_repository_config(repository)

    def export_protocol_data(self) -> dict[str, Any]:
        """Export all protocol data."""
        return self.db.export_data()

    def import_protocol_data(self, data: dict[str, Any]) -> bool:
        """Import protocol data."""
        return self.db.import_data(data)


def create_github_protocol_service(github_token: str) -> GitHubProtocolService:
    """Create GitHub protocol service instance."""
    return GitHubProtocolService(github_token)


__all__ = ["GitHubProtocolService", "create_github_protocol_service"]
