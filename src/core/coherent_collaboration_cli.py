#!/usr/bin/env python3
"""
Coherent Collaboration CLI - Unified interface for AutoDream.OS collaboration tools.
Provides access to Project Registry, Design Authority, Vibe Check, and PR Review.
"""

import argparse
import sys
from pathlib import Path

from .design_authority import design_authority, review_component_plan
from .knowledge_base import knowledge_base
from .pr_review_protocol import CodeChange, create_pull_request, pr_review_protocol
from .project_registry import check_component_exists, register_component, registry_manager
from .vibe_check import vibe_check_directory, vibe_check_file, vibe_check_strict


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


def handle_registry_command(args):
    """Handle registry commands."""
    if args.registry_action == "check-component":
        exists = check_component_exists(args.component_name)
        if exists:
            component = registry_manager.get_component(args.component_name)
            print(f"✅ Component '{args.component_name}' exists")
            print(f"   Path: {component.path}")
            print(f"   Owner: {component.owner}")
            print(f"   Purpose: {component.purpose}")
        else:
            print(f"❌ Component '{args.component_name}' does not exist")
            print("   Safe to create new component")

    elif args.registry_action == "register-component":
        component = register_component(
            name=args.name,
            path=args.path,
            purpose=args.purpose,
            owner=args.owner,
            dependencies=args.dependencies or [],
        )
        print(f"✅ Registered component '{args.name}'")
        print(f"   Path: {component.path}")
        print(f"   Owner: {component.owner}")
        print(f"   Created: {component.created_at}")

    elif args.registry_action == "list-components":
        registry = registry_manager.load_registry()
        components = registry.components

        if args.owner:
            components = {k: v for k, v in components.items() if v.owner == args.owner}

        if not components:
            print("No components found")
            return

        print(f"📋 Components ({len(components)} total):")
        for name, component in components.items():
            print(f"  • {name}")
            print(f"    Path: {component.path}")
            print(f"    Owner: {component.owner}")
            print(f"    Purpose: {component.purpose}")
            print()

    elif args.registry_action == "summary":
        summary = registry_manager.get_registry_summary()
        print("📊 Project Registry Summary:")
        print(f"  Project: {summary['project_name']} v{summary['version']}")
        print(f"  Total Components: {summary['total_components']}")
        print(f"  Active Agents: {', '.join(summary['active_agents'])}")
        print(f"  Last Updated: {summary['last_updated']}")
        print()
        print("📈 Component Breakdown:")
        for owner, count in summary["component_breakdown"]["by_owner"].items():
            print(f"  {owner}: {count} components")


def handle_design_command(args):
    """Handle design authority commands."""
    if args.design_action == "review-plan":
        review = review_component_plan(
            requester=args.requester,
            component_name=args.component_name,
            plan=args.plan,
            context=args.context or "",
        )

        print(f"🎯 Design Review: {review.request_id}")
        print(f"   Component: {review.component_name}")
        print(f"   Status: {'✅ APPROVED' if review.approved else '❌ REJECTED'}")
        print(f"   Severity: {review.severity.value}")
        print()
        print("📝 Feedback:")
        print(review.feedback)

        if review.alternatives:
            print("\n💡 Alternatives:")
            for alt in review.alternatives:
                print(f"   • {alt}")

    elif args.design_action == "review-code":
        if args.file:
            with open(args.file) as f:
                code = f.read()
        elif args.code:
            code = args.code
        else:
            print("Error: Must provide --file or --code")
            return

        review = design_authority.review_code_complexity(
            requester=args.requester, component_name=args.component_name, code_snippet=code
        )

        print(f"🎯 Code Review: {review.request_id}")
        print(f"   Component: {review.component_name}")
        print(f"   Status: {'✅ APPROVED' if review.approved else '❌ REJECTED'}")
        print()
        print("📝 Feedback:")
        print(review.feedback)

    elif args.design_action == "knowledge":
        summary = design_authority.get_knowledge_summary()
        print("🧠 Design Authority Knowledge:")
        print(f"  Principles: {', '.join(summary['principles'])}")
        print(f"  Anti-patterns: {summary['anti_patterns_count']}")
        print(f"  Total Reviews: {summary['total_reviews']}")
        print(f"  Approval Rate: {summary['approval_rate']:.1%}")
        print(f"  Last Updated: {summary['last_updated']}")


def handle_vibe_command(args):
    """Handle vibe check commands."""
    if args.vibe_action == "check-file":
        report = vibe_check_file(args.file_path, args.agent, args.strict)
        print_vibe_report(report)

    elif args.vibe_action == "check-directory":
        report = vibe_check_directory(args.directory, args.agent, args.strict)
        print_vibe_report(report)

    elif args.vibe_action == "check-strict":
        report = vibe_check_strict(args.file_paths, args.agent)
        print_vibe_report(report)


