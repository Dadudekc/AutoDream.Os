#!/usr/bin/env python3
"""
Coherent Collaboration CLI - Unified interface for AutoDream.OS collaboration tools.
Provides access to Project Registry, Design Authority, Vibe Check, and PR Review.

V2 Compliance Refactored: ≤400 lines (split handlers to separate module)
Author: Agent-7 (Web Development Expert)
"""

import argparse
import sys

from .coherent_collaboration_cli_handlers import (
    handle_design_command,
    handle_knowledge_command,
    handle_pr_command,
    handle_registry_command,
    handle_vibe_command,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AutoDream.OS Coherent Collaboration Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check if component exists before creating
  python -m src.core.coherent_collaboration_cli registry check-component ollama_client

  # Review a component plan with Design Authority
  python -m src.core.coherent_collaboration_cli design review-plan Agent-7 "Create simple HTTP client"

  # Run vibe check on file
  python -m src.core.coherent_collaboration_cli vibe check-file src/main.py --agent Agent-7

  # Create a pull request
  python -m src.core.coherent_collaboration_cli pr create --author Agent-7 --title "Add HTTP client"

  # Get pending reviews for agent
  python -m src.core.coherent_collaboration_cli pr pending --reviewer Agent-5
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Registry commands
    registry_parser = subparsers.add_parser("registry", help="Project Registry operations")
    registry_subparsers = registry_parser.add_subparsers(dest="registry_action")

    # Registry: check component
    check_comp_parser = registry_subparsers.add_parser(
        "check-component", help="Check if component exists"
    )
    check_comp_parser.add_argument("component_name", help="Name of component to check")

    # Registry: register component
    register_comp_parser = registry_subparsers.add_parser(
        "register-component", help="Register new component"
    )
    register_comp_parser.add_argument("name", help="Component name")
    register_comp_parser.add_argument("path", help="Component file path")
    register_comp_parser.add_argument("purpose", help="Component purpose")
    register_comp_parser.add_argument("owner", help="Agent owner")
    register_comp_parser.add_argument("--dependencies", nargs="*", help="Component dependencies")

    # Registry: list components
    list_comp_parser = registry_subparsers.add_parser("list-components", help="List all components")
    list_comp_parser.add_argument("--owner", help="Filter by owner")

    # Registry: summary
    registry_subparsers.add_parser("summary", help="Get registry summary")

    # Design Authority commands
    design_parser = subparsers.add_parser("design", help="Design Authority operations")
    design_subparsers = design_parser.add_subparsers(dest="design_action")

    # Design: review plan
    review_plan_parser = design_subparsers.add_parser("review-plan", help="Review component plan")
    review_plan_parser.add_argument("requester", help="Agent requesting review")
    review_plan_parser.add_argument("component_name", help="Name of component")
    review_plan_parser.add_argument("plan", help="Description of plan")
    review_plan_parser.add_argument("--context", help="Additional context")

    # Design: review code
    review_code_parser = design_subparsers.add_parser("review-code", help="Review code complexity")
    review_code_parser.add_argument("requester", help="Agent requesting review")
    review_code_parser.add_argument("component_name", help="Name of component")
    review_code_parser.add_argument("--file", help="File path to review")
    review_code_parser.add_argument("--code", help="Code snippet to review")

    # Design: knowledge
    design_subparsers.add_parser("knowledge", help="Get design knowledge summary")

    # Vibe Check commands
    vibe_parser = subparsers.add_parser("vibe", help="Vibe Check operations")
    vibe_subparsers = vibe_parser.add_subparsers(dest="vibe_action")

    # Vibe: check file
    check_file_parser = vibe_subparsers.add_parser("check-file", help="Check single file")
    check_file_parser.add_argument("file_path", help="Path to file to check")
    check_file_parser.add_argument("--agent", default="", help="Agent author")
    check_file_parser.add_argument("--strict", action="store_true", help="Fail on warnings")

    # Vibe: check directory
    check_dir_parser = vibe_subparsers.add_parser("check-directory", help="Check directory")
    check_dir_parser.add_argument("directory", help="Directory to check")
    check_dir_parser.add_argument("--agent", default="", help="Agent author")
    check_dir_parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    check_dir_parser.add_argument("--patterns", nargs="*", default=["*.py"], help="File patterns")

    # Vibe: check strict
    check_strict_parser = vibe_subparsers.add_parser(
        "check-strict", help="Strict check (fails on warnings)"
    )
    check_strict_parser.add_argument("file_paths", nargs="+", help="Files to check")
    check_strict_parser.add_argument("--agent", default="", help="Agent author")

    # PR Review commands
    pr_parser = subparsers.add_parser("pr", help="Pull Request operations")
    pr_subparsers = pr_parser.add_subparsers(dest="pr_action")

    # PR: create
    create_pr_parser = pr_subparsers.add_parser("create", help="Create pull request")
    create_pr_parser.add_argument("--author", required=True, help="PR author")
    create_pr_parser.add_argument("--title", required=True, help="PR title")
    create_pr_parser.add_argument("--description", required=True, help="PR description")
    create_pr_parser.add_argument("--files", nargs="+", help="Changed files")
    create_pr_parser.add_argument(
        "--priority",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
        help="Review priority",
    )
    create_pr_parser.add_argument("--reviewer", help="Specific reviewer")

    # PR: review
    review_pr_parser = pr_subparsers.add_parser("review", help="Review pull request")
    review_pr_parser.add_argument("pr_id", help="PR ID to review")
    review_pr_parser.add_argument("--reviewer", required=True, help="Reviewing agent")

    # PR: pending
    pending_pr_parser = pr_subparsers.add_parser("pending", help="Get pending reviews")
    pending_pr_parser.add_argument("--reviewer", required=True, help="Reviewer agent")

    # PR: list
    list_pr_parser = pr_subparsers.add_parser("list", help="List PRs")
    list_pr_parser.add_argument("--author", help="Filter by author")
    list_pr_parser.add_argument("--status", help="Filter by status")

    # Knowledge commands
    knowledge_parser = subparsers.add_parser("knowledge", help="Knowledge Base operations")
    knowledge_subparsers = knowledge_parser.add_subparsers(dest="knowledge_action")

    # Knowledge: principles
    knowledge_subparsers.add_parser("principles", help="List design principles")

    # Knowledge: patterns
    knowledge_subparsers.add_parser("patterns", help="List code patterns")

    # Knowledge: anti-patterns
    knowledge_subparsers.add_parser("anti-patterns", help="List anti-patterns")

    # Knowledge: guidelines
    knowledge_subparsers.add_parser("guidelines", help="Show project guidelines")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "registry":
            handle_registry_command(args)
        elif args.command == "design":
            handle_design_command(args)
        elif args.command == "vibe":
            handle_vibe_command(args)
        elif args.command == "pr":
            handle_pr_command(args)
        elif args.command == "knowledge":
            handle_knowledge_command(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
