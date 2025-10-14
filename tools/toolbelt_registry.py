"""
CLI Toolbelt Registry - Tool Discovery and Registration
========================================================

Tool registry and discovery system for CLI Toolbelt.
Maps flags to tool modules with metadata.

Architecture: Agent-2 (C-058-2)
Implementation: Agent-1 (C-058-1)
V2 Compliance: ~120 lines

Author: Agent-1 - Code Integration & Testing Specialist
Date: 2025-10-11
License: MIT
"""

from typing import Any

# Tool Registry - Maps tool IDs to configuration
TOOLS_REGISTRY: dict[str, dict[str, Any]] = {
    "scan": {
        "name": "Project Scanner",
        "module": "tools.run_project_scan",
        "main_function": "main",
        "description": "Scan project structure and generate analysis",
        "flags": ["--scan", "-s"],
        "args_passthrough": True,
    },
    "v2-check": {
        "name": "V2 Compliance Checker",
        "module": "tools.v2_checker_cli",
        "main_function": "main",
        "description": "Check V2 compliance violations",
        "flags": ["--v2-check", "--v2", "-v"],
        "args_passthrough": True,
    },
    "dashboard": {
        "name": "Compliance Dashboard",
        "module": "tools.dashboard_html_generator",
        "main_function": "main",
        "description": "Open compliance tracking dashboard",
        "flags": ["--dashboard", "-d"],
        "args_passthrough": False,
    },
    "complexity": {
        "name": "Complexity Analyzer",
        "module": "tools.complexity_analyzer",
        "main_function": "main",
        "description": "Analyze code complexity metrics",
        "flags": ["--complexity", "-c"],
        "args_passthrough": True,
    },
    "refactor": {
        "name": "Refactoring Suggestions",
        "module": "tools.refactoring_suggestions",
        "main_function": "main",
        "description": "Get intelligent refactoring suggestions",
        "flags": ["--refactor", "-r"],
        "args_passthrough": True,
    },
    "duplication": {
        "name": "Duplication Analyzer",
        "module": "tools.duplication_analyzer",
        "main_function": "main",
        "description": "Find duplicate code across project",
        "flags": ["--duplication", "--dup"],
        "args_passthrough": True,
    },
    "functionality": {
        "name": "Functionality Verification",
        "module": "tools.functionality_verification",
        "main_function": "main",
        "description": "Verify functionality preservation",
        "flags": ["--functionality", "--verify"],
        "args_passthrough": True,
    },
    "leaderboard": {
        "name": "Autonomous Leaderboard",
        "module": "tools.autonomous_leaderboard",
        "main_function": "main",
        "description": "Show agent performance leaderboard",
        "flags": ["--leaderboard", "-l"],
        "args_passthrough": True,
    },
    "history": {
        "name": "Compliance History",
        "module": "tools.compliance_history_tracker",
        "main_function": "main",
        "description": "Track compliance history over time",
        "flags": ["--history"],
        "args_passthrough": True,
    },
    "soft-onboard": {
        "name": "Soft Onboarding",
        "module": "tools.soft_onboard_cli",
        "main_function": "main",
        "description": "Soft onboard agents (6-step session cleanup protocol)",
        "flags": ["--soft-onboard", "--soft"],
        "args_passthrough": True,
    },
    "swarm-brain": {
        "name": "Swarm Brain Update",
        "module": "tools.update_swarm_brain",
        "main_function": "main",
        "description": "Update swarm brain with insights/lessons/patterns",
        "flags": ["--swarm-brain", "--brain"],
        "args_passthrough": True,
    },
    "message": {
        "name": "Send Message",
        "module": "src.services.messaging_cli",
        "main_function": "main",
        "description": "Send messages to agents via messaging system",
        "flags": ["--message-cli", "--msg"],
        "args_passthrough": True,
    },
    "pattern-validator": {
        "name": "Architecture Pattern Validator",
        "module": "tools.arch_pattern_validator",
        "main_function": "main",
        "description": "Validate architectural patterns (Agent-2's tool)",
        "flags": ["--validate-patterns", "--patterns"],
        "args_passthrough": True,
    },
    "linecount": {
        "name": "Quick Line Count",
        "module": "tools.quick_linecount",
        "main_function": "main",
        "description": "Quick line count for files/directories",
        "flags": ["--linecount", "--lines"],
        "args_passthrough": True,
    },
    "validate-imports": {
        "name": "Import Validator",
        "module": "tools.validate_imports",
        "main_function": "main",
        "description": "Validate import statements and dependencies",
        "flags": ["--validate-imports", "--imports"],
        "args_passthrough": True,
    },
    "get-task": {
        "name": "Get Next Task",
        "module": "src.services.messaging_cli",
        "main_function": "main",
        "description": "Claim next task from centralized task system (Step 1 of workflow)",
        "flags": ["--get-task", "--next-task"],
        "args_passthrough": False,
        "override_args": ["--get-next-task"],
    },
    "list-tasks": {
        "name": "List Tasks",
        "module": "src.services.messaging_cli",
        "main_function": "main",
        "description": "List all available tasks in queue",
        "flags": ["--tasks", "--task-list"],
        "args_passthrough": False,
        "override_args": ["--list-tasks"],
    },
    # QA & Validation Tools (Agent-8)
    "memory-scan": {
        "name": "Memory Leak Scanner",
        "module": "tools.memory_leak_scanner",
        "main_function": "main",
        "description": "Detect unbounded caches, lists, and memory leaks",
        "flags": ["--memory-scan", "--memleak"],
        "args_passthrough": True,
    },
    "git-verify": {
        "name": "Git Commit Verifier",
        "module": "tools.git_commit_verifier",
        "main_function": "main",
        "description": "Verify claimed work exists in git history",
        "flags": ["--git-verify", "--verify-commits"],
        "args_passthrough": True,
    },
    "test-pyramid": {
        "name": "Test Pyramid Analyzer",
        "module": "tools.test_pyramid_analyzer",
        "main_function": "main",
        "description": "Analyze test distribution vs 60/30/10 target",
        "flags": ["--test-pyramid", "--pyramid"],
        "args_passthrough": True,
    },
    "v2-batch": {
        "name": "V2 Batch Checker",
        "module": "tools.v2_compliance_batch_checker",
        "main_function": "main",
        "description": "Quick V2 compliance check for multiple files",
        "flags": ["--v2-batch", "--batch"],
        "args_passthrough": True,
    },
    "coverage-check": {
        "name": "Coverage Validator",
        "module": "tools.coverage_validator",
        "main_function": "main",
        "description": "Validate test coverage meets thresholds",
        "flags": ["--coverage-check", "--cov"],
        "args_passthrough": True,
    },
    "qa-checklist": {
        "name": "QA Validation Checklist",
        "module": "tools.qa_validation_checklist",
        "main_function": "main",
        "description": "Automated QA validation checklist",
        "flags": ["--qa-checklist", "--qa"],
        "args_passthrough": True,
    },
    # Agent Coordination & Communication Tools (Agent-6)
    "agent-status": {
        "name": "Agent Status Quick Check",
        "module": "tools.agent_status_quick_check",
        "main_function": "main",
        "description": "Fast agent progress verification (prevents 'already done' confusion)",
        "flags": ["--agent-status", "--status-check"],
        "args_passthrough": True,
    },
    "extension-test": {
        "name": "Extension Test Runner",
        "module": "tools.extension_test_runner",
        "main_function": "main",
        "description": "VSCode extension testing with coverage",
        "flags": ["--extension-test", "--ext-test"],
        "args_passthrough": True,
    },
    "message-history": {
        "name": "Agent Message History",
        "module": "tools.agent_message_history",
        "main_function": "main",
        "description": "View recent agent message exchanges",
        "flags": ["--message-history", "--msg-history"],
        "args_passthrough": True,
    },
    "verify-complete": {
        "name": "Work Completion Verifier",
        "module": "tools.work_completion_verifier",
        "main_function": "main",
        "description": "Verify work completion before sending messages",
        "flags": ["--verify-complete", "--verify-work"],
        "args_passthrough": True,
    },
    # Architecture & Integration Tools (Agent-2)
    "arch-review": {
        "name": "Architecture Review",
        "module": "tools.architecture_review",
        "main_function": "main",
        "description": "Request/provide expert architecture reviews",
        "flags": ["--arch-review", "--review"],
        "args_passthrough": True,
    },
    "real-violations": {
        "name": "Real Violation Scanner",
        "module": "tools.real_violation_scanner",
        "main_function": "main",
        "description": "Verify actual V2 violations (intelligent verification)",
        "flags": ["--real-violations", "--real-v2"],
        "args_passthrough": True,
    },
    "pattern-suggest": {
        "name": "Pattern Suggester",
        "module": "tools.pattern_suggester",
        "main_function": "main",
        "description": "Suggest consolidation patterns for refactoring",
        "flags": ["--pattern-suggest", "--suggest-pattern"],
        "args_passthrough": True,
    },
    "integration-validate": {
        "name": "Integration Validator",
        "module": "tests.integration.system_integration_validator",
        "main_function": "main",
        "description": "Comprehensive system integration validation (C-048-5)",
        "flags": ["--integration-validate", "--int-val"],
        "args_passthrough": False,
    },
    # MASTERPIECE TOOL - Swarm Autonomous Orchestrator (Agent-8)
    "orchestrate": {
        "name": "Swarm Autonomous Orchestrator",
        "module": "tools.swarm_orchestrator",
        "main_function": "run_orchestrator",
        "description": "The Gas Station - Autonomous swarm coordination and gas delivery",
        "flags": ["--orchestrate", "--gas-station", "--swarm"],
        "args_passthrough": True,
    },
    # MASTERPIECE TOOL - Mission Control (Agent-2)
    "mission-control": {
        "name": "Mission Control - Autonomous Mission Generator",
        "module": "tools.mission_control",
        "main_function": "main",
        "description": "THE masterpiece - Runs all 5 workflow steps, generates conflict-free mission brief",
        "flags": ["--mission-control", "--mission", "--mc"],
        "args_passthrough": True,
    },
}