def handle_pr_command(args):
    """Handle pull request commands."""
    if args.pr_action == "create":
        # Simple changes for demonstration
        changes = []
        for file_path in args.files or []:
            changes.append(
                CodeChange(
                    file_path=file_path,
                    change_type="added" if not Path(file_path).exists() else "modified",
                )
            )

        pr_id = create_pull_request(
            author=args.author,
            title=args.title,
            description=args.description,
            changes=changes,
            assigned_reviewer=args.reviewer,
        )

        print(f"✅ Created Pull Request: {pr_id}")
        print(f"   Title: {args.title}")
        print(f"   Author: {args.author}")
        print(f"   Files: {', '.join(args.files or [])}")
        print("   Status: Pending Review")

    elif args.pr_action == "review":
        review_result = pr_review_protocol.review_pull_request(args.pr_id, args.reviewer)

        print(f"🎯 PR Review Complete: {args.pr_id}")
        print(f"   Reviewer: {args.reviewer}")
        print(f"   Status: {review_result.status.value.upper()}")
        print(f"   Approved: {'✅' if review_result.approved else '❌'}")
        print()
        print("📝 Feedback:")
        print(review_result.feedback)

    elif args.pr_action == "pending":
        pending_prs = pr_review_protocol.get_pending_reviews(args.reviewer)

        if not pending_prs:
            print(f"✅ No pending reviews for {args.reviewer}")
            return

        print(f"📋 Pending Reviews for {args.reviewer} ({len(pending_prs)} total):")
        for pr in pending_prs:
            print(f"  • {pr.pr_id}")
            print(f"    Title: {pr.title}")
            print(f"    Author: {pr.author}")
            print(f"    Priority: {pr.priority.value}")
            print(f"    Created: {pr.created_at}")
            print()

    elif args.pr_action == "list":
        all_prs = list(pr_review_protocol.pull_requests.values())

        if args.author:
            all_prs = [pr for pr in all_prs if pr.author == args.author]
        if args.status:
            all_prs = [pr for pr in all_prs if pr.status.value == args.status]

        if not all_prs:
            print("No pull requests found")
            return

        print(f"📋 Pull Requests ({len(all_prs)} total):")
        for pr in all_prs:
            print(f"  • {pr.pr_id}")
            print(f"    Title: {pr.title}")
            print(f"    Author: {pr.author}")
            print(f"    Reviewer: {pr.reviewer}")
            print(f"    Status: {pr.status.value}")
            print(f"    Priority: {pr.priority.value}")
            print()


def handle_knowledge_command(args):
    """Handle knowledge base commands."""
    if args.knowledge_action == "principles":
        principles = knowledge_base.get_required_principles()
        print("🎯 Required Design Principles:")
        for principle in principles:
            print(f"  • {principle.name}")
            print(f"    {principle.description}")
            print(f"    Category: {principle.category.value}")
            print()

    elif args.knowledge_action == "patterns":
        patterns = knowledge_base.get_simple_patterns(max_complexity=5)
        print("🔧 Code Patterns (Complexity ≤ 5):")
        for pattern in patterns:
            print(f"  • {pattern.name}")
            print(f"    {pattern.description}")
            print(f"    Complexity: {pattern.complexity_score}/10")
            print(f"    Type: {pattern.pattern_type}")
            print()

    elif args.knowledge_action == "anti-patterns":
        anti_patterns = knowledge_base.get_critical_anti_patterns()
        print("🚨 Critical Anti-Patterns to Avoid:")
        for anti_pattern in anti_patterns:
            print(f"  • {anti_pattern.name}")
            print(f"    {anti_pattern.description}")
            print(f"    Why bad: {anti_pattern.why_bad}")
            print()

    elif args.knowledge_action == "guidelines":
        guidelines = knowledge_base.get_all_guidelines()
        print("📋 Project Guidelines:")
        for category, rules in guidelines.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            if isinstance(rules, dict):
                for key, value in rules.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {rules}")


def print_vibe_report(report):
    """Print vibe check report in a formatted way."""
    print(f"🎯 Vibe Check Results: {report.result.value.upper()}")
    print(f"📁 Files Checked: {report.total_files}")
    print(f"🚨 Total Violations: {len(report.violations)}")

    if report.summary:
        print(f"   Errors: {report.summary.get('error_count', 0)}")
        print(f"   Warnings: {report.summary.get('warning_count', 0)}")

    if report.violations:
        print("\n🚨 Issues Found:")
        for violation in report.violations[:10]:  # Limit to first 10
            severity_icon = "❌" if violation.severity.value == "error" else "⚠️"
            print(f"{severity_icon} {violation.file_path}:{violation.line_number}")
            print(f"   {violation.description}")
            print(f"   💡 {violation.suggestion}")
            if violation.code_snippet:
                print(f"   📝 {violation.code_snippet}")
            print()

        if len(report.violations) > 10:
            print(f"... and {len(report.violations) - 10} more violations")

    if report.result.value == "fail":
        print("\n❌ Vibe check failed! Please fix issues before proceeding.")
        sys.exit(1)
    else:
        print("\n✅ Vibe check passed!")


if __name__ == "__main__":
    main()
