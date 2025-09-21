#!/usr/bin/env python3
"""
Directive Handlers - V2 Compliant
=================================

CLI interface and main function for Captain Directive Manager.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from directive_services import DirectiveService, InitiativeService


class CaptainDirectiveManager:
    """Captain directive and initiative manager."""
    
    def __init__(self):
        """Initialize directive manager."""
        self.directive_service = DirectiveService()
        self.initiative_service = InitiativeService()
    
    def get_directive_status(self) -> str:
        """Get directive status."""
        return self.directive_service.get_directive_status()
    
    def get_initiative_status(self) -> str:
        """Get initiative status."""
        return self.initiative_service.get_initiative_status()
    
    def create_directive(self, name: str, directive_type: str, 
                        description: str, priority: int, timeline: str) -> bool:
        """Create new directive."""
        return self.directive_service.create_directive(
            name, directive_type, description, priority, timeline
        )
    
    def create_initiative(self, name: str, description: str, category: str,
                         priority: int, timeline: str) -> bool:
        """Create new initiative."""
        return self.initiative_service.create_initiative(
            name, description, category, priority, timeline
        )
    
    def update_directive_progress(self, name: str, progress: int) -> bool:
        """Update directive progress."""
        return self.directive_service.update_directive_progress(name, progress)
    
    def update_initiative_progress(self, name: str, progress: int) -> bool:
        """Update initiative progress."""
        return self.initiative_service.update_initiative_progress(name, progress)
    
    def assign_agents_to_directive(self, name: str, agents: list) -> bool:
        """Assign agents to directive."""
        return self.directive_service.assign_agents_to_directive(name, agents)
    
    def assign_agents_to_initiative(self, name: str, agents: list) -> bool:
        """Assign agents to initiative."""
        return self.initiative_service.assign_agents_to_initiative(name, agents)


def setup_argument_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Captain Directive Manager - Manage strategic directives and initiatives"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Directive subcommand
    directive_parser = subparsers.add_parser('directive', help='Manage directives')
    directive_subparsers = directive_parser.add_subparsers(dest='directive_action')
    
    # Create directive
    create_directive_parser = directive_subparsers.add_parser('create', help='Create directive')
    create_directive_parser.add_argument('name', help='Directive name')
    create_directive_parser.add_argument('type', help='Directive type')
    create_directive_parser.add_argument('description', help='Directive description')
    create_directive_parser.add_argument('priority', type=int, help='Priority (1-10)')
    create_directive_parser.add_argument('timeline', help='Timeline description')
    
    # Update directive
    update_directive_parser = directive_subparsers.add_parser('update', help='Update directive')
    update_directive_parser.add_argument('name', help='Directive name')
    update_directive_parser.add_argument('progress', type=int, help='Progress percentage')
    
    # Assign agents to directive
    assign_directive_parser = directive_subparsers.add_parser('assign', help='Assign agents')
    assign_directive_parser.add_argument('name', help='Directive name')
    assign_directive_parser.add_argument('agents', help='Comma-separated agent list')
    
    # Initiative subcommand
    initiative_parser = subparsers.add_parser('initiative', help='Manage initiatives')
    initiative_subparsers = initiative_parser.add_subparsers(dest='initiative_action')
    
    # Create initiative
    create_initiative_parser = initiative_subparsers.add_parser('create', help='Create initiative')
    create_initiative_parser.add_argument('name', help='Initiative name')
    create_initiative_parser.add_argument('description', help='Initiative description')
    create_initiative_parser.add_argument('category', help='Initiative category')
    create_initiative_parser.add_argument('priority', type=int, help='Priority (1-10)')
    create_initiative_parser.add_argument('timeline', help='Timeline description')
    
    # Update initiative
    update_initiative_parser = initiative_subparsers.add_parser('update', help='Update initiative')
    update_initiative_parser.add_argument('name', help='Initiative name')
    update_initiative_parser.add_argument('progress', type=int, help='Progress percentage')
    
    # Assign agents to initiative
    assign_initiative_parser = initiative_subparsers.add_parser('assign', help='Assign agents')
    assign_initiative_parser.add_argument('name', help='Initiative name')
    assign_initiative_parser.add_argument('agents', help='Comma-separated agent list')
    
    # Status subcommand
    subparsers.add_parser('status', help='Show status')
    
    return parser


def main() -> int:
    """Main function."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        manager = CaptainDirectiveManager()
        
        if args.command == 'directive':
            if args.directive_action == 'create':
                success = manager.create_directive(
                    args.name, args.type, args.description, 
                    args.priority, args.timeline
                )
                return 0 if success else 1
            elif args.directive_action == 'update':
                success = manager.update_directive_progress(args.name, args.progress)
                return 0 if success else 1
            elif args.directive_action == 'assign':
                agents = [agent.strip() for agent in args.agents.split(',')]
                success = manager.assign_agents_to_directive(args.name, agents)
                return 0 if success else 1
        
        elif args.command == 'initiative':
            if args.initiative_action == 'create':
                success = manager.create_initiative(
                    args.name, args.description, args.category,
                    args.priority, args.timeline
                )
                return 0 if success else 1
            elif args.initiative_action == 'update':
                success = manager.update_initiative_progress(args.name, args.progress)
                return 0 if success else 1
            elif args.initiative_action == 'assign':
                agents = [agent.strip() for agent in args.agents.split(',')]
                success = manager.assign_agents_to_initiative(args.name, agents)
                return 0 if success else 1
        
        elif args.command == 'status':
            print(manager.get_directive_status())
            print("\n" + manager.get_initiative_status())
            return 0
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

