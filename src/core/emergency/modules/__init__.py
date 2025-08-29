#!/usr/bin/env python3
"""
Emergency Response System Modules Package
Agent-3: Monolithic File Modularization Contract

This package contains all the modularized components of the emergency response system.
"""

from .emergency_types import (
    EmergencyLevel,
    EmergencyType,
    EmergencyEvent,
    EmergencyProtocol,
    EmergencyAction,
    EmergencyResponse
)

from .emergency_monitoring import EmergencyMonitoring
from .protocol_manager import ProtocolManager
from .emergency_coordination import EmergencyCoordination
from .recovery_manager import RecoveryManager
from .emergency_documentation import EmergencyDocumentation
from .health_integration import HealthIntegration
from .emergency_response_core import EmergencyResponseSystem

__all__ = [
    # Types and enums
    "EmergencyLevel",
    "EmergencyType", 
    "EmergencyEvent",
    "EmergencyProtocol",
    "EmergencyAction",
    "EmergencyResponse",
    
    # Core components
    "EmergencyResponseSystem",
    
    # Module components
    "EmergencyMonitoring",
    "ProtocolManager",
    "EmergencyCoordination", 
    "RecoveryManager",
    "EmergencyDocumentation",
    "HealthIntegration"
]

__version__ = "2.0.0"
__author__ = "Agent-3"
__description__ = "Modularized Emergency Response System"
