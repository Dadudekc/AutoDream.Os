#!/usr/bin/env python3
"""
Agent Toolbelt CLI Wrapper
===========================

Backward-compatible CLI wrapper for Agent Toolbelt V2.

This file maintains the original CLI interface while delegating to the new
modular V2-compliant architecture in tools_v2/.

Usage:
    python tools/agent_toolbelt.py vector context --agent Agent-7 --task "consolidation"
    python tools/agent_toolbelt.py message --agent Agent-4 "Status update"
    python tools/agent_toolbelt.py analyze project
    python tools/agent_toolbelt.py v2 check src/

Author: Agent-7 - Repository Cloning Specialist
V2 Compliance: Thin wrapper delegating to tools_v2/, <200 lines
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import executors
from tools.agent_toolbelt_executors import (
    AgentExecutor,
    AnalysisExecutor,
    ComplianceExecutor,
    ConsolidationExecutor,
    MessagingExecutor,
    RefactorExecutor,
    V2Executor,
    VectorExecutor,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",  # Simplified for CLI output
)
logger = logging.getLogger(__name__)


class AgentToolbeltCLI:
    """CLI interface for Agent Toolbelt V2."""

    def __init__(self):
        """Initialize CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create main argument parser with subcommands."""
        parser = argparse.ArgumentParser(
            description="🛠️ Agent Toolbelt - Unified CLI for all agent tools",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Vector DB operations
  %(prog)s vector context --agent Agent-7 --task "consolidation"
  %(prog)s vector search "V2 compliance patterns"
  %(prog)s vector index --agent Agent-7 --file completed_work.py
  
  # Messaging operations
  %(prog)s message --agent Agent-4 "Status update"
  %(prog)s broadcast "Swarm coordination needed"
  
  # Analysis tools
  %(prog)s analyze project
  %(prog)s analyze complexity src/
  %(prog)s analyze duplicates
  
  # V2 compliance
  %(prog)s v2 check src/tools/
  %(prog)s v2 report --format json
  
  # Agent operations
  %(prog)s status --agent Agent-7
  %(prog)s inbox --agent Agent-7
  %(prog)s claim-task --agent Agent-7

🐝 WE. ARE. SWARM. ⚡️🔥
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Command to execute")

        # Vector DB subcommand
        self._add_vector_parser(subparsers)

        # Messaging subcommand
        self._add_messaging_parser(subparsers)

        # Analysis subcommand
        self._add_analysis_parser(subparsers)

        # V2 compliance subcommand
        self._add_v2_parser(subparsers)

        # Agent operations subcommand
        self._add_agent_parser(subparsers)

        # Consolidation tools subcommand
        self._add_consolidation_parser(subparsers)

        # Refactoring tools subcommand
        self._add_refactor_parser(subparsers)

        # Compliance tools subcommand
        self._add_compliance_parser(subparsers)

        return parser

    def _add_vector_parser(self, subparsers):
        """Add vector database subcommand."""
        vector_parser = subparsers.add_parser(
            "vector", help="Vector database operations (search, index, context, patterns)"
        )
        vector_sub = vector_parser.add_subparsers(dest="vector_action", help="Vector operation")

        # Context command
        context_p = vector_sub.add_parser("context", help="Get intelligent task context")
        context_p.add_argument("--agent", required=True, help="Agent ID")
        context_p.add_argument("--task", required=True, help="Task description")

        # Search command
        search_p = vector_sub.add_parser("search", help="Semantic search")
        search_p.add_argument("query", help="Search query")
        search_p.add_argument("--agent", help="Filter by agent ID")
        search_p.add_argument("--limit", type=int, default=5, help="Max results")

        # Patterns command
        patterns_p = vector_sub.add_parser("patterns", help="Get success patterns")
        patterns_p.add_argument("--agent", required=True, help="Agent ID")
        patterns_p.add_argument("--task-type", required=True, help="Task type")

        # Index command
        index_p = vector_sub.add_parser("index", help="Index work to vector DB")
        index_p.add_argument("--agent", required=True, help="Agent ID")
        index_p.add_argument("--file", help="File to index")
        index_p.add_argument("--inbox", action="store_true", help="Index inbox messages")
        index_p.add_argument("--work-type", default="code", help="Work type")

        # Stats command
        vector_sub.add_parser("stats", help="Show vector DB statistics")

    def _add_messaging_parser(self, subparsers):
        """Add messaging subcommand."""
        msg_parser = subparsers.add_parser("message", help="Messaging operations")
        msg_parser.add_argument("text", nargs="?", help="Message text")
        msg_parser.add_argument("--agent", help="Target agent ID")
        msg_parser.add_argument("--broadcast", action="store_true", help="Broadcast to all")
        msg_parser.add_argument("--priority", choices=["regular", "urgent"], default="regular")
        msg_parser.add_argument("--inbox", action="store_true", help="Read inbox")
        msg_parser.add_argument("--status", action="store_true", help="Get agent status")

    def _add_analysis_parser(self, subparsers):
        """Add analysis subcommand."""
        analysis_parser = subparsers.add_parser("analyze", help="Code analysis tools")
        analysis_sub = analysis_parser.add_subparsers(dest="analysis_type", help="Analysis type")

        # Project scan
        analysis_sub.add_parser("project", help="Run comprehensive project scan")

        # Complexity analysis
        complexity_p = analysis_sub.add_parser("complexity", help="Analyze code complexity")
        complexity_p.add_argument("path", nargs="?", default="src/", help="Path to analyze")
        complexity_p.add_argument("--threshold", type=int, default=10, help="Complexity threshold")

        # Duplication analysis
        dup_p = analysis_sub.add_parser("duplicates", help="Find duplicate code")
        dup_p.add_argument("path", nargs="?", default="src/", help="Path to scan")

        # Refactoring suggestions
        refactor_p = analysis_sub.add_parser("refactor", help="Get refactoring suggestions")
        refactor_p.add_argument("path", help="Path to analyze")

    def _add_v2_parser(self, subparsers):
        """Add V2 compliance subcommand."""
        v2_parser = subparsers.add_parser("v2", help="V2 compliance operations")
        v2_parser.add_argument(
            "action", choices=["check", "report", "violations"], help="V2 operation"
        )
        v2_parser.add_argument("path", nargs="?", default="src/", help="Path to check")
        v2_parser.add_argument("--format", choices=["text", "json"], default="text")
        v2_parser.add_argument("--fix", action="store_true", help="Auto-fix simple violations")

    def _add_agent_parser(self, subparsers):
        """Add agent operations subcommand."""
        agent_parser = subparsers.add_parser("agent", help="Agent operations")
        agent_sub = agent_parser.add_subparsers(dest="agent_action", help="Agent operation")

        # Status
        status_p = agent_sub.add_parser("status", help="Get agent status")
        status_p.add_argument("--agent", required=True, help="Agent ID")

        # Inbox
        inbox_p = agent_sub.add_parser("inbox", help="Check agent inbox")
        inbox_p.add_argument("--agent", required=True, help="Agent ID")
        inbox_p.add_argument("--search", help="Search inbox semantically")

        # Claim task
        claim_p = agent_sub.add_parser("claim-task", help="Claim next available task")
        claim_p.add_argument("--agent", required=True, help="Agent ID")

        # Coordinates
        agent_sub.add_parser("coordinates", help="Show all agent coordinates")

    def _add_consolidation_parser(self, subparsers):
        """Add consolidation tools subcommand."""
        consol_parser = subparsers.add_parser("consolidate", help="Consolidation tools")
        consol_sub = consol_parser.add_subparsers(
            dest="consol_action", help="Consolidation operation"
        )

        # Find duplicates
        dup_p = consol_sub.add_parser("find-duplicates", help="Find duplicate files")
        dup_p.add_argument("path", nargs="?", default="src/", help="Path to scan")
        dup_p.add_argument("--type", choices=["files", "classes", "functions"], default="files")

        # Suggest consolidation
        suggest_p = consol_sub.add_parser("suggest", help="Suggest consolidations")
        suggest_p.add_argument("path", nargs="?", default="src/", help="Path to analyze")
        suggest_p.add_argument("--min-similarity", type=float, default=0.8)

        # Verify consolidation safety
        verify_p = consol_sub.add_parser("verify", help="Verify consolidation safety")
        verify_p.add_argument("source_file", help="Source file to consolidate")
        verify_p.add_argument("target_file", help="Target file")

    def _add_refactor_parser(self, subparsers):
        """Add refactoring tools subcommand."""
        refactor_parser = subparsers.add_parser("refactor", help="Refactoring tools")
        refactor_sub = refactor_parser.add_subparsers(
            dest="refactor_action", help="Refactor operation"
        )

        # Split file
        split_p = refactor_sub.add_parser("split", help="Split file into modules")
        split_p.add_argument("file", help="File to split")
        split_p.add_argument("--strategy", choices=["class", "function", "auto"], default="auto")
        split_p.add_argument("--max-classes", type=int, default=5)

        # Apply facade
        facade_p = refactor_sub.add_parser("facade", help="Apply facade pattern")
        facade_p.add_argument("directory", help="Directory with split modules")
        facade_p.add_argument("--main-file", help="Main facade file name")

        # Extract module
        extract_p = refactor_sub.add_parser("extract", help="Extract classes to module")
        extract_p.add_argument("source_file", help="Source file")
        extract_p.add_argument("class_names", nargs="+", help="Classes to extract")
        extract_p.add_argument("--target", help="Target file name")

    def _add_compliance_parser(self, subparsers):
        """Add compliance checking tools subcommand."""
        comp_parser = subparsers.add_parser("compliance", help="V2 compliance checking")
        comp_parser.add_argument("--file", help="File to check (for backward compat)")
        comp_sub = comp_parser.add_subparsers(
            dest="comp_action", help="Compliance operation", required=False
        )

        # Count classes
        classes_p = comp_sub.add_parser("count-classes", help="Count classes in file")
        classes_p.add_argument("file", help="File to check")
        classes_p.add_argument("--warn", action="store_true", help="Warn if >5")

        # Count functions
        funcs_p = comp_sub.add_parser("count-functions", help="Count functions in file")
        funcs_p.add_argument("file", help="File to check")
        funcs_p.add_argument("--warn", action="store_true", help="Warn if >10")

        # Check file
        check_p = comp_sub.add_parser("check-file", help="Full V2 compliance check")
        check_p.add_argument("file", help="File to check")
        check_p.add_argument("--suggest-fixes", action="store_true")

        # Scan violations
        scan_p = comp_sub.add_parser("scan-violations", help="Scan for all violations")
        scan_p.add_argument("path", nargs="?", default="src/", help="Path to scan")
        scan_p.add_argument("--format", choices=["text", "json"], default="text")

        # Test imports
        import_p = comp_sub.add_parser("test-imports", help="Test all imports in file/module")
        import_p.add_argument("path", help="File or module path")
        import_p.add_argument("--verify-backcompat", action="store_true")

    def execute(self, args=None):
        """Execute toolbelt command."""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return 0

        try:
            if parsed_args.command == "vector":
                return VectorExecutor.execute(parsed_args)
            elif parsed_args.command == "message":
                return MessagingExecutor.execute(parsed_args)
            elif parsed_args.command == "analyze":
                return AnalysisExecutor.execute(parsed_args)
            elif parsed_args.command == "v2":
                return V2Executor.execute(parsed_args)
            elif parsed_args.command == "agent":
                return AgentExecutor.execute(parsed_args)
            elif parsed_args.command == "consolidate":
                return ConsolidationExecutor.execute(parsed_args)
            elif parsed_args.command == "refactor":
                return RefactorExecutor.execute(parsed_args)
            elif parsed_args.command == "compliance":
                if not parsed_args.comp_action and parsed_args.file:
                    # Quick check shorthand
                    parsed_args.comp_action = "check-file"
                    parsed_args.suggest_fixes = True
                return ComplianceExecutor.execute(parsed_args)
            else:
                self.parser.print_help()
                return 1
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return 1


def main():
    """Main entry point."""
    cli = AgentToolbeltCLI()

    try:
        exit_code = cli.execute()

        if exit_code == 0:
            print("\n🐝 WE. ARE. SWARM. ⚡️🔥")

        return exit_code
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
