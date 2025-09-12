#!/usr/bin/env python3
"""
Architectural Onboarding System - Agent Cellphone V2
====================================================

Professional onboarding system based on SOLID principles, SSOT, DRY, KISS
with architectural proof through comprehensive TDD testing.

SOLID Principles Implementation:
- SRP: Each class has single responsibility
- OCP: Open for extension, closed for modification
- DIP: Dependencies injected via constructor

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any

from .agent_assignment_manager import AgentAssignmentManager
from .architectural_models import ArchitecturalPrinciple
from .architectural_principles import PrincipleDefinitions
from .compliance_validator import ComplianceValidator
from .onboarding_message_generator import OnboardingMessageGenerator


class ArchitecturalOnboardingManager:
    """Manages architectural onboarding for agents following SOLID principles.

    This system ensures that each agent is onboarded with specific architectural
    responsibilities and validation rules to maintain professional code quality.

    Uses dependency injection and delegates to specialized components.

EXAMPLE USAGE:
==============

# Import the service
from src.services.architectural_onboarding import Architectural_OnboardingService

# Initialize service
service = Architectural_OnboardingService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Architectural_OnboardingService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

    """

    def __init__(
        self,
        assignment_manager: AgentAssignmentManager | None = None,
        message_generator: OnboardingMessageGenerator | None = None,
        compliance_validator: ComplianceValidator | None = None,
    ):
        """Initialize the architectural onboarding manager with dependency injection."""
        self.assignment_manager = assignment_manager or AgentAssignmentManager()
        self.message_generator = message_generator or OnboardingMessageGenerator(
            PrincipleDefinitions.get_all_principles()
        )
        self.compliance_validator = compliance_validator or ComplianceValidator()

    def get_agent_principle(self, agent_id: str) -> ArchitecturalPrinciple | None:
        """Get the architectural principle assigned to an agent."""
        return self.assignment_manager.get_agent_principle(agent_id)

    def get_principle_guidance(self, principle: ArchitecturalPrinciple):
        """Get detailed guidance for a specific principle."""
        principles = PrincipleDefinitions.get_all_principles()
        return principles.get(principle)

    def assign_principle(self, agent_id: str, principle: ArchitecturalPrinciple) -> None:
        """Assign a principle to an agent."""
        self.assignment_manager.assign_principle(agent_id, principle)

    def get_all_assignments(self) -> dict[str, ArchitecturalPrinciple]:
        """Get all agent assignments."""
        return self.assignment_manager.get_all_assignments()

    def create_onboarding_message(self, agent_id: str) -> str:
        """Create a customized onboarding message for an agent."""
        principle = self.get_agent_principle(agent_id)
        if not principle:
            return self.message_generator.create_welcome_message(agent_id)

        return self.message_generator.create_onboarding_message(agent_id, principle)

    def validate_agent_compliance(self, agent_id: str, code_changes: list[str]) -> dict[str, Any]:
        """Validate that an agent's changes comply with their assigned principle."""
        principle = self.get_agent_principle(agent_id)
        if not principle:
            return {"compliant": True, "principle": None, "issues": [], "recommendations": []}

        result = self.compliance_validator.validate_agent_compliance(
            agent_id, principle, code_changes
        )

        guidance = self.get_principle_guidance(principle)

        return {
            "compliant": result.compliant,
            "principle": result.principle.value if result.principle else None,
            "issues": result.issues,
            "recommendations": result.recommendations,
            "guidance": guidance.description if guidance else None,
        }

    def get_all_principles(self) -> list[ArchitecturalPrinciple]:
        """Get all available architectural principles."""
        principles = PrincipleDefinitions.get_all_principles()
        return list(principles.keys())

    def assign_principle_to_agent(self, agent_id: str, principle: ArchitecturalPrinciple) -> bool:
        """Assign an architectural principle to an agent."""
        try:
            self.assignment_manager.assign_principle(agent_id, principle)
            return True
        except Exception:
            return False

    def get_agents_by_principle(self, principle: ArchitecturalPrinciple) -> list[str]:
        """Get all agents assigned to a specific principle."""
        return self.assignment_manager.get_agents_by_principle(principle)


# Global instance for easy access
architectural_manager = ArchitecturalOnboardingManager()
