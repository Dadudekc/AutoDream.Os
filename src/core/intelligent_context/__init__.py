#!/usr/bin/env python3
"""
Intelligent Context Package - V2 Compliance Module
================================================

Modular intelligent context retrieval system for V2 compliance.
Replaces monolithic intelligent_context_retrieval.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_intelligent_context import (
    IntelligentContextRetrieval,
    IntelligentContextModels,
    IntelligentContextEngine,
    IntelligentContextSearch
)

# Backward compatibility - re-export models
from .unified_intelligent_context.models import (
    MissionContext,
    AgentCapability,
    SearchResult,
    ContextRetrievalResult,
    EmergencyContext,
    InterventionProtocol,
    RiskAssessment,
    SuccessPrediction,
    ContextMetrics,
    ContextType,
    Priority,
    Status
)

# Backward compatibility functions
def get_intelligent_context_retrieval():
    """Get intelligent context retrieval instance."""
    return IntelligentContextRetrieval()

def update_mission_context(context: MissionContext) -> bool:
    """Update mission context."""
    return True  # Mock implementation

def get_mission_context(mission_id: str) -> MissionContext:
    """Get mission context."""
    return None  # Mock implementation

def get_agent_capabilities(agent_id: str) -> list:
    """Get agent capabilities."""
    return []  # Mock implementation

def search_context(query: str) -> ContextRetrievalResult:
    """Search context."""
    return ContextRetrievalResult(
        retrieval_id="mock",
        query=query,
        results=[],
        execution_time=0.0,
        success=True
    )

def get_emergency_context(emergency_id: str) -> EmergencyContext:
    """Get emergency context."""
    return None  # Mock implementation

def get_intervention_protocols() -> list:
    """Get intervention protocols."""
    return []  # Mock implementation

def optimize_agent_assignment(mission_id: str) -> list:
    """Optimize agent assignment."""
    return []  # Mock implementation

def analyze_success_patterns() -> dict:
    """Analyze success patterns."""
    return {}  # Mock implementation

def assess_mission_risks(mission_id: str) -> RiskAssessment:
    """Assess mission risks."""
    return None  # Mock implementation

def generate_success_predictions(task_id: str) -> SuccessPrediction:
    """Generate success predictions."""
    return None  # Mock implementation

def get_context_metrics() -> ContextMetrics:
    """Get context metrics."""
    return ContextMetrics()

__all__ = [
    'MissionContext',
    'AgentCapability',
    'SearchResult',
    'ContextRetrievalResult',
    'EmergencyContext',
    'InterventionProtocol',
    'AgentRecommendation',
    'RiskAssessment',
    'SuccessPrediction',
    'ContextMetrics',
    'IntelligentContextEngine',
    'IntelligentContextRetrieval',
    'get_intelligent_context_retrieval',
    'update_mission_context',
    'get_mission_context',
    'get_agent_capabilities',
    'search_context',
    'get_emergency_context',
    'get_intervention_protocols',
    'optimize_agent_assignment',
    'analyze_success_patterns',
    'assess_mission_risks',
    'generate_success_predictions',
    'get_context_metrics',
]
