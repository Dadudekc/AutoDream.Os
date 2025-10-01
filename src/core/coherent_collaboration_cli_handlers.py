#!/usr/bin/env python3
"""
Coherent Collaboration CLI Handlers
===================================

Command handlers for coherent collaboration CLI.
Modular split from coherent_collaboration_cli.py for V2 compliance.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import sys
from pathlib import Path

from .design_authority import design_authority, review_component_plan
from .knowledge_base import knowledge_base
from .pr_review_protocol import CodeChange, create_pull_request, pr_review_protocol
from .project_registry import check_component_exists, register_component, registry_manager
from .vibe_check import vibe_check_directory, vibe_check_file, vibe_check_strict


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
        for violation in report.violations[:10]:
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


__all__ = [
    'handle_registry_command',
    'handle_design_command',
    'handle_vibe_command',
    'handle_pr_command',
    'handle_knowledge_command',
    'print_vibe_report',
]

