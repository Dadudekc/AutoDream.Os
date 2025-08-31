"""
assessmentsummary.py
Module: assessmentsummary.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:07
"""

# AssessmentSummary - Extracted for SRP compliance

class AssessmentSummary:
    """Overall assessment summary"""
    timestamp: datetime
    total_agents: int
    assessed_agents: int
    overall_status: AssessmentStatus
    critical_requirements: int
    high_priority_requirements: int
    total_estimated_hours: int
    completion_percentage: float
    next_steps: List[str]
    risk_factors: List[str]


@dataclass

