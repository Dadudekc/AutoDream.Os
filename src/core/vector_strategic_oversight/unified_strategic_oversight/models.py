"""
Strategic Oversight Models - Backward Compatibility Wrapper
===========================================================

Backward compatibility wrapper for strategic oversight models.
V2 Compliance: < 30 lines, single responsibility, compatibility layer.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Import everything from the refactored modules
from .models_refactored import *

# Re-export everything for backward compatibility
__all__ = [
    # Enums
    'InsightType', 'ConfidenceLevel', 'ImpactLevel', 'MissionStatus', 'PriorityLevel',
    'ReportType', 'AgentRole', 'EmergencyStatus',
    
    # Core Models
    'StrategicInsight', 'MissionObjective', 'ResourceAllocation',
    
    # Extended Models
    'StrategicRecommendation', 'OversightReport', 'PerformanceMetrics',
    'CoordinationPattern', 'StrategicContext', 'OversightConfig',
    
    # Additional Models
    'SwarmCoordinationInsight', 'StrategicOversightReport', 'AgentPerformanceMetrics',
    'SwarmCoordinationStatus', 'StrategicMission', 'VectorDatabaseMetrics', 'SystemHealthMetrics',
    'AgentCapabilities', 'PatternAnalysis', 'SuccessPrediction', 'RiskAssessment',
    'InterventionHistory', 'EmergencyAlert', 'PerformanceTrend',
    
    # Factory
    'StrategicOversightModels'
]