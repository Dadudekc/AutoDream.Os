"""
Vibe Check - Refactored main interface for automated CI/CD gate.
Analyzes code for violations of project "vibe" (simplicity, clarity, YAGNI).
"""

import os

from .design_authority import DecisionSeverity
from .vibe_check_core import VibeChecker
from .vibe_check_models import VibeCheckReport, VibeCheckResult


def vibe_check_file(file_path: str, agent_author: str = "", strict: bool = True) -> VibeCheckReport:
    """Run vibe check on a single file."""
    checker = VibeChecker(strict_mode=strict)
    return checker.check_file(file_path, agent_author)


def vibe_check_directory(
    directory: str, agent_author: str = "", strict: bool = True
) -> VibeCheckReport:
    """Run vibe check on a directory."""
    checker = VibeChecker(strict_mode=strict)
    return checker.check_directory(directory, agent_author)


def vibe_check_strict(file_paths: list[str], agent_author: str = "") -> VibeCheckReport:
    """Run strict vibe check (fails on warnings)."""
    checker = VibeChecker(strict_mode=True)
    all_violations = []

    for file_path in file_paths:
        if file_path.endswith(".py"):
            file_report = checker.check_file(file_path, agent_author)
            all_violations.extend(file_report.violations)

    error_violations = [v for v in all_violations if v.severity == DecisionSeverity.ERROR]
    warning_violations = [v for v in all_violations if v.severity == DecisionSeverity.WARNING]

    result = (
        VibeCheckResult.FAIL if (error_violations or warning_violations) else VibeCheckResult.PASS
    )

    summary = checker._generate_summary(all_violations)

    return VibeCheckReport(
        result=result,
        total_files=len(file_paths),
        violations=all_violations,
        summary=summary,
        timestamp=checker._get_timestamp(),
        agent_author=agent_author,
    )


def main():
    """CLI entry point for vibe check."""
    import argparse

    parser = argparse.ArgumentParser(description="Run vibe check on code")
    parser.add_argument("path", help="File or directory to check")
    parser.add_argument("--agent", default="", help="Agent author for attribution")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        report = vibe_check_file(args.path, args.agent, args.strict)
    else:
        report = vibe_check_directory(args.path, args.agent, args.strict)

    if args.format == "json":
        import json

        print(
            json.dumps(
                {
                    "result": report.result.value,
                    "total_files": report.total_files,
                    "violations": [
                        {
                            "file": v.file_path,
                            "line": v.line_number,
                            "type": v.violation_type,
                            "description": v.description,
                            "severity": v.severity.value,
                            "suggestion": v.suggestion,
                        }
                        for v in report.violations
                    ],
                    "summary": report.summary,
                },
                indent=2,
            )
        )
    else:
        print(f"Vibe Check Result: {report.result.value}")
        print(f"Files Checked: {report.total_files}")
        print(f"Violations: {len(report.violations)}")

        for violation in report.violations:
            print(f"\n{violation.file_path}:{violation.line_number}")
            print(f"  {violation.violation_type}: {violation.description}")
            print(f"  Suggestion: {violation.suggestion}")


if __name__ == "__main__":
    main()
