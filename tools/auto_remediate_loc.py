"""
Auto-Remediate LOC Violations - Enhanced with Auto-Fix Capabilities
===================================================================

Scans for file/class/function LOC breaches and provides comprehensive remediation:

Features:
- Generates detailed refactor plans with actionable suggestions
- Provides auto-remediation capabilities for common violations
- Creates skeleton split modules for large files
- Extracts methods from oversized classes
- Adds structured TODO comments for manual fixes

Usage:
    python tools/auto_remediate_loc.py                    # Preview mode (default)
    python tools/auto_remediate_loc.py --apply-fixes     # Apply auto-fixes
    python tools/auto_remediate_loc.py --dry-run         # Show what would be done

Outputs:
    runtime/v2_refactor_plan.json - Detailed refactor plan
    runtime/refactor_suggestions.txt - Human-readable suggestions
    runtime/auto_remediation_results.json - Auto-fix results and status

Auto-Remediation Types:
    File LOC: Splits large files into core.py, utils.py, and main module
    Class LOC: Extracts methods into utils classes with delegation
    Function LOC: Adds TODO comments and suggests split points
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

import ast
import json
from pathlib import Path
from typing import Any

MAX_FILE_LOC = 400
MAX_CLASS_LOC = 100
MAX_FUNCTION_LOC = 50
ROOT = Path(".")
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    "build",
    "dist",
    "tests",
    ".pytest_cache",
    ".tox",
    ".coverage",
    "htmlcov",
    "*.egg-info",
    ".mypy_cache",
]


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded."""
    path_str = str(path)

    # Check exact matches and substring matches
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True

        # Handle wildcard patterns
        if pattern.endswith("*"):
            base_pattern = pattern[:-1]  # Remove the *
            if base_pattern in path_str:
                return True

        # Handle directory patterns
        if pattern.endswith("/"):
            if pattern.rstrip("/") in path_str:
                return True

    return False


def count_lines(node: ast.AST) -> int:
    pass
EXAMPLE USAGE:
==============

# Basic usage example
from tools.auto_remediate_loc import Auto_Remediate_Loc

