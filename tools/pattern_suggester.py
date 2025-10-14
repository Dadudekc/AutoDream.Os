#!/usr/bin/env python3
"""
Pattern Suggester - Consolidation Pattern Recommendations
==========================================================

Suggests which architectural pattern to use for refactoring/consolidation.
Based on CONSOLIDATION_ARCHITECTURE_PATTERNS.md.

Author: Agent-2 - Architecture & Design Specialist
Date: 2025-10-12
License: MIT
"""

import argparse
import ast
import sys
from pathlib import Path


def analyze_file_structure(file_path: Path) -> dict:
    """Analyze file to determine appropriate pattern."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()

        # Parse AST
        tree = ast.parse(content)

        # Count components
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
            and not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree))
        ]

        return {
            "line_count": len(lines),
            "class_count": len(classes),
            "function_count": len(functions),
            "has_main": "if __name__" in content,
            "is_cli": "argparse" in content or "sys.argv" in content,
        }
    except Exception as e:
        return {"error": str(e)}


def suggest_pattern(file_path: str) -> dict:
    """
    Suggest consolidation pattern for a file.

    Args:
        file_path: Path to file to analyze

    Returns:
        Pattern suggestion with rationale
    """
    path = Path(file_path)

    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    analysis = analyze_file_structure(path)

    if "error" in analysis:
        return analysis

    lines = analysis["line_count"]

    # Pattern selection logic
    if lines > 600:
        severity = "CRITICAL"
    elif lines > 400:
        severity = "MAJOR"
    else:
        return {"pattern": "NO_REFACTOR_NEEDED", "reason": "File is V2 compliant", "lines": lines}

    # Determine pattern
    if analysis["is_cli"] and analysis["has_main"]:
        pattern = "FACADE"
        rationale = "CLI file with main() - use Facade pattern: thin CLI layer + core modules"
        example = "projectscanner.py: 1154→68 facade + 5 modules"

    elif analysis["class_count"] == 0 and analysis["function_count"] > 10:
        pattern = "SSOT_CONSOLIDATION"
        rationale = "Multiple utility functions - consolidate into SSOT with dataclasses"
        example = "config files: 12→1 SSOT with dataclass-based configs"

    elif analysis["class_count"] == 1 and lines > 600:
        if "login" in file_path.lower() or "auth" in file_path.lower():
            pattern = "STUB_REPLACEMENT"
            rationale = "Large authentication class - consider stub replacement if low usage"
            example = "thea_login_handler.py: 807→22 stub"
        else:
            pattern = "FACADE"
            rationale = "Large single class - split into specialized modules with facade"
            example = "Split class methods into separate modules by responsibility"

    elif analysis["class_count"] > 3:
        pattern = "MODULE_SPLITTING"
        rationale = "Multiple classes - split into separate module files"
        example = "One class per file pattern"

    else:
        pattern = "FACADE"
        rationale = "General refactoring - use Facade + Module Splitting"
        example = "Split by responsibility, create thin facade"

    return {
        "file": file_path,
        "lines": lines,
        "severity": severity,
        "pattern": pattern,
        "rationale": rationale,
        "example": example,
        "analysis": analysis,
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Pattern Suggester - Consolidation Pattern Recommendations"
    )
    parser.add_argument("files", nargs="+", help="Files to analyze for pattern suggestions")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    suggestions = []
    for file in args.files:
        suggestion = suggest_pattern(file)
        suggestions.append(suggestion)

        if not args.json:
            if "error" in suggestion:
                print(f"❌ {file}: {suggestion['error']}")
            elif suggestion["pattern"] == "NO_REFACTOR_NEEDED":
                print(f"✅ {file}: {suggestion['reason']} ({suggestion['lines']} lines)")
            else:
                print(f"\n🏗️ {file} ({suggestion['lines']} lines - {suggestion['severity']})")
                print(f"   Pattern: {suggestion['pattern']}")
                print(f"   Rationale: {suggestion['rationale']}")
                print(f"   Example: {suggestion['example']}")

    if args.json:
        print(json.dumps(suggestions, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
