"""
Complexity Analyzer Core - Main Analysis Logic
==============================================
Core complexity analysis engine with AST visitors and metrics.
Extracted for V2 compliance.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored: Agent-5 (V2 compliance)
License: MIT
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ComplexityMetrics:
    """Complexity metrics for a code entity."""
    entity_name: str
    entity_type: str  # "function", "method", "class"
    cyclomatic: int
    cognitive: int
    nesting_depth: int
    line_count: int
    start_line: int
    end_line: int


@dataclass
class ComplexityViolation:
    """Represents a complexity violation."""
    file_path: str
    entity_name: str
    entity_type: str
    violation_type: str  # "CYCLOMATIC", "COGNITIVE", "NESTING"
    current_value: int
    threshold: int
    line_number: int
    severity: str  # "HIGH", "MEDIUM", "LOW"
    suggestion: str


@dataclass
class ComplexityReport:
    """Complexity analysis report."""
    file_path: str
    total_functions: int
    avg_cyclomatic: float
    avg_cognitive: float
    max_nesting: int
    violations: List[ComplexityViolation]
    metrics: List[ComplexityMetrics]

    @property
    def has_violations(self) -> bool:
        """Check if report has violations."""
        return len(self.violations) > 0


class CyclomaticComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate cyclomatic complexity."""

    def __init__(self):
        """Initialize complexity counter."""
        self.complexity = 1  # Start at 1 (base path)
        self.nesting_level = 0
        self.max_nesting = 0

    def visit_If(self, node):
        """Count if statements."""
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_While(self, node):
        """Count while loops."""
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_For(self, node):
        """Count for loops."""
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_ExceptHandler(self, node):
        """Count except handlers."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        """Count with statements."""
        self.complexity += 1
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_BoolOp(self, node):
        """Count boolean operators (and, or)."""
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        """Count comprehensions."""
        self.complexity += 1
        for if_clause in node.ifs:
            self.complexity += 1
        self.generic_visit(node)


class CognitiveComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate cognitive complexity."""

    def __init__(self):
        """Initialize cognitive complexity counter."""
        self.complexity = 0
        self.nesting_level = 0
        self.in_logical_sequence = False

    def visit_If(self, node):
        """Count if statements with nesting penalty."""
        self.complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_While(self, node):
        """Count while loops with nesting penalty."""
        self.complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_For(self, node):
        """Count for loops with nesting penalty."""
        self.complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_ExceptHandler(self, node):
        """Count except handlers with nesting penalty."""
        self.complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1

    def visit_BoolOp(self, node):
        """Count boolean operators."""
        if not self.in_logical_sequence:
            self.complexity += 1
        self.in_logical_sequence = True
        self.generic_visit(node)
        self.in_logical_sequence = False

    def visit_Continue(self, node):
        """Count continue statements."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_Break(self, node):
        """Count break statements."""
        self.complexity += 1
        self.generic_visit(node)


class ComplexityAnalyzer:
    """Analyzes code complexity using AST."""
    CYCLOMATIC_THRESHOLD = 10
    COGNITIVE_THRESHOLD = 15
    NESTING_THRESHOLD = 4

    def __init__(self):
        """Initialize complexity analyzer."""
        pass

    def analyze_file(self, file_path: str) -> Optional[ComplexityReport]:
        """Analyze file for complexity metrics."""
        path = Path(file_path)
        if not path.exists():
            return None
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(path))
            metrics = []
            violations = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metric = self._analyze_function(node, file_path, content)
                    if metric:
                        metrics.append(metric)
                        violations.extend(self._check_violations(metric, file_path))
            avg_cyclomatic = sum(m.cyclomatic for m in metrics) / len(metrics) if metrics else 0
            avg_cognitive = sum(m.cognitive for m in metrics) / len(metrics) if metrics else 0
            max_nesting = max((m.nesting_depth for m in metrics), default=0)
            return ComplexityReport(
                file_path=file_path,
                total_functions=len(metrics),
                avg_cyclomatic=round(avg_cyclomatic, 1),
                avg_cognitive=round(avg_cognitive, 1),
                max_nesting=max_nesting,
                violations=violations,
                metrics=metrics,
            )
        except (SyntaxError, Exception) as e:
            return None

    def _analyze_function(
        self, node: ast.FunctionDef, file_path: str, content: str
    ) -> Optional[ComplexityMetrics]:
        """Analyze complexity of a single function."""
        try:
            cyclomatic_visitor = CyclomaticComplexityVisitor()
            cyclomatic_visitor.visit(node)
            cognitive_visitor = CognitiveComplexityVisitor()
            cognitive_visitor.visit(node)
            end_line = node.end_lineno if hasattr(node, "end_lineno") else node.lineno
            line_count = end_line - node.lineno + 1
            entity_type = "method" if node.col_offset > 0 else "function"
            return ComplexityMetrics(
                entity_name=node.name,
                entity_type=entity_type,
                cyclomatic=cyclomatic_visitor.complexity,
                cognitive=cognitive_visitor.complexity,
                nesting_depth=cyclomatic_visitor.max_nesting,
                line_count=line_count,
                start_line=node.lineno,
                end_line=end_line,
            )
        except Exception:
            return None

    def _check_violations(
        self, metric: ComplexityMetrics, file_path: str
    ) -> List[ComplexityViolation]:
        """Check for complexity violations."""
        violations = []
        if metric.cyclomatic > self.CYCLOMATIC_THRESHOLD:
            violations.append(ComplexityViolation(
                file_path=file_path, entity_name=metric.entity_name,
                entity_type=metric.entity_type, violation_type="CYCLOMATIC",
                current_value=metric.cyclomatic, threshold=self.CYCLOMATIC_THRESHOLD,
                line_number=metric.start_line,
                severity=self._get_severity(metric.cyclomatic, self.CYCLOMATIC_THRESHOLD),
                suggestion=self._get_cyclomatic_suggestion(metric),
            ))
        if metric.cognitive > self.COGNITIVE_THRESHOLD:
            violations.append(ComplexityViolation(
                file_path=file_path, entity_name=metric.entity_name,
                entity_type=metric.entity_type, violation_type="COGNITIVE",
                current_value=metric.cognitive, threshold=self.COGNITIVE_THRESHOLD,
                line_number=metric.start_line,
                severity=self._get_severity(metric.cognitive, self.COGNITIVE_THRESHOLD),
                suggestion=self._get_cognitive_suggestion(metric),
            ))
        if metric.nesting_depth > self.NESTING_THRESHOLD:
            violations.append(ComplexityViolation(
                file_path=file_path, entity_name=metric.entity_name,
                entity_type=metric.entity_type, violation_type="NESTING",
                current_value=metric.nesting_depth, threshold=self.NESTING_THRESHOLD,
                line_number=metric.start_line,
                severity=self._get_severity(metric.nesting_depth, self.NESTING_THRESHOLD),
                suggestion=self._get_nesting_suggestion(metric),
            ))
        return violations

    def _get_severity(self, value: int, threshold: int) -> str:
        """Determine severity based on how much threshold is exceeded."""
        ratio = value / threshold
        if ratio >= 2.0:
            return "HIGH"
        elif ratio >= 1.5:
            return "MEDIUM"
        else:
            return "LOW"

    def _get_cyclomatic_suggestion(self, metric: ComplexityMetrics) -> str:
        """Get suggestion for reducing cyclomatic complexity."""
        return f"""Function '{metric.entity_name}' has cyclomatic complexity of {metric.cyclomatic} (threshold: {self.CYCLOMATIC_THRESHOLD})
