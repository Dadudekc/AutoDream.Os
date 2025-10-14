#!/usr/bin/env python3
"""
GitHub API Integration
======================

Integrates with GitHub API for issue fetching, PR submission, metrics tracking.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class GitHubIntegration:
    """GitHub API integration for OSS contributions."""

    def __init__(self, token: str | None = None):
        """
        Initialize GitHub integration.

        Args:
            token: GitHub personal access token (optional)
        """
        self.token = token

    def fetch_issues(self, repo_url: str, labels: list[str] = None, limit: int = 10) -> list[dict]:
        """
        Fetch issues from GitHub repository.

        Args:
            repo_url: Repository URL
            labels: Filter by labels (e.g., ["good first issue"])
            limit: Maximum issues to fetch

        Returns:
            List of issue dictionaries
        """
        # Parse repo from URL
        if "github.com/" in repo_url:
            parts = repo_url.split("github.com/")[-1].rstrip("/").split("/")
            owner, repo = parts[0], parts[1].replace(".git", "")
        else:
            logger.error(f"Invalid GitHub URL: {repo_url}")
            return []

        # Use GitHub CLI if available
        try:
            label_filter = f"--label {','.join(labels)}" if labels else ""
            cmd = f"gh issue list --repo {owner}/{repo} {label_filter} --limit {limit} --json number,title,labels,url"

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                import json

                issues = json.loads(result.stdout)
                logger.info(f"✅ Fetched {len(issues)} issues from {repo}")
                return issues
            else:
                logger.warning(f"GitHub CLI failed: {result.stderr}")
                return []

        except Exception as e:
            logger.warning(f"GitHub CLI not available: {e}")
            return []

    def create_branch(self, project_path: Path, branch_name: str) -> bool:
        """
        Create new branch for contribution.

        Args:
            project_path: Path to project
            branch_name: Branch name

        Returns:
            Success status
        """
        try:
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info(f"✅ Branch created: {branch_name}")
                return True
            else:
                logger.error(f"❌ Branch creation failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to create branch: {e}")
            return False

    def commit_changes(self, project_path: Path, message: str, agents: list[str]) -> bool:
        """
        Commit changes with swarm signature.

        Args:
            project_path: Path to project
            message: Commit message
            agents: List of agent IDs involved

        Returns:
            Success status
        """
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)

            # Create commit with swarm signature
            swarm_signature = f"\n\nImplemented by Agent Swarm\nAgents: {', '.join(agents)}"
            full_message = message + swarm_signature

            result = subprocess.run(
                ["git", "commit", "-m", full_message],
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info(f"✅ Changes committed: {message[:50]}...")
                return True
            else:
                logger.warning(f"No changes to commit: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Commit failed: {e}")
            return False

    def push_branch(self, project_path: Path, branch_name: str) -> bool:
        """
        Push branch to origin.

        Args:
            project_path: Path to project
            branch_name: Branch name

        Returns:
            Success status
        """
        try:
            result = subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info(f"✅ Branch pushed: {branch_name}")
                return True
            else:
                logger.error(f"❌ Push failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to push: {e}")
            return False

    def create_pr(
        self, project_path: Path, title: str, description: str, agents: list[str]
    ) -> str | None:
        """
        Create pull request via GitHub CLI.

        Args:
            project_path: Path to project
            title: PR title
            description: PR description
            agents: List of agent IDs

        Returns:
            PR URL if successful
        """
        try:
            # Add swarm signature to description
            swarm_footer = f"""

---
**Contributed by Agent Swarm** 🐝
**Agents involved:** {', '.join(agents)}
**Autonomous Development System**
"""
            full_description = description + swarm_footer

            # Create PR via GitHub CLI
            result = subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", full_description],
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                pr_url = result.stdout.strip()
                logger.info(f"✅ PR created: {pr_url}")
                return pr_url
            else:
                logger.error(f"❌ PR creation failed: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"❌ Failed to create PR: {e}")
            return None
