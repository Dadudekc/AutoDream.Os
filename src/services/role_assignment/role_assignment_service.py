#!/usr/bin/env python3
"""
Role Assignment Service - Direct PyAutoGUI Implementation
========================================================

Direct PyAutoGUI-based role assignment system for V2_SWARM agents.
Captain Agent-4 assigns roles directly via PyAutoGUI messaging.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from src.services.messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


@dataclass
class RoleAssignment:
    """Role assignment data structure."""

    agent_id: str
    role: str
    task: str
    duration: str
    priority: str = "NORMAL"
    assigned_by: str = "Agent-4"
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class RoleCapability:
    """Role capability definition."""

    role: str
    description: str
    capabilities: list[str]
    quality_gates: dict
    escalation_procedures: dict
    ssot_requirements: dict
    behavior_adaptations: dict


class RoleAssignmentService:
    """Role assignment service for Captain Agent-4."""

    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize role assignment service."""
        self.coord_path = coord_path
        self.messaging_service = ConsolidatedMessagingService(coord_path)
        self.role_definitions = self._load_role_definitions()
        self.agent_capabilities = self._load_agent_capabilities()
        self.active_assignments = {}

    def _load_role_definitions(self) -> dict[str, RoleCapability]:
        """Load role definitions from configuration files."""
        roles = {}
        protocols_dir = Path("config/protocols")

        if not protocols_dir.exists():
            logger.warning("Protocols directory not found, creating default roles")
            return self._create_default_roles()

        for protocol_file in protocols_dir.glob("*.json"):
            try:
                with open(protocol_file) as f:
                    role_data = json.load(f)
                    # Filter out fields not in RoleCapability dataclass
                    filtered_data = {
                        k: v for k, v in role_data.items() if k in RoleCapability.__annotations__
                    }
                    roles[role_data["role"]] = RoleCapability(**filtered_data)
            except Exception as e:
                logger.error(f"Failed to load role definition from {protocol_file}: {e}")

        return roles

    def _load_agent_capabilities(self) -> dict[str, list[str]]:
        """Load agent capability mappings."""
        capability_file = Path("config/agent_capabilities.json")

        if not capability_file.exists():
            logger.warning("Agent capabilities file not found, creating default")
            return self._create_default_agent_capabilities()

        try:
            with open(capability_file) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load agent capabilities: {e}")
            return self._create_default_agent_capabilities()

    def _create_default_roles(self) -> dict[str, RoleCapability]:
        """Create default role definitions."""
        return {
            "INTEGRATION_SPECIALIST": RoleCapability(
                role="INTEGRATION_SPECIALIST",
                description="System integration and interoperability specialist",
                capabilities=["system_integration", "api_development", "webhook_management"],
                quality_gates={"file_size_limit": 400, "test_coverage": 85},
                escalation_procedures={"integration_failure": "Notify Captain Agent-4"},
                ssot_requirements={"config_files": "Single source for all integration configs"},
                behavior_adaptations={"focus_areas": ["integration", "apis", "webhooks"]},
            ),
            "QUALITY_ASSURANCE": RoleCapability(
                role="QUALITY_ASSURANCE",
                description="Testing, validation, and compliance specialist",
                capabilities=["test_development", "quality_validation", "compliance_checking"],
                quality_gates={"file_size_limit": 400, "test_coverage": 95},
                escalation_procedures={"quality_failure": "Block deployment"},
                ssot_requirements={"test_configs": "Single test configuration source"},
                behavior_adaptations={"focus_areas": ["testing", "quality", "compliance"]},
            ),
            "SSOT_MANAGER": RoleCapability(
                role="SSOT_MANAGER",
                description="Single source of truth validation and management specialist",
                capabilities=["ssot_validation", "system_integration", "coordination"],
                quality_gates={"file_size_limit": 400, "test_coverage": 85},
                escalation_procedures={"ssot_violation": "Immediate notification to Captain"},
                ssot_requirements={"all_systems": "Single source of truth for all systems"},
                behavior_adaptations={"focus_areas": ["ssot", "integration", "coordination"]},
            ),
        }

    def _create_default_agent_capabilities(self) -> dict[str, list[str]]:
        """Create default agent capability mappings."""
        return {
            "Agent-1": ["INTEGRATION_SPECIALIST", "TASK_EXECUTOR", "TROUBLESHOOTER"],
            "Agent-2": ["ARCHITECTURE_SPECIALIST", "RESEARCHER", "OPTIMIZER"],
            "Agent-3": ["INFRASTRUCTURE_SPECIALIST", "TASK_EXECUTOR"],
            "Agent-5": ["DATA_ANALYST", "RESEARCHER"],
            "Agent-6": ["COORDINATOR", "COMMUNICATION_SPECIALIST"],
            "Agent-7": ["WEB_DEVELOPER", "TASK_EXECUTOR"],
            "Agent-8": ["SSOT_MANAGER", "COORDINATOR", "QUALITY_ASSURANCE"],
        }

    def assign_role(
        self, agent_id: str, role: str, task: str, duration: str, priority: str = "NORMAL"
    ) -> bool:
        """Assign role to agent via direct PyAutoGUI message."""
        try:
            # Validate agent can perform role
            if not self._can_agent_perform_role(agent_id, role):
                logger.error(f"Agent {agent_id} cannot perform role {role}")
                return False

            # Create role assignment
            assignment = RoleAssignment(
                agent_id=agent_id, role=role, task=task, duration=duration, priority=priority
            )

            # Create PyAutoGUI message
            message = self._create_role_assignment_message(assignment)

            # Send via PyAutoGUI (this wakes up the agent)
            success = self.messaging_service.send_message(
                agent_id=agent_id, message=message, from_agent="Agent-4", priority=priority
            )

            if success:
                # Store active assignment
                self.active_assignments[agent_id] = assignment
                logger.info(f"Role assignment sent: {agent_id} -> {role}")
                return True
            else:
                logger.error(f"Failed to send role assignment to {agent_id}")
                return False

        except Exception as e:
            logger.error(f"Error assigning role: {e}")
            return False

    def _can_agent_perform_role(self, agent_id: str, role: str) -> bool:
        """Check if agent can perform the specified role."""
        if agent_id not in self.agent_capabilities:
            logger.warning(f"Unknown agent: {agent_id}")
            return False

        agent_roles = self.agent_capabilities[agent_id]
        return role in agent_roles

    def _create_role_assignment_message(self, assignment: RoleAssignment) -> str:
        """Create role assignment message for PyAutoGUI."""
        return (
            f"ROLE_ASSIGNMENT {assignment.agent_id} {assignment.role} "
            f"'{assignment.task}' '{assignment.duration}' - "
            f"Load {assignment.role.lower()}.json protocols and begin task execution immediately. "
            f"Priority: {assignment.priority}. "
            f"Assigned by: {assignment.assigned_by} at {assignment.timestamp}."
        )

    def list_available_roles(self) -> list[str]:
        """List all available roles."""
        return list(self.role_definitions.keys())

    def list_agent_capabilities(self, agent_id: str) -> list[str]:
        """List capabilities for a specific agent."""
        return self.agent_capabilities.get(agent_id, [])

    def get_active_assignment(self, agent_id: str) -> RoleAssignment | None:
        """Get current active assignment for agent."""
        return self.active_assignments.get(agent_id)

    def complete_assignment(self, agent_id: str) -> bool:
        """Mark assignment as complete and remove from active list."""
        if agent_id in self.active_assignments:
            del self.active_assignments[agent_id]
            logger.info(f"Assignment completed for {agent_id}")
            return True
        return False

    def reassign_role(self, agent_id: str, new_role: str, new_task: str, new_duration: str) -> bool:
        """Reassign agent to different role."""
        # Complete current assignment
        self.complete_assignment(agent_id)

        # Assign new role
        return self.assign_role(agent_id, new_role, new_task, new_duration, "HIGH")


