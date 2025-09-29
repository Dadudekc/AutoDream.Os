#!/usr/bin/env python3
"""
GitHub Agent CLI - Command Line Interface for GitHub Operations
==============================================================

Command line interface for agents to perform GitHub operations using the
GitHub protocol service. Provides easy-to-use commands for all GitHub functions.

V2 Compliance: ≤400 lines, comprehensive GitHub CLI tool
Author: Agent-1 (Architecture Foundation Specialist)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.github_protocol_models import GitHubOperationStatus, GitHubPermissionLevel
from src.services.github_protocol_service import create_github_protocol_service


class GitHubAgentCLI:
    """Command line interface for GitHub agent operations."""

    def __init__(self):
        """Initialize GitHub agent CLI."""
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            print("❌ GITHUB_TOKEN environment variable not set")
            sys.exit(1)

        self.service = create_github_protocol_service(self.token)
        self.agent_id = os.getenv("AGENT_ID", "Agent-1")

    def create_repository(self, args):
        """Create a new repository."""
        repo = self.service.create_repository(
            self.agent_id, args.name, args.description or "", args.private, args.auto_init
        )

        if repo:
            print(f"✅ Repository created: {repo.name}")
            print(f"   URL: {repo.html_url}")
            print(f"   Clone: {repo.clone_url}")
        else:
            print("❌ Failed to create repository")

    def create_issue(self, args):
        """Create a new issue."""
        labels = args.labels.split(",") if args.labels else None
        assignees = args.assignees.split(",") if args.assignees else None

        issue = self.service.create_issue(
            self.agent_id, args.owner, args.repo, args.title, args.body or "", labels, assignees
        )

        if issue:
            print(f"✅ Issue created: #{issue.number}")
            print(f"   Title: {issue.title}")
            print(f"   URL: {issue.html_url}")
        else:
            print("❌ Failed to create issue")

    def create_pull_request(self, args):
        """Create a new pull request."""
        pr = self.service.create_pull_request(
            self.agent_id,
            args.owner,
            args.repo,
            args.title,
            args.head_branch,
            args.base_branch,
            args.body or "",
        )

        if pr:
            print(f"✅ Pull request created: #{pr.number}")
            print(f"   Title: {pr.title}")
            print(f"   URL: {pr.html_url}")
        else:
            print("❌ Failed to create pull request")

    def create_file(self, args):
        """Create a new file."""
        # Read file content if path provided
        if args.file_path:
            try:
                with open(args.file_path) as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Error reading file {args.file_path}: {e}")
                return
        else:
            content = args.content or ""

        success = self.service.create_file(
            self.agent_id, args.owner, args.repo, args.path, content, args.message, args.branch
        )

        if success:
            print(f"✅ File created: {args.path}")
        else:
            print("❌ Failed to create file")

    def create_branch(self, args):
        """Create a new branch."""
        success = self.service.create_branch(
            self.agent_id, args.owner, args.repo, args.branch_name, args.from_branch
        )

        if success:
            print(f"✅ Branch created: {args.branch_name}")
        else:
            print("❌ Failed to create branch")

    def grant_permission(self, args):
        """Grant permission to agent."""
        permission_level = GitHubPermissionLevel(args.permission_level.lower())

        success = self.service.grant_agent_permission(
            args.agent_id, args.repository, permission_level, self.agent_id
        )

        if success:
            print(
                f"✅ Permission granted: {args.agent_id} -> {args.repository} ({args.permission_level})"
            )
        else:
            print("❌ Failed to grant permission")

    def list_operations(self, args):
        """List agent operations."""
        status = None
        if args.status:
            status = GitHubOperationStatus(args.status.lower())

        operations = self.service.get_agent_operations(self.agent_id, status)

        print(f"📊 Operations for {self.agent_id}:")
        for op in operations:
            print(f"   {op.operation_id}: {op.operation_type.value} - {op.status.value}")
            if op.error_message:
                print(f"      Error: {op.error_message}")

    def show_audit_logs(self, args):
        """Show audit logs."""
        logs = self.service.get_audit_logs(args.agent_id, args.repository, args.limit)

        print("📋 Audit logs:")
        for log in logs:
            print(f"   {log['timestamp']}: {log['agent_id']} - {log['action']}")
            if log["repository"]:
                print(f"      Repository: {log['repository']}")

    def export_data(self, args):
        """Export protocol data."""
        data = self.service.export_protocol_data()

        output_file = (
            args.output or f"github_protocol_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"✅ Data exported to: {output_file}")

    def run(self):
        """Run the CLI."""
        parser = argparse.ArgumentParser(description="GitHub Agent CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Create repository command
        repo_parser = subparsers.add_parser("create-repo", help="Create repository")
        repo_parser.add_argument("name", help="Repository name")
        repo_parser.add_argument("-d", "--description", help="Repository description")
        repo_parser.add_argument(
            "-p", "--private", action="store_true", help="Make repository private"
        )
        repo_parser.add_argument(
            "-a", "--auto-init", action="store_true", help="Auto-initialize repository"
        )

        # Create issue command
        issue_parser = subparsers.add_parser("create-issue", help="Create issue")
        issue_parser.add_argument("owner", help="Repository owner")
        issue_parser.add_argument("repo", help="Repository name")
        issue_parser.add_argument("title", help="Issue title")
        issue_parser.add_argument("-b", "--body", help="Issue body")
        issue_parser.add_argument("-l", "--labels", help="Comma-separated labels")
        issue_parser.add_argument("-a", "--assignees", help="Comma-separated assignees")

        # Create pull request command
        pr_parser = subparsers.add_parser("create-pr", help="Create pull request")
        pr_parser.add_argument("owner", help="Repository owner")
        pr_parser.add_argument("repo", help="Repository name")
        pr_parser.add_argument("title", help="Pull request title")
        pr_parser.add_argument("head_branch", help="Head branch")
        pr_parser.add_argument("base_branch", help="Base branch")
        pr_parser.add_argument("-b", "--body", help="Pull request body")

        # Create file command
        file_parser = subparsers.add_parser("create-file", help="Create file")
        file_parser.add_argument("owner", help="Repository owner")
        file_parser.add_argument("repo", help="Repository name")
        file_parser.add_argument("path", help="File path")
        file_parser.add_argument("message", help="Commit message")
        file_parser.add_argument("-c", "--content", help="File content")
        file_parser.add_argument("-f", "--file-path", help="Path to file to upload")
        file_parser.add_argument("-b", "--branch", help="Branch name")

        # Create branch command
        branch_parser = subparsers.add_parser("create-branch", help="Create branch")
        branch_parser.add_argument("owner", help="Repository owner")
        branch_parser.add_argument("repo", help="Repository name")
        branch_parser.add_argument("branch_name", help="Branch name")
        branch_parser.add_argument("-f", "--from-branch", default="main", help="Source branch")

        # Grant permission command
        perm_parser = subparsers.add_parser("grant-permission", help="Grant permission")
        perm_parser.add_argument("agent_id", help="Agent ID")
        perm_parser.add_argument("repository", help="Repository name")
        perm_parser.add_argument(
            "permission_level", choices=["read", "write", "admin", "owner"], help="Permission level"
        )

        # List operations command
        ops_parser = subparsers.add_parser("list-operations", help="List operations")
        ops_parser.add_argument(
            "-s",
            "--status",
            choices=["pending", "in_progress", "completed", "failed"],
            help="Filter by status",
        )

        # Show audit logs command
        logs_parser = subparsers.add_parser("audit-logs", help="Show audit logs")
        logs_parser.add_argument("-a", "--agent-id", help="Filter by agent ID")
        logs_parser.add_argument("-r", "--repository", help="Filter by repository")
        logs_parser.add_argument("-l", "--limit", type=int, default=50, help="Limit number of logs")

        # Export data command
        export_parser = subparsers.add_parser("export", help="Export protocol data")
        export_parser.add_argument("-o", "--output", help="Output file")

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Route to appropriate handler
        handlers = {
            "create-repo": self.create_repository,
            "create-issue": self.create_issue,
            "create-pr": self.create_pull_request,
            "create-file": self.create_file,
            "create-branch": self.create_branch,
            "grant-permission": self.grant_permission,
            "list-operations": self.list_operations,
            "audit-logs": self.show_audit_logs,
            "export": self.export_data,
        }

        handler = handlers.get(args.command)
        if handler:
            handler(args)
        else:
            print(f"❌ Unknown command: {args.command}")


def main():
    """Main entry point."""
    cli = GitHubAgentCLI()
    cli.run()


if __name__ == "__main__":
    main()
