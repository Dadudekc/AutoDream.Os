"""
Dual Role Coordination System
Manages Agent-8's dual responsibilities: Team Beta Documentation Specialist + Phase 3 Integration Leader
V2 Compliant: ≤400 lines, simple data classes, direct method calls
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class RoleType(Enum):
    """Role type enumeration"""

    TEAM_BETA = "team_beta"
    PHASE_3_INTEGRATION = "phase_3_integration"


class Priority(Enum):
    """Priority enumeration"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class RoleResponsibility:
    """Role responsibility structure"""

    role_type: RoleType
    role_name: str
    leader: str
    mission: str
    priority: Priority
    estimated_cycles: int
    status: str = "active"
    progress: float = 0.0


@dataclass
class CoordinationTask:
    """Coordination task structure"""

    task_id: str
    name: str
    description: str
    role_type: RoleType
    assigned_to: str
    leader: str
    priority: Priority
    estimated_cycles: int
    dependencies: list[str]
    status: str = "pending"


class DualRoleCoordinationSystem:
    """Dual Role Coordination System for Agent-8"""

    def __init__(self):
        self.roles = self._initialize_dual_roles()
        self.coordination_tasks = self._initialize_coordination_tasks()
        self.coordination_protocols = self._initialize_coordination_protocols()
        self.integration_support = self._initialize_integration_support()

    def _initialize_dual_roles(self) -> list[RoleResponsibility]:
        """Initialize Agent-8's dual roles"""
        return [
            RoleResponsibility(
                role_type=RoleType.TEAM_BETA,
                role_name="Team Beta Documentation Specialist",
                leader="Agent-5",
                mission="Document VSCode fork and repository cloning processes",
                priority=Priority.HIGH,
                estimated_cycles=300,
            ),
            RoleResponsibility(
                role_type=RoleType.PHASE_3_INTEGRATION,
                role_name="Phase 3 System Integration Leader",
                leader="Agent-4 (Captain)",
                mission="Phase 3 System Integration for Dream.OS",
                priority=Priority.CRITICAL,
                estimated_cycles=720,
            ),
        ]

    def _initialize_coordination_tasks(self) -> list[CoordinationTask]:
        """Initialize coordination tasks for both roles"""
        return [
            # Team Beta Documentation Tasks (under Agent-5 leadership)
            CoordinationTask(
                task_id="team_beta_vsc_docs",
                name="VSCode Fork Documentation",
                description="Document VSCode fork installation, features, and usage",
                role_type=RoleType.TEAM_BETA,
                assigned_to="Agent-8",
                leader="Agent-5",
                priority=Priority.MEDIUM,
                estimated_cycles=80,
                dependencies=[],
            ),
            CoordinationTask(
                task_id="team_beta_repo_docs",
                name="Repository Cloning Documentation",
                description="Document repository cloning processes and setup guides",
                role_type=RoleType.TEAM_BETA,
                assigned_to="Agent-8",
                leader="Agent-5",
                priority=Priority.MEDIUM,
                estimated_cycles=100,
                dependencies=["team_beta_vsc_docs"],
            ),
            CoordinationTask(
                task_id="team_beta_user_guides",
                name="User-Friendly and Agent-Friendly Guides",
                description="Create comprehensive guides for users and agents",
                role_type=RoleType.TEAM_BETA,
                assigned_to="Agent-8",
                leader="Agent-5",
                priority=Priority.MEDIUM,
                estimated_cycles=120,
                dependencies=["team_beta_repo_docs"],
            ),
            # Phase 3 Integration Tasks (under Agent-4 leadership)
            CoordinationTask(
                task_id="phase3_system_init",
                name="Phase 3 System Initialization",
                description="Initialize Dream.OS environment and validate prerequisites",
                role_type=RoleType.PHASE_3_INTEGRATION,
                assigned_to="Agent-8",
                leader="Agent-4",
                priority=Priority.CRITICAL,
                estimated_cycles=60,
                dependencies=[],
            ),
            CoordinationTask(
                task_id="phase3_v3_integration",
                name="V3 Component Integration",
                description="Orchestrate integration of all V3 components into Dream.OS core",
                role_type=RoleType.PHASE_3_INTEGRATION,
                assigned_to="Agent-8",
                leader="Agent-4",
                priority=Priority.CRITICAL,
                estimated_cycles=180,
                dependencies=["phase3_system_init"],
            ),
            CoordinationTask(
                task_id="phase3_dream_os_integration",
                name="Dream.OS Native Integration",
                description="Lead native integration of V3 components and Dream.OS services",
                role_type=RoleType.PHASE_3_INTEGRATION,
                assigned_to="Agent-8",
                leader="Agent-4",
                priority=Priority.CRITICAL,
                estimated_cycles=200,
                dependencies=["phase3_v3_integration"],
            ),
            CoordinationTask(
                task_id="phase3_quality_integration",
                name="Quality Integration and Validation",
                description="Ensure integrated components meet V2 compliance and quality standards",
                role_type=RoleType.PHASE_3_INTEGRATION,
                assigned_to="Agent-8",
                leader="Agent-4",
                priority=Priority.MEDIUM,
                estimated_cycles=100,
                dependencies=["phase3_dream_os_integration"],
            ),
        ]

    def _initialize_coordination_protocols(self) -> dict[str, Any]:
        """Initialize coordination protocols for dual roles"""
        return {
            "team_beta_coordination": {
                "leader": "Agent-5",
                "mission": "VSCode forking and repository cloning",
                "coordination_method": "PyAutoGUI messaging system",
                "status_updates": "Daily",
                "authority": "Agent-5 has full authority to coordinate Team Beta efforts",
            },
            "phase_3_coordination": {
                "leader": "Agent-4 (Captain)",
                "mission": "Phase 3 System Integration",
                "coordination_method": "Captain coordination protocols",
                "status_updates": "Regular",
                "authority": "Agent-8 leads Phase 3 integration under Captain guidance",
            },
            "dual_role_management": {
                "coordination_strategy": "Parallel execution with priority management",
                "conflict_resolution": "Captain Agent-4 has final authority",
                "resource_allocation": "Dynamic based on priority and dependencies",
                "communication": "Separate channels for each role",
            },
        }

    def _initialize_integration_support(self) -> dict[str, Any]:
        """Initialize integration support capabilities"""
        return {
            "integration_specialist_capabilities": [
                "System integration support",
                "API management assistance",
                "Cross-platform compatibility",
                "Performance optimization",
                "Quality assurance validation",
                "V2 compliance enforcement",
                "Documentation and knowledge transfer",
            ],
            "team_beta_support": {
                "vscode_integration": "Dream.OS integration with VSCode fork",
                "repository_integration": "Repository cloning and dependency resolution",
                "testing_integration": "Testing framework integration",
                "documentation_integration": "Documentation system integration",
            },
            "phase_3_support": {
                "v3_integration": "V3 component integration orchestration",
                "dream_os_integration": "Dream.OS native integration leadership",
                "quality_integration": "Quality assurance and V2 compliance",
                "system_optimization": "Performance optimization and monitoring",
            },
        }

    def get_dual_role_status(self) -> dict[str, Any]:
        """Get dual role status"""
        team_beta_role = next(
            (role for role in self.roles if role.role_type == RoleType.TEAM_BETA), None
        )
        phase_3_role = next(
            (role for role in self.roles if role.role_type == RoleType.PHASE_3_INTEGRATION), None
        )

        return {
            "agent_id": "Agent-8",
            "specialization": "Integration Specialist",
            "dual_role_status": "ACTIVE",
            "team_beta_role": {
                "role": team_beta_role.role_name if team_beta_role else "N/A",
                "leader": team_beta_role.leader if team_beta_role else "N/A",
                "mission": team_beta_role.mission if team_beta_role else "N/A",
                "priority": team_beta_role.priority.value if team_beta_role else "N/A",
                "estimated_cycles": team_beta_role.estimated_cycles if team_beta_role else 0,
            },
            "phase_3_role": {
                "role": phase_3_role.role_name if phase_3_role else "N/A",
                "leader": phase_3_role.leader if phase_3_role else "N/A",
                "mission": phase_3_role.mission if phase_3_role else "N/A",
                "priority": phase_3_role.priority.value if phase_3_role else "N/A",
                "estimated_cycles": phase_3_role.estimated_cycles if phase_3_role else 0,
            },
        }

    def get_coordination_plan(self) -> dict[str, Any]:
        """Get coordination plan for dual roles"""
        team_beta_tasks = [
            task for task in self.coordination_tasks if task.role_type == RoleType.TEAM_BETA
        ]
        phase_3_tasks = [
            task
            for task in self.coordination_tasks
            if task.role_type == RoleType.PHASE_3_INTEGRATION
        ]

        return {
            "coordination_strategy": "Parallel execution with priority management",
            "team_beta_coordination": {
                "leader": "Agent-5",
                "total_tasks": len(team_beta_tasks),
                "total_cycles": sum(task.estimated_cycles for task in team_beta_tasks),
                "coordination_method": "PyAutoGUI messaging system",
                "authority": "Agent-5 has full authority",
            },
            "phase_3_coordination": {
                "leader": "Agent-4 (Captain)",
                "total_tasks": len(phase_3_tasks),
                "total_cycles": sum(task.estimated_cycles for task in phase_3_tasks),
                "coordination_method": "Captain coordination protocols",
                "authority": "Agent-8 leads under Captain guidance",
            },
            "conflict_resolution": "Captain Agent-4 has final authority",
            "resource_allocation": "Dynamic based on priority and dependencies",
        }

    def get_task_priorities(self) -> list[CoordinationTask]:
        """Get tasks sorted by priority"""
        return sorted(
            self.coordination_tasks,
            key=lambda task: (
                task.priority.value == Priority.CRITICAL.value,
                task.priority.value == Priority.HIGH.value,
                task.priority.value == Priority.MEDIUM.value,
                task.priority.value == Priority.LOW.value,
            ),
            reverse=True,
        )

    def get_integration_support_summary(self) -> dict[str, Any]:
        """Get integration support summary"""
        return {
            "integration_specialist": "Agent-8",
            "total_capabilities": len(
                self.integration_support["integration_specialist_capabilities"]
            ),
            "team_beta_support_areas": len(self.integration_support["team_beta_support"]),
            "phase_3_support_areas": len(self.integration_support["phase_3_support"]),
            "dual_role_coordination": "ACTIVE",
            "support_availability": "Available for both Team Beta and Phase 3 operations",
        }


