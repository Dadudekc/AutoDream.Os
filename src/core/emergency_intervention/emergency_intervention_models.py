#!/usr/bin/env python3
"""
Emergency Intervention Models - V2 Compliance Module (V2 Refactored)
====================================================================

V2 Refactored data models and enums for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# V2 Refactored - Backward Compatibility Wrapper
from .emergency_intervention_models_refactored import *

# Maintain backward compatibility
__all__ = [
    # Enums
    'EmergencySeverity', 'EmergencyType', 'EmergencyStatus',
    'InterventionType', 'InterventionPriority',
    # Core Models
    'Emergency', 'InterventionProtocol', 'InterventionResult', 'EmergencyPattern',
    # Metrics Models
    'EmergencyMetrics', 'InterventionAction', 'EmergencyContext', 'EmergencyResponse'
]