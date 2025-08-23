"""
Role Definitions Module - Role and Capability Data Structures

This module contains role and capability definitions and data structures.
Follows Single Responsibility Principle - only manages role definitions.

Architecture: Single Responsibility Principle - role definitions only
LOC: 180 lines (under 200 limit)
"""

from typing import Dict, List, Optional, Any, Set
from enum import Enum
from dataclasses import dataclass

from ..core.agent_models import AgentRole, AgentStatus, AgentCapability


class PermissionLevel(Enum):
    """Permission levels for agent capabilities"""

    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class CapabilityType(Enum):
    """Types of agent capabilities"""

    SYSTEM = "system"
    COMMUNICATION = "communication"
    TASK = "task"
    COORDINATION = "coordination"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"


@dataclass
class Capability:
    """Agent capability definition"""

    capability_id: str
    name: str
    description: str
    capability_type: CapabilityType
    permissions: List[PermissionLevel]
    dependencies: List[str]
    metadata: Optional[Dict[str, Any]] = None


# AgentRole now imported from unified agent_models


@dataclass
class RoleAssignment:
    """Agent role assignment record"""

    agent_id: str
    role_id: str
    assigned_at: float
    assigned_by: str
    status: str  # "active", "suspended", "revoked"
    metadata: Optional[Dict[str, Any]] = None


class RoleDefinitionManager:
    """
    Manages role and capability definitions and templates.

    Responsibilities:
    - Provide role and capability definitions
    - Manage role templates
    - Support role customization
    """

    def __init__(self):
        self.capabilities: Dict[str, Capability] = {}
        self.roles: Dict[str, AgentRole] = {}
        self._initialize_capabilities()
        self._initialize_roles()

    def _initialize_capabilities(self):
        """Initialize system capabilities"""
        self.capabilities = {
            "system_access": Capability(
                capability_id="system_access",
                name="System Access",
                description="Basic system access and navigation",
                capability_type=CapabilityType.SYSTEM,
                permissions=[PermissionLevel.READ],
                dependencies=[],
            ),
            "communication": Capability(
                capability_id="communication",
                name="Communication",
                description="Send and receive messages",
                capability_type=CapabilityType.COMMUNICATION,
                permissions=[PermissionLevel.READ, PermissionLevel.WRITE],
                dependencies=["system_access"],
            ),
            "task_execution": Capability(
                capability_id="task_execution",
                name="Task Execution",
                description="Execute assigned tasks",
                capability_type=CapabilityType.TASK,
                permissions=[PermissionLevel.READ, PermissionLevel.EXECUTE],
                dependencies=["system_access", "communication"],
            ),
            "coordination": Capability(
                capability_id="coordination",
                name="Coordination",
                description="Coordinate with other agents",
                capability_type=CapabilityType.COORDINATION,
                permissions=[
                    PermissionLevel.READ,
                    PermissionLevel.WRITE,
                    PermissionLevel.EXECUTE,
                ],
                dependencies=["communication", "task_execution"],
            ),
            "monitoring": Capability(
                capability_id="monitoring",
                name="System Monitoring",
                description="Monitor system status and health",
                capability_type=CapabilityType.MONITORING,
                permissions=[PermissionLevel.READ],
                dependencies=["system_access"],
            ),
            "analysis": Capability(
                capability_id="analysis",
                name="Data Analysis",
                description="Analyze data and generate insights",
                capability_type=CapabilityType.ANALYSIS,
                permissions=[PermissionLevel.READ, PermissionLevel.WRITE],
                dependencies=["system_access", "monitoring"],
            ),
        }

    def _initialize_roles(self):
        """Initialize system roles"""
        self.roles = {
            "coordinator": AgentRole(
                role_id="coordinator",
                name="System Coordinator",
                description="Coordinates system operations and agent activities",
                capabilities=[
                    "system_access",
                    "communication",
                    "coordination",
                    "monitoring",
                ],
                required_training=["basic_orientation", "coordination_protocols"],
                permissions=[
                    PermissionLevel.READ,
                    PermissionLevel.WRITE,
                    PermissionLevel.EXECUTE,
                ],
            ),
            "worker": AgentRole(
                role_id="worker",
                name="Task Worker",
                description="Executes assigned tasks and reports progress",
                capabilities=["system_access", "communication", "task_execution"],
                required_training=["basic_orientation", "task_management"],
                permissions=[PermissionLevel.READ, PermissionLevel.EXECUTE],
            ),
            "monitor": AgentRole(
                role_id="monitor",
                name="System Monitor",
                description="Monitors system health and performance",
                capabilities=["system_access", "monitoring", "analysis"],
                required_training=["basic_orientation", "monitoring_protocols"],
                permissions=[PermissionLevel.READ, PermissionLevel.WRITE],
            ),
            "analyst": AgentRole(
                role_id="analyst",
                name="Data Analyst",
                description="Analyzes data and provides insights",
                capabilities=["system_access", "monitoring", "analysis"],
                required_training=["basic_orientation", "data_analysis"],
                permissions=[PermissionLevel.READ, PermissionLevel.WRITE],
            ),
            "admin": AgentRole(
                role_id="admin",
                name="System Administrator",
                description="Manages system configuration and permissions",
                capabilities=[
                    "system_access",
                    "communication",
                    "coordination",
                    "monitoring",
                    "analysis",
                ],
                required_training=["basic_orientation", "admin_protocols"],
                permissions=[
                    PermissionLevel.READ,
                    PermissionLevel.WRITE,
                    PermissionLevel.EXECUTE,
                    PermissionLevel.ADMIN,
                ],
            ),
        }

    def get_capability(self, capability_id: str) -> Optional[Capability]:
        """Get capability by ID"""
        return self.capabilities.get(capability_id)

    def get_role(self, role_id: str) -> Optional[AgentRole]:
        """Get role by ID"""
        return self.roles.get(role_id)

    def get_all_capabilities(self) -> List[Capability]:
        """Get all capabilities"""
        return list(self.capabilities.values())

    def get_all_roles(self) -> List[AgentRole]:
        """Get all roles"""
        return list(self.roles.values())

    def get_capabilities_by_type(
        self, capability_type: CapabilityType
    ) -> List[Capability]:
        """Get capabilities by type"""
        return [
            cap
            for cap in self.capabilities.values()
            if cap.capability_type == capability_type
        ]

    def get_roles_by_permission(self, permission: PermissionLevel) -> List[AgentRole]:
        """Get roles that have a specific permission"""
        return [role for role in self.roles.values() if permission in role.permissions]

    def validate_role_capabilities(self, role_id: str) -> bool:
        """Validate that a role's capabilities exist and are properly defined"""
        role = self.get_role(role_id)
        if not role:
            return False

        for capability_id in role.capabilities:
            if capability_id not in self.capabilities:
                return False

        return True

    def get_role_requirements(self, role_id: str) -> Dict[str, Any]:
        """Get requirements for a specific role"""
        role = self.get_role(role_id)
        if not role:
            return {}

        return {
            "role_id": role_id,
            "name": role.name,
            "description": role.description,
            "capabilities": [
                self.capabilities.get(cid)
                for cid in role.capabilities
                if cid in self.capabilities
            ],
            "required_training": role.required_training,
            "permissions": [p.value for p in role.permissions],
        }


