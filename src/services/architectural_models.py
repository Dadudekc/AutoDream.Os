"""
Architectural Models - V2 Compliance Module
==========================================

Data models for architectural principles following SOLID principles.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


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
    """Structured guidance for each architectural principle."""

    principle: ArchitecturalPrinciple
    display_name: str
    description: str
    responsibilities: List[str]
    guidelines: List[str]
    examples: List[str]
    validation_rules: List[str]


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
    issues: List[str]
    recommendations: List[str]
    validated_at: str
