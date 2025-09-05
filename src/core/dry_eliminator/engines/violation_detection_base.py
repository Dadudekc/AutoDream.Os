"""
DRY Elimination Violation Detection Engine Base
==============================================

Base violation detection engine for DRY elimination system.
Handles core violation detection functionality.

V2 COMPLIANT: Focused violation detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR VIOLATION DETECTION
@license MIT
"""

import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

from ..dry_eliminator_models import (
    DRYViolation, DRYViolationType, ViolationSeverity, create_dry_violation
)


class ViolationDetectionEngineBase:
    """Base violation detection engine for DRY elimination system"""
    
    def __init__(self):
        """Initialize violation detection engine"""
        self.logger = logging.getLogger(__name__)
        self.detected_violations: List[DRYViolation] = []
    
    def get_violations_by_type(self) -> Dict[str, int]:
        """Get violations grouped by type"""
        type_counts = defaultdict(int)
        for violation in self.detected_violations:
            type_counts[violation.violation_type.value] += 1
        return dict(type_counts)
    
    def get_violations_by_severity(self) -> Dict[str, int]:
        """Get violations grouped by severity"""
        severity_counts = defaultdict(int)
        for violation in self.detected_violations:
            severity_counts[violation.severity.value] += 1
        return dict(severity_counts)
    
    def get_total_potential_savings(self) -> int:
        """Get total potential line savings from violations"""
        total_savings = 0
        for violation in self.detected_violations:
            if hasattr(violation, 'potential_savings'):
                total_savings += violation.potential_savings
        return total_savings
    
    def clear_violations(self):
        """Clear all detected violations"""
        self.detected_violations.clear()
        self.logger.info("Cleared all detected violations")
    
    def add_violation(self, violation: DRYViolation):
        """Add a violation to the detected violations list"""
        self.detected_violations.append(violation)
        self.logger.debug(f"Added violation: {violation.violation_id}")
    
    def get_violations(self) -> List[DRYViolation]:
        """Get all detected violations"""
        return self.detected_violations.copy()
