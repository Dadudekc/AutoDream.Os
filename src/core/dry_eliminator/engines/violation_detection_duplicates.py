"""
DRY Elimination Violation Detection Duplicates
=============================================

Duplicate detection functionality for DRY elimination system.
Handles duplicate imports, methods, constants, and code blocks.

V2 COMPLIANT: Focused duplicate detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR VIOLATION DETECTION
@license MIT
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

from ..dry_eliminator_models import (
    DRYViolation, DRYViolationType, ViolationSeverity, create_dry_violation
)


class ViolationDetectionDuplicates:
    """Duplicate detection for DRY elimination system"""
    
    def __init__(self, logger: logging.Logger):
        """Initialize duplicate detection"""
        self.logger = logger
    
    def detect_duplicate_imports(self, import_patterns: Dict[str, List[Tuple[Path, int]]]) -> List[DRYViolation]:
        """Detect duplicate import statements"""
        violations = []
        
        for import_name, locations in import_patterns.items():
            if len(locations) > 1:
                # Create violation for duplicate imports
                primary_location = locations[0]
                duplicate_locations = [f"{loc[0]}:{loc[1]}" for loc in locations[1:]]
                
                violation_id = f"import_{hash(import_name) % 10000}"
                violation = create_dry_violation(
                    violation_id=violation_id,
                    violation_type=DRYViolationType.DUPLICATE_IMPORT,
                    severity=ViolationSeverity.LOW,
                    file_path=str(primary_location[0]),
                    line_number=primary_location[1],
                    code_snippet=f"import {import_name}"
                )
                violation.duplicate_locations = duplicate_locations
                violations.append(violation)
                
                self.logger.debug(f"Detected duplicate import: {import_name} in {len(locations)} locations")
        
        return violations
    
    def detect_duplicate_methods(self, method_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate method definitions"""
        violations = []
        
        for method_name, locations in method_patterns.items():
            if len(locations) > 1:
                # Create violation for duplicate methods
                primary_location = locations[0]
                duplicate_locations = [f"{loc[0]}:{loc[1]}" for loc in locations[1:]]
                
                violation_id = f"method_{hash(method_name) % 10000}"
                violation = create_dry_violation(
                    violation_id=violation_id,
                    violation_type=DRYViolationType.DUPLICATE_FUNCTION,
                    severity=ViolationSeverity.MEDIUM,
                    file_path=str(primary_location[0]),
                    line_number=primary_location[1],
                    code_snippet=primary_location[2]
                )
                violation.duplicate_locations = duplicate_locations
                violations.append(violation)
                
                self.logger.debug(f"Detected duplicate method: {method_name} in {len(locations)} locations")
        
        return violations
    
    def detect_duplicate_constants(self, constant_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate constant definitions"""
        violations = []
        
        for constant_name, locations in constant_patterns.items():
            if len(locations) > 1:
                # Create violation for duplicate constants
                primary_location = locations[0]
                duplicate_locations = [f"{loc[0]}:{loc[1]}" for loc in locations[1:]]
                
                violation_id = f"constant_{hash(constant_name) % 10000}"
                violation = create_dry_violation(
                    violation_id=violation_id,
                    violation_type=DRYViolationType.DUPLICATE_CODE,
                    severity=ViolationSeverity.LOW,
                    file_path=str(primary_location[0]),
                    line_number=primary_location[1],
                    code_snippet=primary_location[2]
                )
                violation.duplicate_locations = duplicate_locations
                violations.append(violation)
                
                self.logger.debug(f"Detected duplicate constant: {constant_name} in {len(locations)} locations")
        
        return violations
    
    def detect_duplicate_code_blocks(self, duplicate_blocks: List[List[Dict]]) -> List[DRYViolation]:
        """Detect duplicate code blocks"""
        violations = []
        
        for block_group in duplicate_blocks:
            if len(block_group) > 1:
                # Create violation for duplicate code blocks
                primary_block = block_group[0]
                duplicate_locations = [f"{block['file']}:{block['line']}" for block in block_group[1:]]
                
                violation_id = f"block_{hash(primary_block['content']) % 10000}"
                violation = create_dry_violation(
                    violation_id=violation_id,
                    violation_type=DRYViolationType.DUPLICATE_CODE,
                    severity=ViolationSeverity.HIGH,
                    file_path=primary_block['file'],
                    line_number=primary_block['line'],
                    code_snippet=primary_block['content'][:100] + "..." if len(primary_block['content']) > 100 else primary_block['content']
                )
                violation.duplicate_locations = duplicate_locations
                violations.append(violation)
                
                self.logger.debug(f"Detected duplicate code block in {len(block_group)} locations")
        
        return violations
