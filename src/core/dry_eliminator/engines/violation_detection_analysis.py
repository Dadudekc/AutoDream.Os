"""
DRY Elimination Violation Detection Analysis
===========================================

Analysis functionality for DRY elimination system.
Handles unused imports, long parameter lists, and code analysis.

V2 COMPLIANT: Focused analysis detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR VIOLATION DETECTION
@license MIT
"""

import logging
import re
from pathlib import Path
from typing import List

from ..dry_eliminator_models import (
    DRYViolation, DRYViolationType, ViolationSeverity, create_dry_violation
)


class ViolationDetectionAnalysis:
    """Analysis detection for DRY elimination system"""
    
    def __init__(self, logger: logging.Logger):
        """Initialize analysis detection"""
        self.logger = logger
    
    def detect_unused_imports(self, file_paths: List[Path]) -> List[DRYViolation]:
        """Detect unused import statements"""
        violations = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all import statements
                import_pattern = r'^from\s+(\S+)\s+import\s+(\S+)|^import\s+(\S+)'
                imports = re.findall(import_pattern, content, re.MULTILINE)
                
                for import_match in imports:
                    if import_match[0] and import_match[1]:  # from ... import ...
                        import_name = import_match[1]
                    elif import_match[2]:  # import ...
                        import_name = import_match[2]
                    else:
                        continue
                    
                    # Check if import is used
                    if not self._is_import_used(content, import_name):
                        violation_id = f"unused_import_{hash(str(file_path) + import_name) % 10000}"
                        violation = create_dry_violation(
                            violation_id=violation_id,
                            violation_type=DRYViolationType.DUPLICATE_IMPORT,
                            severity=ViolationSeverity.LOW,
                            file_path=str(file_path),
                            line_number=0,  # Will be updated with actual line number
                            code_snippet=f"import {import_name}"
                        )
                        violations.append(violation)
                        
                        self.logger.debug(f"Detected unused import: {import_name} in {file_path}")
            
            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {e}")
        
        return violations
    
    def _is_import_used(self, content: str, import_name: str) -> bool:
        """Check if an import is used in the content"""
        # Simple usage detection - can be enhanced
        usage_patterns = [
            rf'\b{re.escape(import_name)}\b',  # Direct usage
            rf'{re.escape(import_name)}\.',     # Attribute access
            rf'{re.escape(import_name)}\[',     # Index access
            rf'{re.escape(import_name)}\(',     # Function call
        ]
        
        for pattern in usage_patterns:
            if re.search(pattern, content):
                return True
        
        return False
    
    def detect_long_parameter_lists(self, file_paths: List[Path], max_params: int = 5) -> List[DRYViolation]:
        """Detect functions with long parameter lists"""
        violations = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find function definitions
                function_pattern = r'def\s+(\w+)\s*\((.*?)\):'
                functions = re.finditer(function_pattern, content, re.MULTILINE | re.DOTALL)
                
                for match in functions:
                    function_name = match.group(1)
                    parameters = match.group(2).strip()
                    
                    if parameters:
                        # Count parameters (simple comma-based counting)
                        param_count = len([p.strip() for p in parameters.split(',') if p.strip()])
                        
                        if param_count > max_params:
                            # Find line number
                            line_number = content[:match.start()].count('\n') + 1
                            
                            violation_id = f"long_params_{hash(str(file_path) + function_name) % 10000}"
                            violation = create_dry_violation(
                                violation_id=violation_id,
                                violation_type=DRYViolationType.DUPLICATE_CODE,
                                severity=ViolationSeverity.MEDIUM,
                                file_path=str(file_path),
                                line_number=line_number,
                                code_snippet=f"def {function_name}({parameters})"
                            )
                            violations.append(violation)
                            
                            self.logger.debug(f"Detected long parameter list: {function_name} with {param_count} parameters")
            
            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {e}")
        
        return violations
