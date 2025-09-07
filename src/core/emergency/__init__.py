from .emergency_documentation import (
from .emergency_orchestrator import EmergencyResponseOrchestrator
from .emergency_response_system import (
from .failure_detection_system import (
from .recovery_procedures import (

#!/usr/bin/env python3
"""
Emergency Response System Module - Contract EMERGENCY-RESTORE-005
===============================================================

Comprehensive emergency response protocols for system failures.
Implements automated failure detection, rapid recovery procedures,
and emergency documentation as required by the contract.

Author: Agent-6 (Data & Analytics Specialist)
Contract: EMERGENCY-RESTORE-005: Emergency Response Protocol (400 pts)
License: MIT
"""

    EmergencyResponseSystem,
    EmergencyLevel,
    EmergencyType,
    EmergencyEvent,
    EmergencyProtocol
)

    FailureDetectionSystem,
    DetectionType,
    DetectionRule
)

    RecoveryProceduresSystem,
    RecoveryActionType,
    RecoveryAction,
    RecoveryProcedure
)

    EmergencyDocumentationSystem,
    EmergencyReport,
    EmergencySummary
)


# Main exports
__all__ = [
    # Core emergency response system
    "EmergencyResponseSystem",
    "EmergencyLevel",
    "EmergencyType",
    "EmergencyEvent",
    "EmergencyProtocol",
    
    # Failure detection system
    "FailureDetectionSystem",
    "DetectionType",
    "DetectionRule",
    
    # Recovery procedures
    "RecoveryProceduresSystem",
    "RecoveryActionType",
    "RecoveryAction",
    "RecoveryProcedure",
    
    # Emergency documentation
    "EmergencyDocumentationSystem",
    "EmergencyReport",
    "EmergencySummary",
    
    # Main orchestrator
    "EmergencyResponseOrchestrator"
]

# Version information
__version__ = "1.0.0"
__author__ = "Agent-6 (Data & Analytics Specialist)"
__contract__ = "EMERGENCY-RESTORE-005: Emergency Response Protocol (400 pts)"
__description__ = "Comprehensive emergency response protocols for system failures"