class ToolRegistry:
    """Tool registry for CLI Toolbelt."""

    def __init__(self):
        """Initialize tool registry."""
        self.tools = TOOLS_REGISTRY
        self._flag_map = self._build_flag_map()

    def _build_flag_map(self) -> dict[str, str]:
        """Build mapping from flags to tool IDs."""
        flag_map = {}
        for tool_id, config in self.tools.items():
            for flag in config["flags"]:
                flag_map[flag] = tool_id
        return flag_map

    def get_tool_for_flag(self, flag: str) -> dict[str, Any] | None:
        """
        Get tool configuration by flag.

        Args:
            flag: Tool flag (e.g., "--scan", "-s")

        Returns:
            Tool configuration or None if not found
        """
        tool_id = self._flag_map.get(flag)
        if tool_id:
            return self.tools[tool_id]
        return None

    def get_tool_by_name(self, name: str) -> dict[str, Any] | None:
        """
        Get tool configuration by tool ID.

        Args:
            name: Tool ID (e.g., "scan", "v2-check")

        Returns:
            Tool configuration or None if not found
        """
        return self.tools.get(name)

    def list_tools(self) -> list[dict[str, Any]]:
        """
        List all available tools.

        Returns:
            List of tool configurations
        """
        return [{"id": tool_id, **config} for tool_id, config in self.tools.items()]

    def get_all_flags(self) -> list[str]:
        """Get list of all registered flags."""
        return list(self._flag_map.keys())
