#!/usr/bin/env python3
"""
OSS Task Integration
====================

Integrates external OSS issues with swarm's task system.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging

logger = logging.getLogger(__name__)


class OSSTaskIntegration:
    """Integrates OSS issues with task system."""

    def __init__(self, project_manager, task_repository):
        """
        Initialize task integration.

        Args:
            project_manager: OpenSourceProjectManager instance
            task_repository: SqliteTaskRepository instance
        """
        self.project_manager = project_manager
        self.task_repo = task_repository

    def create_task_from_issue(
        self, project_id: str, issue_number: int, issue_data: dict
    ) -> str | None:
        """
        Create task from GitHub issue.

        Args:
            project_id: OSS project ID
            issue_number: GitHub issue number
            issue_data: Issue metadata

        Returns:
            Task ID if created
        """
        try:
            # Extract issue details
            title = f"[OSS] {issue_data.get('title', f'Issue #{issue_number}')}"
            description = f"""**Open Source Contribution**

Project: {self.project_manager.get_project(project_id).get('name', 'Unknown')}
Issue: #{issue_number}
URL: {issue_data.get('url', 'N/A')}

{issue_data.get('body', '')}
"""

            # Determine priority from labels
            labels = issue_data.get("labels", [])
            priority = self._determine_priority(labels)

            # Create task
            task_id = self.task_repo.create_from_message(
                title=title,
                description=description,
                priority=priority,
                state="todo",
                source={
                    "type": "github_issue",
                    "project_id": project_id,
                    "issue_number": issue_number,
                    "issue_url": issue_data.get("url"),
                },
                tags=["oss", "external"] + [label.get("name") for label in labels],
            )

            logger.info(f"✅ Task created from issue: {task_id}")
            return task_id

        except Exception as e:
            logger.error(f"❌ Failed to create task from issue: {e}")
            return None

    def _determine_priority(self, labels: list[dict]) -> str:
        """Determine priority from GitHub labels."""
        label_names = [label.get("name", "").lower() for label in labels]

        if any(word in label_names for word in ["critical", "urgent", "security", "blocker"]):
            return "P0"

        if any(word in label_names for word in ["high", "important", "bug"]):
            return "P1"

        if any(word in label_names for word in ["good first issue", "help wanted", "enhancement"]):
            return "P2"

        return "P3"

    def bulk_import_issues(
        self, project_id: str, issues: list[dict], max_tasks: int = 10
    ) -> list[str]:
        """
        Import multiple issues as tasks.

        Args:
            project_id: OSS project ID
            issues: List of issue data
            max_tasks: Maximum tasks to create

        Returns:
            List of created task IDs
        """
        task_ids = []

        for issue in issues[:max_tasks]:
            task_id = self.create_task_from_issue(project_id, issue.get("number"), issue)
            if task_id:
                task_ids.append(task_id)

        logger.info(f"✅ Imported {len(task_ids)} issues as tasks")
        return task_ids
