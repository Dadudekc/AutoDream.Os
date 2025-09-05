"""
Emergency Intervention Unified Models Refactored - KISS Simplified
=================================================================

Refactored data models and enums for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency models.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# Import all emergency intervention components
from .models_enums import (
    EmergencySeverity, EmergencyType, EmergencyStatus,
    InterventionAction, InterventionPriority, AlertLevel
)
from .models_core import (
    EmergencyEvent, InterventionPlan, InterventionResult
)
from .models_metrics import (
    EmergencyMetrics, EmergencyConfig, EmergencyAlert,
    EmergencyLog, EmergencyReport
)

# Re-export all public components for backward compatibility
__all__ = [
    # Enums
    'EmergencySeverity', 'EmergencyType', 'EmergencyStatus',
    'InterventionAction', 'InterventionPriority', 'AlertLevel',
    # Core Models
    'EmergencyEvent', 'InterventionPlan', 'InterventionResult',
    # Metrics Models
    'EmergencyMetrics', 'EmergencyConfig', 'EmergencyAlert',
    'EmergencyLog', 'EmergencyReport'
]
