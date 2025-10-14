#!/usr/bin/env python3
"""
Intelligent Context Models - V2 Compliance Module (Facade)
===========================================================

Data models and enums for intelligent context retrieval operations.

REFACTORED FOR V2 COMPLIANCE (ROI 90.00 - #1 HIGHEST IN CODEBASE):
- Original: 13 classes in 1 file (VIOLATION)
- Refactored: 7 focused modules with clean imports
- Pattern: Facade pattern (re-exports for backward compatibility)

Modules:
- context_enums.py: Enums (3 classes)
- mission_models.py: Mission context (1 class)
- agent_models.py: Agent capabilities (2 classes)
- context_results.py: Search and retrieval results (2 classes)
- emergency_models.py: Emergency interventions (2 classes)
- analysis_models.py: Risk and success predictions (2 classes)
- metrics_models.py: Context metrics (1 class)

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import all classes for backward compatibility (Facade pattern)
from .context_enums import AgentStatus, MissionPhase, RiskLevel
from .mission_models import MissionContext
from .agent_models import AgentCapability, AgentRecommendation
from .context_results import ContextRetrievalResult, SearchResult
from .emergency_models import EmergencyContext, InterventionProtocol
from .analysis_models import RiskAssessment, SuccessPrediction
from .metrics_models import ContextMetrics

# Re-export all classes for backward compatibility
__all__ = [
    # Enums
    "MissionPhase",
    "AgentStatus",
    "RiskLevel",
    # Mission
    "MissionContext",
    # Agent
    "AgentCapability",
    "AgentRecommendation",
    # Results
    "SearchResult",
    "ContextRetrievalResult",
    # Emergency
    "EmergencyContext",
    "InterventionProtocol",
    # Analysis
    "RiskAssessment",
    "SuccessPrediction",
    # Metrics
    "ContextMetrics",
]

