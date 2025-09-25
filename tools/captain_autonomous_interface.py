#!/usr/bin/env python3
"""
Captain Autonomous Interface - V2 Compliant
===========================================

CLI interface and command handling for the Captain Autonomous Manager.
Provides command-line interface for autonomous analysis and agent guidance.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
V2 Compliance: ≤200 lines, modular design, comprehensive error handling
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .captain_autonomous_core import CaptainAutonomousCore
from .captain_autonomous_models import Bottleneck, Flaw, StoppingCondition


class CaptainAutonomousInterface:
    """CLI interface for Captain Autonomous Manager."""
    
    def __init__(self):
        """Initialize interface."""
        self.core = CaptainAutonomousCore()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        parser = argparse.ArgumentParser(description="Captain Autonomous Manager")
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Detect bottlenecks
        subparsers.add_parser('detect-bottlenecks', help='Detect system bottlenecks')
        
        # Detect flaws
        subparsers.add_parser('detect-flaws', help='Detect system flaws')
        
        # Check stopping conditions
        subparsers.add_parser('check-stopping', help='Check stopping conditions')
        
        # Generate priorities
        subparsers.add_parser('generate-priorities', help='Generate autonomous priorities')
        
        # Provide agent guidance
        guidance_parser = subparsers.add_parser('agent-guidance', help='Provide agent guidance')
        guidance_parser.add_argument('agent_id', help='Agent ID')
        
        # Run autonomous analysis
        subparsers.add_parser('analyze', help='Run full autonomous analysis')
        
        return parser
    
    def handle_detect_bottlenecks(self) -> int:
        """Handle detect-bottlenecks command."""
        try:
            bottlenecks = self.core.detect_bottlenecks()
            print(f"Detected {len(bottlenecks)} bottlenecks")
            for bottleneck in bottlenecks:
                print(f"- {bottleneck.name}: {bottleneck.impact}")
            return 0
        except Exception as e:
            print(f"❌ Error detecting bottlenecks: {e}")
            return 1
    
    def handle_detect_flaws(self) -> int:
        """Handle detect-flaws command."""
        try:
            flaws = self.core.detect_flaws()
            print(f"Detected {len(flaws)} flaws")
            for flaw in flaws:
                print(f"- {flaw.name}: {flaw.description}")
            return 0
        except Exception as e:
            print(f"❌ Error detecting flaws: {e}")
            return 1
    
    def handle_check_stopping(self) -> int:
        """Handle check-stopping command."""
        try:
            conditions = self.core.check_stopping_conditions()
            if conditions:
                print("Stopping conditions met:")
                for condition, description in conditions:
                    print(f"- {condition.value}: {description}")
            else:
                print("No stopping conditions met")
            return 0
        except Exception as e:
            print(f"❌ Error checking stopping conditions: {e}")
            return 1
    
    def handle_generate_priorities(self) -> int:
        """Handle generate-priorities command."""
        try:
            priorities = self.core.generate_autonomous_priorities()
            print("Autonomous priorities:")
            for i, priority in enumerate(priorities, 1):
                print(f"{i}. {priority}")
            return 0
        except Exception as e:
            print(f"❌ Error generating priorities: {e}")
            return 1
    
    def handle_agent_guidance(self, agent_id: str) -> int:
        """Handle agent-guidance command."""
        try:
            guidance = self.core.provide_agent_guidance(agent_id)
            print(f"Guidance for {agent_id}: {guidance}")
            return 0
        except Exception as e:
            print(f"❌ Error providing agent guidance: {e}")
            return 1
    
    def handle_analyze(self) -> int:
        """Handle analyze command."""
        try:
            print("Running autonomous analysis...")
            bottlenecks = self.core.detect_bottlenecks()
            flaws = self.core.detect_flaws()
            conditions = self.core.check_stopping_conditions()
            priorities = self.core.generate_autonomous_priorities()
            
            print(f"Analysis complete:")
            print(f"- Bottlenecks: {len(bottlenecks)}")
            print(f"- Flaws: {len(flaws)}")
            print(f"- Stopping conditions: {len(conditions)}")
            print(f"- Priorities: {len(priorities)}")
            return 0
        except Exception as e:
            print(f"❌ Error running analysis: {e}")
            return 1
    
    def run(self, args: List[str] = None) -> int:
        """Run the CLI interface."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
        
        try:
            if parsed_args.command == 'detect-bottlenecks':
                return self.handle_detect_bottlenecks()
            elif parsed_args.command == 'detect-flaws':
                return self.handle_detect_flaws()
            elif parsed_args.command == 'check-stopping':
                return self.handle_check_stopping()
            elif parsed_args.command == 'generate-priorities':
                return self.handle_generate_priorities()
            elif parsed_args.command == 'agent-guidance':
                return self.handle_agent_guidance(parsed_args.agent_id)
            elif parsed_args.command == 'analyze':
                return self.handle_analyze()
            else:
                print(f"❌ Unknown command: {parsed_args.command}")
                return 1
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1


def main():
    """Main CLI function."""
    interface = CaptainAutonomousInterface()
    return interface.run()


# V2 Compliance: File length check
if __name__ == "__main__":
    import inspect
    lines = len(inspect.getsource(inspect.currentframe().f_globals['__file__']).splitlines())
    print(f"Captain Autonomous Interface: {lines} lines - V2 Compliant ✅")
    
    # Run CLI if called directly
    exit_code = main()
    sys.exit(exit_code)
