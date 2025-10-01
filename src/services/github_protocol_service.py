#!/usr/bin/env python3
"""
GitHub Protocol Service - Agent GitHub Operations
================================================

Unified GitHub protocol service integrating core, operations, and workflows.

V2 Compliance: ≤400 lines - REFACTORED FROM 485 LINES
Refactored By: Agent-6 (Quality Assurance Specialist)
Split into: core.py, operations.py, workflows.py
"""

import os

from .github_protocol_core import GitHubProtocolService
from .github_protocol_operations import GitHubOperations
from .github_protocol_workflows import GitHubWorkflows


# Extend main service with operations and workflows
class GitHubProtocolServiceComplete(GitHubProtocolService):
    """Complete GitHub protocol service with all capabilities."""

    def __init__(self, github_token: str, db_path: str = "github_protocol.db"):
        """Initialize complete GitHub protocol service."""
        super().__init__(github_token, db_path)
        self.operations = GitHubOperations(self)
        self.workflows = GitHubWorkflows(self)

    # Delegate to operations
    def create_repository(
        self,
        agent_id: str,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True,
    ):
        """Create repository."""
        return self.operations.create_repository(agent_id, name, description, private, auto_init)

    def create_issue(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] = None,
        assignees: list[str] = None,
    ):
        """Create issue."""
        return self.operations.create_issue(agent_id, owner, repo, title, body, labels, assignees)

    def create_pull_request(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        title: str,
        head_branch: str,
        base_branch: str,
        body: str = "",
    ):
        """Create pull request."""
        return self.operations.create_pull_request(
            agent_id, owner, repo, title, head_branch, base_branch, body
        )

    def create_file(
        self,
        agent_id: str,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str = None,
    ):
        """Create file."""
        return self.operations.create_file(agent_id, owner, repo, path, content, message, branch)

    def create_branch(
        self, agent_id: str, owner: str, repo: str, branch_name: str, from_branch: str = "main"
    ):
        """Create branch."""
        return self.operations.create_branch(agent_id, owner, repo, branch_name, from_branch)

    # Delegate to workflows
    def create_workflow_template(
        self,
        template_id: str,
        name: str,
        description: str,
        workflow_type: str,
        template_content: str,
        parameters: dict,
        created_by: str,
    ):
        """Create workflow template."""
        return self.workflows.create_workflow_template(
            template_id, name, description, workflow_type, template_content, parameters, created_by
        )

    def get_workflow_template(self, template_id: str):
        """Get workflow template."""
        return self.workflows.get_workflow_template(template_id)


def create_github_protocol_service_complete(github_token: str) -> GitHubProtocolServiceComplete:
    """Create complete GitHub protocol service instance."""
    return GitHubProtocolServiceComplete(github_token)


if __name__ == "__main__":
    # Example usage
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        exit(1)

    service = create_github_protocol_service_complete(token)

    # Grant permission to Agent-1
    service.grant_agent_permission("Agent-1", "test-repo", GitHubPermissionLevel.ADMIN)

    print(
        f"✅ Permission granted: {service.check_agent_permission('Agent-1', 'test-repo', GitHubPermissionLevel.WRITE)}"
    )

    # Create repository
    repo = service.create_repository(
        "Agent-1", "agent-test-repo", "Test repository created by Agent-1", private=False
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
