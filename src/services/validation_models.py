#!/usr/bin/env python3
"""
Validation Models Module - Agent Cellphone V2
===========================================

Data models and structures for CLI validation system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationError:
    """Structured validation error with correlation ID."""
    code: int
    message: str
    hint: str
    correlation_id: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            "level": "error",
            "code": self.code,
            "msg": self.message,
            "hint": self.hint,
            "corr": self.correlation_id,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details or {}
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class ValidationResult:
    """Result of validation operation."""
    is_valid: bool
    error: Optional[ValidationError] = None

    @classmethod
    def success(cls) -> 'ValidationResult':
        """Create successful validation result."""
        return cls(is_valid=True)

    @classmethod
    def failure(cls, error: ValidationError) -> 'ValidationResult':
        """Create failed validation result."""
        return cls(is_valid=False, error=error)


class ValidationExitCodes:
    """Standard exit codes for validation errors."""
    SUCCESS = 0
    INVALID_FLAGS = 2
    DEPENDENCY_MISSING = 3
    MODE_MISMATCH = 4
    LOCK_TIMEOUT = 7
    QUEUE_FULL = 8
    INTERNAL_ERROR = 9


@dataclass
class ValidationRules:
    """Container for validation rules."""
    mutual_exclusions: list = None
    dependencies: Dict[str, list] = None
    mode_gated_flags: list = None

    def __post_init__(self):
        """Initialize default values."""
        if self.mutual_exclusions is None:
            self.mutual_exclusions = [
                (['agent'], ['bulk', 'onboarding', 'wrapup']),
            ]

        if self.dependencies is None:
            self.dependencies = {
                'get_next_task': ['agent'],
                'onboard': ['agent'],
            }

        if self.mode_gated_flags is None:
            self.mode_gated_flags = ['no_paste', 'new_tab_method']
