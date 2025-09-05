#!/usr/bin/env python3
"""
DRY Elimination Violation Detection Engine
==========================================

Violation detection engine for DRY elimination system.
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


class ViolationDetectionEngine:
    """Violation detection engine for DRY elimination system"""
    
    def __init__(self):
        """Initialize violation detection engine"""
        self.logger = logging.getLogger(__name__)
        self.detected_violations: List[DRYViolation] = []
    
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
                    violation_type=DRYViolationType.DUPLICATE_IMPORTS,
                    severity=ViolationSeverity.LOW,
                    file_path=str(primary_location[0]),
                    line_number=primary_location[1],
                    code_snippet=f"import {import_name}"
                )
                violation.duplicate_locations = duplicate_locations
                violation.potential_savings = len(locations) - 1
                
                violations.append(violation)
        
        return violations
    
    def detect_duplicate_methods(self, method_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate method implementations"""
        violations = []
        
        for method_sig, locations in method_patterns.items():
            if len(locations) > 1:
                # Group by similar method bodies
                body_groups = defaultdict(list)
                for location in locations:
                    body_hash = hash(location[2][:100])  # Hash first 100 chars
                    body_groups[body_hash].append(location)
                
                for body_hash, group_locations in body_groups.items():
                    if len(group_locations) > 1:
                        primary_location = group_locations[0]
                        duplicate_locations = [f"{loc[0]}:{loc[1]}" for loc in group_locations[1:]]
                        
                        violation_id = f"method_{hash(method_sig + str(body_hash)) % 10000}"
                        violation = create_dry_violation(
                            violation_id=violation_id,
                            violation_type=DRYViolationType.DUPLICATE_METHODS,
                            severity=ViolationSeverity.MEDIUM,
                            file_path=str(primary_location[0]),
                            line_number=primary_location[1],
                            code_snippet=primary_location[2][:100]
                        )
                        violation.duplicate_locations = duplicate_locations
                        violation.potential_savings = (len(group_locations) - 1) * 5  # Estimate 5 lines per method
                        
                        violations.append(violation)
        
        return violations
    
    def detect_duplicate_constants(self, constant_patterns: Dict[str, List[Tuple[Path, int, str]]]) -> List[DRYViolation]:
        """Detect duplicate constant definitions"""
        violations = []
        
        for const_name, locations in constant_patterns.items():
            if len(locations) > 1:
                # Group by constant value
                value_groups = defaultdict(list)
                for location in locations:
                    value_hash = hash(location[2])
                    value_groups[value_hash].append(location)
                
                for value_hash, group_locations in value_groups.items():
                    if len(group_locations) > 1:
                        primary_location = group_locations[0]
                        duplicate_locations = [f"{loc[0]}:{loc[1]}" for loc in group_locations[1:]]
                        
                        violation_id = f"const_{hash(const_name + str(value_hash)) % 10000}"
                        violation = create_dry_violation(
                            violation_id=violation_id,
                            violation_type=DRYViolationType.DUPLICATE_CONSTANTS,
                            severity=ViolationSeverity.LOW,
                            file_path=str(primary_location[0]),
                            line_number=primary_location[1],
                            code_snippet=primary_location[2][:100]
                        )
                        violation.duplicate_locations = duplicate_locations
                        violation.potential_savings = len(group_locations) - 1
                        
                        violations.append(violation)
        
        return violations
    
    def detect_unused_imports(self, file_paths: List[Path]) -> List[DRYViolation]:
        """Detect unused import statements"""
        violations = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple unused import detection
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    
                    if line.startswith('import ') or line.startswith('from '):
                        # Extract import name
                        if line.startswith('import '):
                            import_name = line.split()[1].split('.')[0]
                        else:  # from ... import ...
                            import_name = line.split()[-1].split('.')[0]
                        
                        # Check if import is used in the file
                        if not self._is_import_used(content, import_name):
                            violation_id = f"unused_{hash(import_name + str(file_path)) % 10000}"
                            violation = create_dry_violation(
                                violation_id=violation_id,
                                violation_type=DRYViolationType.UNUSED_IMPORTS,
                                severity=ViolationSeverity.LOW,
                                file_path=str(file_path),
                                line_number=line_num,
                                code_snippet=line
                            )
                            violation.potential_savings = 1
                            violations.append(violation)
            
            except Exception as e:
                self.logger.warning(f"Could not analyze {file_path} for unused imports: {e}")
        
        return violations
    
    def _is_import_used(self, content: str, import_name: str) -> bool:
        """Check if import is used in the content"""
        # Simple check - look for the import name in the content
        # This is a basic implementation and could be improved
        lines = content.split('\n')
        
        for line in lines:
            # Skip import lines
            if line.strip().startswith(('import ', 'from ')):
                continue
            
            # Check if import name appears in the line
            if import_name in line:
                return True
        
        return False
    
    def detect_long_parameter_lists(self, file_paths: List[Path], max_params: int = 5) -> List[DRYViolation]:
        """Detect functions with too many parameters"""
        violations = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    
                    # Look for function definitions
                    if line.startswith('def ') and '(' in line and ')' in line:
                        # Extract parameters
                        param_start = line.find('(')
                        param_end = line.find(')')
                        if param_start != -1 and param_end != -1:
                            params_str = line[param_start + 1:param_end]
                            params = [p.strip() for p in params_str.split(',') if p.strip()]
                            
                            if len(params) > max_params:
                                violation_id = f"long_params_{hash(line) % 10000}"
                                violation = create_dry_violation(
                                    violation_id=violation_id,
                                    violation_type=DRYViolationType.LONG_PARAMETER_LISTS,
                                    severity=ViolationSeverity.MEDIUM,
                                    file_path=str(file_path),
                                    line_number=line_num,
                                    code_snippet=line
                                )
                                violation.potential_savings = 1  # Could be refactored
                                violations.append(violation)
            
            except Exception as e:
                self.logger.warning(f"Could not analyze {file_path} for long parameter lists: {e}")
        
        return violations
    
    def detect_duplicate_code_blocks(self, duplicate_blocks: List[List[Dict]]) -> List[DRYViolation]:
        """Detect duplicate code blocks"""
        violations = []
        
        for block_group in duplicate_blocks:
            if len(block_group) > 1:
                primary_block = block_group[0]
                duplicate_locations = [f"{block['file_path']}:{block['start_line']}" for block in block_group[1:]]
                
                violation_id = f"duplicate_block_{hash(primary_block['content']) % 10000}"
                violation = create_dry_violation(
                    violation_id=violation_id,
                    violation_type=DRYViolationType.DUPLICATE_CODE_BLOCKS,
                    severity=ViolationSeverity.HIGH,
                    file_path=str(primary_block['file_path']),
                    line_number=primary_block['start_line'],
                    code_snippet=primary_block['content'][:100]
                )
                violation.duplicate_locations = duplicate_locations
                violation.potential_savings = len(block_group) - 1
                violations.append(violation)
        
        return violations
    
    def get_violations_by_type(self) -> Dict[str, int]:
        """Get violation count by type"""
        type_counts = defaultdict(int)
        for violation in self.detected_violations:
            type_counts[violation.violation_type.value] += 1
        return dict(type_counts)
    
    def get_violations_by_severity(self) -> Dict[str, int]:
        """Get violation count by severity"""
        severity_counts = defaultdict(int)
        for violation in self.detected_violations:
            severity_counts[violation.severity.value] += 1
        return dict(severity_counts)
    
    def get_total_potential_savings(self) -> int:
        """Get total potential lines that could be saved"""
        return sum(violation.potential_savings for violation in self.detected_violations)
    
    def clear_violations(self):
        """Clear detected violations"""
        self.detected_violations.clear()


# Factory function for dependency injection
def create_violation_detection_engine() -> ViolationDetectionEngine:
    """Factory function to create violation detection engine"""
    return ViolationDetectionEngine()


# Export for DI
__all__ = ['ViolationDetectionEngine', 'create_violation_detection_engine']
