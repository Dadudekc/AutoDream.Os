#!/usr/bin/env python3
"""
Validation Result - Standardized Validation Output
================================================

Standardized validation result structure following V2 standards.
Provides consistent validation output across all system components.

Author: Agent-8 (Integration Enhancement Manager)
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum


class ValidationStatus(Enum):
    """Validation status enumeration"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


class ValidationSeverity(Enum):
    """Validation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Standardized validation result structure"""
    
    # Core validation information
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    
    # Validation details
    validator_name: str
    target_object: str
    validation_timestamp: float
    
    # Additional metadata
    details: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    error_code: Optional[str] = None
    execution_time: Optional[float] = None
    
    def is_successful(self) -> bool:
        """Check if validation was successful"""
        return self.status in [ValidationStatus.PASSED, ValidationStatus.SKIPPED]
    
    def is_critical(self) -> bool:
        """Check if validation result is critical"""
        return self.severity == ValidationSeverity.CRITICAL
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation result summary"""
        return {
            "status": self.status.value,
            "severity": self.severity.value,
            "message": self.message,
            "validator": self.validator_name,
            "target": self.target_object,
            "successful": self.is_successful(),
            "critical": self.is_critical()
        }
