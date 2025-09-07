"""
agentassessmentresult.py
Module: agentassessmentresult.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:07
"""

# AgentAssessmentResult - Extracted for SRP compliance

class AgentAssessmentResult:
    """Individual agent assessment result"""
    agent_id: str
    agent_name: str
    assessment_status: AssessmentStatus
    web_integration_score: float
    integration_requirements: List[str]
    current_capabilities: List[str]
    missing_features: List[str]
    priority: IntegrationPriority
    estimated_effort_hours: int
    dependencies: List[str]
    last_assessed: datetime
    notes: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass

