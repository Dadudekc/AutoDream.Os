#!/usr/bin/env python3
"""
GitHub Protocol Data Models - Core Data Structures
=================================================

Core data models for GitHub protocol operations.
Defines the structure for permissions, operations, and audit logs.

V2 Compliance: ≤400 lines, focused data models module
Author: Agent-6 (Quality Assurance Specialist)
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from .github_protocol_enums import GitHubOperationStatus, GitHubPermissionLevel


@dataclass
class GitHubAgentPermission:
    """GitHub agent permission record."""

    agent_id: str
    repository: str
    permission_level: GitHubPermissionLevel
    granted_by: str
    granted_at: datetime
    expires_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GitHubOperation:
    """GitHub operation record."""

    operation_id: str
    agent_id: str
    operation_type: str
    repository: str
    status: GitHubOperationStatus
    created_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GitHubAuditLog:
    """GitHub audit log record."""

    log_id: str
    agent_id: str
    operation_id: str
    repository: str
    action: str
    timestamp: datetime
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GitHubRepositoryConfig:
    """GitHub repository configuration."""

    repository: str
    auto_approve_operations: bool = False
    require_approval_for: list[str] | None = None
    max_operations_per_hour: int = 100
    allowed_agents: list[str] | None = None
    notification_settings: dict[str, Any] | None = None
    workflow_templates: list[str] | None = None
    security_settings: dict[str, Any] | None = None
    backup_settings: dict[str, Any] | None = None
    monitoring_settings: dict[str, Any] | None = None
    compliance_settings: dict[str, Any] | None = None
    integration_settings: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GitHubWorkflowTemplate:
    """GitHub workflow template."""

    template_id: str
    name: str
    description: str
    workflow_type: str
    template_content: str
    parameters: dict[str, Any]
    created_by: str
    created_at: datetime
    is_active: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


__all__ = [
    "GitHubAgentPermission",
    "GitHubOperation",
    "GitHubAuditLog",
    "GitHubRepositoryConfig",
    "GitHubWorkflowTemplate",
]


