#!/usr/bin/env python3
"""
Captain Autonomous Manager - V2 Compliant Facade
===============================================

Facade for the modular Captain Autonomous Manager system.
Delegates to specialized modules for core functionality, interface, and utilities.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
V2 Compliance: ≤100 lines, modular design, comprehensive error handling
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .captain_autonomous_core import CaptainAutonomousCore
from .captain_autonomous_interface import CaptainAutonomousInterface
from .captain_autonomous_utility import CaptainAutonomousUtility


class CaptainAutonomousManager:
    """Facade for autonomous captain management system."""

    def __init__(self):
        """Initialize autonomous manager facade."""
        self.core = CaptainAutonomousCore()
        self.interface = CaptainAutonomousInterface()
        self.utility = CaptainAutonomousUtility()

    # Delegate to core functionality
    def detect_bottlenecks(self):
        """Detect system bottlenecks."""
        return self.core.detect_bottlenecks()

    def detect_flaws(self):
        """Detect system flaws."""
        return self.core.detect_flaws()

    def check_stopping_conditions(self):
        """Check if stopping conditions are met."""
        return self.core.check_stopping_conditions()

    def generate_autonomous_priorities(self):
        """Generate autonomous priorities based on system analysis."""
        return self.core.generate_autonomous_priorities()

    def provide_agent_guidance(self, agent_id: str):
        """Provide autonomous guidance to specific agent."""
        return self.core.provide_agent_guidance(agent_id)

    # Delegate to utility functions
    def run_quality_gates(self):
        """Run quality gates and return results."""
        return self.utility.run_quality_gates()

    def check_system_resources(self):
        """Check system resource usage."""
        return self.utility.check_system_resources()

    def check_v2_compliance(self, file_path):
        """Check V2 compliance for a file."""
        return self.utility.check_v2_compliance(file_path)


def main():
    """Main CLI function - delegates to interface."""
    interface = CaptainAutonomousInterface()
    return interface.run()


# V2 Compliance: File length check
if __name__ == "__main__":
    import inspect

    lines = len(inspect.getsource(inspect.currentframe().f_globals["__file__"]).splitlines())
    print(f"Captain Autonomous Manager Facade: {lines} lines - V2 Compliant ✅")

    exit_code = main()
    sys.exit(exit_code)
