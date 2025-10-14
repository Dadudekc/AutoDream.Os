#!/usr/bin/env python3
"""
Contribution Tracker
====================

Tracks swarm's open source contributions and builds recognition portfolio.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ContributionMetrics:
    """Metrics for swarm's OSS contributions."""

    total_projects: int = 0
    total_prs: int = 0
    merged_prs: int = 0
    open_prs: int = 0
    total_commits: int = 0
    issues_closed: int = 0
    total_stars: int = 0
    reputation_score: float = 0.0
    agent_contributions: dict[str, int] = field(default_factory=dict)

    def calculate_reputation(self):
        """Calculate reputation score."""
        # Simple formula: (merged PRs * 10) + (closed issues * 5) + stars
        self.reputation_score = (
            (self.merged_prs * 10) + (self.issues_closed * 5) + (self.total_stars * 0.1)
        )


class ContributionTracker:
    """Tracks and analyzes swarm's OSS contributions."""

    def __init__(self, portfolio_file: str = "D:\\OpenSource_Swarm_Projects\\swarm_portfolio.json"):
        """
        Initialize contribution tracker.

        Args:
            portfolio_file: Path to portfolio JSON file
        """
        self.portfolio_file = Path(portfolio_file)
        self.portfolio_file.parent.mkdir(parents=True, exist_ok=True)
        self.portfolio = self._load_portfolio()
        # Save on init to ensure file exists
        self._save_portfolio()

    def _load_portfolio(self) -> dict:
        """Load portfolio data."""
        if self.portfolio_file.exists():
            return json.loads(self.portfolio_file.read_text(encoding="utf-8"))

        return {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "projects": {},
            "contributions": [],
            "metrics": {
                "total_projects": 0,
                "total_prs": 0,
                "merged_prs": 0,
                "total_commits": 0,
                "issues_closed": 0,
                "total_stars": 0,
            },
            "agents": {},
        }

    def _save_portfolio(self):
        """Save portfolio data."""
        self.portfolio["last_updated"] = datetime.now().isoformat()
        self.portfolio_file.write_text(
            json.dumps(self.portfolio, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def log_contribution(
        self,
        project_name: str,
        contribution_type: str,
        description: str,
        agents: list[str],
        pr_url: str | None = None,
        status: str = "submitted",
    ):
        """
        Log a contribution.

        Args:
            project_name: Project name
            contribution_type: Type (pr, commit, issue)
            description: Contribution description
            agents: List of agent IDs involved
            pr_url: PR URL if applicable
            status: Status (submitted, merged, closed)
        """
        contribution = {
            "id": f"contrib-{len(self.portfolio['contributions']) + 1}",
            "project": project_name,
            "type": contribution_type,
            "description": description,
            "agents": agents,
            "pr_url": pr_url,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }

        self.portfolio["contributions"].append(contribution)

        # Update agent contributions
        for agent in agents:
            if agent not in self.portfolio["agents"]:
                self.portfolio["agents"][agent] = {"contributions": 0, "merged_prs": 0}

            self.portfolio["agents"][agent]["contributions"] += 1

            if status == "merged" and contribution_type == "pr":
                self.portfolio["agents"][agent]["merged_prs"] += 1

        # Update metrics
        if contribution_type == "pr":
            self.portfolio["metrics"]["total_prs"] += 1
            if status == "merged":
                self.portfolio["metrics"]["merged_prs"] += 1

        if contribution_type == "commit":
            self.portfolio["metrics"]["total_commits"] += 1

        if contribution_type == "issue" and status == "closed":
            self.portfolio["metrics"]["issues_closed"] += 1

        self._save_portfolio()
        logger.info(f"✅ Contribution logged: {project_name} - {contribution_type}")

    def get_metrics(self) -> ContributionMetrics:
        """Get contribution metrics."""
        metrics_data = self.portfolio["metrics"]

        metrics = ContributionMetrics(
            total_projects=len(self.portfolio["projects"]),
            total_prs=metrics_data.get("total_prs", 0),
            merged_prs=metrics_data.get("merged_prs", 0),
            total_commits=metrics_data.get("total_commits", 0),
            issues_closed=metrics_data.get("issues_closed", 0),
            total_stars=metrics_data.get("total_stars", 0),
            agent_contributions=self.portfolio.get("agents", {}),
        )

        metrics.calculate_reputation()
        return metrics

    def get_agent_contributions(self, agent_id: str) -> dict:
        """Get contributions for specific agent."""
        return self.portfolio.get("agents", {}).get(agent_id, {"contributions": 0, "merged_prs": 0})

    def register_project(self, project_name: str, github_url: str, metadata: dict):
        """Register new project in portfolio."""
        self.portfolio["projects"][project_name] = {
            "name": project_name,
            "github_url": github_url,
            "added_at": datetime.now().isoformat(),
            "status": "active",
            **metadata,
        }

        self.portfolio["metrics"]["total_projects"] = len(self.portfolio["projects"])
        self._save_portfolio()
