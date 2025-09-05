#!/usr/bin/env python3
"""
Strategic Oversight Models - V2 Compliance Module
================================================

Backward compatibility wrapper for strategic oversight models.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import all components from modular architecture
from .models_core import *
from .models_extended import *

# Backward compatibility - export all classes and enums
__all__ = [
    # Core models
    'InsightType', 'ConfidenceLevel', 'ImpactLevel', 'MissionStatus',
    'StrategicInsight', 'MissionContext', 'AgentCapability', 'PerformanceMetrics',
    'RiskAssessment', 'OptimizationRecommendation',
    # Extended models
    'AlertSeverity', 'ActionType', 'StrategicAlert', 'StrategicAction',
    'StrategicReport', 'StrategicMetrics', 'StrategicConfiguration',
    'StrategicEvent', 'StrategicPattern', 'StrategicTrend'
]
