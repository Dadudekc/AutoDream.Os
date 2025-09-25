#!/usr/bin/env python3
"""
GitHub Protocol Database Models
==============================

Database models and schema for GitHub operations protocol.
Defines the structure for storing GitHub operations, permissions, and audit logs.

V2 Compliance: ≤400 lines, comprehensive GitHub protocol models
Author: Agent-1 (Architecture Foundation Specialist)
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json


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


@dataclass
class GitHubAgentPermission:
    """GitHub agent permission model."""
    agent_id: str
    repository: str
    permission_level: GitHubPermissionLevel
    granted_by: str
    granted_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    notes: str = ""


@dataclass
class GitHubOperation:
    """GitHub operation model."""
    operation_id: str
    agent_id: str
    operation_type: GitHubOperationType
    repository: str
    parameters: Dict[str, Any]
    status: GitHubOperationStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result_data: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class GitHubAuditLog:
    """GitHub audit log model."""
    log_id: str
    agent_id: str
    operation_id: str
    action: str
    repository: str
    details: Dict[str, Any]
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class GitHubRepositoryConfig:
    """GitHub repository configuration model."""
    repository: str
    owner: str
    default_branch: str
    protected_branches: List[str]
    required_checks: List[str]
    auto_merge_enabled: bool = False
    auto_delete_branches: bool = True
    issue_templates: List[str] = None
    pr_templates: List[str] = None
    webhook_urls: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.issue_templates is None:
            self.issue_templates = []
        if self.pr_templates is None:
            self.pr_templates = []
        if self.webhook_urls is None:
            self.webhook_urls = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class GitHubWorkflowTemplate:
    """GitHub workflow template model."""
    template_id: str
    name: str
    description: str
    workflow_type: str
    template_content: str
    parameters: Dict[str, Any]
    created_by: str
    created_at: datetime
    is_active: bool = True
    usage_count: int = 0


class GitHubProtocolDatabase:
    """
    GitHub protocol database operations.
    
    Manages GitHub operations, permissions, and audit logs.
    """
    
    def __init__(self, db_path: str = "github_protocol.db"):
        """Initialize GitHub protocol database."""
        self.db_path = db_path
        self.permissions: Dict[str, GitHubAgentPermission] = {}
        self.operations: Dict[str, GitHubOperation] = {}
        self.audit_logs: List[GitHubAuditLog] = []
        self.repository_configs: Dict[str, GitHubRepositoryConfig] = {}
        self.workflow_templates: Dict[str, GitHubWorkflowTemplate] = {}
    
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
                {"permission_level": permission.permission_level.value}
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
                permission.is_active = False
                
                # Log permission revocation
                self._log_audit(
                    agent_id,
                    "permission_revoked",
                    repository,
                    {"permission_level": permission.permission_level.value}
                )
                
                return True
            return False
        except Exception:
            return False
    
    def check_permission(self, agent_id: str, repository: str, 
                        required_level: GitHubPermissionLevel) -> bool:
        """Check if agent has required permission level."""
        key = f"{agent_id}:{repository}"
        
        if key not in self.permissions:
            return False
        
        permission = self.permissions[key]
        
        if not permission.is_active:
            return False
        
        if permission.expires_at and permission.expires_at < datetime.utcnow():
            return False
        
        # Check permission level hierarchy
        level_hierarchy = {
            GitHubPermissionLevel.READ: 1,
            GitHubPermissionLevel.WRITE: 2,
            GitHubPermissionLevel.ADMIN: 3,
            GitHubPermissionLevel.OWNER: 4
        }
        
        return (level_hierarchy[permission.permission_level] >= 
                level_hierarchy[required_level])
    
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
                    "operation_type": operation.operation_type.value,
                    "operation_id": operation.operation_id
                }
            )
            
            return True
        except Exception:
            return False
    
    def update_operation_status(self, operation_id: str, 
                               status: GitHubOperationStatus,
                               error_message: str = None,
                               result_data: Dict[str, Any] = None) -> bool:
        """Update operation status."""
        try:
            if operation_id not in self.operations:
                return False
            
            operation = self.operations[operation_id]
            operation.status = status
            
            if status == GitHubOperationStatus.IN_PROGRESS:
                operation.started_at = datetime.utcnow()
            elif status in [GitHubOperationStatus.COMPLETED, GitHubOperationStatus.FAILED]:
                operation.completed_at = datetime.utcnow()
            
            if error_message:
                operation.error_message = error_message
            
            if result_data:
                operation.result_data = result_data
            
            # Log status update
            self._log_audit(
                operation.agent_id,
                "operation_status_updated",
                operation.repository,
                {
                    "operation_id": operation_id,
                    "status": status.value,
                    "error_message": error_message
                }
            )
            
            return True
        except Exception:
            return False
    
    def get_agent_operations(self, agent_id: str, 
                            status: GitHubOperationStatus = None) -> List[GitHubOperation]:
        """Get operations for specific agent."""
        operations = [
            op for op in self.operations.values() 
            if op.agent_id == agent_id
        ]
        
        if status:
            operations = [op for op in operations if op.status == status]
        
        return sorted(operations, key=lambda x: x.created_at, reverse=True)
    
    def get_repository_config(self, repository: str) -> Optional[GitHubRepositoryConfig]:
        """Get repository configuration."""
        return self.repository_configs.get(repository)
    
    def set_repository_config(self, config: GitHubRepositoryConfig) -> bool:
        """Set repository configuration."""
        try:
            config.updated_at = datetime.utcnow()
            self.repository_configs[config.repository] = config
            
            # Log config update
            self._log_audit(
                "system",
                "repository_config_updated",
                config.repository,
                {"config_keys": list(config.__dict__.keys())}
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
                {
                    "template_id": template.template_id,
                    "template_name": template.name
                }
            )
            
            return True
        except Exception:
            return False
    
    def get_workflow_template(self, template_id: str) -> Optional[GitHubWorkflowTemplate]:
        """Get workflow template."""
        return self.workflow_templates.get(template_id)
    
    def increment_template_usage(self, template_id: str) -> bool:
        """Increment workflow template usage count."""
        try:
            if template_id in self.workflow_templates:
                self.workflow_templates[template_id].usage_count += 1
                return True
            return False
        except Exception:
            return False
    
    def _log_audit(self, agent_id: str, action: str, repository: str, 
                   details: Dict[str, Any]) -> None:
        """Log audit event."""
        log_entry = GitHubAuditLog(
            log_id=f"log_{len(self.audit_logs) + 1}",
            agent_id=agent_id,
            operation_id="",
            action=action,
            repository=repository,
            details=details,
            timestamp=datetime.utcnow()
        )
        
        self.audit_logs.append(log_entry)
    
    def get_audit_logs(self, agent_id: str = None, 
                      repository: str = None,
                      limit: int = 100) -> List[GitHubAuditLog]:
        """Get audit logs with filters."""
        logs = self.audit_logs
        
        if agent_id:
            logs = [log for log in logs if log.agent_id == agent_id]
        
        if repository:
            logs = [log for log in logs if log.repository == repository]
        
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def export_data(self) -> Dict[str, Any]:
        """Export all database data."""
        return {
            "permissions": {k: asdict(v) for k, v in self.permissions.items()},
            "operations": {k: asdict(v) for k, v in self.operations.items()},
            "audit_logs": [asdict(log) for log in self.audit_logs],
            "repository_configs": {k: asdict(v) for k, v in self.repository_configs.items()},
            "workflow_templates": {k: asdict(v) for k, v in self.workflow_templates.items()}
        }
    
    def import_data(self, data: Dict[str, Any]) -> bool:
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
                v["operation_type"] = GitHubOperationType(v["operation_type"])
                v["status"] = GitHubOperationStatus(v["status"])
                v["created_at"] = datetime.fromisoformat(v["created_at"])
                if v.get("started_at"):
                    v["started_at"] = datetime.fromisoformat(v["started_at"])
                if v.get("completed_at"):
                    v["completed_at"] = datetime.fromisoformat(v["completed_at"])
                self.operations[k] = GitHubOperation(**v)
            
            # Import audit logs
            for log_data in data.get("audit_logs", []):
                log_data["timestamp"] = datetime.fromisoformat(log_data["timestamp"])
                self.audit_logs.append(GitHubAuditLog(**log_data))
            
            # Import repository configs
            for k, v in data.get("repository_configs", {}).items():
                v["created_at"] = datetime.fromisoformat(v["created_at"])
                v["updated_at"] = datetime.fromisoformat(v["updated_at"])
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


if __name__ == "__main__":
    # Example usage
    db = create_github_protocol_db()
    
    # Grant permission
    permission = GitHubAgentPermission(
        agent_id="Agent-1",
        repository="test-repo",
        permission_level=GitHubPermissionLevel.ADMIN,
        granted_by="Agent-4",
        granted_at=datetime.utcnow()
    )
    
    db.grant_permission(permission)
    print(f"✅ Permission granted: {db.check_permission('Agent-1', 'test-repo', GitHubPermissionLevel.WRITE)}")
    
    # Create operation
    operation = GitHubOperation(
        operation_id="op_001",
        agent_id="Agent-1",
        operation_type=GitHubOperationType.CREATE_REPOSITORY,
        repository="test-repo",
        parameters={"name": "test-repo", "private": False},
        status=GitHubOperationStatus.PENDING,
        created_at=datetime.utcnow()
    )
    
    db.create_operation(operation)
    print(f"✅ Operation created: {operation.operation_id}")
    
    # Export data
    exported = db.export_data()
    print(f"📊 Database exported: {len(exported['permissions'])} permissions, {len(exported['operations'])} operations")

