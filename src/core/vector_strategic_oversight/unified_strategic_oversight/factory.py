"""
Strategic Oversight Factory - Backward Compatibility Wrapper
============================================================

Backward compatibility wrapper for strategic oversight factory.
V2 Compliance: < 30 lines, single responsibility, compatibility layer.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Import everything from the refactored factory
from .factory_refactored import *

# Re-export everything for backward compatibility
__all__ = [
    'StrategicOversightFactory',
    'StrategicOversightReport', 'SwarmCoordinationInsight', 'StrategicRecommendation',
    'AgentPerformanceMetrics', 'SwarmCoordinationStatus', 'StrategicMission',
    'VectorDatabaseMetrics', 'SystemHealthMetrics'
]