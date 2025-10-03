#!/usr/bin/env python3
"""
GitHub Protocol Enums - Core Enumerations
=========================================

Core enumerations for GitHub protocol operations.
Defines operation types, permission levels, and status values.

V2 Compliance: ≤400 lines, focused enumerations module
Author: Agent-6 (Quality Assurance Specialist)
"""

from enum import Enum


class GitHubOperationType(Enum):
    """GitHub operation types."""

    CREATE_REPOSITORY = "create_repository"
    DELETE_REPOSITORY = "delete_repository"
    CREATE_ISSUE = "create_issue"
    UPDATE_ISSUE = "update_issue"
    CLOSE_ISSUE = "close_issue"
    CREATE_PULL_REQUEST = "create_pull_request"
    MERGE_PULL_REQUEST = "merge_pull_request"
    CREATE_BRANCH = "create_branch"
    DELETE_BRANCH = "delete_branch"
    CREATE_FILE = "create_file"
    UPDATE_FILE = "update_file"
    DELETE_FILE = "delete_file"
    SEARCH_REPOSITORIES = "search_repositories"
    LIST_ISSUES = "list_issues"
    LIST_PULL_REQUESTS = "list_pull_requests"


class GitHubPermissionLevel(Enum):
    """GitHub permission levels."""

    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    OWNER = "owner"


class GitHubOperationStatus(Enum):
    """GitHub operation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


__all__ = ["GitHubOperationType", "GitHubPermissionLevel", "GitHubOperationStatus"]

