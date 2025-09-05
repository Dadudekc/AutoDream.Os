"""
Strategic Oversight Models - Refactored Entry Point
===================================================

Unified entry point for strategic oversight models with backward compatibility.
V2 Compliance: < 50 lines, single responsibility, unified interface.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Core models and enums
from .models_core import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, PriorityLevel,
    StrategicInsight, MissionObjective, ResourceAllocation
)

# Extended models
from .models_extended import (
    StrategicRecommendation, OversightReport, PerformanceMetrics,
    CoordinationPattern, StrategicContext, OversightConfig
)

# Additional models from existing files
from .data_models import (
    SwarmCoordinationInsight, StrategicOversightReport, AgentPerformanceMetrics,
    SwarmCoordinationStatus, StrategicMission, VectorDatabaseMetrics, SystemHealthMetrics
)

from .extended_models import (
    AgentCapabilities, PatternAnalysis, SuccessPrediction, RiskAssessment,
    InterventionHistory, EmergencyAlert, PerformanceTrend, CoordinationPattern
)

from .enums import ReportType, AgentRole, EmergencyStatus

# Factory methods and configuration
from .models_factory import StrategicOversightModels

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
