#!/usr/bin/env python3
"""
Emergency Intervention Package - V2 Compliance Module
====================================================

Modular emergency intervention system for V2 compliance.
Refactored from monolithic implementation.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from .unified_emergency import (
    EmergencyInterventionOrchestrator,
    EmergencyInterventionModels,
    EmergencyInterventionEngine,
    EmergencyProtocols
)

# Re-export for backward compatibility
__all__ = [
    'EmergencyInterventionOrchestrator',
    'EmergencyInterventionModels',
    'EmergencyInterventionEngine',
    'EmergencyProtocols'
]