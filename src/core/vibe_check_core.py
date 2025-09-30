"""
Vibe Check Core - Main vibe check management logic.
"""

import ast
from datetime import datetime
from pathlib import Path
from typing import Any

from .design_authority import DecisionSeverity
from .vibe_check_analyzers import VibeAnalyzer
from .vibe_check_models import VibeCheckReport, VibeCheckResult, VibeViolation
from .vibe_check_patterns import VibePatternDetector


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
            "complexity_score": 8,
            "function_length": 30,
            "nesting_depth": 3,
            "parameter_count": 5,
            "class_length": 100,
            "file_length": 300,
        }
        self.analyzer = VibeAnalyzer(self.violation_thresholds)
        self.pattern_detector = VibePatternDetector()

    def check_file(self, file_path: str, agent_author: str = "") -> VibeCheckReport:
        """Perform vibe check on a single file."""
        violations = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                violations.append(
                    VibeViolation(
                        file_path=file_path,
                        line_number=e.lineno or 0,
                        violation_type="syntax_error",
                        description=f"Syntax error: {e.msg}",
                        severity=DecisionSeverity.ERROR,
                        suggestion="Fix syntax errors before running vibe check",
                    )
                )
                return VibeCheckReport(
                    result=VibeCheckResult.FAIL,
                    total_files=1,
                    violations=violations,
                    summary={"syntax_errors": 1},
                    timestamp=self._get_timestamp(),
                    agent_author=agent_author,
                )

            # Run all checks
            violations.extend(self.analyzer.check_complexity(file_path, tree))
            violations.extend(self.analyzer.check_function_length(file_path, content, tree))
            violations.extend(self.analyzer.check_nesting_depth(file_path, content, tree))
            violations.extend(self.analyzer.check_parameter_count(file_path, tree))
            violations.extend(self.analyzer.check_file_length(file_path, content))
            violations.extend(self.pattern_detector.check_duplication(file_path, content))
            violations.extend(self.pattern_detector.check_anti_patterns(file_path, content))

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

            summary = self._generate_summary(violations)

            return VibeCheckReport(
                result=result,
                total_files=1,
                violations=violations,
                summary=summary,
                timestamp=self._get_timestamp(),
                agent_author=agent_author,
            )

        except Exception as e:
            return VibeCheckReport(
                result=VibeCheckResult.FAIL,
                total_files=1,
                violations=[
                    VibeViolation(
                        file_path=file_path,
                        line_number=0,
                        violation_type="analysis_error",
                        description=f"Failed to analyze file: {str(e)}",
                        severity=DecisionSeverity.ERROR,
                        suggestion="Check file accessibility and format",
                    )
                ],
                summary={"analysis_errors": 1},
                timestamp=self._get_timestamp(),
                agent_author=agent_author,
            )

    def check_directory(
        self, directory: str, agent_author: str = "", file_patterns: list[str] = None
    ) -> VibeCheckReport:
        """Perform vibe check on all files in a directory."""
        if file_patterns is None:
            file_patterns = ["*.py"]

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
        summary["total_files_checked"] = total_files

        return VibeCheckReport(
            result=result,
            total_files=total_files,
            violations=all_violations,
            summary=summary,
            timestamp=self._get_timestamp(),
            agent_author=agent_author,
        )

    def run_pre_commit_check(
        self, staged_files: list[str], agent_author: str = ""
    ) -> VibeCheckReport:
        """Run vibe check on staged files for pre-commit hook."""
        all_violations = []
        total_files = len(staged_files)

        for file_path in staged_files:
            if file_path.endswith(".py"):
                file_report = self.check_file(file_path, agent_author)
                all_violations.extend(file_report.violations)

        error_violations = [v for v in all_violations if v.severity == DecisionSeverity.ERROR]
        result = VibeCheckResult.FAIL if error_violations else VibeCheckResult.PASS

        summary = self._generate_summary(all_violations)
        summary["staged_files_checked"] = total_files

        return VibeCheckReport(
            result=result,
            total_files=total_files,
            violations=all_violations,
            summary=summary,
            timestamp=self._get_timestamp(),
            agent_author=agent_author,
        )

    def _generate_summary(self, violations: list[VibeViolation]) -> dict[str, Any]:
        """Generate summary statistics from violations."""
        summary = {
            "total_violations": len(violations),
            "error_count": len([v for v in violations if v.severity == DecisionSeverity.ERROR]),
            "warning_count": len([v for v in violations if v.severity == DecisionSeverity.WARNING]),
            "violation_types": {},
        }

        for violation in violations:
            violation_type = violation.violation_type
            summary["violation_types"][violation_type] = (
                summary["violation_types"].get(violation_type, 0) + 1
            )

        return summary

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().isoformat()