def get_dual_role_coordination_status() -> dict[str, Any]:
    """Get dual role coordination status"""
    coordination_system = DualRoleCoordinationSystem()
    return {
        "dual_role_status": coordination_system.get_dual_role_status(),
        "coordination_plan": coordination_system.get_coordination_plan(),
        "integration_support": coordination_system.get_integration_support_summary(),
    }


if __name__ == "__main__":
    # Test dual role coordination system
    coordination_system = DualRoleCoordinationSystem()

    print("🎯 Agent-8 Dual Role Coordination System:")
    status = coordination_system.get_dual_role_status()
    print(f"Agent: {status['agent_id']} ({status['specialization']})")
    print(f"Dual Role Status: {status['dual_role_status']}")

    print("\n📋 Team Beta Role:")
    team_beta = status["team_beta_role"]
    print(f"  Role: {team_beta['role']}")
    print(f"  Leader: {team_beta['leader']}")
    print(f"  Priority: {team_beta['priority']}")
    print(f"  Cycles: {team_beta['estimated_cycles']}")

    print("\n📋 Phase 3 Integration Role:")
    phase_3 = status["phase_3_role"]
    print(f"  Role: {phase_3['role']}")
    print(f"  Leader: {phase_3['leader']}")
    print(f"  Priority: {phase_3['priority']}")
    print(f"  Cycles: {phase_3['estimated_cycles']}")

    print("\n🤝 Coordination Plan:")
    coordination = coordination_system.get_coordination_plan()
    print(f"Strategy: {coordination['coordination_strategy']}")
    print(f"Team Beta Leader: {coordination['team_beta_coordination']['leader']}")
    print(f"Phase 3 Leader: {coordination['phase_3_coordination']['leader']}")
    print(f"Conflict Resolution: {coordination['conflict_resolution']}")

    print("\n📊 Task Priorities:")
    priorities = coordination_system.get_task_priorities()
    for task in priorities[:5]:  # Show top 5 tasks
        print(f"  - {task.name} ({task.priority.value}) - {task.leader}")

    print("\n🔧 Integration Support:")
    support = coordination_system.get_integration_support_summary()
    print(f"Total Capabilities: {support['total_capabilities']}")
    print(f"Team Beta Support Areas: {support['team_beta_support_areas']}")
    print(f"Phase 3 Support Areas: {support['phase_3_support_areas']}")
    print(f"Dual Role Coordination: {support['dual_role_coordination']}")
