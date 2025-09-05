"""
Emergency Intervention Models Refactored - V2 Compliance Module
==============================================================

Refactored data models and enums for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import all emergency intervention components
from .emergency_intervention_enums import (
    EmergencySeverity, EmergencyType, EmergencyStatus,
    InterventionType, InterventionPriority
)
from .emergency_intervention_models import (
    Emergency, InterventionProtocol, InterventionResult, EmergencyPattern
)
from .emergency_intervention_metrics import (
    EmergencyMetrics, InterventionAction, EmergencyContext, EmergencyResponse
)

# Re-export all public components for backward compatibility
__all__ = [
    # Enums
    'EmergencySeverity', 'EmergencyType', 'EmergencyStatus',
    'InterventionType', 'InterventionPriority',
    # Core Models
    'Emergency', 'InterventionProtocol', 'InterventionResult', 'EmergencyPattern',
    # Metrics Models
    'EmergencyMetrics', 'InterventionAction', 'EmergencyContext', 'EmergencyResponse'
]
