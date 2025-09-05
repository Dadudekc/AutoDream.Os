#!/usr/bin/env python3
"""
Intelligent Context Models - V2 Compliance Module
================================================

Backward compatibility wrapper for intelligent context models.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import all components from modular architecture
from .models_core import *
from .models_extended import *

# Backward compatibility - export all classes and enums
__all__ = [
    # Core models
    'ContextType', 'Priority', 'Status', 'MissionContext', 'AgentCapability',
    'SearchResult', 'AgentRecommendation', 'RiskAssessment', 'SuccessPrediction',
    # Extended models
    'MissionPhase', 'AgentStatus', 'RiskLevel', 'EmergencyContext',
    'InterventionProtocol', 'InterventionResult', 'EmergencyPattern',
    'EmergencyMetrics', 'InterventionAction', 'EmergencyResponse', 'EmergencyHistory'
]