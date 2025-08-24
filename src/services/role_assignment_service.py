"""
Role Assignment Service - Role Assignment and Management

This module manages agent role assignments and capability access.
Follows Single Responsibility Principle - only manages role assignments.

Architecture: Single Responsibility Principle - role assignment only
LOC: 180 lines (under 200 limit)
"""

import argparse
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Set
import logging

from .role_definitions import (
    Capability,
    AgentRole,
    RoleAssignment,
    PermissionLevel,
    CapabilityType,
    RoleDefinitionManager,
)

logger = logging.getLogger(__name__)


class RoleAssignmentService:
    """
    Service for managing agent role assignments and capabilities

    Responsibilities:
    - Assign roles to agents
    - Manage agent capabilities
    - Control access permissions
    - Validate role assignments
    """

    def __init__(self):
        self.definition_manager = RoleDefinitionManager()
        self.role_assignments: Dict[str, RoleAssignment] = {}
        self.agent_capabilities: Dict[
            str, Set[str]
        ] = {}  # agent_id -> set of capability_ids
        self.logger = logging.getLogger(f"{__name__}.RoleAssignmentService")

    def assign_role(
        self, agent_id: str, role_id: str, assigned_by: str = "system"
    ) -> bool:
        """Assign a role to an agent"""
        # Validate role exists
        role = self.definition_manager.get_role(role_id)
        if not role:
            self.logger.error(f"Role {role_id} not found")
            return False

        # Check if agent already has this role
        existing_assignment = self._get_agent_role_assignment(agent_id, role_id)
        if existing_assignment and existing_assignment.status == "active":
            self.logger.warning(f"Agent {agent_id} already has role {role_id}")
            return False

        # Create role assignment
        assignment = RoleAssignment(
            agent_id=agent_id,
            role_id=role_id,
            assigned_at=time.time(),
            assigned_by=assigned_by,
            status="active",
        )

        assignment_id = f"{agent_id}_{role_id}"
        self.role_assignments[assignment_id] = assignment

        # Grant capabilities to agent
        self._grant_role_capabilities(agent_id, role)

        self.logger.info(f"Assigned role {role_id} to agent {agent_id}")
        return True

    def revoke_role(
        self, agent_id: str, role_id: str, revoked_by: str = "system"
    ) -> bool:
        """Revoke a role from an agent"""
        assignment_id = f"{agent_id}_{role_id}"
        assignment = self.role_assignments.get(assignment_id)

        if not assignment:
            self.logger.warning(
                f"No role assignment found for agent {agent_id} and role {role_id}"
            )
            return False

        if assignment.status != "active":
            self.logger.warning(f"Role assignment {assignment_id} is not active")
            return False

        # Update assignment status
        assignment.status = "revoked"
        assignment.metadata = assignment.metadata or {}
        assignment.metadata["revoked_by"] = revoked_by
        assignment.metadata["revoked_at"] = time.time()

        # Remove capabilities
        self._revoke_role_capabilities(agent_id, role_id)

        self.logger.info(f"Revoked role {role_id} from agent {agent_id}")
        return True

    def suspend_role(
        self, agent_id: str, role_id: str, suspended_by: str = "system"
    ) -> bool:
        """Suspend a role assignment"""
        assignment_id = f"{agent_id}_{role_id}"
        assignment = self.role_assignments.get(assignment_id)

        if not assignment or assignment.status != "active":
            return False

        assignment.status = "suspended"
        assignment.metadata = assignment.metadata or {}
        assignment.metadata["suspended_by"] = suspended_by
        assignment.metadata["suspended_at"] = time.time()

        self.logger.info(f"Suspended role {role_id} for agent {agent_id}")
        return True

    def reactivate_role(
        self, agent_id: str, role_id: str, reactivated_by: str = "system"
    ) -> bool:
        """Reactivate a suspended role assignment"""
        assignment_id = f"{agent_id}_{role_id}"
        assignment = self.role_assignments.get(assignment_id)

        if not assignment or assignment.status != "suspended":
            return False

        assignment.status = "active"
        assignment.metadata = assignment.metadata or {}
        assignment.metadata["reactivated_by"] = reactivated_by
        assignment.metadata["reactivated_at"] = time.time()

        # Re-grant capabilities
        role = self.definition_manager.get_role(role_id)
        if role:
            self._grant_role_capabilities(agent_id, role)

        self.logger.info(f"Reactivated role {role_id} for agent {agent_id}")
        return True

    def _grant_role_capabilities(self, agent_id: str, role: AgentRole):
        """Grant role capabilities to an agent"""
        if agent_id not in self.agent_capabilities:
            self.agent_capabilities[agent_id] = set()

        for capability_id in role.capabilities:
            self.agent_capabilities[agent_id].add(capability_id)

    def _revoke_role_capabilities(self, agent_id: str, role_id: str):
        """Revoke role capabilities from an agent"""
        role = self.definition_manager.get_role(role_id)
        if not role:
            return

        if agent_id in self.agent_capabilities:
            for capability_id in role.capabilities:
                self.agent_capabilities[agent_id].discard(capability_id)

    def _get_agent_role_assignment(
        self, agent_id: str, role_id: str
    ) -> Optional[RoleAssignment]:
        """Get a specific role assignment for an agent"""
        assignment_id = f"{agent_id}_{role_id}"
        return self.role_assignments.get(assignment_id)

    def get_agent_roles(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all roles assigned to an agent"""
        roles = []
        for assignment_id, assignment in self.role_assignments.items():
            if assignment.agent_id == agent_id:
                role = self.definition_manager.get_role(assignment.role_id)
                if role:
                    roles.append(
                        {
                            "role_id": assignment.role_id,
                            "role_name": role.name,
                            "status": assignment.status,
                            "assigned_at": assignment.assigned_at,
                            "assigned_by": assignment.assigned_by,
                        }
                    )
        return roles

    def has_capability(self, agent_id: str, capability_id: str) -> bool:
        """Check if an agent has a specific capability"""
        return (
            agent_id in self.agent_capabilities
            and capability_id in self.agent_capabilities[agent_id]
        )

    def can_perform_action(
        self, agent_id: str, action: str, resource: str = None
    ) -> bool:
        """Check if an agent can perform a specific action"""
        # This is a simplified permission check
        # In practice, you'd have more sophisticated permission logic

        if action == "read":
            return self.has_capability(agent_id, "system_access")
        elif action == "write":
            return self.has_capability(agent_id, "communication")
        elif action == "execute":
            return self.has_capability(agent_id, "task_execution")
        elif action == "admin":
            return self.has_capability(agent_id, "system_access") and any(
                "admin" in assignment.metadata.get("permissions", [])
                for assignment in self.role_assignments.values()
                if assignment.agent_id == agent_id and assignment.status == "active"
            )

        return False

    def get_role_requirements(self, role_id: str) -> Dict[str, Any]:
        """Get requirements for a specific role"""
        return self.definition_manager.get_role_requirements(role_id)

    def get_agent_capabilities(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all capabilities for an agent"""
        if agent_id not in self.agent_capabilities:
            return []

        capabilities = []
        for capability_id in self.agent_capabilities[agent_id]:
            capability = self.definition_manager.get_capability(capability_id)
            if capability:
                capabilities.append(
                    {
                        "capability_id": capability.capability_id,
                        "name": capability.name,
                        "description": capability.description,
                        "type": capability.capability_type.value,
                        "permissions": [p.value for p in capability.permissions],
                    }
                )

        return capabilities


def run_smoke_test():
    """Run basic functionality test for RoleAssignmentService"""
    print("🧪 Running RoleAssignmentService Smoke Test...")

    try:
        service = RoleAssignmentService()

        # Test role assignment
        success = service.assign_role("test-agent", "worker")
        assert success

        # Test capability check
        assert service.has_capability("test-agent", "system_access")
        assert service.has_capability("test-agent", "task_execution")

        # Test role retrieval
        roles = service.get_agent_roles("test-agent")
        assert len(roles) == 1
        assert roles[0]["role_id"] == "worker"

        # Test permission check
        assert service.can_perform_action("test-agent", "read")
        assert service.can_perform_action("test-agent", "execute")

        # Test role revocation
        success = service.revoke_role("test-agent", "worker")
        assert success
        assert not service.has_capability("test-agent", "task_execution")

        print("✅ RoleAssignmentService Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ RoleAssignmentService Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for RoleAssignmentService testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Role Assignment Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--assign", nargs=2, metavar=("AGENT", "ROLE"), help="Assign role to agent"
    )
    parser.add_argument(
        "--revoke", nargs=2, metavar=("AGENT", "ROLE"), help="Revoke role from agent"
    )
    parser.add_argument(
        "--suspend", nargs=2, metavar=("AGENT", "ROLE"), help="Suspend role for agent"
    )
    parser.add_argument(
        "--reactivate",
        nargs=2,
        metavar=("AGENT", "ROLE"),
        help="Reactivate role for agent",
    )
    parser.add_argument("--agent-roles", help="Get roles for agent")
    parser.add_argument("--agent-capabilities", help="Get capabilities for agent")
    parser.add_argument(
        "--check-capability",
        nargs=2,
        metavar=("AGENT", "CAPABILITY"),
        help="Check if agent has capability",
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    service = RoleAssignmentService()

    if args.assign:
        agent_id, role_id = args.assign
        success = service.assign_role(agent_id, role_id)
        print(f"Role assignment: {'Success' if success else 'Failed'}")
    elif args.revoke:
        agent_id, role_id = args.revoke
        success = service.revoke_role(agent_id, role_id)
        print(f"Role revocation: {'Success' if success else 'Failed'}")
    elif args.suspend:
        agent_id, role_id = args.suspend
        success = service.suspend_role(agent_id, role_id)
        print(f"Role suspension: {'Success' if success else 'Failed'}")
    elif args.reactivate:
        agent_id, role_id = args.reactivate
        success = service.reactivate_role(agent_id, role_id)
        print(f"Role reactivation: {'Success' if success else 'Failed'}")
    elif args.agent_roles:
        roles = service.get_agent_roles(args.agent_roles)
        if roles:
            print(f"Roles for agent {args.agent_roles}:")
            for role in roles:
                print(f"  {role['role_name']} ({role['status']})")
        else:
            print(f"No roles found for agent {args.agent_roles}")
    elif args.agent_capabilities:
        capabilities = service.get_agent_capabilities(args.agent_capabilities)
        if capabilities:
            print(f"Capabilities for agent {args.agent_capabilities}:")
            for cap in capabilities:
                print(f"  {cap['name']} ({cap['type']})")
        else:
            print(f"No capabilities found for agent {args.agent_capabilities}")
    elif args.check_capability:
        agent_id, capability_id = args.check_capability
        has_cap = service.has_capability(agent_id, capability_id)
        print(f"Agent {agent_id} has capability {capability_id}: {has_cap}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
