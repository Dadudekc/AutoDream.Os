"""
Vibe Check - Automated CI/CD gate for design principle enforcement.
Analyzes code for violations of project "vibe" (simplicity, clarity, YAGNI).
"""

import ast
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .design_authority import design_authority, DecisionSeverity


class VibeCheckResult(Enum):
    """Result of vibe check analysis."""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class VibeViolation:
    """Represents a vibe check violation."""
    file_path: str
    line_number: int
    violation_type: str
    description: str
    severity: DecisionSeverity
    suggestion: str
    code_snippet: str = ""


@dataclass
class VibeCheckReport:
    """Comprehensive vibe check report."""
    result: VibeCheckResult
    total_files: int
    violations: List[VibeViolation]
    summary: Dict[str, Any]
    timestamp: str
    agent_author: str = ""


class VibeChecker:
    """
    Automated vibe checker that enforces project design principles.
    
    This tool analyzes code for:
    - Duplication detection
    - Complexity violations
    - Anti-pattern usage
    - Design principle adherence
    """
    
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.violation_thresholds = {
            'complexity_score': 8,  # Max cyclomatic complexity
            'function_length': 30,  # Max lines per function
            'nesting_depth': 3,     # Max nesting levels
            'parameter_count': 5,   # Max function parameters
            'class_length': 100,    # Max lines per class
            'file_length': 300      # Max lines per file
        }
    
    def check_file(self, file_path: str, agent_author: str = "") -> VibeCheckReport:
        """
        Perform vibe check on a single file.
        
        Args:
            file_path: Path to the file to check
            agent_author: Agent that authored the file
            
        Returns:
            VibeCheckReport with violations and recommendations
        """
        violations = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for analysis
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                violations.append(VibeViolation(
                    file_path=file_path,
                    line_number=e.lineno or 0,
                    violation_type="syntax_error",
                    description=f"Syntax error: {e.msg}",
                    severity=DecisionSeverity.ERROR,
                    suggestion="Fix syntax errors before running vibe check"
                ))
                return VibeCheckReport(
                    result=VibeCheckResult.FAIL,
                    total_files=1,
                    violations=violations,
                    summary={'syntax_errors': 1},
                    timestamp=self._get_timestamp(),
                    agent_author=agent_author
                )
            
            # Run various checks
            violations.extend(self._check_complexity(file_path, tree))
            violations.extend(self._check_function_length(file_path, content, tree))
            violations.extend(self._check_nesting_depth(file_path, content, tree))
            violations.extend(self._check_parameter_count(file_path, tree))
            violations.extend(self._check_file_length(file_path, content))
            violations.extend(self._check_duplication(file_path, content))
            violations.extend(self._check_anti_patterns(file_path, content))
            
            # Determine overall result
            error_violations = [v for v in violations if v.severity == DecisionSeverity.ERROR]
            warning_violations = [v for v in violations if v.severity == DecisionSeverity.WARNING]
            
            if error_violations:
                result = VibeCheckResult.FAIL
            elif warning_violations and self.strict_mode:
                result = VibeCheckResult.FAIL
            elif warning_violations:
                result = VibeCheckResult.WARNING
            else:
                result = VibeCheckResult.PASS
            
            # Generate summary
            summary = self._generate_summary(violations)
            
            return VibeCheckReport(
                result=result,
                total_files=1,
                violations=violations,
                summary=summary,
                timestamp=self._get_timestamp(),
                agent_author=agent_author
            )
            
        except Exception as e:
            return VibeCheckReport(
                result=VibeCheckResult.FAIL,
                total_files=1,
                violations=[VibeViolation(
                    file_path=file_path,
                    line_number=0,
                    violation_type="analysis_error",
                    description=f"Failed to analyze file: {str(e)}",
                    severity=DecisionSeverity.ERROR,
                    suggestion="Check file accessibility and format"
                )],
                summary={'analysis_errors': 1},
                timestamp=self._get_timestamp(),
                agent_author=agent_author
            )
    
    def check_directory(self, directory: str, agent_author: str = "", 
                       file_patterns: List[str] = None) -> VibeCheckReport:
        """
        Perform vibe check on all files in a directory.
        
        Args:
            directory: Directory to check
            agent_author: Agent that authored the changes
            file_patterns: File patterns to include (default: ['*.py'])
            
        Returns:
            VibeCheckReport for the entire directory
        """
        if file_patterns is None:
            file_patterns = ['*.py']
        
        all_violations = []
        total_files = 0
        
        for pattern in file_patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    total_files += 1
                    file_report = self.check_file(str(file_path), agent_author)
                    all_violations.extend(file_report.violations)
        
        # Aggregate results
        error_violations = [v for v in all_violations if v.severity == DecisionSeverity.ERROR]
        warning_violations = [v for v in all_violations if v.severity == DecisionSeverity.WARNING]
        
        if error_violations:
            result = VibeCheckResult.FAIL
        elif warning_violations and self.strict_mode:
            result = VibeCheckResult.FAIL
        elif warning_violations:
            result = VibeCheckResult.WARNING
        else:
            result = VibeCheckResult.PASS
        
        summary = self._generate_summary(all_violations)
        summary['total_files_checked'] = total_files
        
        return VibeCheckReport(
            result=result,
            total_files=total_files,
            violations=all_violations,
            summary=summary,
            timestamp=self._get_timestamp(),
            agent_author=agent_author
        )
    
    def _check_complexity(self, file_path: str, tree: ast.AST) -> List[VibeViolation]:
        """Check cyclomatic complexity of functions."""
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > self.violation_thresholds['complexity_score']:
                    violations.append(VibeViolation(
                        file_path=file_path,
                        line_number=node.lineno,
                        violation_type="high_complexity",
                        description=f"Function '{node.name}' has complexity {complexity} (max: {self.violation_thresholds['complexity_score']})",
                        severity=DecisionSeverity.ERROR,
                        suggestion="Break down into smaller functions or simplify logic"
                    ))
        
        return violations
    
    def _check_function_length(self, file_path: str, content: str, tree: ast.AST) -> List[VibeViolation]:
        """Check function length in lines."""
        violations = []
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count lines in function (rough estimate)
                func_start = node.lineno - 1
                func_end = node.end_lineno or func_start + 1
                func_length = func_end - func_start
                
                if func_length > self.violation_thresholds['function_length']:
                    violations.append(VibeViolation(
                        file_path=file_path,
                        line_number=node.lineno,
                        violation_type="long_function",
                        description=f"Function '{node.name}' has {func_length} lines (max: {self.violation_thresholds['function_length']})",
                        severity=DecisionSeverity.ERROR,
                        suggestion="Break into smaller functions",
                        code_snippet=lines[func_start:func_end][:3] if len(lines) > func_start else ""
                    ))
        
        return violations
    
    def _check_nesting_depth(self, file_path: str, content: str, tree: ast.AST) -> List[VibeViolation]:
        """Check maximum nesting depth."""
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                max_depth = self._calculate_nesting_depth(node)
                if max_depth > self.violation_thresholds['nesting_depth']:
                    violations.append(VibeViolation(
                        file_path=file_path,
                        line_number=node.lineno,
                        violation_type="deep_nesting",
                        description=f"{node.__class__.__name__} '{node.name}' has nesting depth {max_depth} (max: {self.violation_thresholds['nesting_depth']})",
                        severity=DecisionSeverity.ERROR,
                        suggestion="Use early returns or extract nested logic"
                    ))
        
        return violations
    
    def _check_parameter_count(self, file_path: str, tree: ast.AST) -> List[VibeViolation]:
        """Check function parameter count."""
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                arg_count = len(node.args.args)
                if arg_count > self.violation_thresholds['parameter_count']:
                    violations.append(VibeViolation(
                        file_path=file_path,
                        line_number=node.lineno,
                        violation_type="too_many_parameters",
                        description=f"Function '{node.name}' has {arg_count} parameters (max: {self.violation_thresholds['parameter_count']})",
                        severity=DecisionSeverity.WARNING,
                        suggestion="Consider using a dataclass or dictionary for parameters"
                    ))
        
        return violations
    
    def _check_file_length(self, file_path: str, content: str) -> List[VibeViolation]:
        """Check total file length."""
        violations = []
        lines = len(content.split('\n'))
        
        if lines > self.violation_thresholds['file_length']:
            violations.append(VibeViolation(
                file_path=file_path,
                line_number=0,
                violation_type="long_file",
                description=f"File has {lines} lines (max: {self.violation_thresholds['file_length']})",
                severity=DecisionSeverity.ERROR,
                suggestion="Split into smaller modules"
            ))
        
        return violations
    
    def _check_duplication(self, file_path: str, content: str) -> List[VibeViolation]:
        """Check for code duplication (simplified version)."""
        violations = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Simple duplication check - look for repeated lines
        line_counts = {}
        for line in lines:
            if len(line) > 20:  # Only check substantial lines
                line_counts[line] = line_counts.get(line, 0) + 1
        
        for line, count in line_counts.items():
            if count > 3:  # Same line appears more than 3 times
                violations.append(VibeViolation(
                    file_path=file_path,
                    line_number=0,  # Can't pinpoint exact line easily
                    violation_type="duplication",
                    description=f"Line appears {count} times: '{line[:50]}...'",
                    severity=DecisionSeverity.WARNING,
                    suggestion="Extract into a function or constant"
                ))
        
        return violations
    
    def _check_anti_patterns(self, file_path: str, content: str) -> List[VibeViolation]:
        """Check for common anti-patterns."""
        violations = []
        content_lower = content.lower()
        
        anti_patterns = {
            'bare_except': (r'except\s*:', 'Use specific exception types'),
            'global_vars': (r'global\s+\w+', 'Avoid global variables'),
            'deep_copy': (r'copy\.deepcopy', 'Consider if deep copy is necessary'),
            'eval_usage': (r'\beval\s*\(', 'Avoid eval() for security'),
            'exec_usage': (r'\bexec\s*\(', 'Avoid exec() for security'),
            'complex_list_comp': (r'\[.*for.*for.*\]', 'Simplify nested list comprehensions')
        }
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern_name, (pattern, suggestion) in anti_patterns.items():
                if pattern in line.lower():
                    violations.append(VibeViolation(
                        file_path=file_path,
                        line_number=i,
                        violation_type=f"anti_pattern_{pattern_name}",
                        description=f"Anti-pattern detected: {pattern_name}",
                        severity=DecisionSeverity.WARNING,
                        suggestion=suggestion,
                        code_snippet=line.strip()
                    ))
        
        return violations
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth in a function or class."""
        max_depth = 0
        current_depth = 0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                # Reset depth for nested functions/classes
                current_depth = 0
        
        return max_depth
    
    def _generate_summary(self, violations: List[VibeViolation]) -> Dict[str, Any]:
        """Generate summary statistics from violations."""
        summary = {
            'total_violations': len(violations),
            'error_count': len([v for v in violations if v.severity == DecisionSeverity.ERROR]),
            'warning_count': len([v for v in violations if v.severity == DecisionSeverity.WARNING]),
            'violation_types': {}
        }
        
        for violation in violations:
            violation_type = violation.violation_type
            summary['violation_types'][violation_type] = summary['violation_types'].get(violation_type, 0) + 1
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run_pre_commit_check(self, staged_files: List[str], agent_author: str = "") -> VibeCheckReport:
        """Run vibe check on staged files for pre-commit hook."""
        all_violations = []
        total_files = len(staged_files)
        
        for file_path in staged_files:
            if file_path.endswith('.py'):
                file_report = self.check_file(file_path, agent_author)
                all_violations.extend(file_report.violations)
        
        # Determine result
        error_violations = [v for v in all_violations if v.severity == DecisionSeverity.ERROR]
        
        result = VibeCheckResult.FAIL if error_violations else VibeCheckResult.PASS
        
        summary = self._generate_summary(all_violations)
        summary['staged_files_checked'] = total_files
        
        return VibeCheckReport(
            result=result,
            total_files=total_files,
            violations=all_violations,
            summary=summary,
            timestamp=self._get_timestamp(),
            agent_author=agent_author
        )


def vibe_check_file(file_path: str, agent_author: str = "", strict: bool = True) -> VibeCheckReport:
    """Run vibe check on a single file."""
    checker = VibeChecker(strict_mode=strict)
    return checker.check_file(file_path, agent_author)


def vibe_check_directory(directory: str, agent_author: str = "", strict: bool = True) -> VibeCheckReport:
    """Run vibe check on a directory."""
    checker = VibeChecker(strict_mode=strict)
    return checker.check_directory(directory, agent_author)


def vibe_check_strict(file_paths: List[str], agent_author: str = "") -> VibeCheckReport:
    """Run strict vibe check (fails on warnings)."""
    checker = VibeChecker(strict_mode=True)
    all_violations = []
    
    for file_path in file_paths:
        if file_path.endswith('.py'):
            file_report = checker.check_file(file_path, agent_author)
            all_violations.extend(file_report.violations)
    
    error_violations = [v for v in all_violations if v.severity == DecisionSeverity.ERROR]
    warning_violations = [v for v in all_violations if v.severity == DecisionSeverity.WARNING]
    
    result = VibeCheckResult.FAIL if (error_violations or warning_violations) else VibeCheckResult.PASS
    
    summary = checker._generate_summary(all_violations)
    
    return VibeCheckReport(
        result=result,
        total_files=len(file_paths),
        violations=all_violations,
        summary=summary,
        timestamp=checker._get_timestamp(),
        agent_author=agent_author
    )


def main():
    """CLI entry point for vibe check."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run vibe check on code')
    parser.add_argument('path', help='File or directory to check')
    parser.add_argument('--agent', default='', help='Agent author for attribution')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        report = vibe_check_file(args.path, args.agent, args.strict)
    else:
        report = vibe_check_directory(args.path, args.agent, args.strict)
    
    if args.format == 'json':
        import json
        print(json.dumps({
            'result': report.result.value,
            'total_files': report.total_files,
            'violations': [
                {
                    'file': v.file_path,
                    'line': v.line_number,
                    'type': v.violation_type,
                    'description': v.description,
                    'severity': v.severity.value,
                    'suggestion': v.suggestion
                } for v in report.violations
            ],
            'summary': report.summary,
            'timestamp': report.timestamp
        }, indent=2))
    else:
        # Text output
        print(f"🎯 Vibe Check Results: {report.result.value.upper()}")
        print(f"📁 Files checked: {report.total_files}")
        print(f"🚨 Violations: {len(report.violations)}")
        
        if report.violations:
            print("\n🚨 Issues found:")
            for violation in report.violations:
                severity_icon = "❌" if violation.severity == DecisionSeverity.ERROR else "⚠️"
                print(f"{severity_icon} {violation.file_path}:{violation.line_number}")
                print(f"   {violation.description}")
                print(f"   💡 {violation.suggestion}")
                print()
        
        if report.result == VibeCheckResult.FAIL:
            sys.exit(1)


if __name__ == '__main__':
    main()