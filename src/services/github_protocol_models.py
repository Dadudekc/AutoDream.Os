#!/usr/bin/env python3
"""
GitHub Protocol Models - Unified Interface
==========================================

Unified interface for GitHub protocol models.
Provides backward compatibility and easy access to all GitHub protocol components.

V2 Compliance: ≤400 lines, unified interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

from .github_protocol_data_models import (
    GitHubAgentPermission,
    GitHubAuditLog,
    GitHubOperation,
    GitHubRepositoryConfig,
    GitHubWorkflowTemplate,
)

# Import all components from modular structure
from .github_protocol_database import GitHubProtocolDatabase, create_github_protocol_db
from .github_protocol_enums import GitHubOperationStatus, GitHubOperationType, GitHubPermissionLevel

# Re-export all components for backward compatibility
__all__ = [
    # Enums
    "GitHubOperationType",
    "GitHubPermissionLevel",
    "GitHubOperationStatus",
    # Data Models
    "GitHubAgentPermission",
    "GitHubOperation",
    "GitHubAuditLog",
    "GitHubRepositoryConfig",
    "GitHubWorkflowTemplate",
    # Database
    "GitHubProtocolDatabase",
    "create_github_protocol_db",
]
