#!/usr/bin/env python3
"""
Protocol Compliance Checker Core
===============================

Core classes and data structures for protocol compliance checking.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass
from enum import Enum


class ComplianceLevel(Enum):
    """Compliance level."""

    COMPLIANT = "compliant"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


class ProtocolCategory(Enum):
    """Protocol category."""

    GIT_WORKFLOW = "git_workflow"
    CODE_QUALITY = "code_quality"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    AGENT_COORDINATION = "agent_coordination"
    BRANCH_STRATEGY = "branch_strategy"


@dataclass
class ComplianceIssue:
    """Compliance issue."""

    category: ProtocolCategory
    level: ComplianceLevel
    message: str
    suggestion: str
    file_path: str | None = None
    line_number: int | None = None


@dataclass
class ComplianceReport:
    """Compliance report."""

    timestamp: str
    project_root: str
    total_issues: int
    critical_issues: int
    violations: int
    warnings: int
    compliant_items: int
    issues: list[ComplianceIssue]
    recommendations: list[str]
