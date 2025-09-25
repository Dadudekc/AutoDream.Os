#!/usr/bin/env python3
"""
GitHub Protocol Service - Agent GitHub Operations
================================================

Comprehensive GitHub protocol service that integrates the GitHub controller
with the protocol database for full agent GitHub operations management.

V2 Compliance: ≤400 lines, comprehensive GitHub protocol service
Author: Agent-1 (Architecture Foundation Specialist)
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .github_protocol_models import (
    GitHubProtocolDatabase, GitHubOperation, GitHubOperationType,
    GitHubOperationStatus, GitHubPermissionLevel, GitHubAgentPermission,
    GitHubRepositoryConfig, GitHubWorkflowTemplate
)
from tools.github_agent_controller import GitHubAgentController, GitHubRepository, GitHubIssue, GitHubPullRequest


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
            auto_delete_branches=True
        )
        
        self.db.set_repository_config(default_config)
    
    def grant_agent_permission(self, agent_id: str, repository: str, 
                              permission_level: GitHubPermissionLevel,
                              granted_by: str = "Agent-4",
                              expires_at: datetime = None) -> bool:
        """Grant GitHub permission to agent."""
        permission = GitHubAgentPermission(
            agent_id=agent_id,
            repository=repository,
            permission_level=permission_level,
            granted_by=granted_by,
            granted_at=datetime.utcnow(),
            expires_at=expires_at
        )
        
        return self.db.grant_permission(permission)
    
    def check_agent_permission(self, agent_id: str, repository: str, 
                              required_level: GitHubPermissionLevel) -> bool:
        """Check if agent has required permission."""
        return self.db.check_permission(agent_id, repository, required_level)
    
    def create_repository(self, agent_id: str, name: str, description: str = "",
                         private: bool = False, auto_init: bool = True) -> Optional[GitHubRepository]:
        """Create repository with permission check and operation tracking."""
        operation_id = f"create_repo_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Check permission
        if not self.check_agent_permission(agent_id, name, GitHubPermissionLevel.ADMIN):
            self.logger.warning(f"Agent {agent_id} lacks permission to create repository {name}")
            return None
        
        # Create operation
        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_REPOSITORY,
            repository=name,
            parameters={
                "name": name,
                "description": description,
                "private": private,
                "auto_init": auto_init
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)
        
        try:
            # Execute GitHub operation
            repository = self.controller.create_repository(name, description, private, auto_init)
            
            # Update operation status
            self.db.update_operation_status(
                operation_id, 
                GitHubOperationStatus.COMPLETED,
                result_data=asdict(repository)
            )
            
            # Set repository configuration
            config = GitHubRepositoryConfig(
                repository=name,
                owner=self.controller.get_user_info()["login"],
                default_branch=repository.default_branch,
                protected_branches=[repository.default_branch],
                required_checks=["tests", "linting"]
            )
            self.db.set_repository_config(config)
            
            return repository
            
        except Exception as e:
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.FAILED,
                error_message=str(e)
            )
            self.logger.error(f"Failed to create repository {name}: {e}")
            return None
    
    def create_issue(self, agent_id: str, owner: str, repo: str, 
                    title: str, body: str = "", labels: List[str] = None,
                    assignees: List[str] = None) -> Optional[GitHubIssue]:
        """Create issue with permission check and operation tracking."""
        operation_id = f"create_issue_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Check permission
        if not self.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create issue in {repo}")
            return None
        
        # Create operation
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
                "assignees": assignees or []
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)
        
        try:
            # Execute GitHub operation
            issue = self.controller.create_issue(owner, repo, title, body, labels, assignees)
            
            # Update operation status
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED,
                result_data=asdict(issue)
            )
            
            return issue
            
        except Exception as e:
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.FAILED,
                error_message=str(e)
            )
            self.logger.error(f"Failed to create issue in {repo}: {e}")
            return None
    
    def create_pull_request(self, agent_id: str, owner: str, repo: str,
                           title: str, head_branch: str, base_branch: str,
                           body: str = "") -> Optional[GitHubPullRequest]:
        """Create pull request with permission check and operation tracking."""
        operation_id = f"create_pr_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Check permission
        if not self.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create PR in {repo}")
            return None
        
        # Create operation
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
                "body": body
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)
        
        try:
            # Execute GitHub operation
            pr = self.controller.create_pull_request(owner, repo, title, head_branch, base_branch, body)
            
            # Update operation status
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED,
                result_data=asdict(pr)
            )
            
            return pr
            
        except Exception as e:
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.FAILED,
                error_message=str(e)
            )
            self.logger.error(f"Failed to create PR in {repo}: {e}")
            return None
    
    def create_file(self, agent_id: str, owner: str, repo: str, path: str,
                   content: str, message: str, branch: str = None) -> bool:
        """Create file with permission check and operation tracking."""
        operation_id = f"create_file_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Check permission
        if not self.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create file in {repo}")
            return False
        
        # Create operation
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
                "branch": branch
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)
        
        try:
            # Execute GitHub operation
            success = self.controller.create_file(owner, repo, path, content, message, branch)
            
            # Update operation status
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED if success else GitHubOperationStatus.FAILED,
                result_data={"success": success}
            )
            
            return success
            
        except Exception as e:
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.FAILED,
                error_message=str(e)
            )
            self.logger.error(f"Failed to create file {path} in {repo}: {e}")
            return False
    
    def create_branch(self, agent_id: str, owner: str, repo: str,
                     branch_name: str, from_branch: str = "main") -> bool:
        """Create branch with permission check and operation tracking."""
        operation_id = f"create_branch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Check permission
        if not self.check_agent_permission(agent_id, repo, GitHubPermissionLevel.WRITE):
            self.logger.warning(f"Agent {agent_id} lacks permission to create branch in {repo}")
            return False
        
        # Create operation
        operation = GitHubOperation(
            operation_id=operation_id,
            agent_id=agent_id,
            operation_type=GitHubOperationType.CREATE_BRANCH,
            repository=repo,
            parameters={
                "owner": owner,
                "repo": repo,
                "branch_name": branch_name,
                "from_branch": from_branch
            },
            status=GitHubOperationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        self.db.create_operation(operation)
        self.db.update_operation_status(operation_id, GitHubOperationStatus.IN_PROGRESS)
        
        try:
            # Execute GitHub operation
            success = self.controller.create_branch(owner, repo, branch_name, from_branch)
            
            # Update operation status
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.COMPLETED if success else GitHubOperationStatus.FAILED,
                result_data={"success": success}
            )
            
            return success
            
        except Exception as e:
            self.db.update_operation_status(
                operation_id,
                GitHubOperationStatus.FAILED,
                error_message=str(e)
            )
            self.logger.error(f"Failed to create branch {branch_name} in {repo}: {e}")
            return False
    
    def get_agent_operations(self, agent_id: str, 
                            status: GitHubOperationStatus = None) -> List[GitHubOperation]:
        """Get operations for specific agent."""
        return self.db.get_agent_operations(agent_id, status)
    
    def get_audit_logs(self, agent_id: str = None, repository: str = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit logs with filters."""
        logs = self.db.get_audit_logs(agent_id, repository, limit)
        return [asdict(log) for log in logs]
    
    def create_workflow_template(self, template_id: str, name: str, description: str,
                                workflow_type: str, template_content: str,
                                parameters: Dict[str, Any], created_by: str) -> bool:
        """Create workflow template."""
        template = GitHubWorkflowTemplate(
            template_id=template_id,
            name=name,
            description=description,
            workflow_type=workflow_type,
            template_content=template_content,
            parameters=parameters,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        return self.db.create_workflow_template(template)
    
    def get_workflow_template(self, template_id: str) -> Optional[GitHubWorkflowTemplate]:
        """Get workflow template."""
        return self.db.get_workflow_template(template_id)
    
    def set_repository_config(self, config: GitHubRepositoryConfig) -> bool:
        """Set repository configuration."""
        return self.db.set_repository_config(config)
    
    def get_repository_config(self, repository: str) -> Optional[GitHubRepositoryConfig]:
        """Get repository configuration."""
        return self.db.get_repository_config(repository)
    
    def export_protocol_data(self) -> Dict[str, Any]:
        """Export all protocol data."""
        return self.db.export_data()
    
    def import_protocol_data(self, data: Dict[str, Any]) -> bool:
        """Import protocol data."""
        return self.db.import_data(data)


def create_github_protocol_service(github_token: str) -> GitHubProtocolService:
    """Create GitHub protocol service instance."""
    return GitHubProtocolService(github_token)


if __name__ == "__main__":
    # Example usage
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        exit(1)
    
    service = create_github_protocol_service(token)
    
    # Grant permission to Agent-1
    service.grant_agent_permission(
        "Agent-1", 
        "test-repo", 
        GitHubPermissionLevel.ADMIN
    )
    
    print(f"✅ Permission granted: {service.check_agent_permission('Agent-1', 'test-repo', GitHubPermissionLevel.WRITE)}")
    
    # Create repository
    repo = service.create_repository(
        "Agent-1",
        "agent-test-repo",
        "Test repository created by Agent-1",
        private=False
    )
    
    if repo:
        print(f"✅ Repository created: {repo.name}")
    else:
        print("❌ Failed to create repository")
    
    # Get operations
    operations = service.get_agent_operations("Agent-1")
    print(f"📊 Agent-1 operations: {len(operations)}")
    
    # Export data
    exported = service.export_protocol_data()
    print(f"📊 Protocol data exported: {len(exported['operations'])} operations")

