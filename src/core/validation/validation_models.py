#!/usr/bin/env python3
"""
Validation Models - Agent Cellphone V2
=====================================

Data models and enums for validation system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """Validation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ValidationResult(Enum):
    """Validation result types."""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


@dataclass
class ValidationIssue:
    """Individual validation issue."""
    rule_id: str
    rule_name: str
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any]
    timestamp: datetime
    component: str
