#!/usr/bin/env python3
"""
Open Source Contribution System Tests
======================================

Tests for OSS contribution infrastructure.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import pytest

from src.opensource.contribution_tracker import ContributionTracker
from src.opensource.portfolio_builder import PortfolioBuilder
from src.opensource.project_manager import OpenSourceProjectManager


class TestProjectManager:
    """Test project manager functionality."""

    def test_init(self, tmp_path):
        """Test project manager initialization."""
        pm = OpenSourceProjectManager(str(tmp_path))
        assert pm.projects_root == tmp_path
        assert pm.projects_root.exists()
        assert pm.registry_file.exists()

    def test_register_project(self, tmp_path):
        """Test project registration."""
        pm = OpenSourceProjectManager(str(tmp_path))
        pm.registry["projects"]["test-001"] = {
            "id": "test-001",
            "name": "test-project",
            "github_url": "https://github.com/test/repo",
        }
        pm._save_registry()

        # Reload and verify
        pm2 = OpenSourceProjectManager(str(tmp_path))
        assert "test-001" in pm2.registry["projects"]

    def test_get_project(self, tmp_path):
        """Test getting project details."""
        pm = OpenSourceProjectManager(str(tmp_path))
        pm.registry["projects"]["test-001"] = {"id": "test-001", "name": "test"}
        pm._save_registry()

        project = pm.get_project("test-001")
        assert project is not None
        assert project["name"] == "test"

    def test_list_projects(self, tmp_path):
        """Test listing projects."""
        pm = OpenSourceProjectManager(str(tmp_path))
        pm.registry["projects"]["test-001"] = {"id": "test-001"}
        pm.registry["projects"]["test-002"] = {"id": "test-002"}
        pm._save_registry()

        projects = pm.list_projects()
        assert len(projects) == 2


class TestContributionTracker:
    """Test contribution tracking."""

    def test_init(self, tmp_path):
        """Test tracker initialization."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))
        assert tracker.portfolio_file.exists()

    def test_log_contribution(self, tmp_path):
        """Test logging contribution."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))

        tracker.log_contribution(
            project_name="test-project",
            contribution_type="pr",
            description="Fix bug",
            agents=["Agent-2"],
            status="merged",
        )

        assert tracker.portfolio["metrics"]["total_prs"] == 1
        assert tracker.portfolio["metrics"]["merged_prs"] == 1
        assert "Agent-2" in tracker.portfolio["agents"]

    def test_get_metrics(self, tmp_path):
        """Test getting metrics."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))

        tracker.log_contribution("proj", "pr", "test", ["Agent-2"], status="merged")

        metrics = tracker.get_metrics()
        assert metrics.total_prs == 1
        assert metrics.merged_prs == 1
        assert metrics.reputation_score > 0

    def test_agent_contributions(self, tmp_path):
        """Test agent contribution tracking."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))

        tracker.log_contribution("proj", "pr", "test", ["Agent-2"], status="merged")

        agent_stats = tracker.get_agent_contributions("Agent-2")
        assert agent_stats["contributions"] == 1
        assert agent_stats["merged_prs"] == 1


class TestPortfolioBuilder:
    """Test portfolio generation."""

    def test_generate_readme(self, tmp_path):
        """Test README generation."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))

        tracker.log_contribution("pytest", "pr", "test", ["Agent-2"], status="merged")

        builder = PortfolioBuilder(tracker)
        readme_path = tmp_path / "README.md"
        builder.generate_readme(str(readme_path))

        assert readme_path.exists()
        content = readme_path.read_text()
        assert "Agent Swarm" in content
        assert "Agent-2" in content

    def test_generate_html(self, tmp_path):
        """Test HTML dashboard generation."""
        portfolio_file = tmp_path / "portfolio.json"
        tracker = ContributionTracker(str(portfolio_file))

        builder = PortfolioBuilder(tracker)
        html_path = tmp_path / "portfolio.html"
        builder.generate_dashboard_html(str(html_path))

        assert html_path.exists()
        content = html_path.read_text()
        assert "Agent Swarm" in content
        assert "<html" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
