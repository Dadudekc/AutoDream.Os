"""
Architectural Models - V2 Compliance Module
==========================================

Data models for architectural principles following SOLID principles.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from dataclasses import dataclass
from enum import Enum


class ArchitecturalPrinciple(Enum):
    """Core architectural principles for professional development."""

    # SOLID Principles
    SINGLE_RESPONSIBILITY = "SRP"
    OPEN_CLOSED = "OCP"
    LISKOV_SUBSTITUTION = "LSP"
    INTERFACE_SEGREGATION = "ISP"
    DEPENDENCY_INVERSION = "DIP"

    # Other Key Principles
    SINGLE_SOURCE_OF_TRUTH = "SSOT"
    DONT_REPEAT_YOURSELF = "DRY"
    KEEP_IT_SIMPLE_STUPID = "KISS"

    # TDD & Testing
    TEST_DRIVEN_DEVELOPMENT = "TDD"


@dataclass
class ArchitecturalGuidance:

EXAMPLE USAGE:
==============

# Import the service
from src.services.architectural_models import Architectural_ModelsService

# Initialize service
service = Architectural_ModelsService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Architectural_ModelsService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

    """Structured guidance for each architectural principle."""

    principle: ArchitecturalPrinciple
    display_name: str
    description: str
    responsibilities: list[str]
    guidelines: list[str]
    examples: list[str]
    validation_rules: list[str]


@dataclass
class AgentAssignment:
    """Assignment of architectural principle to an agent."""

    agent_id: str
    principle: ArchitecturalPrinciple
    assigned_at: str
    assigned_by: str = "system"


@dataclass
class ComplianceValidationResult:
    """Result of compliance validation."""

    agent_id: str
    principle: ArchitecturalPrinciple
    compliant: bool
    issues: list[str]
    recommendations: list[str]
    validated_at: str
