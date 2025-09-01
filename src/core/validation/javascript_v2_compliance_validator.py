#!/usr/bin/env python3
"""
JavaScript V2 Compliance Validator - Agent Cellphone V2
======================================================

Specialized validator for JavaScript V2 compliance validation.
Provides comprehensive validation for modular architecture patterns, performance optimization,
and V2 compliance standards specific to JavaScript/web development components.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import re
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationIssue, ValidationSeverity


class JavaScriptComplianceRule(Enum):
    """JavaScript V2 compliance rules."""
    MODULE_STRUCTURE = "module_structure"
    LINE_COUNT_LIMIT = "line_count_limit"
    FUNCTION_SIZE_LIMIT = "function_size_limit"
    DEPENDENCY_INJECTION = "dependency_injection"
    SINGLE_RESPONSIBILITY = "single_responsibility"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ERROR_HANDLING = "error_handling"
    DOCUMENTATION = "documentation"


@dataclass
class JavaScriptFileMetrics:
    """Metrics for JavaScript file analysis."""
    file_path: str
    total_lines: int
    function_count: int
    class_count: int
    import_count: int
    export_count: int
    comment_lines: int
    complexity_score: float
    v2_compliant: bool
    violations: List[str] = field(default_factory=list)


class JavaScriptV2ComplianceValidator:
    """
    JavaScript V2 compliance validator for web development components.
    
    Provides comprehensive validation for:
    - Modular architecture compliance
    - Line count and function size limits
    - Dependency injection patterns
    - Performance optimization validation
    - Error handling compliance
    - Documentation requirements
    """

    def __init__(self):
        """Initialize the JavaScript V2 compliance validator."""
        self.compliance_thresholds = {
            "max_file_lines": 300,  # V2 line limit
            "max_function_lines": 50,  # Function size limit
            "max_class_lines": 100,  # Class size limit
            "min_comment_ratio": 0.1,  # 10% minimum comments
            "max_complexity": 10,  # Cyclomatic complexity limit
        }
        
        self.violation_patterns = {
            "large_functions": re.compile(r'function\s+\w+.*?\{[^}]{200,}\}', re.DOTALL),
            "deep_nesting": re.compile(r'(\{.*?){4,}', re.DOTALL),
            "long_chains": re.compile(r'\.\w+\(\)\.\w+\(\)\.\w+\(\)\.\w+\(\)'),
            "global_variables": re.compile(r'var\s+\w+\s*=\s*[^;]+;'),
            "missing_error_handling": re.compile(r'(async\s+)?function.*?\{[^}]*\}(?!\s*catch)'),
        }

    def validate_javascript_file(self, file_path: str) -> List[ValidationIssue]:
        """
        Validate a JavaScript file for V2 compliance.
        
        Args:
            file_path: Path to the JavaScript file
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Read and analyze file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metrics = self._analyze_file_metrics(file_path, content)
            
            # Validate against V2 compliance rules
            issues.extend(self._validate_line_count(metrics))
            issues.extend(self._validate_module_structure(metrics, content))
            issues.extend(self._validate_function_sizes(metrics, content))
            issues.extend(self._validate_dependency_injection(metrics, content))
            issues.extend(self._validate_performance_patterns(metrics, content))
            issues.extend(self._validate_error_handling(metrics, content))
            issues.extend(self._validate_documentation(metrics, content))
            
        except Exception as e:
            issues.append(ValidationIssue(
                rule_id="file_analysis_error",
                rule_name="File Analysis Error",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to analyze file {file_path}: {str(e)}",
                details={"file_path": file_path, "error": str(e)},
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        return issues

    def _analyze_file_metrics(self, file_path: str, content: str) -> JavaScriptFileMetrics:
        """Analyze JavaScript file and extract metrics."""
        lines = content.split('\n')
        total_lines = len(lines)
        
        # Count various elements
        function_count = len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*\(.*?\)\s*=>', content))
        class_count = len(re.findall(r'class\s+\w+', content))
        import_count = len(re.findall(r'import\s+.*?from', content))
        export_count = len(re.findall(r'export\s+', content))
        comment_lines = len([line for line in lines if line.strip().startswith('//') or line.strip().startswith('/*')])
        
        # Calculate complexity score (simplified)
        complexity_score = self._calculate_complexity(content)
        
        return JavaScriptFileMetrics(
            file_path=file_path,
            total_lines=total_lines,
            function_count=function_count,
            class_count=class_count,
            import_count=import_count,
            export_count=export_count,
            comment_lines=comment_lines,
            complexity_score=complexity_score,
            v2_compliant=True  # Will be updated based on validation
        )

    def _calculate_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity score."""
        complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'catch', '&&', '||', '?']
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        return complexity

    def _validate_line_count(self, metrics: JavaScriptFileMetrics) -> List[ValidationIssue]:
        """Validate file line count against V2 limits."""
        issues = []
        
        if metrics.total_lines > self.compliance_thresholds["max_file_lines"]:
            issues.append(ValidationIssue(
                rule_id="line_count_exceeded",
                rule_name="Line Count Exceeded",
                severity=ValidationSeverity.ERROR,
                message=f"File exceeds V2 line limit: {metrics.total_lines} > {self.compliance_thresholds['max_file_lines']}",
                details={
                    "file_path": metrics.file_path,
                    "current_lines": metrics.total_lines,
                    "limit": self.compliance_thresholds["max_file_lines"],
                    "excess": metrics.total_lines - self.compliance_thresholds["max_file_lines"]
                },
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
            metrics.v2_compliant = False
        
        return issues

    def _validate_module_structure(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate ES6 module structure compliance."""
        issues = []
        
        # Check for proper import/export structure
        if metrics.import_count == 0 and metrics.export_count == 0:
            issues.append(ValidationIssue(
                rule_id="missing_module_structure",
                rule_name="Missing Module Structure",
                severity=ValidationSeverity.WARNING,
                message="File lacks ES6 module structure (imports/exports)",
                details={
                    "file_path": metrics.file_path,
                    "import_count": metrics.import_count,
                    "export_count": metrics.export_count
                },
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        # Check for default exports
        if metrics.export_count > 0 and not re.search(r'export\s+default', content):
            issues.append(ValidationIssue(
                rule_id="missing_default_export",
                rule_name="Missing Default Export",
                severity=ValidationSeverity.WARNING,
                message="Module exports found but no default export",
                details={"file_path": metrics.file_path},
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        return issues

    def _validate_function_sizes(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate function sizes against limits."""
        issues = []
        
        # Find large functions
        large_functions = self.violation_patterns["large_functions"].findall(content)
        
        for i, func in enumerate(large_functions):
            func_lines = len(func.split('\n'))
            if func_lines > self.compliance_thresholds["max_function_lines"]:
                issues.append(ValidationIssue(
                    rule_id="function_too_large",
                    rule_name="Function Too Large",
                    severity=ValidationSeverity.WARNING,
                    message=f"Function {i+1} exceeds size limit: {func_lines} > {self.compliance_thresholds['max_function_lines']}",
                    details={
                        "file_path": metrics.file_path,
                        "function_index": i+1,
                        "current_lines": func_lines,
                        "limit": self.compliance_thresholds["max_function_lines"]
                    },
                    timestamp=datetime.now(),
                    component="javascript_validator"
                ))
        
        return issues

    def _validate_dependency_injection(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate dependency injection patterns."""
        issues = []
        
        # Check for constructor dependency injection
        class_pattern = re.compile(r'class\s+\w+.*?constructor\s*\([^)]*\)', re.DOTALL)
        classes = class_pattern.findall(content)
        
        for i, class_def in enumerate(classes):
            # Check if constructor has parameters (dependency injection)
            constructor_match = re.search(r'constructor\s*\(([^)]*)\)', class_def)
            if constructor_match:
                params = constructor_match.group(1).strip()
                if not params:
                    issues.append(ValidationIssue(
                        rule_id="missing_dependency_injection",
                        rule_name="Missing Dependency Injection",
                        severity=ValidationSeverity.INFO,
                        message=f"Class {i+1} constructor lacks dependency injection parameters",
                        details={
                            "file_path": metrics.file_path,
                            "class_index": i+1
                        },
                        timestamp=datetime.now(),
                        component="javascript_validator"
                    ))
        
        return issues

    def _validate_performance_patterns(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate performance optimization patterns."""
        issues = []
        
        # Check for performance anti-patterns
        if self.violation_patterns["deep_nesting"].search(content):
            issues.append(ValidationIssue(
                rule_id="deep_nesting_detected",
                rule_name="Deep Nesting Detected",
                severity=ValidationSeverity.WARNING,
                message="Code contains deep nesting which may impact performance",
                details={"file_path": metrics.file_path},
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        if self.violation_patterns["long_chains"].search(content):
            issues.append(ValidationIssue(
                rule_id="long_method_chains",
                rule_name="Long Method Chains",
                severity=ValidationSeverity.WARNING,
                message="Code contains long method chains which may impact readability",
                details={"file_path": metrics.file_path},
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        # Check complexity
        if metrics.complexity_score > self.compliance_thresholds["max_complexity"]:
            issues.append(ValidationIssue(
                rule_id="high_complexity",
                rule_name="High Complexity",
                severity=ValidationSeverity.WARNING,
                message=f"File complexity exceeds limit: {metrics.complexity_score} > {self.compliance_thresholds['max_complexity']}",
                details={
                    "file_path": metrics.file_path,
                    "complexity_score": metrics.complexity_score,
                    "limit": self.compliance_thresholds["max_complexity"]
                },
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        return issues

    def _validate_error_handling(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate error handling patterns."""
        issues = []
        
        # Check for async functions without error handling
        async_functions = re.findall(r'async\s+function\s+\w+.*?\{[^}]*\}', content, re.DOTALL)
        
        for i, func in enumerate(async_functions):
            if not re.search(r'try\s*\{|catch\s*\(', func):
                issues.append(ValidationIssue(
                    rule_id="missing_error_handling",
                    rule_name="Missing Error Handling",
                    severity=ValidationSeverity.WARNING,
                    message=f"Async function {i+1} lacks error handling (try/catch)",
                    details={
                        "file_path": metrics.file_path,
                        "function_index": i+1
                    },
                    timestamp=datetime.now(),
                    component="javascript_validator"
                ))
        
        return issues

    def _validate_documentation(self, metrics: JavaScriptFileMetrics, content: str) -> List[ValidationIssue]:
        """Validate documentation requirements."""
        issues = []
        
        # Check comment ratio
        comment_ratio = metrics.comment_lines / metrics.total_lines if metrics.total_lines > 0 else 0
        
        if comment_ratio < self.compliance_thresholds["min_comment_ratio"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_documentation",
                rule_name="Insufficient Documentation",
                severity=ValidationSeverity.INFO,
                message=f"Comment ratio below minimum: {comment_ratio:.2%} < {self.compliance_thresholds['min_comment_ratio']:.2%}",
                details={
                    "file_path": metrics.file_path,
                    "comment_ratio": comment_ratio,
                    "comment_lines": metrics.comment_lines,
                    "total_lines": metrics.total_lines,
                    "minimum_ratio": self.compliance_thresholds["min_comment_ratio"]
                },
                timestamp=datetime.now(),
                component="javascript_validator"
            ))
        
        # Check for JSDoc comments on exported functions
        exported_functions = re.findall(r'export\s+(?:async\s+)?function\s+(\w+)', content)
        
        for func_name in exported_functions:
            # Look for JSDoc comment before the function
            func_pattern = rf'export\s+(?:async\s+)?function\s+{func_name}'
            func_match = re.search(func_pattern, content)
            
            if func_match:
                # Check if there's a JSDoc comment before this function
                before_func = content[:func_match.start()]
                if not re.search(r'/\*\*.*?\*/', before_func, re.DOTALL):
                    issues.append(ValidationIssue(
                        rule_id="missing_jsdoc",
                        rule_name="Missing JSDoc",
                        severity=ValidationSeverity.INFO,
                        message=f"Exported function '{func_name}' lacks JSDoc documentation",
                        details={
                            "file_path": metrics.file_path,
                            "function_name": func_name
                        },
                        timestamp=datetime.now(),
                        component="javascript_validator"
                    ))
        
        return issues

    def validate_multiple_files(self, file_paths: List[str]) -> Dict[str, List[ValidationIssue]]:
        """Validate multiple JavaScript files."""
        results = {}
        
        for file_path in file_paths:
            if os.path.exists(file_path) and file_path.endswith('.js'):
                results[file_path] = self.validate_javascript_file(file_path)
            else:
                results[file_path] = [ValidationIssue(
                    rule_id="file_not_found",
                    rule_name="File Not Found",
                    severity=ValidationSeverity.ERROR,
                    message=f"File not found or not a JavaScript file: {file_path}",
                    details={"file_path": file_path},
                    timestamp=datetime.now(),
                    component="javascript_validator"
                )]
        
        return results

    def generate_compliance_report(self, validation_results: Dict[str, List[ValidationIssue]]) -> Dict[str, Any]:
        """Generate comprehensive compliance report."""
        total_files = len(validation_results)
        compliant_files = 0
        total_issues = 0
        issue_summary = {
            "error": 0,
            "warning": 0,
            "info": 0
        }
        
        file_summaries = []
        
        for file_path, issues in validation_results.items():
            file_compliant = len(issues) == 0
            if file_compliant:
                compliant_files += 1
            
            total_issues += len(issues)
            
            # Count issues by severity
            for issue in issues:
                if issue.severity == ValidationSeverity.ERROR:
                    issue_summary["error"] += 1
                elif issue.severity == ValidationSeverity.WARNING:
                    issue_summary["warning"] += 1
                else:
                    issue_summary["info"] += 1
            
            file_summaries.append({
                "file_path": file_path,
                "compliant": file_compliant,
                "issue_count": len(issues),
                "issues": [
                    {
                        "rule_id": issue.rule_id,
                        "rule_name": issue.rule_name,
                        "severity": issue.severity.value,
                        "message": issue.message
                    }
                    for issue in issues
                ]
            })
        
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": total_files,
                "compliant_files": compliant_files,
                "compliance_rate": round(compliance_rate, 2),
                "total_issues": total_issues,
                "issue_breakdown": issue_summary
            },
            "file_details": file_summaries,
            "recommendations": self._generate_recommendations(issue_summary, compliance_rate)
        }

    def _generate_recommendations(self, issue_summary: Dict[str, int], compliance_rate: float) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if compliance_rate < 80:
            recommendations.append("Focus on achieving 80%+ compliance rate across all JavaScript files")
        
        if issue_summary["error"] > 0:
            recommendations.append("Address all ERROR level issues immediately - these violate V2 compliance")
        
        if issue_summary["warning"] > 5:
            recommendations.append("Review and address WARNING level issues to improve code quality")
        
        if issue_summary["info"] > 10:
            recommendations.append("Consider improving documentation and code structure based on INFO level suggestions")
        
        recommendations.append("Implement automated validation in CI/CD pipeline to maintain V2 compliance")
        recommendations.append("Consider refactoring large files into smaller, focused modules")
        
        return recommendations
