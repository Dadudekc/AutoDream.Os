#!/usr/bin/env python3
"""
Validation Types - V2 Modular Architecture
==========================================

Data structures for performance validation.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ValidationStatus(Enum):
    """Validation result status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"
    ERROR = "error"


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ValidationType(Enum):
    """Types of validation."""
    THRESHOLD = "threshold"
    TREND = "trend"
    COMPARISON = "comparison"
    CUSTOM = "custom"


@dataclass
class ValidationRule:
    """A validation rule definition."""
    name: str
    rule_type: ValidationType
    severity: ValidationSeverity
    enabled: bool = True
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            "name": self.name,
            "rule_type": self.rule_type.value,
            "severity": self.severity.value,
            "enabled": self.enabled,
            "description": self.description,
            "parameters": self.parameters
        }


@dataclass
class ValidationContext:
    """Context for validation execution."""
    validation_id: str
    timestamp: datetime
    source: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "validation_id": self.validation_id,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "parameters": self.parameters,
            "metadata": self.metadata
        }


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    metric_name: str
    current_value: Any
    threshold: Any
    severity: ValidationSeverity
    message: str
    passed: bool
    timestamp: str
    
    def is_passed(self) -> bool:
        """Check if validation passed."""
        return self.passed
    
    def is_failed(self) -> bool:
        """Check if validation failed."""
        return not self.passed
    
    def is_critical(self) -> bool:
        """Check if validation is critical."""
        return self.severity == ValidationSeverity.CRITICAL
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "metric_name": self.metric_name,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "severity": self.severity.value,
            "message": self.message,
            "passed": self.passed,
            "timestamp": self.timestamp
        }


@dataclass
class ValidationSummary:
    """Summary of validation results."""
    total_validations: int
    passed_validations: int
    failed_validations: int
    success_rate: float
    severity_distribution: Dict[str, int]
    last_validation: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        return {
            "total_validations": self.total_validations,
            "passed_validations": self.passed_validations,
            "failed_validations": self.failed_validations,
            "success_rate": self.success_rate,
            "severity_distribution": self.severity_distribution,
            "last_validation": self.last_validation
        }
