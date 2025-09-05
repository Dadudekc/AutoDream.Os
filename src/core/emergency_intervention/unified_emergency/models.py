"""
Emergency Intervention Models - KISS Simplified (V2 Refactored)
==============================================================

V2 Refactored data models and enums for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency models.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# V2 Refactored - Backward Compatibility Wrapper
from .models_refactored import *

# Maintain backward compatibility
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