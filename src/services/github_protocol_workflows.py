#!/usr/bin/env python3
"""
GitHub Protocol Workflows - Workflow Template Management
=========================================================

Workflow template management for GitHub protocol service.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: github_protocol_service.py (485 lines) - Workflows module
"""

from datetime import datetime
from typing import Any

from .github_protocol_models import GitHubWorkflowTemplate


class GitHubWorkflows:
    """Workflow template management for GitHub protocol service."""

    def __init__(self, service):
        """Initialize workflows handler."""
        self.service = service
        self.db = service.db

    def create_workflow_template(
        self,
        template_id: str,
        name: str,
        description: str,
        workflow_type: str,
        template_content: str,
        parameters: dict[str, Any],
        created_by: str,
    ) -> bool:
        """Create workflow template."""
        template = GitHubWorkflowTemplate(
            template_id=template_id,
            name=name,
            description=description,
            workflow_type=workflow_type,
            template_content=template_content,
            parameters=parameters,
            created_by=created_by,
            created_at=datetime.utcnow(),
        )

        return self.db.create_workflow_template(template)

    def get_workflow_template(self, template_id: str) -> GitHubWorkflowTemplate | None:
        """Get workflow template."""
        return self.db.get_workflow_template(template_id)


__all__ = ["GitHubWorkflows"]
