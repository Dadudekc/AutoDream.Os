#!/usr/bin/env python3
"""
Open Source Contribution Tools
===============================

Tools for OSS project management and contributions.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
from typing import Any

from ..adapters.base_adapter import IToolAdapter

logger = logging.getLogger(__name__)


class OSSCloneTool(IToolAdapter):
    """Clone external OSS project."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute project clone."""
        try:
            from src.opensource.project_manager import OpenSourceProjectManager

            github_url = params.get("github_url")
            project_name = params.get("project_name")

            if not github_url:
                return {"success": False, "error": "github_url required"}

            pm = OpenSourceProjectManager()
            project_id = pm.clone_project(github_url, project_name)

            if project_id:
                project = pm.get_project(project_id)
                return {
                    "success": True,
                    "project_id": project_id,
                    "name": project["name"],
                    "path": project["clone_path"],
                }
            else:
                return {"success": False, "error": "Clone failed"}

        except Exception as e:
            return {"success": False, "error": str(e)}


class OSSFetchIssuesTool(IToolAdapter):
    """Fetch GitHub issues from OSS project."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute issue fetching."""
        try:
            from src.opensource.github_integration import GitHubIntegration
            from src.opensource.project_manager import OpenSourceProjectManager

            project_id = params.get("project_id")
            labels = params.get("labels", [])

            if not project_id:
                return {"success": False, "error": "project_id required"}

            pm = OpenSourceProjectManager()
            github = GitHubIntegration()

            project = pm.get_project(project_id)
            if not project:
                return {"success": False, "error": f"Project not found: {project_id}"}

            issues = github.fetch_issues(project["github_url"], labels)

            return {"success": True, "issues": issues, "count": len(issues)}

        except Exception as e:
            return {"success": False, "error": str(e)}


class OSSImportIssuesTool(IToolAdapter):
    """Import GitHub issues as tasks."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute issue import."""
        try:
            from src.infrastructure.persistence.sqlite_task_repo import SqliteTaskRepository
            from src.opensource.github_integration import GitHubIntegration
            from src.opensource.project_manager import OpenSourceProjectManager
            from src.opensource.task_integration import OSSTaskIntegration

            project_id = params.get("project_id")
            labels = params.get("labels", ["good first issue"])
            max_tasks = params.get("max_tasks", 10)

            if not project_id:
                return {"success": False, "error": "project_id required"}

            pm = OpenSourceProjectManager()
            github = GitHubIntegration()
            repo = SqliteTaskRepository()
            integration = OSSTaskIntegration(pm, repo)

            project = pm.get_project(project_id)
            if not project:
                return {"success": False, "error": f"Project not found: {project_id}"}

            issues = github.fetch_issues(project["github_url"], labels)
            task_ids = integration.bulk_import_issues(project_id, issues, max_tasks)

            return {
                "success": True,
                "tasks_created": len(task_ids),
                "task_ids": task_ids,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


class OSSPortfolioTool(IToolAdapter):
    """Generate OSS contribution portfolio."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute portfolio generation."""
        try:
            from src.opensource.contribution_tracker import ContributionTracker
            from src.opensource.portfolio_builder import PortfolioBuilder

            format_type = params.get("format", "markdown")

            tracker = ContributionTracker()
            builder = PortfolioBuilder(tracker)

            if format_type == "markdown":
                builder.generate_readme()
                return {"success": True, "format": "markdown", "file": "README.md"}
            elif format_type == "html":
                builder.generate_dashboard_html()
                return {"success": True, "format": "html", "file": "portfolio.html"}
            elif format_type == "json":
                builder.export_portfolio_json()
                return {"success": True, "format": "json", "file": "portfolio_export.json"}
            else:
                return {"success": False, "error": f"Unknown format: {format_type}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


class OSSStatusTool(IToolAdapter):
    """Get OSS contribution status."""

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute status check."""
        try:
            from src.opensource.contribution_tracker import ContributionTracker

            tracker = ContributionTracker()
            metrics = tracker.get_metrics()

            return {
                "success": True,
                "total_projects": metrics.total_projects,
                "total_prs": metrics.total_prs,
                "merged_prs": metrics.merged_prs,
                "merge_rate": (
                    (metrics.merged_prs / metrics.total_prs * 100) if metrics.total_prs > 0 else 0
                ),
                "reputation_score": metrics.reputation_score,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
