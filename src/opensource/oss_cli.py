#!/usr/bin/env python3
"""
OSS CLI Commands
================

Command-line interface for open source contribution management.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import argparse
import logging
import sys

from .contribution_tracker import ContributionTracker
from .github_integration import GitHubIntegration
from .portfolio_builder import PortfolioBuilder
from .project_manager import OpenSourceProjectManager
from .task_integration import OSSTaskIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_parser():
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(description="Agent Swarm - Open Source Contribution Manager")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Clone project
    clone_parser = subparsers.add_parser("clone", help="Clone OSS project")
    clone_parser.add_argument("url", help="GitHub repository URL")
    clone_parser.add_argument("--name", help="Project name (auto-detected if not provided)")

    # List projects
    subparsers.add_parser("list", help="List registered projects")

    # Fetch issues
    issues_parser = subparsers.add_parser("issues", help="Fetch GitHub issues")
    issues_parser.add_argument("project_id", help="Project ID")
    issues_parser.add_argument(
        "--labels", nargs="+", help='Labels to filter (e.g., "good first issue")'
    )
    issues_parser.add_argument("--import-tasks", action="store_true", help="Import issues as tasks")

    # Create PR
    pr_parser = subparsers.add_parser("pr", help="Create pull request")
    pr_parser.add_argument("project_id", help="Project ID")
    pr_parser.add_argument("--title", required=True, help="PR title")
    pr_parser.add_argument("--description", required=True, help="PR description")
    pr_parser.add_argument("--agents", nargs="+", required=True, help="Agent IDs")

    # Portfolio
    portfolio_parser = subparsers.add_parser("portfolio", help="Generate portfolio")
    portfolio_parser.add_argument(
        "--format", choices=["markdown", "html", "json"], default="markdown"
    )

    # Status
    subparsers.add_parser("status", help="Show contribution status")

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Initialize managers
    pm = OpenSourceProjectManager()
    tracker = ContributionTracker()
    github = GitHubIntegration()
    portfolio = PortfolioBuilder(tracker)

    try:
        if args.command == "clone":
            project_id = pm.clone_project(args.url, args.name)
            if project_id:
                print(f"✅ Project cloned: {project_id}")
                tracker.register_project(args.name or "project", args.url, {})
            else:
                print("❌ Clone failed")
                return 1

        elif args.command == "list":
            projects = pm.list_projects()
            print(f"\n🐝 Registered OSS Projects ({len(projects)}):")
            print("=" * 60)
            for proj in projects:
                print(f"ID: {proj['id']}")
                print(f"Name: {proj['name']}")
                print(f"URL: {proj['github_url']}")
                print(f"Status: {proj['status']}")
                print(
                    f"PRs: {proj['metrics']['prs_submitted']} submitted, "
                    f"{proj['metrics']['prs_merged']} merged"
                )
                print("-" * 60)

        elif args.command == "issues":
            project = pm.get_project(args.project_id)
            if not project:
                print(f"❌ Project not found: {args.project_id}")
                return 1

            issues = github.fetch_issues(project["github_url"], args.labels)
            print(f"\n📋 Issues from {project['name']} ({len(issues)}):")
            print("=" * 60)

            for issue in issues:
                print(f"#{issue['number']}: {issue['title']}")
                print(f"URL: {issue['url']}")
                print()

            if args.import_tasks:
                from src.infrastructure.persistence.sqlite_task_repo import (
                    SqliteTaskRepository,
                )

                repo = SqliteTaskRepository()
                integration = OSSTaskIntegration(pm, repo)
                task_ids = integration.bulk_import_issues(args.project_id, issues)
                print(f"✅ Imported {len(task_ids)} issues as tasks")

        elif args.command == "portfolio":
            print("📊 Generating portfolio...")
            if args.format == "markdown":
                portfolio.generate_readme()
                print("✅ README generated")
            elif args.format == "html":
                portfolio.generate_dashboard_html()
                print("✅ HTML dashboard generated")
            elif args.format == "json":
                portfolio.export_portfolio_json()
                print("✅ JSON export generated")

        elif args.command == "status":
            metrics = tracker.get_metrics()
            print("\n🐝 Agent Swarm - OSS Contribution Status")
            print("=" * 60)
            print(f"Projects: {metrics.total_projects}")
            print(f"PRs Submitted: {metrics.total_prs}")
            print(f"PRs Merged: {metrics.merged_prs}")
            print(
                f"Merge Rate: {(metrics.merged_prs / metrics.total_prs * 100) if metrics.total_prs > 0 else 0:.1f}%"
            )
            print(f"Issues Closed: {metrics.issues_closed}")
            print(f"Reputation Score: {metrics.reputation_score:.1f}")
            print("\n🤖 Agent Contributions:")
            for agent_id, stats in metrics.agent_contributions.items():
                print(f"  {agent_id}: {stats.get('contributions', 0)} contributions")

        return 0

    except Exception as e:
        logger.error(f"❌ Command failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
