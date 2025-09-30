#!/usr/bin/env python3
"""
Protocol Compliance Checker
===========================

Tool to verify compliance with Agent Protocol System standards.
Checks git workflow, code quality, documentation, and agent coordination protocols.
Refactored into modular components for V2 compliance.

Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

# Import all components from refactored modules
from .protocol_compliance_checker_core import (
    ComplianceIssue,
    ComplianceLevel,
    ComplianceReport,
    ProtocolCategory,
)
from .protocol_compliance_checker_main import ProtocolComplianceChecker
from .protocol_compliance_checker_utils import (
    format_compliance_report,
    main,
    print_compliance_report,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "ComplianceLevel",
    "ProtocolCategory",
    "ComplianceIssue",
    "ComplianceReport",
    # Main checker
    "ProtocolComplianceChecker",
    # Utility functions
    "print_compliance_report",
    "format_compliance_report",
    "main",
]


# For direct execution
if __name__ == "__main__":
    main()
