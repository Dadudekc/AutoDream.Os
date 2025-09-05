"""
Emergency Protocols - V2 Compliance Redirect
============================================

V2 compliance redirect to modular emergency protocols system.
Refactored from 367-line monolithic file into focused modules.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .protocols_v2 import (
    EmergencyProtocols,
    create_emergency_protocols,
    get_emergency_protocols
)

# Re-export for backward compatibility
__all__ = [
    'EmergencyProtocols',
    'create_emergency_protocols',
    'get_emergency_protocols'
]