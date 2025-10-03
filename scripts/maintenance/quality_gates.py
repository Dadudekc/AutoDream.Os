#!/usr/bin/env python3
"""
Quality Gates for Agent Work - Preventing Overcomplexity
========================================================

Automated quality gates to enforce simplicity and prevent overengineering
in agent-generated code. Ensures V2 compliance and maintains code quality.

Author: Agent-4 (Captain & Operations Coordinator)
Date: 2025-09-17
Version: 1.0.0
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QualityLevel(Enum):
    """Quality levels for code assessment."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class QualityMetrics:
    """Quality metrics for a file."""
    file_path: str
    line_count: int
    enum_count: int
    class_count: int
    function_count: int
    max_inheritance_depth: int
    max_function_complexity: int
    max_parameter_count: int
    abc_count: int
    async_function_count: int
    quality_level: QualityLevel
    violations: List[str]
    score: int


class QualityGateChecker:
    """Quality gate checker for Python files."""
    
    def __init__(self):
        self.violations = []
        self.metrics = {}
    
    def check_file(self, file_path: str) -> QualityMetrics:
        """Check a single Python file for quality violations."""
        logger.info(f"Checking quality gates for: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Calculate metrics
            line_count = len(content.splitlines())
            enum_count = self._count_enums(tree)
            class_count = self._count_classes(tree)
            function_count = self._count_functions(tree)
            max_inheritance_depth = self._max_inheritance_depth(tree)
            max_function_complexity = self._max_function_complexity(tree)
            max_parameter_count = self._max_parameter_count(tree)
            abc_count = self._count_abstract_classes(tree)
            async_function_count = self._count_async_functions(tree)
            
            # Check violations
            violations = self._check_violations(
                file_path, line_count, enum_count, class_count, 
                function_count, max_inheritance_depth, max_function_complexity,
                max_parameter_count, abc_count, async_function_count
            )
            
            # Calculate quality level and score
            quality_level, score = self._calculate_quality(
                violations, line_count, enum_count, class_count
            )
            
            return QualityMetrics(
                file_path=file_path,
                line_count=line_count,
                enum_count=enum_count,
                class_count=class_count,
                function_count=function_count,
                max_inheritance_depth=max_inheritance_depth,
                max_function_complexity=max_function_complexity,
                max_parameter_count=max_parameter_count,
                abc_count=abc_count,
                async_function_count=async_function_count,
                quality_level=quality_level,
                violations=violations,
                score=score
            )
            
        except Exception as e:
            logger.error(f"Error checking {file_path}: {e}")
            return QualityMetrics(
                file_path=file_path,
                line_count=0,
                enum_count=0,
                class_count=0,
                function_count=0,
                max_inheritance_depth=0,
                max_function_complexity=0,
                max_parameter_count=0,
                abc_count=0,
                async_function_count=0,
                quality_level=QualityLevel.CRITICAL,
                violations=[f"Error parsing file: {e}"],
                score=0
            )
    
    def _count_enums(self, tree: ast.AST) -> int:
        """Count enum classes in the AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'Enum':
                        count += 1
        return count
    
    def _count_classes(self, tree: ast.AST) -> int:
        """Count class definitions in the AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                count += 1
        return count
    
    def _count_functions(self, tree: ast.AST) -> int:
        """Count function definitions in the AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                count += 1
        return count
    
    def _max_inheritance_depth(self, tree: ast.AST) -> int:
        """Calculate maximum inheritance depth."""
        max_depth = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                depth = len(node.bases)
                max_depth = max(max_depth, depth)
        return max_depth
    
    def _max_function_complexity(self, tree: ast.AST) -> int:
        """Calculate maximum function complexity."""
        max_complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                max_complexity = max(max_complexity, complexity)
        return max_complexity
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                                ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
        return complexity
    
    def _max_parameter_count(self, tree: ast.AST) -> int:
        """Calculate maximum parameter count in functions."""
        max_params = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args)
                max_params = max(max_params, param_count)
        return max_params
    
    def _count_abstract_classes(self, tree: ast.AST) -> int:
        """Count abstract base classes."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'ABC':
                        count += 1
        return count
    
    def _count_async_functions(self, tree: ast.AST) -> int:
        """Count async function definitions."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                if isinstance(node, ast.AsyncFunctionDef):
                    count += 1
        return count
    
    def _check_violations(self, file_path: str, line_count: int, enum_count: int,
                         class_count: int, function_count: int, 
                         max_inheritance_depth: int, max_function_complexity: int,
                         max_parameter_count: int, abc_count: int, 
                         async_function_count: int) -> List[str]:
        """Check for quality violations."""
        violations = []
        
        # File size violations
        if line_count > 400:
            violations.append(f"File size violation: {line_count} lines (limit: 400)")
        
        # Enum violations
        if enum_count > 3:
            violations.append(f"Too many enums: {enum_count} (limit: 3)")
        
        # Class violations
        if class_count > 5:
            violations.append(f"Too many classes: {class_count} (limit: 5)")
        
        # Function violations
        if function_count > 10:
            violations.append(f"Too many functions: {function_count} (limit: 10)")
        
        # Inheritance violations
        if max_inheritance_depth > 2:
            violations.append(f"Too deep inheritance: {max_inheritance_depth} levels (limit: 2)")
        
        # Complexity violations
        if max_function_complexity > 10:
            violations.append(f"Function too complex: {max_function_complexity} (limit: 10)")
        
        # Parameter violations
        if max_parameter_count > 5:
            violations.append(f"Too many parameters: {max_parameter_count} (limit: 5)")
        
        # ABC violations
        if abc_count > 0:
            violations.append(f"Abstract base classes found: {abc_count} (not recommended)")
        
        # Async violations (context-dependent)
        if async_function_count > 0 and "async" not in file_path.lower():
            violations.append(f"Async functions found: {async_function_count} (may be unnecessary)")
        
        return violations
    
    def _calculate_quality(self, violations: List[str], line_count: int, 
                          enum_count: int, class_count: int) -> Tuple[QualityLevel, int]:
        """Calculate quality level and score."""
        if not violations:
            return QualityLevel.EXCELLENT, 100
        
        # Calculate score based on violations
        score = 100
        for violation in violations:
            if "File size violation" in violation:
                score -= 30
            elif "Too many" in violation:
                score -= 15
            elif "Abstract base classes" in violation:
                score -= 10
            elif "Async functions" in violation:
                score -= 5
            else:
                score -= 10
        
        score = max(0, score)
        
        # Determine quality level
        if score >= 90:
            return QualityLevel.EXCELLENT, score
        elif score >= 75:
            return QualityLevel.GOOD, score
        elif score >= 60:
            return QualityLevel.ACCEPTABLE, score
        elif score >= 40:
            return QualityLevel.POOR, score
        else:
            return QualityLevel.CRITICAL, score


def check_project_quality(project_path: str = ".") -> Dict[str, QualityMetrics]:
    """Check quality gates for all Python files in a project."""
    checker = QualityGateChecker()
    results = {}
    
    project_path = Path(project_path)
    
    # Find all Python files
    python_files = list(project_path.rglob("*.py"))
    
    logger.info(f"Found {len(python_files)} Python files to check")
    
    for file_path in python_files:
        # Skip __pycache__ and test files for now
        if "__pycache__" in str(file_path) or "test" in str(file_path):
            continue
        
        relative_path = str(file_path.relative_to(project_path))
        results[relative_path] = checker.check_file(str(file_path))
    
    return results


def generate_quality_report(results: Dict[str, QualityMetrics]) -> str:
    """Generate a quality report from check results."""
    report = []
    report.append("=" * 80)
    report.append("QUALITY GATES REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Summary statistics
    total_files = len(results)
    excellent_files = sum(1 for r in results.values() if r.quality_level == QualityLevel.EXCELLENT)
    good_files = sum(1 for r in results.values() if r.quality_level == QualityLevel.GOOD)
    acceptable_files = sum(1 for r in results.values() if r.quality_level == QualityLevel.ACCEPTABLE)
    poor_files = sum(1 for r in results.values() if r.quality_level == QualityLevel.POOR)
    critical_files = sum(1 for r in results.values() if r.quality_level == QualityLevel.CRITICAL)
    
    report.append(f"Total Files Checked: {total_files}")
    report.append(f"Excellent: {excellent_files}")
    report.append(f"Good: {good_files}")
    report.append(f"Acceptable: {acceptable_files}")
    report.append(f"Poor: {poor_files}")
    report.append(f"Critical: {critical_files}")
    report.append("")
    
    # Files with violations
    violation_files = {path: metrics for path, metrics in results.items() if metrics.violations}
    
    if violation_files:
        report.append("FILES WITH VIOLATIONS:")
        report.append("-" * 40)
        
        for file_path, metrics in violation_files.items():
            report.append(f"\n{file_path} (Score: {metrics.score})")
            report.append(f"  Quality Level: {metrics.quality_level.value.upper()}")
            report.append(f"  Line Count: {metrics.line_count}")
            report.append(f"  Violations:")
            for violation in metrics.violations:
                report.append(f"    - {violation}")
    else:
        report.append("🎉 NO VIOLATIONS FOUND! All files pass quality gates.")
    
    return "\n".join(report)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check quality gates for Python files")
    parser.add_argument("--path", default=".", help="Project path to check")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Check quality
    results = check_project_quality(args.path)
    
    # Generate report
    report = generate_quality_report(results)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Quality report saved to: {args.output}")
    else:
        print(report)
