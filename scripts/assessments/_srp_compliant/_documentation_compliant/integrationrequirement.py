"""
integrationrequirement.py
Module: integrationrequirement.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:07
"""

# IntegrationRequirement - Extracted for SRP compliance

class IntegrationRequirement:
    """Web integration requirement specification"""
    requirement_id: str
    requirement_type: WebIntegrationType
    description: str
    priority: IntegrationPriority
    complexity: str
    estimated_hours: int
    dependencies: List[str]
    agent_dependencies: List[str]
    status: str = "pending"


@dataclass

