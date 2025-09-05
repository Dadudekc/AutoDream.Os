"""
Intelligent Context Package - V2 Compliance Refactored
=====================================================

Modular intelligent context retrieval system for V2 compliance.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
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

# Import modular components
from .core.context_core import ContextCore

# Global context core instance
_context_core = None

def get_context_core() -> ContextCore:
    """Get global context core instance."""
    global _context_core
    
    if _context_core is None:
        _context_core = ContextCore()
    
    return _context_core

# Backward compatibility functions
def get_intelligent_context_retrieval():
    """Get intelligent context retrieval instance."""
    return IntelligentContextRetrieval()

def update_mission_context(context: MissionContext) -> bool:
    """Update mission context."""
    return get_context_core().update_mission_context(context)

def get_mission_context(mission_id: str) -> MissionContext:
    """Get mission context."""
    return get_context_core().get_mission_context(mission_id)

def get_agent_capabilities(agent_id: str) -> list:
    """Get agent capabilities."""
    return get_context_core().get_agent_capabilities(agent_id)

def search_context(query: str) -> ContextRetrievalResult:
    """Search context."""
    return get_context_core().search_context(query)

def get_emergency_context(emergency_id: str) -> EmergencyContext:
    """Get emergency context."""
    return get_context_core().get_emergency_context(emergency_id)

def get_intervention_protocols() -> list:
    """Get intervention protocols."""
    return get_context_core().get_intervention_protocols()

def optimize_agent_assignment(mission_id: str) -> list:
    """Optimize agent assignment."""
    return get_context_core().optimize_agent_assignment(mission_id)

def analyze_success_patterns() -> dict:
    """Analyze success patterns."""
    return get_context_core().analyze_success_patterns()

def assess_mission_risks(mission_id: str) -> RiskAssessment:
    """Assess mission risks."""
    return get_context_core().assess_mission_risks(mission_id)

def generate_success_predictions(task_id: str) -> SuccessPrediction:
    """Generate success predictions."""
    return get_context_core().generate_success_predictions(task_id)

def get_context_metrics() -> ContextMetrics:
    """Get context metrics."""
    return get_context_core().get_context_metrics()

__all__ = [
    'MissionContext',
    'AgentCapability',
    'SearchResult',
    'ContextRetrievalResult',
    'EmergencyContext',
    'InterventionProtocol',
    'RiskAssessment',
    'SuccessPrediction',
    'ContextMetrics',
    'ContextType',
    'Priority',
    'Status',
    'IntelligentContextRetrieval',
    'IntelligentContextModels',
    'IntelligentContextEngine',
    'IntelligentContextSearch',
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
    'get_context_metrics'
]