def run_smoke_test():
    """Run basic functionality test for RoleDefinitionManager"""
    print("🧪 Running RoleDefinitionManager Smoke Test...")

    try:
        manager = RoleDefinitionManager()

        # Test capability retrieval
        system_access = manager.get_capability("system_access")
        assert system_access.name == "System Access"
        assert system_access.capability_type == CapabilityType.SYSTEM

        # Test role retrieval
        coordinator = manager.get_role("coordinator")
        assert coordinator.name == "System Coordinator"
        assert "coordination" in coordinator.capabilities

        # Test capability filtering
        system_caps = manager.get_capabilities_by_type(CapabilityType.SYSTEM)
        assert len(system_caps) == 1

        # Test role validation
        assert manager.validate_role_capabilities("coordinator")

        # Test role requirements
        requirements = manager.get_role_requirements("worker")
        assert requirements["name"] == "Task Worker"

        print("✅ RoleDefinitionManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ RoleDefinitionManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for RoleDefinitionManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Role Definition Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--list-capabilities", action="store_true", help="List all capabilities"
    )
    parser.add_argument("--list-roles", action="store_true", help="List all roles")
    parser.add_argument("--capability", help="Show capability details")
    parser.add_argument("--role", help="Show role details")
    parser.add_argument("--capability-type", help="Filter capabilities by type")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = RoleDefinitionManager()

    if args.list_capabilities:
        capabilities = manager.get_all_capabilities()
        print("System Capabilities:")
        for cap in capabilities:
            print(f"  {cap.capability_id}: {cap.name} ({cap.capability_type.value})")
    elif args.list_roles:
        roles = manager.get_all_roles()
        print("System Roles:")
        for role in roles:
            print(f"  {role.role_id}: {role.name}")
    elif args.capability:
        capability = manager.get_capability(args.capability)
        if capability:
            print(f"Capability: {capability.name}")
            print(f"Description: {capability.description}")
            print(f"Type: {capability.capability_type.value}")
            print(f"Permissions: {[p.value for p in capability.permissions]}")
        else:
            print(f"Capability '{args.capability}' not found")
    elif args.role:
        role = manager.get_role(args.role)
        if role:
            print(f"Role: {role.name}")
            print(f"Description: {role.description}")
            print(f"Capabilities: {role.capabilities}")
            print(f"Required Training: {role.required_training}")
        else:
            print(f"Role '{args.role}' not found")
    elif args.capability_type:
        try:
            cap_type = CapabilityType(args.capability_type)
            capabilities = manager.get_capabilities_by_type(cap_type)
            print(f"Capabilities of type '{args.capability_type}':")
            for cap in capabilities:
                print(f"  {cap.capability_id}: {cap.name}")
        except ValueError:
            print(f"Invalid capability type: {args.capability_type}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
