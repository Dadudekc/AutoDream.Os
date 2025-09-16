"""
V2 Compliance Analysis CLI Tool
================================

Core tool for analyzing V2 compliance violations and enforcing CI gates.

Features:
- Detect syntax errors, LOC violations, line length issues, and print statements
- Generate detailed violation reports
- Provide CI gate functionality
- Support for different output formats

Usage:
    python tools/analysis_cli.py --violations --n 100000 > runtime/violations_full.txt
    python tools/analysis_cli.py --ci-gate
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
MAX_FILE_LOC = 400
MAX_CLASS_LOC = 100
MAX_FUNCTION_LOC = 50
MAX_LINE_LENGTH = 100
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    "build",
    "dist",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".tox",
    ".coverage",
    "htmlcov",
    "*.egg-info",
    ".mypy_cache",
    ".DS_Store",
]


def should_exclude_file(path: Path) -> bool:
    """Check if file should be excluded from analysis."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    if "test" in path_str.lower() and not path_str.endswith("test_models.py"):
        return False
    return False


def count_lines(node: ast.AST) -> int:
    """Count lines in an AST node."""
    if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
        return node.end_lineno - node.lineno + 1
    return 1


def analyze_file(file_path: Path) -> dict[str, Any]:
    """Analyze a single Python file for V2 compliance violations."""
    violations = {
        "file": str(file_path),
        "syntax_errors": [],
        "loc_violations": [],
        "line_length_violations": [],
        "print_statements": [],
        "total_lines": 0,
        "classes": [],
        "functions": [],
    }
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            violations["total_lines"] = len(content.splitlines())
        tree = ast.parse(content, filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_lines = count_lines(node)
                violations["classes"].append(
                    {"name": node.name, "lines": class_lines, "line_number": node.lineno}
                )
                if class_lines > MAX_CLASS_LOC:
                    violations["loc_violations"].append(
                        {
                            "type": "class",
                            "name": node.name,
                            "lines": class_lines,
                            "line_number": node.lineno,
                            "max_allowed": MAX_CLASS_LOC,
                        }
                    )
            elif isinstance(node, ast.FunctionDef):
                func_lines = count_lines(node)
                violations["functions"].append(
                    {"name": node.name, "lines": func_lines, "line_number": node.lineno}
                )
                if func_lines > MAX_FUNCTION_LOC:
                    violations["loc_violations"].append(
                        {
                            "type": "function",
                            "name": node.name,
                            "lines": func_lines,
                            "line_number": node.lineno,
                            "max_allowed": MAX_FUNCTION_LOC,
                        }
                    )
        if violations["total_lines"] > MAX_FILE_LOC:
            violations["loc_violations"].append(
                {
                    "type": "file",
                    "name": file_path.name,
                    "lines": violations["total_lines"],
                    "line_number": 1,
                    "max_allowed": MAX_FILE_LOC,
                }
            )
        for i, line in enumerate(content.splitlines(), 1):
            if len(line) > MAX_LINE_LENGTH:
                violations["line_length_violations"].append(
                    {
                        "line_number": i,
                        "length": len(line),
                        "max_allowed": MAX_LINE_LENGTH,
                        "content": line[:50] + "..." if len(line) > 50 else line,
                    }
                )
            if "logger.info(" in line and not line.strip().startswith("#"):
                violations["print_statements"].append({"line_number": i, "content": line.strip()})
    except SyntaxError as e:
        violations["syntax_errors"].append(
            {"line_number": e.lineno, "message": str(e), "text": e.text}
        )
    except Exception as e:
        violations["syntax_errors"].append(
            {"line_number": 0, "message": f"Error analyzing file: {e}", "text": ""}
        )
    return violations


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="V2 Compliance Analysis CLI")
    parser.add_argument("--violations", action="store_true", help="Generate violations report")
    parser.add_argument("--n", type=int, default=1000, help="Number of files to analyze")
    parser.add_argument("--ci-gate", action="store_true", help="Run CI gate validation")
    parser.add_argument("--file", type=str, help="Analyze specific file")
    parser.add_argument("--summary", action="store_true", help="Generate summary report")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    args = parser.parse_args()
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            violations = analyze_file(file_path)
            if args.format == "json":
                logger.info(json.dumps(violations, indent=2))
            else:
                print_violations_report([violations])
        else:
            logger.info(f"File not found: {args.file}")
            sys.exit(1)
    else:
        project_root = Path.cwd()
        violations = []
        for py_file in project_root.rglob("*.py"):
            if should_exclude_file(py_file):
                continue
            if len(violations) >= args.n:
                break
            violations.append(analyze_file(py_file))
        if args.summary:
            print_summary_report(violations)
        elif args.ci_gate:
            run_ci_gate(violations)
        else:
            print_violations_report(violations)


