#!/usr/bin/env python3
"""
Directive Services - V2 Compliant
=================================

Core business logic for Captain Directive Manager.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
from datetime import datetime
from pathlib import Path

from directive_models import Directive, DirectiveType, Initiative, InitiativeStatus


class DirectiveService:
    """Service for managing directives."""

    def __init__(self, directives_file: str = "agent_workspaces/Agent-4/directives.json"):
        """Initialize directive service."""
        self.directives_file = directives_file
        self.directives = {}
        self._load_directives()

    def _load_directives(self) -> None:
        """Load directives from file."""
        try:
            if Path(self.directives_file).exists():
                with open(self.directives_file) as f:
                    data = json.load(f)
                    for name, directive_data in data.items():
                        directive = Directive(
                            name=directive_data["name"],
                            directive_type=DirectiveType(directive_data["type"]),
                            description=directive_data["description"],
                            priority=directive_data["priority"],
                            timeline=directive_data["timeline"],
                        )
                        directive.status = directive_data["status"]
                        directive.created_at = datetime.fromisoformat(directive_data["created_at"])
                        directive.updated_at = datetime.fromisoformat(directive_data["updated_at"])
                        directive.progress = directive_data["progress"]
                        directive.assigned_agents = directive_data["assigned_agents"]
                        directive.milestones = directive_data["milestones"]
                        directive.notes = directive_data["notes"]
                        self.directives[name] = directive
        except Exception as e:
            print(f"Error loading directives: {e}")

    def _save_directives(self) -> None:
        """Save directives to file."""
        try:
            data = {}
            for name, directive in self.directives.items():
                data[name] = {
                    "name": directive.name,
                    "type": directive.type.value,
                    "description": directive.description,
                    "priority": directive.priority,
                    "timeline": directive.timeline,
                    "status": directive.status.value,
                    "created_at": directive.created_at.isoformat(),
                    "updated_at": directive.updated_at.isoformat(),
                    "progress": directive.progress,
                    "assigned_agents": directive.assigned_agents,
                    "milestones": directive.milestones,
                    "notes": directive.notes,
                }

            with open(self.directives_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving directives: {e}")

    def create_directive(
        self, name: str, directive_type: str, description: str, priority: int, timeline: str
    ) -> bool:
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

    def assign_agents_to_directive(self, name: str, agents: list[str]) -> bool:
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

    def get_directive_status(self) -> str:
        """Get directive status summary."""
        if not self.directives:
            return "No directives found."

        status = "📋 DIRECTIVE STATUS\n" + "=" * 50 + "\n"
        for name, directive in self.directives.items():
            status += f"📌 {name}\n"
            status += f"   Type: {directive.type.value.title()}\n"
            status += f"   Status: {directive.status.value.title()}\n"
            status += f"   Progress: {directive.progress}%\n"
            status += f"   Priority: {directive.priority}\n"
            status += f"   Timeline: {directive.timeline}\n"
            status += f"   Agents: {', '.join(directive.assigned_agents) or 'None'}\n"
            status += f"   Updated: {directive.updated_at.strftime('%Y-%m-%d %H:%M')}\n\n"

        return status


class InitiativeService:
    """Service for managing initiatives."""

    def __init__(self, initiatives_file: str = "agent_workspaces/Agent-4/initiatives.json"):
        """Initialize initiative service."""
        self.initiatives_file = initiatives_file
        self.initiatives = {}
        self._load_initiatives()

    def _load_initiatives(self) -> None:
        """Load initiatives from file."""
        try:
            if Path(self.initiatives_file).exists():
                with open(self.initiatives_file) as f:
                    data = json.load(f)
                    for name, initiative_data in data.items():
                        initiative = Initiative(
                            name=initiative_data["name"],
                            description=initiative_data["description"],
                            category=initiative_data["category"],
                            priority=initiative_data["priority"],
                            timeline=initiative_data["timeline"],
                        )
                        initiative.status = InitiativeStatus(initiative_data["status"])
                        initiative.created_at = datetime.fromisoformat(
                            initiative_data["created_at"]
                        )
                        initiative.updated_at = datetime.fromisoformat(
                            initiative_data["updated_at"]
                        )
                        initiative.progress = initiative_data["progress"]
                        initiative.assigned_agents = initiative_data["assigned_agents"]
                        initiative.resources = initiative_data["resources"]
                        initiative.milestones = initiative_data["milestones"]
                        initiative.notes = initiative_data["notes"]
                        self.initiatives[name] = initiative
        except Exception as e:
            print(f"Error loading initiatives: {e}")

    def _save_initiatives(self) -> None:
        """Save initiatives to file."""
        try:
            data = {}
            for name, initiative in self.initiatives.items():
                data[name] = {
                    "name": initiative.name,
                    "description": initiative.description,
                    "category": initiative.category,
                    "priority": initiative.priority,
                    "timeline": initiative.timeline,
                    "status": initiative.status.value,
                    "created_at": initiative.created_at.isoformat(),
                    "updated_at": initiative.updated_at.isoformat(),
                    "progress": initiative.progress,
                    "assigned_agents": initiative.assigned_agents,
                    "resources": initiative.resources,
                    "milestones": initiative.milestones,
                    "notes": initiative.notes,
                }

            with open(self.initiatives_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving initiatives: {e}")

    def create_initiative(
        self, name: str, description: str, category: str, priority: int, timeline: str
    ) -> bool:
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

    def assign_agents_to_initiative(self, name: str, agents: list[str]) -> bool:
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

    def get_initiative_status(self) -> str:
        """Get initiative status summary."""
        if not self.initiatives:
            return "No initiatives found."

        status = "🚀 INITIATIVE STATUS\n" + "=" * 50 + "\n"
        for name, initiative in self.initiatives.items():
            status += f"📌 {name}\n"
            status += f"   Category: {initiative.category}\n"
            status += f"   Status: {initiative.status.value.title()}\n"
            status += f"   Progress: {initiative.progress}%\n"
            status += f"   Priority: {initiative.priority}\n"
            status += f"   Timeline: {initiative.timeline}\n"
            status += f"   Agents: {', '.join(initiative.assigned_agents) or 'None'}\n"
            status += f"   Updated: {initiative.updated_at.strftime('%Y-%m-%d %H:%M')}\n\n"

        return status
