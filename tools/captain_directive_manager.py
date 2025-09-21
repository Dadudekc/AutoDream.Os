#!/usr/bin/env python3
"""
Captain Directive Manager - V2 Compliant
=========================================

Manages strategic directives and initiatives for the Captain.
Provides directive lifecycle management and progress tracking.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# V2 Compliance: File under 400 lines, functions under 30 lines


class DirectiveType(Enum):
    """Directive type enumeration."""
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    EMERGENCY = "emergency"


class DirectiveStatus(Enum):
    """Directive status enumeration."""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InitiativeStatus(Enum):
    """Initiative status enumeration."""
    CONCEPTION = "conception"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Directive:
    """Directive data class."""
    
    def __init__(self, name: str, directive_type: DirectiveType, 
                 description: str, priority: int, timeline: str):
        """Initialize directive."""
        self.name = name
        self.type = directive_type
        self.description = description
        self.priority = priority
        self.timeline = timeline
        self.status = DirectiveStatus.PLANNING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.progress = 0
        self.assigned_agents = []
        self.milestones = []
        self.notes = []


class Initiative:
    """Initiative data class."""
    
    def __init__(self, name: str, description: str, category: str,
                 priority: int, timeline: str):
        """Initialize initiative."""
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.timeline = timeline
        self.status = InitiativeStatus.CONCEPTION
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.progress = 0
        self.assigned_agents = []
        self.resources = []
        self.milestones = []
        self.notes = []


class CaptainDirectiveManager:
    """Captain directive and initiative manager."""
    
    def __init__(self):
        """Initialize directive manager."""
        self.directives_file = Path("swarm_coordination/directives.json")
        self.initiatives_file = Path("swarm_coordination/initiatives.json")
        self.directives_file.parent.mkdir(parents=True, exist_ok=True)
        self.directives = self._load_directives()
        self.initiatives = self._load_initiatives()
    
    def _load_directives(self) -> Dict[str, Directive]:
        """Load directives from file."""
        if not self.directives_file.exists():
            return {}
        
        try:
            with open(self.directives_file, 'r') as f:
                data = json.load(f)
            
            directives = {}
            for name, directive_data in data.items():
                directive = Directive(
                    name=directive_data['name'],
                    directive_type=DirectiveType(directive_data['type']),
                    description=directive_data['description'],
                    priority=directive_data['priority'],
                    timeline=directive_data['timeline']
                )
                directive.status = DirectiveStatus(directive_data['status'])
                directive.progress = directive_data['progress']
                directive.assigned_agents = directive_data['assigned_agents']
                directive.milestones = directive_data['milestones']
                directive.notes = directive_data['notes']
                directives[name] = directive
            
            return directives
        except Exception as e:
            print(f"Error loading directives: {e}")
            return {}
    
    def _load_initiatives(self) -> Dict[str, Initiative]:
        """Load initiatives from file."""
        if not self.initiatives_file.exists():
            return {}
        
        try:
            with open(self.initiatives_file, 'r') as f:
                data = json.load(f)
            
            initiatives = {}
            for name, initiative_data in data.items():
                initiative = Initiative(
                    name=initiative_data['name'],
                    description=initiative_data['description'],
                    category=initiative_data['category'],
                    priority=initiative_data['priority'],
                    timeline=initiative_data['timeline']
                )
                initiative.status = InitiativeStatus(initiative_data['status'])
                initiative.progress = initiative_data['progress']
                initiative.assigned_agents = initiative_data['assigned_agents']
                initiative.resources = initiative_data['resources']
                initiative.milestones = initiative_data['milestones']
                initiative.notes = initiative_data['notes']
                initiatives[name] = initiative
            
            return initiatives
        except Exception as e:
            print(f"Error loading initiatives: {e}")
            return {}
    
    def _save_directives(self):
        """Save directives to file."""
        try:
            data = {}
            for name, directive in self.directives.items():
                data[name] = {
                    'name': directive.name,
                    'type': directive.type.value,
                    'description': directive.description,
                    'priority': directive.priority,
                    'timeline': directive.timeline,
                    'status': directive.status.value,
                    'created_at': directive.created_at.isoformat(),
                    'updated_at': directive.updated_at.isoformat(),
                    'progress': directive.progress,
                    'assigned_agents': directive.assigned_agents,
                    'milestones': directive.milestones,
                    'notes': directive.notes
                }
            
            with open(self.directives_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving directives: {e}")
    
    def _save_initiatives(self):
        """Save initiatives to file."""
        try:
            data = {}
            for name, initiative in self.initiatives.items():
                data[name] = {
                    'name': initiative.name,
                    'description': initiative.description,
                    'category': initiative.category,
                    'priority': initiative.priority,
                    'timeline': initiative.timeline,
                    'status': initiative.status.value,
                    'created_at': initiative.created_at.isoformat(),
                    'updated_at': initiative.updated_at.isoformat(),
                    'progress': initiative.progress,
                    'assigned_agents': initiative.assigned_agents,
                    'resources': initiative.resources,
                    'milestones': initiative.milestones,
                    'notes': initiative.notes
                }
            
            with open(self.initiatives_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving initiatives: {e}")
    
    def create_directive(self, name: str, directive_type: str, 
                        description: str, priority: int, timeline: str) -> bool:
        """Create new directive."""
        try:
            directive_type_enum = DirectiveType(directive_type.lower())
            directive = Directive(name, directive_type_enum, description, priority, timeline)
            self.directives[name] = directive
            self._save_directives()
            print(f"✅ Directive '{name}' created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating directive: {e}")
            return False
    
    def create_initiative(self, name: str, description: str, category: str,
                         priority: int, timeline: str) -> bool:
        """Create new initiative."""
        try:
            initiative = Initiative(name, description, category, priority, timeline)
            self.initiatives[name] = initiative
            self._save_initiatives()
            print(f"✅ Initiative '{name}' created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating initiative: {e}")
            return False
    
    def update_directive_progress(self, name: str, progress: int) -> bool:
        """Update directive progress."""
        if name not in self.directives:
            print(f"❌ Directive '{name}' not found")
            return False
        
        try:
            self.directives[name].progress = progress
            self.directives[name].updated_at = datetime.now()
            self._save_directives()
            print(f"✅ Directive '{name}' progress updated to {progress}%")
            return True
        except Exception as e:
            print(f"❌ Error updating directive progress: {e}")
            return False
    
    def update_initiative_progress(self, name: str, progress: int) -> bool:
        """Update initiative progress."""
        if name not in self.initiatives:
            print(f"❌ Initiative '{name}' not found")
            return False
        
        try:
            self.initiatives[name].progress = progress
            self.initiatives[name].updated_at = datetime.now()
            self._save_initiatives()
            print(f"✅ Initiative '{name}' progress updated to {progress}%")
            return True
        except Exception as e:
            print(f"❌ Error updating initiative progress: {e}")
            return False
    
    def assign_agents_to_directive(self, name: str, agents: List[str]) -> bool:
        """Assign agents to directive."""
        if name not in self.directives:
            print(f"❌ Directive '{name}' not found")
            return False
        
        try:
            self.directives[name].assigned_agents = agents
            self.directives[name].updated_at = datetime.now()
            self._save_directives()
            print(f"✅ Agents {agents} assigned to directive '{name}'")
            return True
        except Exception as e:
            print(f"❌ Error assigning agents: {e}")
            return False
    
    def assign_agents_to_initiative(self, name: str, agents: List[str]) -> bool:
        """Assign agents to initiative."""
        if name not in self.initiatives:
            print(f"❌ Initiative '{name}' not found")
            return False
        
        try:
            self.initiatives[name].assigned_agents = agents
            self.initiatives[name].updated_at = datetime.now()
            self._save_initiatives()
            print(f"✅ Agents {agents} assigned to initiative '{name}'")
            return True
        except Exception as e:
            print(f"❌ Error assigning agents: {e}")
            return False
    
    def get_directive_status(self) -> str:
        """Get directive status report."""
        if not self.directives:
            return "No directives found"
        
        report = "📋 DIRECTIVE STATUS REPORT\n"
        report += "=" * 50 + "\n"
        
        for name, directive in self.directives.items():
            report += f"\n🎯 {name}\n"
            report += f"   Type: {directive.type.value.title()}\n"
            report += f"   Status: {directive.status.value.title()}\n"
            report += f"   Progress: {directive.progress}%\n"
            report += f"   Priority: P{directive.priority}\n"
            report += f"   Timeline: {directive.timeline}\n"
            report += f"   Assigned Agents: {', '.join(directive.assigned_agents) or 'None'}\n"
        
        return report
    
    def get_initiative_status(self) -> str:
        """Get initiative status report."""
        if not self.initiatives:
            return "No initiatives found"
        
        report = "🚀 INITIATIVE STATUS REPORT\n"
        report += "=" * 50 + "\n"
        
        for name, initiative in self.initiatives.items():
            report += f"\n🎯 {name}\n"
            report += f"   Category: {initiative.category}\n"
            report += f"   Status: {initiative.status.value.title()}\n"
            report += f"   Progress: {initiative.progress}%\n"
            report += f"   Priority: P{initiative.priority}\n"
            report += f"   Timeline: {initiative.timeline}\n"
            report += f"   Assigned Agents: {', '.join(initiative.assigned_agents) or 'None'}\n"
        
        return report


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Captain Directive Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Directive commands
    directive_parser = subparsers.add_parser('directive', help='Directive management')
    directive_subparsers = directive_parser.add_subparsers(dest='directive_action')
    
    # Create directive
    create_directive_parser = directive_subparsers.add_parser('create', help='Create directive')
    create_directive_parser.add_argument('name', help='Directive name')
    create_directive_parser.add_argument('type', choices=['strategic', 'tactical', 'operational', 'emergency'])
    create_directive_parser.add_argument('description', help='Directive description')
    create_directive_parser.add_argument('priority', type=int, choices=[0, 1, 2, 3])
    create_directive_parser.add_argument('timeline', help='Timeline description')
    
    # Update directive progress
    update_directive_parser = directive_subparsers.add_parser('update', help='Update directive')
    update_directive_parser.add_argument('name', help='Directive name')
    update_directive_parser.add_argument('progress', type=int, help='Progress percentage')
    
    # Assign agents to directive
    assign_directive_parser = directive_subparsers.add_parser('assign', help='Assign agents')
    assign_directive_parser.add_argument('name', help='Directive name')
    assign_directive_parser.add_argument('agents', help='Comma-separated agent list')
    
    # Initiative commands
    initiative_parser = subparsers.add_parser('initiative', help='Initiative management')
    initiative_subparsers = initiative_parser.add_subparsers(dest='initiative_action')
    
    # Create initiative
    create_initiative_parser = initiative_subparsers.add_parser('create', help='Create initiative')
    create_initiative_parser.add_argument('name', help='Initiative name')
    create_initiative_parser.add_argument('description', help='Initiative description')
    create_initiative_parser.add_argument('category', help='Initiative category')
    create_initiative_parser.add_argument('priority', type=int, choices=[0, 1, 2, 3])
    create_initiative_parser.add_argument('timeline', help='Timeline description')
    
    # Update initiative progress
    update_initiative_parser = initiative_subparsers.add_parser('update', help='Update initiative')
    update_initiative_parser.add_argument('name', help='Initiative name')
    update_initiative_parser.add_argument('progress', type=int, help='Progress percentage')
    
    # Assign agents to initiative
    assign_initiative_parser = initiative_subparsers.add_parser('assign', help='Assign agents')
    assign_initiative_parser.add_argument('name', help='Initiative name')
    assign_initiative_parser.add_argument('agents', help='Comma-separated agent list')
    
    # Status commands
    subparsers.add_parser('status', help='Show status reports')
    
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