def main():
    """CLI interface for role assignment service."""
    import argparse

    parser = argparse.ArgumentParser(description="Role Assignment Service CLI")
    parser.add_argument("--assign-role", action="store_true", help="Assign role to agent")
    parser.add_argument("--agent", required=True, help="Agent ID")
    parser.add_argument("--role", help="Role to assign")
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--duration", help="Duration (e.g., '2 cycles')")
    parser.add_argument("--priority", default="NORMAL", help="Priority level")
    parser.add_argument("--list-roles", action="store_true", help="List available roles")
    parser.add_argument("--list-capabilities", action="store_true", help="List agent capabilities")
    parser.add_argument("--active-assignments", action="store_true", help="Show active assignments")

    args = parser.parse_args()

    service = RoleAssignmentService()

    if args.list_roles:
        roles = service.list_available_roles()
        print("Available Roles:")
        for role in roles:
            print(f"  - {role}")

    elif args.list_capabilities:
        capabilities = service.list_agent_capabilities(args.agent)
        print(f"Capabilities for {args.agent}:")
        for capability in capabilities:
            print(f"  - {capability}")

    elif args.active_assignments:
        print("Active Assignments:")
        for agent_id, assignment in service.active_assignments.items():
            print(f"  {agent_id}: {assignment.role} - {assignment.task}")

    elif args.assign_role:
        if not all([args.role, args.task, args.duration]):
            print("Error: --role, --task, and --duration are required for role assignment")
            return

        success = service.assign_role(
            args.agent, args.role, args.task, args.duration, args.priority
        )
        if success:
            print(f"Role assignment sent: {args.agent} -> {args.role}")
        else:
            print(f"Failed to assign role: {args.agent} -> {args.role}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