def print_violations_report(violations: list[dict[str, Any]]) -> None:
    """Print detailed violations report."""
    logger.info("V2 Compliance Analysis Report")
    logger.info("=" * 50)
    total_files = len(violations)
    files_with_violations = sum(
        1
        for v in violations
        if any(
            [
                v["syntax_errors"],
                v["loc_violations"],
                v["line_length_violations"],
                v["print_statements"],
            ]
        )
    )
    logger.info("📊 Analysis Summary:")
    logger.info(f"   • Total files analyzed: {total_files}")
    logger.info(f"   • Files with violations: {files_with_violations}")
    logger.info(
        f"   • Compliance rate: {(total_files - files_with_violations) / total_files * 100:.1f}%"
    )
    logger.info("")
    for violation in violations:
        if any(
            [
                violation["syntax_errors"],
                violation["loc_violations"],
                violation["line_length_violations"],
                violation["print_statements"],
            ]
        ):
            logger.info(f"📁 {violation['file']}")
            if violation["syntax_errors"]:
                logger.info("   Syntax Errors:")
                for error in violation["syntax_errors"]:
                    logger.info(f"      Line {error['line_number']}: {error['message']}")
            if violation["loc_violations"]:
                logger.info("   LOC Violations:")
                for loc in violation["loc_violations"]:
                    logger.info(
                        f"      {loc['type'].title()} '{loc['name']}': {loc['lines']} lines (max: {loc['max_allowed']})"
                    )
            if violation["line_length_violations"]:
                logger.info("   Line Length Violations:")
                for line in violation["line_length_violations"][:5]:
                    logger.info(f"      Line {line['line_number']}: {line['length']} chars")
            if violation["print_statements"]:
                logger.info("   Print Statements:")
                for print_stmt in violation["print_statements"][:3]:
                    logger.info(f"      Line {print_stmt['line_number']}: {print_stmt['content']}")
            logger.info("")


def print_summary_report(violations: list[dict[str, Any]]) -> None:
    """Print summary report."""
    total_files = len(violations)
    syntax_errors = sum(len(v["syntax_errors"]) for v in violations)
    loc_violations = sum(len(v["loc_violations"]) for v in violations)
    line_length_violations = sum(len(v["line_length_violations"]) for v in violations)
    print_statements = sum(len(v["print_statements"]) for v in violations)
    logger.info("📊 V2 Compliance Summary")
    logger.info("=" * 30)
    logger.info(f"Total files: {total_files}")
    logger.info(f"Syntax errors: {syntax_errors}")
    logger.info(f"LOC violations: {loc_violations}")
    logger.info(f"Line length violations: {line_length_violations}")
    logger.info(f"Print statements: {print_statements}")


def run_ci_gate(violations: list[dict[str, Any]]) -> None:
    """Run CI gate validation."""
    total_violations = sum(
        len(v["syntax_errors"])
        + len(v["loc_violations"])
        + len(v["line_length_violations"])
        + len(v["print_statements"])
        for v in violations
    )
    if total_violations == 0:
        logger.info("✅ CI Gate: PASSED - No violations found")
        sys.exit(0)
    else:
        logger.info(f"CI Gate: FAILED - {total_violations} violations found")
        sys.exit(1)


if __name__ == "__main__":
    main()
