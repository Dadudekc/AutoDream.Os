#!/usr/bin/env python3
"""
Security Infrastructure Package
Comprehensive security tools for Agent_Cellphone_V2_Repository
"""

# Import network security components
from .network_security import (
    NetworkScanner,
    VulnerabilityAssessor,
    AnomalyDetector,
    ThreatIntelligence,
    IncidentResponse,
    NetworkDevice,
    SecurityEvent,
)

# Import authentication components
from .authentication_manager import (
    AuthenticationManager,
    RoleBasedAccessControl,
)
from .session_manager import SessionManager
from .models import User, UserSession

# Import security monitoring components
# from .security_monitoring import (
#     SecurityMonitor,
#     AlertSystem,
#     SecurityLogEntry,
#     SecurityAlert,
# )

# Import compliance and audit components
from .compliance_audit import (
    SecurityPolicyValidator,
    AuditLogger,
    ComplianceReporter,
    SecurityPolicy,
    ValidationResult,
    AuditEvent,
    ComplianceReport,
)

# Package version
__version__ = "1.0.0"

# Package description
__description__ = "Comprehensive security infrastructure for network security, monitoring, and compliance"

# Export all security components
__all__ = [
    # Network Security
    "NetworkScanner",
    "VulnerabilityAssessor",
    "AnomalyDetector",
    "ThreatIntelligence",
    "IncidentResponse",
    "NetworkDevice",
    "SecurityEvent",
    # Authentication
    "AuthenticationManager",
    "SessionManager",
    "RoleBasedAccessControl",
    "User",
    "UserSession",
    # Security Monitoring
    # "SecurityMonitor",
    # "AlertSystem",
    # "SecurityLogEntry",
    # "SecurityAlert",
    # Compliance and Audit
    "SecurityPolicyValidator",
    "AuditLogger",
    "ComplianceReporter",
    "SecurityPolicy",
    "ValidationResult",
    "AuditEvent",
    "ComplianceReport",
]
