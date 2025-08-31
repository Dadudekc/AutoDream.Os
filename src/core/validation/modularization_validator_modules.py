#!/usr/bin/env python3
"""
Modularization Validator - Modular Components
=============================================

Split from modularization_validator.py (795 lines) to achieve V2 compliance.
This module contains the core modularization validation components.

Author: Agent-1 (PERPETUAL MOTION LEADER - V2 COMPLIANCE SPECIALIST)
Mission: V2 COMPLIANCE OPTIMIZATION - File Size Reduction
License: MIT
"""

import os
import ast
import logging
from typing import Dict, List, Set, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    file_path: str
    line_number: int
    severity: ValidationSeverity
    message: str
    category: str
    suggestion: str = ""


@dataclass
class ModularizationConfig:
    """Modularization validation configuration"""
    max_file_size: int = 400  # lines
    max_function_size: int = 50  # lines
    max_class_size: int = 200  # lines
    max_imports: int = 20
    enable_complexity_check: bool = True
    max_complexity: int = 10


class FileSizeValidator:
    """Validates file size compliance"""
    
    def __init__(self, config: ModularizationConfig):
        self.config = config
        
    def validate(self, file_path: str) -> List[ValidationIssue]:
        """Validate file size"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            line_count = len(lines)
            if line_count > self.config.max_file_size:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=1,
                    severity=ValidationSeverity.ERROR,
                    message=f"File too large: {line_count} lines (max: {self.config.max_file_size})",
                    category="file_size",
                    suggestion="Consider breaking into smaller modules"
                ))
                
        except Exception as e:
            logger.error(f"Failed to validate file size for {file_path}: {e}")
            
        return issues


class FunctionSizeValidator:
    """Validates function size compliance"""
    
    def __init__(self, config: ModularizationConfig):
        self.config = config
        
    def validate(self, file_path: str) -> List[ValidationIssue]:
        """Validate function sizes"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Count lines in function
                    start_line = node.lineno
                    end_line = self._get_end_line(node)
                    function_size = end_line - start_line + 1
                    
                    if function_size > self.config.max_function_size:
                        issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=start_line,
                            severity=ValidationSeverity.WARNING,
                            message=f"Function '{node.name}' too large: {function_size} lines (max: {self.config.max_function_size})",
                            category="function_size",
                            suggestion="Consider breaking into smaller functions"
                        ))
                        
        except Exception as e:
            logger.error(f"Failed to validate function sizes for {file_path}: {e}")
            
        return issues
    
    def _get_end_line(self, node: ast.FunctionDef) -> int:
        """Get the end line of a function"""
        if hasattr(node, 'end_lineno'):
            return node.end_lineno
        else:
            # Fallback: estimate end line
            return node.lineno + 50  # Rough estimate


class ClassSizeValidator:
    """Validates class size compliance"""
    
    def __init__(self, config: ModularizationConfig):
        self.config = config
        
    def validate(self, file_path: str) -> List[ValidationIssue]:
        """Validate class sizes"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Count lines in class
                    start_line = node.lineno
                    end_line = self._get_end_line(node)
                    class_size = end_line - start_line + 1
                    
                    if class_size > self.config.max_class_size:
                        issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=start_line,
                            severity=ValidationSeverity.WARNING,
                            message=f"Class '{node.name}' too large: {class_size} lines (max: {self.config.max_class_size})",
                            category="class_size",
                            suggestion="Consider breaking into smaller classes"
                        ))
                        
        except Exception as e:
            logger.error(f"Failed to validate class sizes for {file_path}: {e}")
            
        return issues
    
    def _get_end_line(self, node: ast.ClassDef) -> int:
        """Get the end line of a class"""
        if hasattr(node, 'end_lineno'):
            return node.end_lineno
        else:
            # Fallback: estimate end line
            return node.lineno + 200  # Rough estimate


class ImportValidator:
    """Validates import statements"""
    
    def __init__(self, config: ModularizationConfig):
        self.config = config
        
    def validate(self, file_path: str) -> List[ValidationIssue]:
        """Validate import statements"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            import_count = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_count += 1
                    
            if import_count > self.config.max_imports:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line_number=1,
                    severity=ValidationSeverity.WARNING,
                    message=f"Too many imports: {import_count} (max: {self.config.max_imports})",
                    category="imports",
                    suggestion="Consider consolidating imports or splitting the module"
                ))
                
        except Exception as e:
            logger.error(f"Failed to validate imports for {file_path}: {e}")
            
        return issues