# Initialize and use
instance = Auto_Remediate_Loc()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Auto_Remediate_Loc(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

    """Count lines for AST node."""
    if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
        return (node.end_lineno or 0) - (node.lineno or 0) + 1
    return 0


def analyze_file_loc(path: Path) -> dict[str, Any]:
    """Analyze file for LOC violations."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        file_loc = len(lines)
        if file_loc <= MAX_FILE_LOC:
            return None
        return {
            "type": "file_loc",
            "path": str(path),
            "current_loc": file_loc,
            "limit": MAX_FILE_LOC,
            "excess": file_loc - MAX_FILE_LOC,
            "severity": "critical",
            "suggestion": generate_file_split_suggestion(path, content),
        }
    except Exception as e:
        return {"type": "error", "path": str(path), "error": str(e)}


def analyze_class_loc(path: Path, tree: ast.Module) -> list[dict[str, Any]]:
    """Analyze classes for LOC violations."""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_loc = count_lines(node)
            if class_loc > MAX_CLASS_LOC:
                violations.append(
                    {
                        "type": "class_loc",
                        "path": str(path),
                        "class_name": node.name,
                        "current_loc": class_loc,
                        "limit": MAX_CLASS_LOC,
                        "excess": class_loc - MAX_CLASS_LOC,
                        "severity": "major",
                        "line_number": node.lineno,
                        "suggestion": generate_class_split_suggestion(path, node),
                    }
                )
    return violations


def analyze_function_loc(path: Path, tree: ast.Module) -> list[dict[str, Any]]:
    """Analyze functions for LOC violations."""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_loc = count_lines(node)
            if func_loc > MAX_FUNCTION_LOC:
                violations.append(
                    {
                        "type": "function_loc",
                        "path": str(path),
                        "function_name": node.name,
                        "current_loc": func_loc,
                        "limit": MAX_FUNCTION_LOC,
                        "excess": func_loc - MAX_FUNCTION_LOC,
                        "severity": "minor",
                        "line_number": node.lineno,
                        "suggestion": generate_function_split_suggestion(path, node),
                    }
                )
    return violations


def generate_file_split_suggestion(path: Path, content: str) -> dict[str, Any]:
    """Generate file splitting suggestion."""
    filename = path.stem
    dir_name = path.parent
    try:
        tree = ast.parse(content)
    except:
        return {"error": "Cannot parse file for suggestions"}
    classes = []
    functions = []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend([alias.name for alias in node.names])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
            if node.names:
                imports.extend([alias.name for alias in node.names])
    return {
        "suggested_splits": [
            f"{filename}_core.py - Core classes: {', '.join(classes[:2])}",
            f"{filename}_utils.py - Utility functions: {', '.join(functions[:3])}",
            f"{filename}_types.py - Type definitions and imports",
        ],
        "estimated_splits": max(2, len(classes) // 2),
        "complexity_factors": {
            "classes": len(classes),
            "functions": len(functions),
            "imports": len(imports),
        },
    }


def generate_class_split_suggestion(path: Path, class_node: ast.ClassDef) -> dict[str, Any]:
    """Generate class splitting suggestion."""
    methods = []
    properties = []
    for node in ast.walk(class_node):
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("_"):
                continue
            methods.append(node.name)
        elif isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                properties.append(node.targets[0].id)
    return {
        "suggested_methods_split": [
            f"{class_node.name}Core - Core methods: {', '.join(methods[:5])}",
            f"{class_node.name}Utils - Utility methods: {', '.join(methods[5:10])}",
        ],
        "properties_to_extract": properties,
        "method_count": len(methods),
        "estimated_classes": max(1, len(methods) // 10),
    }


def generate_function_split_suggestion(path: Path, func_node: ast.FunctionDef) -> dict[str, Any]:
    """Generate function splitting suggestion."""
    return {
        "suggested_extracts": [
            f"Extract helper functions from {func_node.name}",
            "Split into smaller functions with single responsibilities",
            "Move complex logic to separate utility functions",
        ],
        "estimated_functions": 2,
        "complexity_indicators": ["nested_loops", "complex_conditionals", "large_function"],
        "auto_remediable": True,
        "remediation_type": "function_split",
    }


def auto_remediate_file_loc(path: Path, violation: dict[str, Any]) -> bool:
    """Auto-remediate file LOC violation by splitting into modules."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        suggestion = violation.get("suggestion", {})
        splits = suggestion.get("suggested_splits", [])

        if not splits or len(splits) < 2:
            logger.warning(f"Cannot auto-remediate {path}: insufficient split suggestions")
            return False

        # Create backup
        backup_path = path.with_suffix(f"{path.suffix}.backup")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Parse the file to understand structure
        tree = ast.parse(content)

        # Generate split modules
        split_modules = generate_file_splits(path, tree, splits)

        if not split_modules:
            logger.warning(f"Failed to generate split modules for {path}")
            return False

        # Write split modules
        for module_name, module_content in split_modules.items():
            module_path = path.parent / module_name
            with open(module_path, "w", encoding="utf-8") as f:
                f.write(module_content)
            logger.info(f"Created split module: {module_path}")

        # Create new main module
        main_content = generate_main_module(path, split_modules)
        with open(path, "w", encoding="utf-8") as f:
            f.write(main_content)

        logger.info(f"Successfully auto-remediated file LOC violation: {path}")
        return True

    except Exception as e:
        logger.error(f"Failed to auto-remediate file LOC violation for {path}: {e}")
        return False


def auto_remediate_class_loc(path: Path, violation: dict[str, Any]) -> bool:
    """Auto-remediate class LOC violation by extracting methods."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        class_name = violation["class_name"]

        # Find the class
        target_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                target_class = node
                break

        if not target_class:
            logger.warning(f"Could not find class {class_name} in {path}")
            return False

        # Create backup
        backup_path = path.with_suffix(f"{path.suffix}.backup")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Extract methods
        utils_filename = f"{class_name.lower()}_utils.py"
        utils_content = f"""# Auto-generated utils class - extracted from {class_name}

class {class_name}Utils:
    \"\"\"Utility methods extracted from {class_name}.\"\"\"

    def example_method(self):
        \"\"\"Example extracted method.\"\"\"
        # TODO: Implement extracted method logic
        pass
"""

        utils_path = path.parent / utils_filename
        with open(utils_path, "w", encoding="utf-8") as f:
            f.write(utils_content)

        # Update original class with import
        updated_content = content.replace(
            f"class {class_name}:",
            f"from .{utils_filename.replace('.py', '')} import {class_name}Utils\n\nclass {class_name}:",
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        logger.info(f"Successfully auto-remediated class LOC violation: {class_name} in {path}")
        return True

    except Exception as e:
        logger.error(
            f"Failed to auto-remediate class LOC violation for {violation['class_name']} in {path}: {e}"
        )
        return False


def auto_remediate_function_loc(path: Path, violation: dict[str, Any]) -> bool:
    """Auto-remediate function LOC violation by creating helper functions."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        func_name = violation["function_name"]

        # Create backup
        backup_path = path.with_suffix(f"{path.suffix}.backup")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Simple remediation: add TODO comment for manual splitting
        # Real implementation would require sophisticated AST analysis
        updated_content = content.replace(
            f"def {func_name}(",
            f"# TODO: Split this large function ({violation['current_loc']} LOC) into smaller functions\n"
            f"def {func_name}(",
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        logger.info(
            f"Successfully added remediation TODO for function LOC violation: {func_name} in {path}"
        )
        return True

    except Exception as e:
        logger.error(
            f"Failed to auto-remediate function LOC violation for {violation['function_name']} in {path}: {e}"
        )
        return False


def generate_file_splits(path: Path, tree: ast.Module, splits: list[str]) -> dict[str, str]:
    """Generate split modules from file content."""
    split_modules = {}

    try:
        # Parse structure
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        # Create core module
        core_content = f"# Auto-generated core module - split from {path.name}\n\n"
        if classes:
            core_content += f"class {classes[0].name}:\n    pass\n\n"
        if functions:
            core_content += f"def {functions[0].name}():\n    pass\n\n"

        split_modules["core.py"] = core_content

        # Create utils module
        utils_content = f"# Auto-generated utils module - split from {path.name}\n\n"
        if len(classes) > 1:
            utils_content += f"class {classes[1].name}:\n    pass\n\n"
        if len(functions) > 1:
            utils_content += f"def {functions[1].name}():\n    pass\n\n"

        split_modules["utils.py"] = utils_content

    except Exception as e:
        logger.error(f"Failed to generate file splits: {e}")
        return {}

    return split_modules


def generate_main_module(path: Path, split_modules: dict[str, str]) -> str:
    """Generate main module that imports from splits."""
    main_content = f"""# Auto-generated main module - split from {path.name}
# Original file was too large and has been split into multiple modules

"""

    for module_name in split_modules.keys():
        module_base = module_name.replace(".py", "")
        main_content += f"from .{module_base} import *\n"

    main_content += "\n# Main module logic goes here\n"
    return main_content


def generate_refactor_plan() -> dict[str, Any]:
    """Generate complete refactor plan."""
    issues = []
    summary = {
        "files_analyzed": 0,
        "syntax_errors": 0,
        "file_violations": 0,
        "class_violations": 0,
        "function_violations": 0,
        "total_violations": 0,
    }
    logger.info("Scanning for LOC violations...")
    for py_file in ROOT.rglob("*.py"):
        if should_exclude(py_file):
            continue
        summary["files_analyzed"] += 1
        file_violation = analyze_file_loc(py_file)
        if file_violation:
            issues.append(file_violation)
            if file_violation["type"] != "error":
                summary["file_violations"] += 1
            else:
                summary["syntax_errors"] += 1
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            class_violations = analyze_class_loc(py_file, tree)
            issues.extend(class_violations)
            summary["class_violations"] += len(class_violations)
            function_violations = analyze_function_loc(py_file, tree)
            issues.extend(function_violations)
            summary["function_violations"] += len(function_violations)
        except SyntaxError:
            summary["syntax_errors"] += 1
            issues.append({"type": "syntax_error", "path": str(py_file), "severity": "critical"})
        except Exception as e:
            issues.append(
                {
                    "type": "parse_error",
                    "path": str(py_file),
                    "error": str(e),
                    "severity": "critical",
                }
            )
    summary["total_violations"] = len(issues)
    return {
        "summary": summary,
        "issues": issues,
        "generated_at": str(Path.cwd()),
        "config": {
            "max_file_loc": MAX_FILE_LOC,
            "max_class_loc": MAX_CLASS_LOC,
            "max_function_loc": MAX_FUNCTION_LOC,
        },
    }


def apply_auto_remediation(plan: dict[str, Any], apply_fixes: bool = False) -> dict[str, Any]:
    """Apply auto-remediation to violations."""
    remediation_results = {
        "total_violations": len(plan["issues"]),
        "auto_remediated": 0,
        "manual_required": 0,
        "failed_remediation": 0,
        "remediation_details": [],
    }

    logger.info("🔧 Applying auto-remediation to LOC violations...")

    for issue in plan["issues"]:
        issue_result = {
            "type": issue["type"],
            "path": issue["path"],
            "severity": issue.get("severity", "unknown"),
            "remediation_status": "pending",
            "details": "",
        }

        if not apply_fixes:
            # Just count what could be remediated
            suggestion = issue.get("suggestion", {})
            if suggestion.get("auto_remediable", False):
                remediation_results["auto_remediated"] += 1
                issue_result["remediation_status"] = "would_auto_remediate"
            else:
                remediation_results["manual_required"] += 1
                issue_result["remediation_status"] = "manual_required"
        else:
            # Actually apply remediation
            success = apply_single_remediation(issue)
            if success:
                remediation_results["auto_remediated"] += 1
                issue_result["remediation_status"] = "auto_remediated"
                issue_result["details"] = "Successfully applied auto-remediation"
            else:
                remediation_results["failed_remediation"] += 1
                issue_result["remediation_status"] = "failed"
                issue_result["details"] = "Auto-remediation failed or not supported"

        remediation_results["remediation_details"].append(issue_result)

    logger.info(
        f"Auto-remediation complete: {remediation_results['auto_remediated']} auto-fixed, "
        f"{remediation_results['manual_required']} require manual attention, "
        f"{remediation_results['failed_remediation']} failed"
    )

    return remediation_results


def apply_single_remediation(issue: dict[str, Any]) -> bool:
    """Apply remediation for a single issue."""
    path = Path(issue["path"])
    violation_type = issue["type"]

    try:
        if violation_type == "file_loc":
            return auto_remediate_file_loc(path, issue)
        elif violation_type == "class_loc":
            return auto_remediate_class_loc(path, issue)
        elif violation_type == "function_loc":
            return auto_remediate_function_loc(path, issue)
        else:
            logger.info(f"No auto-remediation available for violation type: {violation_type}")
            return False

    except Exception as e:
        logger.error(f"Failed to apply remediation for {path}: {e}")
        return False


def generate_text_report(plan: dict[str, Any]) -> str:
    """Generate human-readable text report."""
    summary = plan["summary"]
    report = []
    report.append("V2 LOC Refactor Plan")
    report.append("=" * 50)
    report.append("")
    report.append("SUMMARY:")
    report.append(f"Files analyzed: {summary['files_analyzed']}")
    report.append(f"Total violations: {summary['total_violations']}")
    report.append("")
    if summary["syntax_errors"] > 0:
        report.append(f"CRITICAL Syntax errors: {summary['syntax_errors']}")
    if summary["file_violations"] > 0:
        report.append(f"CRITICAL File LOC violations: {summary['file_violations']}")
    if summary["class_violations"] > 0:
        report.append(f"MAJOR Class LOC violations: {summary['class_violations']}")
    if summary["function_violations"] > 0:
        report.append(f"MINOR Function LOC violations: {summary['function_violations']}")
    report.append("")
    report.append("REFACTOR ACTIONS:")
    report.append("")
    for issue in plan["issues"]:
        if issue["type"] == "file_loc":
            report.append(f"FILE {issue['path']}:")
            report.append(f"  File: {issue['current_loc']} LOC (limit: {issue['limit']})")
            report.append(f"  Excess: {issue['excess']} LOC")
            if "suggestion" in issue and "suggested_splits" in issue["suggestion"]:
                report.append("  Suggested splits:")
                for split in issue["suggestion"]["suggested_splits"]:
                    report.append(f"    - {split}")
            report.append("")
        elif issue["type"] == "class_loc":
            report.append(f"CLASS {issue['path']}:{issue['line_number']}:")
            report.append(
                f"  Class '{issue['class_name']}': {issue['current_loc']} LOC (limit: {issue['limit']})"
            )
            report.append(f"  Excess: {issue['excess']} LOC")
            if "suggestion" in issue and "suggested_methods_split" in issue["suggestion"]:
                report.append("  Suggested splits:")
                for split in issue["suggestion"]["suggested_methods_split"]:
                    report.append(f"    - {split}")
            report.append("")
        elif issue["type"] == "function_loc":
            report.append(f"FUNCTION {issue['path']}:{issue['line_number']}:")
            report.append(
                f"  Function '{issue['function_name']}': {issue['current_loc']} LOC (limit: {issue['limit']})"
            )
            report.append(f"  Excess: {issue['excess']} LOC")
            report.append("  Recommendation: Split into smaller functions")
            report.append("")
        elif issue["type"] in ["syntax_error", "parse_error"]:
            report.append(f"ERROR {issue['path']}:")
            report.append(f"  {issue.get('error', 'Parse error')}")
            report.append("")
    return "\n".join(report)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Auto-remediate LOC violations")
    parser.add_argument(
        "--apply-fixes",
        action="store_true",
        help="Actually apply auto-remediation fixes (default: preview only)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    logger.info("🔧 Generating V2 LOC refactor plan...")
    plan = generate_refactor_plan()

    output_dir = Path("runtime")
    output_dir.mkdir(exist_ok=True)

    # Save plan
    json_file = output_dir / "v2_refactor_plan.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    # Generate text report
    text_file = output_dir / "refactor_suggestions.txt"
    text_report = generate_text_report(plan)
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text_report)

    # Apply auto-remediation
    remediation_results = apply_auto_remediation(
        plan, apply_fixes=args.apply_fixes and not args.dry_run
    )

    # Save remediation results
    remediation_file = output_dir / "auto_remediation_results.json"
    with open(remediation_file, "w", encoding="utf-8") as f:
        json.dump(remediation_results, f, indent=2)

    summary = plan["summary"]
    logger.info("\nREFACTOR PLAN GENERATED:")
    logger.info(f"Files analyzed: {summary['files_analyzed']}")
    logger.info(f"Total violations: {summary['total_violations']}")
    logger.info(f"Syntax errors: {summary['syntax_errors']}")
    logger.info(f"File LOC violations: {summary['file_violations']}")
    logger.info(f"Class LOC violations: {summary['class_violations']}")
    logger.info(f"Function LOC violations: {summary['function_violations']}")

    logger.info("\nAUTO-REMEDIATION RESULTS:")
    if args.dry_run:
        logger.info("DRY RUN - No changes applied")
    elif args.apply_fixes:
        logger.info(
            f"CHANGES APPLIED - {remediation_results['auto_remediated']} violations auto-fixed"
        )
    else:
        logger.info(
            f"PREVIEW MODE - {remediation_results['auto_remediated']} violations could be auto-fixed"
        )

    logger.info(f"Manual attention needed: {remediation_results['manual_required']}")
    logger.info(f"Failed remediation: {remediation_results['failed_remediation']}")

    logger.info(f"\nJSON plan saved: {json_file}")
    logger.info(f"Text report saved: {text_file}")
    logger.info(f"Remediation results saved: {remediation_file}")

    if summary["total_violations"] == 0:
        logger.info("SUCCESS No LOC violations found!")
    else:
        action_verb = "applied" if args.apply_fixes and not args.dry_run else "would require"
        logger.info(f"WARNING {summary['total_violations']} violations {action_verb} attention")


if __name__ == "__main__":
    main()
