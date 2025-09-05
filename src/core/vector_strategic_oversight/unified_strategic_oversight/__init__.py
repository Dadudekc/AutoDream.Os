"""
Unified Strategic Oversight Package
==================================

Modular vector strategic oversight system.
V2 Compliance: Clean, focused, single-responsibility modules.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

# Import modular components
from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus,
    ReportType, PriorityLevel, AgentRole
)
from .data_models import (
    SwarmCoordinationInsight, StrategicRecommendation, StrategicOversightReport,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics
)
from .factory_methods import StrategicOversightFactory
from .validators import StrategicOversightValidator
from .orchestrator import VectorStrategicOversightOrchestrator

__all__ = [
    # Enums
    'InsightType', 'ConfidenceLevel', 'ImpactLevel', 'MissionStatus',
    'ReportType', 'PriorityLevel', 'AgentRole',
    
    # Data Models
    'SwarmCoordinationInsight', 'StrategicRecommendation', 'StrategicOversightReport',
    'AgentPerformanceMetrics', 'SwarmCoordinationStatus', 'StrategicMission',
    'VectorDatabaseMetrics', 'SystemHealthMetrics',
    
    # Factory Methods
    'StrategicOversightFactory',
    
    # Validators
    'StrategicOversightValidator',
    
    # Orchestrator
    'VectorStrategicOversightOrchestrator'
]
