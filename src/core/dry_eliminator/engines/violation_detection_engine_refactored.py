"""
DRY Elimination Violation Detection Engine Refactored
====================================================

Refactored violation detection engine for DRY elimination system.
Handles duplicate detection, unused code detection, and violation analysis.

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
from .violation_detection_base import ViolationDetectionEngineBase
from .violation_detection_duplicates import ViolationDetectionDuplicates
from .violation_detection_analysis import ViolationDetectionAnalysis


class ViolationDetectionEngine(ViolationDetectionEngineBase):
    """Refactored violation detection engine for DRY elimination system"""
    
    def __init__(self):
        """Initialize violation detection engine"""
        super().__init__()
        
        # Initialize modular components
        self.duplicates_detector = ViolationDetectionDuplicates(self.logger)
        self.analysis_detector = ViolationDetectionAnalysis(self.logger)
    
    def detect_duplicate_imports(self, import_patterns: Dict[str, List[Tuple[Path, int]]]) -> List[DRYViolation]:
        """Detect duplicate import statements"""
        violations = self.duplicates_detector.detect_duplicate_imports(import_patterns)
        for violation in violations:
            self.add_violation(violation)
        return violations
    
    def detect_duplicate_methods(self, method_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate method definitions"""
        violations = self.duplicates_detector.detect_duplicate_methods(method_patterns)
        for violation in violations:
            self.add_violation(violation)
        return violations
    
    def detect_duplicate_constants(self, constant_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate constant definitions"""
        violations = self.duplicates_detector.detect_duplicate_constants(constant_patterns)
        for violation in violations:
            self.add_violation(violation)
        return violations
    
    def detect_unused_imports(self, file_paths: List[Path]) -> List[DRYViolation]:
        """Detect unused import statements"""
        violations = self.analysis_detector.detect_unused_imports(file_paths)
        for violation in violations:
            self.add_violation(violation)
        return violations
    
    def detect_long_parameter_lists(self, file_paths: List[Path], max_params: int = 5) -> List[DRYViolation]:
        """Detect functions with long parameter lists"""
        violations = self.analysis_detector.detect_long_parameter_lists(file_paths, max_params)
        for violation in violations:
            self.add_violation(violation)
        return violations
    
    def detect_duplicate_code_blocks(self, duplicate_blocks: List[List[Dict]]) -> List[DRYViolation]:
        """Detect duplicate code blocks"""
        violations = self.duplicates_detector.detect_duplicate_code_blocks(duplicate_blocks)
        for violation in violations:
            self.add_violation(violation)
        return violations
