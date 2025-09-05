#!/usr/bin/env python3
"""
Emergency Intervention Orchestrator - V2 Compliance Redirect
===========================================================

V2 compliance redirect to modular emergency intervention system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# V2 COMPLIANCE REDIRECT - see emergency_intervention package

from .emergency_intervention import (
    EmergencySeverity,
    EmergencyType,
    EmergencyStatus,
    Emergency,
    InterventionProtocol,
    InterventionResult,
    EmergencyPattern,
    EmergencyMetrics,
    InterventionAction,
    EmergencyContext,
    EmergencyResponse,
    EmergencyHistory,
    EmergencyInterventionEngine,
    EmergencyInterventionOrchestrator,
    get_emergency_intervention_system,
    report_emergency,
    get_emergency_status,
    get_intervention_protocols,
    get_emergency_metrics,
    get_emergency_history,
    activate_emergency_response,
    resolve_emergency,
    get_emergency_patterns,
    optimize_intervention_strategies,
)

# Re-export for backward compatibility
__all__ = [
    'EmergencySeverity',
    'EmergencyType',
    'EmergencyStatus',
    'Emergency',
    'InterventionProtocol',
    'InterventionResult',
    'EmergencyPattern',
    'EmergencyMetrics',
    'InterventionAction',
    'EmergencyContext',
    'EmergencyResponse',
    'EmergencyHistory',
    'EmergencyInterventionEngine',
    'EmergencyInterventionOrchestrator',
    'get_emergency_intervention_system',
    'report_emergency',
    'get_emergency_status',
    'get_intervention_protocols',
    'get_emergency_metrics',
    'get_emergency_history',
    'activate_emergency_response',
    'resolve_emergency',
    'get_emergency_patterns',
    'optimize_intervention_strategies',
]
