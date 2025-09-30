"""
Quality Gates Core - V2 Compliant
=================================

Core quality gates functionality separated for V2 compliance.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import ast
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

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
    violations: list[str]
    score: int


class QualityGateChecker:
    """Core quality gate checker functionality."""
    
    def __init__(self):
        """Initialize quality gate checker."""
        self.violations = []
    
    def check_file(self, file_path: str) -> QualityMetrics:
        """Check a single file for quality violations."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            metrics = self._analyze_file(file_path, tree, content)
            return metrics
        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            return self._create_error_metrics(file_path)
    
    def _analyze_file(self, file_path: str, tree: ast.AST, content: str) -> QualityMetrics:
        """Analyze file and return quality metrics."""
        lines = content.split('\n')
        line_count = len(lines)
        
        # Count various elements
        enum_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and self._is_enum(n)])
        class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        function_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        
        # Calculate complexity metrics
        max_inheritance_depth = self._calculate_max_inheritance_depth(tree)
        max_function_complexity = self._calculate_max_function_complexity(tree)
        max_parameter_count = self._calculate_max_parameter_count(tree)
        abc_count = self._count_abstract_classes(tree)
        async_function_count = self._count_async_functions(tree)
        
        # Check violations
        violations = self._check_violations(file_path, line_count, enum_count, class_count, 
                                          function_count, max_inheritance_depth, 
                                          max_function_complexity, max_parameter_count, 
                                          abc_count, async_function_count)
        
        # Calculate quality score
        score = self._calculate_quality_score(violations, line_count, class_count, function_count)
        quality_level = self._determine_quality_level(score)
        
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
    
    def _is_enum(self, node: ast.ClassDef) -> bool:
        """Check if class is an enum."""
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in ['Enum', 'IntEnum', 'Flag']:
                return True
        return False
    
    def _calculate_max_inheritance_depth(self, tree: ast.AST) -> int:
        """Calculate maximum inheritance depth."""
        max_depth = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                depth = self._get_inheritance_depth(node)
                max_depth = max(max_depth, depth)
        return max_depth
    
    def _get_inheritance_depth(self, node: ast.ClassDef, visited: set = None) -> int:
        """Get inheritance depth for a class."""
        if visited is None:
            visited = set()
        
        if node in visited:
            return 0
        
        visited.add(node)
        max_depth = 0
        
        for base in node.bases:
            if isinstance(base, ast.Name):
                # This is a simplified check - in practice, you'd need to resolve the base class
                max_depth = max(max_depth, 1)
        
        return max_depth
    
    def _calculate_max_function_complexity(self, tree: ast.AST) -> int:
        """Calculate maximum function complexity."""
        max_complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                max_complexity = max(max_complexity, complexity)
        return max_complexity
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_max_parameter_count(self, tree: ast.AST) -> int:
        """Calculate maximum parameter count."""
        max_params = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args) + len(node.args.kwonlyargs)
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
        """Count async functions."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith)):
                count += 1
        return count
    
    def _check_violations(self, file_path: str, line_count: int, enum_count: int, 
                         class_count: int, function_count: int, max_inheritance_depth: int,
                         max_function_complexity: int, max_parameter_count: int,
                         abc_count: int, async_function_count: int) -> list[str]:
        """Check for V2 compliance violations."""
        violations = []
        
        # File size check
        if line_count > 400:
            violations.append(f"File size violation: {line_count} lines (limit: 400)")
        
        # Enum count check
        if enum_count > 3:
            violations.append(f"Too many enums: {enum_count} (limit: 3)")
        
        # Class count check
        if class_count > 5:
            violations.append(f"Too many classes: {class_count} (limit: 5)")
        
        # Function count check
        if function_count > 10:
            violations.append(f"Too many functions: {function_count} (limit: 10)")
        
        # Inheritance depth check
        if max_inheritance_depth > 2:
            violations.append(f"Too many inheritance levels: {max_inheritance_depth} (limit: 2)")
        
        # Function complexity check
        if max_function_complexity > 10:
            violations.append(f"Function too complex: {max_function_complexity} (limit: 10)")
        
        # Parameter count check
        if max_parameter_count > 5:
            violations.append(f"Too many parameters: {max_parameter_count} (limit: 5)")
        
        # Abstract class check
        if abc_count > 0:
            violations.append(f"Abstract base classes found: {abc_count} (not recommended)")
        
        # Async function check
        if async_function_count > 0:
            violations.append(f"Async functions found: {async_function_count} (may be unnecessary)")
        
        return violations
    
    def _calculate_quality_score(self, violations: list[str], line_count: int, 
                                class_count: int, function_count: int) -> int:
        """Calculate quality score based on violations."""
        base_score = 100
        
        # Deduct points for violations
        for violation in violations:
            if "File size violation" in violation:
                base_score -= 20
            elif "Too many classes" in violation:
                base_score -= 15
            elif "Too many functions" in violation:
                base_score -= 10
            elif "Function too complex" in violation:
                base_score -= 10
            elif "Too many parameters" in violation:
                base_score -= 5
            elif "Abstract base classes" in violation:
                base_score -= 5
            elif "Async functions" in violation:
                base_score -= 2
        
        return max(0, base_score)
    
    def _determine_quality_level(self, score: int) -> QualityLevel:
        """Determine quality level based on score."""
        if score >= 95:
            return QualityLevel.EXCELLENT
        elif score >= 75:
            return QualityLevel.GOOD
        elif score >= 60:
            return QualityLevel.ACCEPTABLE
        elif score >= 40:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL
    
    def _create_error_metrics(self, file_path: str) -> QualityMetrics:
        """Create error metrics for failed file analysis."""
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
            violations=["Analysis failed"],
            score=0
        )