Suggestions to reduce complexity:
  1. Extract conditional logic into separate helper functions
  2. Use early returns to reduce nested conditions
  3. Replace complex if-elif chains with dictionaries or strategy pattern
  4. Consider extracting loop bodies into helper functions"""

    def _get_cognitive_suggestion(self, metric: ComplexityMetrics) -> str:
        """Get suggestion for reducing cognitive complexity."""
        return f"""Function '{metric.entity_name}' has cognitive complexity of {metric.cognitive} (threshold: {self.COGNITIVE_THRESHOLD})
Suggestions to improve readability:
  1. Reduce nesting levels (current max: {metric.nesting_depth})
  2. Extract nested logic into well-named helper functions
  3. Use guard clauses (early returns) to reduce indentation
  4. Simplify boolean expressions"""

    def _get_nesting_suggestion(self, metric: ComplexityMetrics) -> str:
        """Get suggestion for reducing nesting depth."""
        return f"""Function '{metric.entity_name}' has nesting depth of {metric.nesting_depth} (threshold: {self.NESTING_THRESHOLD})
Suggestions to reduce nesting:
  1. Use early returns/continues to avoid deep nesting
  2. Extract inner loops into separate functions
  3. Replace nested conditions with boolean expressions
  4. Use guard clauses at function start"""


class ComplexityAnalysisService:
    """Service for complexity analysis operations."""

    def __init__(self):
        """Initialize complexity analysis service."""
        self.analyzer = ComplexityAnalyzer()

    def analyze_file(self, file_path: str, verbose: bool = False) -> Optional[str]:
        """Analyze single file and return formatted report."""
        try:
            from .complexity_analyzer_formatters import format_report
        except ImportError:
            from complexity_analyzer_formatters import format_report
        report = self.analyzer.analyze_file(file_path)
        if not report:
            return None
        return format_report(report, verbose)

    def analyze_directory(
        self, directory: str, pattern: str = "**/*.py", verbose: bool = False
    ) -> List[ComplexityReport]:
        """Analyze all files in directory."""
        reports = []
        dir_path = Path(directory)
        for file_path in dir_path.glob(pattern):
            if self._should_skip_file(file_path):
                continue
            report = self.analyzer.analyze_file(str(file_path))
            if report:
                reports.append(report)
        return reports

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = ["__pycache__", ".venv", "venv", "env", ".git", "migrations", ".pytest_cache"]
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def generate_summary_report(self, reports: List[ComplexityReport], limit: int = 20) -> str:
        """Generate summary report for multiple files."""
        try:
            from .complexity_analyzer_formatters import generate_summary_report
        except ImportError:
            from complexity_analyzer_formatters import generate_summary_report
        return generate_summary_report(reports, limit)

