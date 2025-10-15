#!/usr/bin/env python3
"""
⚠️ DEPRECATED - Use modular v2_checker system instead!

This monolithic file is DEPRECATED and will be removed in a future version.

Use instead:
    python -m tools_v2.toolbelt v2.compliance_check

Or use the modular version:
    tools/v2_checker_cli.py (modern modular refactor)
    tools/v2_checker_models.py
    tools/v2_checker_formatters.py

Migration: Infrastructure Consolidation Mission (Agent-2 LEAD)
Deprecation date: 2025-10-15
Removal planned: 2025-11-15 (30 days)

==============================================
OLD MONOLITHIC VERSION BELOW (336 lines)
==============================================

V2 Compliance Checker - Automated Quality Gate (DEPRECATED)

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import warnings
warnings.warn(
    "⚠️ DEPRECATED: tools/v2_compliance_checker.py is deprecated. "
    "Use 'python -m tools_v2.toolbelt v2.compliance_check' or tools/v2_checker_cli.py instead. "
    "This monolithic file will be removed after 2025-11-15.",
    DeprecationWarning,
    stacklevel=2
)

import ast
from pathlib import Path

try:
    from .v2_checker_models import ComplianceReport, ComplianceViolation
except ImportError:
    from v2_checker_models import ComplianceReport, ComplianceViolation

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
        self.violations: list[ComplianceViolation] = []

    def scan_file(self, file_path: Path) -> list[ComplianceViolation]:
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
        self, file_path: Path, tree: ast.AST, lines: list[str]
    ) -> list[ComplianceViolation]:
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
                    isinstance(base, ast.Name) and base.id == "Enum" for base in node.bases
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

    def _get_node_line_count(self, node: ast.AST, lines: list[str]) -> int:
        """Get line count for an AST node."""
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            return 0

        start = node.lineno - 1
        end = node.end_lineno if node.end_lineno else node.lineno

        return end - start

    def scan_directory(
        self, directory: Path | None = None, pattern: str = "**/*.py"
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

        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 100.0

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

    def format_report(
        self,
        report: ComplianceReport,
        verbose: bool = False,
        show_suggestions: bool = False,
        show_complexity: bool = False,
    ) -> str:
        """Format compliance report as string (delegates to formatter)."""
        try:
            from .v2_checker_formatters import format_report as fmt_report
        except ImportError:
            from v2_checker_formatters import format_report as fmt_report

        # Group violations by file
        violations_by_file: dict[str, list[ComplianceViolation]] = {}
        for v in report.violations:
            if v.file_path not in violations_by_file:
                violations_by_file[v.file_path] = []
            violations_by_file[v.file_path].append(v)

        return fmt_report(report, violations_by_file, verbose, show_suggestions, show_complexity)


# CLI entry point moved to v2_checker_cli.py for V2 compliance
if __name__ == "__main__":
    try:
        from .v2_checker_cli import main
    except ImportError:
        from v2_checker_cli import main
    main()
