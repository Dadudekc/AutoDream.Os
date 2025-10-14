#!/usr/bin/env python3
"""
Intelligent Context Models - V2 Compliant Architecture
=======================================================

Backward-compatible facade for intelligent context models.

This module maintains the original API while delegating to the new modular
V2-compliant architecture.

Usage:
    # Original imports still work (backward compatibility)
    from src.core.intelligent_context import MissionContext, AgentCapability
    from src.core.intelligent_context import MissionPhase, AgentStatus, RiskLevel

    # Or import from new modules directly
    from src.core.intelligent_context.core_models import MissionContext
    from src.core.intelligent_context.enums import MissionPhase

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored for V2 compliance (≤5 classes per file)
License: MIT
"""

# Enums
# Analysis models
from .analysis_models import AgentRecommendation, RiskAssessment, SuccessPrediction

# Core models
from .core_models import AgentCapability, MissionContext

# Emergency models
from .emergency_models import EmergencyContext, InterventionProtocol
from .enums import AgentStatus, MissionPhase, RiskLevel

# Metrics
from .metrics import ContextMetrics

# Search models
from .search_models import ContextRetrievalResult, SearchResult

__all__ = [
    # Enums
    "MissionPhase",
    "AgentStatus",
    "RiskLevel",
    # Core models
    "MissionContext",
    "AgentCapability",
    # Search models
    "SearchResult",
    "ContextRetrievalResult",
    # Emergency models
    "EmergencyContext",
    "InterventionProtocol",
    # Analysis models
    "AgentRecommendation",
    "RiskAssessment",
    "SuccessPrediction",
    # Metrics
    "ContextMetrics",
]

# Module metadata
__version__ = "2.0.0"
__author__ = "Agent-7 - Knowledge & OSS Contribution Specialist"
__refactored_from__ = "intelligent_context_models.py"
__v2_compliance__ = True