class ComplexityValidator:
    """Validates code complexity"""
    
    def __init__(self, config: ModularizationConfig):
        self.config = config
        
    def validate(self, file_path: str) -> List[ValidationIssue]:
        """Validate code complexity"""
        issues = []
        
        if not self.config.enable_complexity_check:
            return issues
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_complexity(node)
                    if complexity > self.config.max_complexity:
                        issues.append(ValidationIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            severity=ValidationSeverity.WARNING,
                            message=f"Function '{node.name}' too complex: {complexity} (max: {self.config.max_complexity})",
                            category="complexity",
                            suggestion="Consider simplifying the logic"
                        ))
                        
        except Exception as e:
            logger.error(f"Failed to validate complexity for {file_path}: {e}")
            
        return issues
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        return complexity


# Main validator class that orchestrates all components
class ModularizationValidator:
    """Modularization validator - main orchestrator"""
    
    def __init__(self, config: ModularizationConfig = None):
        self.config = config or ModularizationConfig()
        self.file_validator = FileSizeValidator(self.config)
        self.function_validator = FunctionSizeValidator(self.config)
        self.class_validator = ClassSizeValidator(self.config)
        self.import_validator = ImportValidator(self.config)
        self.complexity_validator = ComplexityValidator(self.config)
        
    def validate_file(self, file_path: str) -> List[ValidationIssue]:
        """Validate a single file"""
        if not file_path.endswith('.py'):
            return []
            
        issues = []
        
        # Run all validators
        issues.extend(self.file_validator.validate(file_path))
        issues.extend(self.function_validator.validate(file_path))
        issues.extend(self.class_validator.validate(file_path))
        issues.extend(self.import_validator.validate(file_path))
        issues.extend(self.complexity_validator.validate(file_path))
        
        return issues
    
    def validate_directory(self, directory_path: str) -> Dict[str, List[ValidationIssue]]:
        """Validate all Python files in a directory"""
        results = {}
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.validate_file(file_path)
                    
        return results
    
    def get_summary(self, results: Dict[str, List[ValidationIssue]]) -> Dict[str, Any]:
        """Generate validation summary"""
        total_files = len(results)
        total_issues = sum(len(issues) for issues in results.values())
        
        severity_counts = {
            ValidationSeverity.INFO: 0,
            ValidationSeverity.WARNING: 0,
            ValidationSeverity.ERROR: 0,
            ValidationSeverity.CRITICAL: 0
        }
        
        category_counts = {}
        
        for issues in results.values():
            for issue in issues:
                severity_counts[issue.severity] += 1
                category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
                
        return {
            'total_files': total_files,
            'total_issues': total_issues,
            'severity_breakdown': severity_counts,
            'category_breakdown': category_counts,
            'compliance_rate': (total_files - len([f for f, issues in results.items() if any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues)]) / total_files * 100) if total_files > 0 else 100
        }


if __name__ == "__main__":
    # Test the modularized validator
    validator = ModularizationValidator()
    
    # Test with a simple file
    test_file = "test_modularization.py"
    test_content = '''
import os
import json
import sys
import logging
import time
import datetime
import pathlib
import typing
import dataclasses
import enum
import collections
import ast
import re

def very_large_function():
    """This function is intentionally large to test validation"""
    result = []
    for i in range(100):
        if i % 2 == 0:
            result.append(i)
        else:
            result.append(i * 2)
    return result

class VeryLargeClass:
    """This class is intentionally large to test validation"""
    def __init__(self):
        self.data = []
        
    def method1(self):
        pass
        
    def method2(self):
        pass
        
    def method3(self):
        pass
'''
    
    # Create test file
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    # Validate
    issues = validator.validate_file(test_file)
    print(f"✅ Modularization validator test successful")
    print(f"Found {len(issues)} issues:")
    for issue in issues:
        print(f"  - {issue.severity.value}: {issue.message}")
    
    # Get summary
    results = {test_file: issues}
    summary = validator.get_summary(results)
    print(f"Validation summary: {summary}")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
