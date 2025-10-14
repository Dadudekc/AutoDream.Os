#!/usr/bin/env python3
"""
Open Source Project Manager
============================

Manages external open source projects for swarm contributions.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import json
import logging
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenSourceProjectManager:
    """Manages swarm's open source project contributions."""

    def __init__(self, projects_root: str = "D:\\OpenSource_Swarm_Projects"):
        """
        Initialize project manager.

        Args:
            projects_root: Root directory for external projects
        """
        self.projects_root = Path(projects_root)
        self.projects_root.mkdir(parents=True, exist_ok=True)

        # Registry file
        self.registry_file = self.projects_root / "swarm_project_registry.json"
        self.portfolio_file = self.projects_root / "swarm_portfolio.json"

        # Load or initialize registry
        self.registry = self._load_registry()
        self.portfolio = self._load_portfolio()

        # Save on init to ensure files exist
        self._save_registry()
        self._save_portfolio()

        logger.info(f"OSS Project Manager initialized: {self.projects_root}")

    def _load_registry(self) -> dict:
        """Load project registry."""
        if self.registry_file.exists():
            return json.loads(self.registry_file.read_text(encoding="utf-8"))
        return {"projects": {}, "last_updated": datetime.now().isoformat()}

    def _save_registry(self):
        """Save project registry."""
        self.registry["last_updated"] = datetime.now().isoformat()
        self.registry_file.write_text(
            json.dumps(self.registry, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _load_portfolio(self) -> dict:
        """Load swarm portfolio."""
        if self.portfolio_file.exists():
            return json.loads(self.portfolio_file.read_text(encoding="utf-8"))
        return {
            "total_projects": 0,
            "total_prs": 0,
            "merged_prs": 0,
            "total_commits": 0,
            "projects": {},
        }

    def _save_portfolio(self):
        """Save swarm portfolio."""
        self.portfolio_file.write_text(
            json.dumps(self.portfolio, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def clone_project(self, github_url: str, project_name: str | None = None) -> str:
        """
        Clone external open source project.

        Args:
            github_url: GitHub repository URL
            project_name: Optional project name (auto-detected if None)

        Returns:
            Project ID
        """
        # Extract project name from URL if not provided
        if not project_name:
            project_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")

        # Generate project ID
        project_id = f"oss-{uuid.uuid4().hex[:8]}"

        # Create project directory
        project_path = self.projects_root / project_name
        if project_path.exists():
            logger.warning(f"Project already exists: {project_path}")
            # Find existing project ID
            for pid, proj in self.registry["projects"].items():
                if proj["name"] == project_name:
                    return pid
            # If not in registry, re-register
            project_id = f"oss-{uuid.uuid4().hex[:8]}"

        try:
            # Clone repository
            logger.info(f"Cloning {github_url} to {project_path}...")
            result = subprocess.run(
                ["git", "clone", github_url, str(project_path)],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                logger.error(f"Clone failed: {result.stderr}")
                return None

            # Register project
            self.registry["projects"][project_id] = {
                "id": project_id,
                "name": project_name,
                "github_url": github_url,
                "clone_path": str(project_path),
                "status": "active",
                "cloned_at": datetime.now().isoformat(),
                "contributions": [],
                "metrics": {
                    "prs_submitted": 0,
                    "prs_merged": 0,
                    "issues_closed": 0,
                    "commits": 0,
                },
            }

            self._save_registry()

            # Create swarm tracking file in project
            tracking_file = project_path / "swarm_tracking.json"
            tracking_file.write_text(
                json.dumps(
                    {
                        "swarm_project_id": project_id,
                        "managed_by": "Agent Swarm",
                        "swarm_home": str(Path.cwd()),
                        "cloned_at": datetime.now().isoformat(),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            logger.info(f"✅ Project cloned: {project_id} ({project_name})")

            # Observability: Log success
            try:
                from src.obs.metrics import log_oss_clone_success

                log_oss_clone_success()
            except ImportError:
                pass

            return project_id

        except Exception as e:
            logger.error(f"❌ Failed to clone project: {e}")

            # Observability: Log failure
            try:
                from src.obs.metrics import log_oss_clone_failure

                log_oss_clone_failure()
            except ImportError:
                pass

            return None

    def get_project(self, project_id: str) -> dict | None:
        """Get project details."""
        return self.registry["projects"].get(project_id)

    def list_projects(self) -> list[dict]:
        """List all registered projects."""
        return list(self.registry["projects"].values())

    def get_project_path(self, project_id: str) -> Path | None:
        """Get path to cloned project."""
        project = self.get_project(project_id)
        if project:
            return Path(project["clone_path"])
        return None

    def add_contribution(
        self, project_id: str, contribution_type: str, description: str, agents: list[str]
    ):
        """
        Add contribution record.

        Args:
            project_id: Project ID
            contribution_type: Type (pr, issue, commit)
            description: Contribution description
            agents: List of involved agent IDs
        """
        project = self.get_project(project_id)
        if not project:
            logger.error(f"Project not found: {project_id}")
            return

        contribution = {
            "id": uuid.uuid4().hex[:8],
            "type": contribution_type,
            "description": description,
            "agents": agents,
            "timestamp": datetime.now().isoformat(),
            "status": "submitted",
        }

        project["contributions"].append(contribution)
        self._save_registry()

        logger.info(f"✅ Contribution logged: {project_id} - {contribution_type}")
