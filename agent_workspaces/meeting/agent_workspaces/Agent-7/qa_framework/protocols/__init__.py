"""
🎯 QUALITY ASSURANCE FRAMEWORK - PROTOCOLS MODULE
Agent-7 - Quality Completion Optimization Manager

Protocol definitions for testing, validation, and compliance.
Follows V2 coding standards: ≤300 lines per module.
"""

from .testing_protocols import (
    TestingProtocols,
    TestCoverageRequirements,
    TestQualityStandards
)

from .validation_protocols import (
    ValidationProtocols,
    ValidationProcesses,
    QualityGates
)

from .compliance_protocols import (
    ComplianceProtocols,
    V2ComplianceChecker,
    StandardsValidator
)

__all__ = [
    "TestingProtocols",
    "TestCoverageRequirements",
    "TestQualityStandards",
    "ValidationProtocols",
    "ValidationProcesses",
    "QualityGates",
    "ComplianceProtocols",
    "V2ComplianceChecker",
    "StandardsValidator"
]
