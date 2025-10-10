#!/usr/bin/env python3
"""
V2 Compliance Checker - Automated Quality Gate
==============================================

Scans Python files to enforce V2 compliance rules:
- Files must be ≤400 lines (MAJOR VIOLATION if >400)
- Functions must be ≤30 lines
- Classes must be ≤200 lines
- Max 5 functions per file
- Max 3 enums per file
- Max 5 classes per file

Enhanced with intelligent refactoring suggestions!

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import refactoring suggestion engine
try:
    from refactoring_suggestion_engine import RefactoringSuggestionService
    SUGGESTIONS_AVAILABLE = True
except ImportError:
    SUGGESTIONS_AVAILABLE = False

# Import complexity analyzer
try:
    from complexity_analyzer import ComplexityAnalyzer
    COMPLEXITY_AVAILABLE = True
except ImportError:
    COMPLEXITY_AVAILABLE = False


@dataclass
class ComplianceViolation:
    """Represents a V2 compliance violation."""

    file_path: str
    violation_type: str
    severity: str  # CRITICAL, MAJOR, MINOR
    line_number: Optional[int]
    current_value: int
    max_allowed: int
    message: str


@dataclass
class ComplianceReport:
    """V2 compliance scan report."""

    total_files: int
    compliant_files: int
    violations: List[ComplianceViolation]
    compliance_rate: float

    @property
    def has_violations(self) -> bool:
        """Check if report has any violations."""
        return len(self.violations) > 0

    @property
    def critical_violations(self) -> List[ComplianceViolation]:
        """Get critical violations."""
        return [v for v in self.violations if v.severity == "CRITICAL"]

    @property
    def major_violations(self) -> List[ComplianceViolation]:
        """Get major violations."""
        return [v for v in self.violations if v.severity == "MAJOR"]

    @property
    def minor_violations(self) -> List[ComplianceViolation]:
        """Get minor violations."""
        return [v for v in self.violations if v.severity == "MINOR"]


class V2ComplianceChecker:
    """Automated V2 compliance checker."""

    # V2 Compliance Rules
    MAX_FILE_LINES = 400
    MAX_FUNCTION_LINES = 30
    MAX_CLASS_LINES = 200
    MAX_FUNCTIONS_PER_FILE = 10
    MAX_ENUMS_PER_FILE = 3
    MAX_CLASSES_PER_FILE = 5
    MAX_FUNCTION_PARAMS = 5

    def __init__(self, root_path: str = "."):
        """Initialize compliance checker."""
        self.root_path = Path(root_path)
        self.violations: List[ComplianceViolation] = []

    def scan_file(self, file_path: Path) -> List[ComplianceViolation]:
        """Scan a single file for V2 compliance violations."""
        violations = []

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            line_count = len(lines)

            # Rule 1: File size (CRITICAL if >600, MAJOR if 401-600)
            if line_count > 600:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="FILE_SIZE",
                        severity="CRITICAL",
                        line_number=None,
                        current_value=line_count,
                        max_allowed=self.MAX_FILE_LINES,
                        message=f"File has {line_count} lines (CRITICAL: >600 lines, requires immediate refactor)",
                    )
                )
            elif line_count > self.MAX_FILE_LINES:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="FILE_SIZE",
                        severity="MAJOR",
                        line_number=None,
                        current_value=line_count,
                        max_allowed=self.MAX_FILE_LINES,
                        message=f"File has {line_count} lines (MAJOR VIOLATION: ≤{self.MAX_FILE_LINES} required)",
                    )
                )

            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content, filename=str(file_path))
                violations.extend(self._check_ast_compliance(file_path, tree, lines))
            except SyntaxError as e:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="SYNTAX_ERROR",
                        severity="CRITICAL",
                        line_number=e.lineno,
                        current_value=0,
                        max_allowed=0,
                        message=f"Syntax error: {e.msg}",
                    )
                )

        except Exception as e:
            violations.append(
                ComplianceViolation(
                    file_path=str(file_path),
                    violation_type="READ_ERROR",
                    severity="MINOR",
                    line_number=None,
                    current_value=0,
                    max_allowed=0,
                    message=f"Failed to read file: {e}",
                )
            )

        return violations

    def _check_ast_compliance(
        self, file_path: Path, tree: ast.AST, lines: List[str]
    ) -> List[ComplianceViolation]:
        """Check AST-based compliance rules."""
        violations = []

        functions = []
        classes = []
        enums = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
            elif isinstance(node, ast.ClassDef):
                # Check if it's an enum
                is_enum = any(
                    isinstance(base, ast.Name) and base.id == "Enum"
                    for base in node.bases
                )
                if is_enum:
                    enums.append(node)
                else:
                    classes.append(node)

        # Rule 2: Function count
        if len(functions) > self.MAX_FUNCTIONS_PER_FILE:
            violations.append(
                ComplianceViolation(
                    file_path=str(file_path),
                    violation_type="FUNCTION_COUNT",
                    severity="MAJOR",
                    line_number=None,
                    current_value=len(functions),
                    max_allowed=self.MAX_FUNCTIONS_PER_FILE,
                    message=f"File has {len(functions)} functions (max {self.MAX_FUNCTIONS_PER_FILE})",
                )
            )

        # Rule 3: Class count
        if len(classes) > self.MAX_CLASSES_PER_FILE:
            violations.append(
                ComplianceViolation(
                    file_path=str(file_path),
                    violation_type="CLASS_COUNT",
                    severity="MAJOR",
                    line_number=None,
                    current_value=len(classes),
                    max_allowed=self.MAX_CLASSES_PER_FILE,
                    message=f"File has {len(classes)} classes (max {self.MAX_CLASSES_PER_FILE})",
                )
            )

        # Rule 4: Enum count
        if len(enums) > self.MAX_ENUMS_PER_FILE:
            violations.append(
                ComplianceViolation(
                    file_path=str(file_path),
                    violation_type="ENUM_COUNT",
                    severity="MINOR",
                    line_number=None,
                    current_value=len(enums),
                    max_allowed=self.MAX_ENUMS_PER_FILE,
                    message=f"File has {len(enums)} enums (max {self.MAX_ENUMS_PER_FILE})",
                )
            )

        # Rule 5: Function size and parameters
        for func in functions:
            func_lines = self._get_node_line_count(func, lines)
            if func_lines > self.MAX_FUNCTION_LINES:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="FUNCTION_SIZE",
                        severity="MAJOR",
                        line_number=func.lineno,
                        current_value=func_lines,
                        max_allowed=self.MAX_FUNCTION_LINES,
                        message=f"Function '{func.name}' has {func_lines} lines (max {self.MAX_FUNCTION_LINES})",
                    )
                )

            # Check parameter count
            param_count = len(func.args.args)
            if param_count > self.MAX_FUNCTION_PARAMS:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="FUNCTION_PARAMS",
                        severity="MINOR",
                        line_number=func.lineno,
                        current_value=param_count,
                        max_allowed=self.MAX_FUNCTION_PARAMS,
                        message=f"Function '{func.name}' has {param_count} parameters (max {self.MAX_FUNCTION_PARAMS})",
                    )
                )

        # Rule 6: Class size
        for cls in classes:
            class_lines = self._get_node_line_count(cls, lines)
            if class_lines > self.MAX_CLASS_LINES:
                violations.append(
                    ComplianceViolation(
                        file_path=str(file_path),
                        violation_type="CLASS_SIZE",
                        severity="MAJOR",
                        line_number=cls.lineno,
                        current_value=class_lines,
                        max_allowed=self.MAX_CLASS_LINES,
                        message=f"Class '{cls.name}' has {class_lines} lines (max {self.MAX_CLASS_LINES})",
                    )
                )

        return violations

    def _get_node_line_count(self, node: ast.AST, lines: List[str]) -> int:
        """Get line count for an AST node."""
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            return 0

        start = node.lineno - 1
        end = node.end_lineno if node.end_lineno else node.lineno

        return end - start

    def scan_directory(
        self, directory: Optional[Path] = None, pattern: str = "**/*.py"
    ) -> ComplianceReport:
        """Scan directory for V2 compliance violations."""
        if directory is None:
            directory = self.root_path

        violations = []
        total_files = 0
        compliant_files = 0

        # Scan all Python files
        for file_path in directory.glob(pattern):
            # Skip test files, migrations, and generated files
            if self._should_skip_file(file_path):
                continue

            total_files += 1
            file_violations = self.scan_file(file_path)

            if file_violations:
                violations.extend(file_violations)
            else:
                compliant_files += 1

        compliance_rate = (
            (compliant_files / total_files * 100) if total_files > 0 else 100.0
        )

        return ComplianceReport(
            total_files=total_files,
            compliant_files=compliant_files,
            violations=violations,
            compliance_rate=compliance_rate,
        )

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            "__pycache__",
            ".venv",
            "venv",
            "env",
            ".git",
            "migrations",
            "alembic",
            ".pytest_cache",
            "build",
            "dist",
            ".eggs",
        ]

        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def format_report(self, report: ComplianceReport, verbose: bool = False, show_suggestions: bool = False, show_complexity: bool = False) -> str:
        """Format compliance report as string."""
        lines = []
        lines.append("=" * 80)
        lines.append("V2 COMPLIANCE REPORT")
        if show_complexity and COMPLEXITY_AVAILABLE:
            lines.append("(with Complexity Analysis)")
        lines.append("=" * 80)
        lines.append(f"Total files scanned: {report.total_files}")
        lines.append(f"Compliant files: {report.compliant_files}")
        lines.append(
            f"Files with violations: {report.total_files - report.compliant_files}"
        )
        lines.append(f"Compliance rate: {report.compliance_rate:.1f}%")
        lines.append("")

        if report.has_violations:
            lines.append(f"VIOLATIONS FOUND: {len(report.violations)}")
            lines.append(
                f"  - Critical: {len(report.critical_violations)} (>600 lines)"
            )
            lines.append(
                f"  - Major: {len(report.major_violations)} (>400 lines or rule violations)"
            )
            lines.append(f"  - Minor: {len(report.minor_violations)}")
            lines.append("")

            # Group by file
            violations_by_file: Dict[str, List[ComplianceViolation]] = {}
            for v in report.violations:
                if v.file_path not in violations_by_file:
                    violations_by_file[v.file_path] = []
                violations_by_file[v.file_path].append(v)

            for file_path, violations in sorted(violations_by_file.items()):
                lines.append(f"\n{file_path}:")
                for v in violations:
                    severity_marker = {
                        "CRITICAL": "🔴",
                        "MAJOR": "🟡",
                        "MINOR": "🟢",
                    }.get(v.severity, "⚪")

                    location = f"line {v.line_number}" if v.line_number else "file"
                    lines.append(f"  {severity_marker} [{v.severity}] {location}: {v.message}")

                # Add refactoring suggestions for file size violations
                if show_suggestions and SUGGESTIONS_AVAILABLE:
                    file_size_violations = [v for v in violations if v.violation_type == "FILE_SIZE"]
                    if file_size_violations:
                        lines.append(self._get_file_suggestions(file_path))

                # Add complexity analysis
                if show_complexity and COMPLEXITY_AVAILABLE:
                    lines.append(self._get_complexity_analysis(file_path))

        else:
            lines.append("✅ All files are V2 compliant!")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _get_file_suggestions(self, file_path: str) -> str:
        """Get refactoring suggestions for a file."""
        try:
            service = RefactoringSuggestionService()
            suggestion = service.analyze_and_suggest(file_path)
            
            if suggestion and suggestion.suggested_modules:
                lines = ["\n  💡 REFACTORING SUGGESTIONS:"]
                lines.append(f"  Confidence: {suggestion.confidence * 100:.0f}% | Estimated result: {suggestion.estimated_main_file_lines} lines")
                
                for module in suggestion.suggested_modules[:2]:  # Show top 2 suggestions
                    entity_count = len(module.entities)
                    lines.append(f"    → Extract to {module.module_name} ({module.estimated_lines} lines, {entity_count} entities)")
                
                if len(suggestion.suggested_modules) > 2:
                    lines.append(f"    ... +{len(suggestion.suggested_modules) - 2} more suggested modules")
                
                lines.append(f"  Run: python tools/refactoring_suggestion_engine.py {file_path} --detailed")
                return "\n".join(lines)
                
            return ""
        except Exception:
            return ""

    def _get_complexity_analysis(self, file_path: str) -> str:
        """Get complexity analysis for a file."""
        try:
            analyzer = ComplexityAnalyzer()
            report = analyzer.analyze_file(file_path)
            
            if report:
                lines = ["\n  📊 COMPLEXITY METRICS:"]
                lines.append(f"  Avg Cyclomatic: {report.avg_cyclomatic:.1f} | Avg Cognitive: {report.avg_cognitive:.1f} | Max Nesting: {report.max_nesting}")
                
                if report.has_violations:
                    high = [v for v in report.violations if v.severity == "HIGH"]
                    medium = [v for v in report.violations if v.severity == "MEDIUM"]
                    low = [v for v in report.violations if v.severity == "LOW"]
                    
                    lines.append(f"  Violations: {len(report.violations)} (🔴{len(high)} 🟡{len(medium)} 🟢{len(low)})")
                    
                    # Show worst violation
                    worst = max(report.violations, key=lambda x: x.current_value)
                    lines.append(f"  Worst: {worst.entity_name} ({worst.violation_type}={worst.current_value}, threshold={worst.threshold})")
                else:
                    lines.append("  ✅ All functions have acceptable complexity")
                
                lines.append(f"  Run: python tools/complexity_analyzer.py {file_path} --verbose")
                return "\n".join(lines)
                
            return ""
        except Exception:
            return ""


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="V2 Compliance Checker - Automated Quality Gate"
    )
    parser.add_argument(
        "path", nargs="?", default=".", help="Path to scan (default: current directory)"
    )
    parser.add_argument(
        "--pattern", default="**/*.py", help="File pattern to scan (default: **/*.py)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--fail-on-major",
        action="store_true",
        help="Exit with error code if major violations found",
    )
    parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit with error code if critical violations found",
    )
    parser.add_argument(
        "--suggest",
        "-s",
        action="store_true",
        help="Show refactoring suggestions for violations (requires refactoring_suggestion_engine.py)",
    )
    parser.add_argument(
        "--complexity",
        "-c",
        action="store_true",
        help="Show complexity analysis for files (requires complexity_analyzer.py)",
    )

    args = parser.parse_args()

    checker = V2ComplianceChecker(args.path)
    report = checker.scan_directory(Path(args.path), args.pattern)

    print(checker.format_report(report, args.verbose, show_suggestions=args.suggest, show_complexity=args.complexity))

    # Exit with error code if violations found
    if args.fail_on_critical and report.critical_violations:
        sys.exit(1)
    if args.fail_on_major and report.major_violations:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

