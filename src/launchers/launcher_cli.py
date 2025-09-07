from pathlib import Path
from typing import Dict, Any
import argparse
import sys

                import traceback
    from .launcher_core import LauncherCore
    from .launcher_modes import LauncherModes
    from launcher_core import LauncherCore
    from launcher_modes import LauncherModes
from src.utils.stability_improvements import stability_manager, safe_import

#!/usr/bin/env python3
"""
Launcher CLI - Command Line Interface

This module provides the command-line interface for the launcher including:
- Argument parsing and validation
- User interaction and help
- Mode selection and execution

Architecture: Single Responsibility Principle - CLI interface only
LOC: 150 lines (under 200 limit)
"""



# Import launcher components
try:
except ImportError:
    # Fallback for when running directly
    sys.path.insert(0, str(Path(__file__).parent))


class LauncherCLI:
    """Command-line interface for the launcher system"""

    def __init__(self):
        self.core = LauncherCore()
        self.modes = LauncherModes()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all options."""
        parser = argparse.ArgumentParser(
            description="Unified Launcher for Agent Cellphone System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --check                    # Check system status
  %(prog)s --init                     # Initialize agents
  %(prog)s --mode onboarding         # Run onboarding sequence
  %(prog)s --mode coordination       # Run coordination test
  %(prog)s --mode autonomous         # Run autonomous workflow
  %(prog)s --mode cleanup            # Run repository cleanup
  %(prog)s --status                  # Get agent status
  %(prog)s --shutdown                # Shutdown agents
  %(prog)s --list-modes              # List available modes
  %(prog)s --test                    # Test all functionality
            """,
        )

        # System operations
        parser.add_argument(
            "--check", action="store_true", help="Check system status and dependencies"
        )
        parser.add_argument(
            "--init", action="store_true", help="Initialize all 5 agents"
        )
        parser.add_argument(
            "--status", action="store_true", help="Get status of all agents"
        )
        parser.add_argument(
            "--shutdown", action="store_true", help="Shutdown all agents gracefully"
        )

        # Mode operations
        parser.add_argument(
            "--mode",
            choices=["onboarding", "coordination", "autonomous", "cleanup"],
            help="Run a specific launcher mode",
        )
        parser.add_argument(
            "--list-modes",
            action="store_true",
            help="List all available launcher modes",
        )

        # Testing and debugging
        parser.add_argument(
            "--test", action="store_true", help="Test all launcher functionality"
        )
        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )

        return parser

    def print_banner(self):
        """Print the system banner."""
        print("=" * 80)
        print("🚀 UNIFIED 5-AGENT AGENT CELLPHONE SYSTEM")
        print("=" * 80)
        print("🔧 Consolidated working implementation with unified entry point...")
        print("📱 5-Agent Mode: Agent-1, Agent-2, Agent-3, Agent-4, Agent-5")
        print("🎯 Real onboarding, messaging, and coordination")
        print("=" * 80)

    def run_system_check(self) -> bool:
        """Run system check and return status."""
        print("🔍 Running system check...")
        return self.core.check_system()

    def run_agent_initialization(self) -> bool:
        """Run agent initialization and return status."""
        print("🚀 Initializing agents...")
        return self.core.initialize_agents()

    def run_mode_execution(self, mode: str) -> bool:
        """Run a specific mode and return status."""
        if not self.core.agents:
            print("❌ No agents initialized. Run --init first.")
            return False

        print(f"🚀 Running {mode} mode...")
        return self.modes.run_mode(mode, self.core.agents)

    def list_available_modes(self):
        """List all available launcher modes."""
        modes = self.modes.get_available_modes()
        print("Available launcher modes:")
        for mode in modes:
            print(f"  - {mode}")

    def get_agent_status(self):
        """Get and display agent status."""
        if not self.core.agents:
            print("❌ No agents initialized. Run --init first.")
            return

        status = self.core.get_agent_status()
        print("Agent Status:")
        for agent_id, agent_status in status.items():
            print(f"  {agent_id}: {agent_status}")

    def run_tests(self):
        """Run all launcher tests."""
        print("🧪 Running launcher tests...")

        # Test system check
        print("Testing system check...")
        system_ok = self.run_system_check()

        # Test mode listing
        print("Testing mode listing...")
        self.list_available_modes()

        # Test with empty agents (simulation)
        print("Testing mode execution (simulation)...")
        test_agents = {}
        for mode in self.modes.get_available_modes():
            print(f"  Testing {mode} mode...")
            self.modes.run_mode(mode, test_agents)

        print("✅ All tests completed")

    def run(self, args=None):
        """Run the launcher CLI with the given arguments."""
        if args is None:
            args = self.parser.parse_args()

        # Print banner for most operations
        if any(
            [args.check, args.init, args.mode, args.status, args.shutdown, args.test]
        ):
            self.print_banner()

        try:
            # Handle system operations
            if args.check:
                self.run_system_check()

            elif args.init:
                if self.run_system_check():
                    self.run_agent_initialization()

            elif args.status:
                self.get_agent_status()

            elif args.shutdown:
                self.core.shutdown_agents()

            # Handle mode operations
            elif args.mode:
                if self.run_system_check() and self.run_agent_initialization():
                    self.run_mode_execution(args.mode)

            elif args.list_modes:
                self.list_available_modes()

            # Handle testing
            elif args.test:
                self.run_tests()

            # Default: show help
            else:
                self.parser.print_help()

        except KeyboardInterrupt:
            print("\n👋 Launcher interrupted by user")
        except Exception as e:
            print(f"❌ Launcher error: {e}")
            if args.verbose:

                traceback.print_exc()


def main():
    """Main entry point for the launcher CLI."""
    cli = LauncherCLI()
    cli.run()


if __name__ == "__main__":
    main()
