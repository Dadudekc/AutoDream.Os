#!/usr/bin/env python3
"""
GitHub Protocol Operations - GitHub Operations
===============================================

GitHub operations including repositories, issues, PRs, files, and branches.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: github_protocol_service.py (485 lines) - Operations module
"""

import logging
from dataclasses import asdict
from datetime import datetime

from tools.github_agent_controller import GitHubIssue, GitHubPullRequest, GitHubRepository

from .github_protocol_models import (
    GitHubOperation,
    GitHubOperationStatus,
    GitHubOperationType,
    GitHubPermissionLevel,
)


class GitHubOperations:
    """GitHub operations handler for protocol service."""

    def __init__(self, service):
        """Initialize operations handler."""
        self.service = service
        self.controller = service.controller
        self.db = service.db
        self.logger = logging.getLogger(f"{__name__}.GitHubOperations")

    def create_repository(
        self,
        agent_id: str,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True,
    ) -> GitHubRepository | None:
        """Create repository with permission check and operation tracking."""
        operation_id = f"create_repo_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not self.service.check_agent_permission(agent_id, name, GitHubPermissionLevel.ADMIN):
            self.logger.warning(f"Agent {agent_id} lacks permission to create repository {name}")
            return None

        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_REPOSITORY,
            repository=name,
            parameters={
                "name": name,
                "description": description,
                "private": private,
                "auto_init": auto_init,
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow(),
        )

        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)

        try:
            repository = self.controller.create_repository(name, description, private, auto_init)
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.COMPLETED, result_data=asdict(repository)
            )

            config = GitHubRepositoryConfig(
                repository=name,
                owner=self.controller.get_user_info()["login"],
                default_branch=repository.default_branch,
                protected_branches=[repository.default_branch],
                required_checks=["tests", "linting"],
            )
            self.db.set_repository_config(config)

            return repository

        except Exception as e:
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.FAILED, error_message=str(e)
            )
            self.logger.error(f"Failed to create repository {name}: {e}")
            return None

    def create_issue(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] = None,
        assignees: list[str] = None,
    ) -> GitHubIssue | None:
        """Create issue with permission check and operation tracking."""
        operation_id = f"create_issue_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not self.service.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create issue in {repo}")
            return None

        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_ISSUE,
            repository=repo,
            parameters={
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body,
                "labels": labels or [],
                "assignees": assignees or [],
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow(),
        )

        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)

        try:
            issue = self.controller.create_issue(owner, repo, title, body, labels, assignees)
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.COMPLETED, result_data=asdict(issue)
            )
            return issue

        except Exception as e:
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.FAILED, error_message=str(e)
            )
            self.logger.error(f"Failed to create issue in {repo}: {e}")
            return None

    def create_pull_request(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        title: str,
        head_branch: str,
        base_branch: str,
        body: str = "",
    ) -> GitHubPullRequest | None:
        """Create pull request with permission check and operation tracking."""
        operation_id = f"create_pr_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not self.service.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create PR in {repo}")
            return None

        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_PULL_REQUEST,
            repository=repo,
            parameters={
                "owner": owner,
                "repo": repo,
                "title": title,
                "head_branch": head_branch,
                "base_branch": base_branch,
                "body": body,
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow(),
        )

        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)

        try:
            pr = self.controller.create_pull_request(
                owner, repo, title, head_branch, base_branch, body
            )
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.COMPLETED, result_data=asdict(pr)
            )
            return pr

        except Exception as e:
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.FAILED, error_message=str(e)
            )
            self.logger.error(f"Failed to create PR in {repo}: {e}")
            return None

    def create_file(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str = None,
    ) -> bool:
        """Create file with permission check and operation tracking."""
        operation_id = f"create_file_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not self.service.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create file in {repo}")
            return False

        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_FILE,
            repository=repo,
            parameters={
                "owner": owner,
                "repo": repo,
                "path": path,
                "content": content,
                "message": message,
                "branch": branch,
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow(),
        )

        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)

        try:
            success = self.controller.create_file(owner, repo, path, content, message, branch)
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED if success else GitHubOperationStatus.FAILED,
                result_data={"success": success},
            )
            return success

        except Exception as e:
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.FAILED, error_message=str(e)
            )
            self.logger.error(f"Failed to create file {path} in {repo}: {e}")
            return False

    def create_branch(
        self, agent_id: str, owner: str, repo: str, branch_name: str, from_branch: str = "main"
    ) -> bool:
        """Create branch with permission check and operation tracking."""
        operation_id = f"create_branch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not self.service.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create branch in {repo}")
            return False

        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_BRANCH,
            repository=repo,
            parameters={
                "owner": owner,
                "repo": repo,
                "branch_name": branch_name,
                "from_branch": from_branch,
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow(),
        )

        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)

        try:
            success = self.controller.create_branch(owner, repo, branch_name, from_branch)
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED if success else GitHubOperationStatus.FAILED,
                result_data={"success": success},
            )
            return success

        except Exception as e:
            self.db.update_operation_status(
                operation_id, GitHubOperationStatus.FAILED, error_message=str(e)
            )
            self.logger.error(f"Failed to create branch {branch_name} in {repo}: {e}")
            return False


__all__ = ["GitHubProtocolService"]
