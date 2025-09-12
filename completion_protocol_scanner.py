#!/usr/bin/env python3
"""
Completion Protocol Scanner - V2 Compliant Module
================================================

Scans repository for missing AGENT_COMPLETION_PROTOCOL.md markers.
Ensures all CLI entrypoints have proper completion indicators.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import ast
import os
from typing import Any


def scan_python_file(file_path: str) -> dict[str, Any]:
    """Scan a Python file for completion protocol compliance."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        # Check for main block
        has_main = False
        has_completion_marker = False
        completion_marker_line = None

        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                if (isinstance(node.test.left, ast.NameConstant) and
                    node.test.left.value is None and
                    isinstance(node.test.ops[0], ast.Eq) and
                    isinstance(node.test.comparators[0], ast.NameConstant) and
                    node.test.comparators[0].value is None):
                    has_main = True

                    # Check if completion marker exists in main block
                    for stmt in node.body:
                        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                            if (isinstance(stmt.value.func, ast.Attribute) and
                                isinstance(stmt.value.func.value, ast.Name) and
                                stmt.value.func.value.id == 'print'):
                                # Check if it's the completion marker
                                if (len(stmt.value.args) == 1 and
                                    isinstance(stmt.value.args[0], ast.Constant) and
                                    "⚡ WE. ARE. SWARM. ⚡️🔥" in str(stmt.value.args[0].value)):
                                    has_completion_marker = True
                                    completion_marker_line = stmt.lineno

        # Also check for completion marker anywhere in the file
        if not has_completion_marker:
            if "⚡ WE. ARE. SWARM. ⚡️🔥" in content:
                has_completion_marker = True
                # Find line number
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if "⚡ WE. ARE. SWARM. ⚡️🔥" in line:
                        completion_marker_line = i
                        break

        return {
            "file_path": file_path,
            "has_main": has_main,
            "has_completion_marker": has_completion_marker,
            "completion_marker_line": completion_marker_line,
            "needs_patch": has_main and not has_completion_marker,
            "line_count": len(content.splitlines()),
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "has_main": False,
            "has_completion_marker": False,
            "completion_marker_line": None,
            "needs_patch": False,
            "line_count": 0,
            "file_size": 0,
            "error": str(e)
        }


def scan_directory(directory: str, extensions: list[str] = [".py"]) -> list[dict[str, Any]]:
    """Scan directory for Python files that need completion protocol patches."""
    results = []

    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'node_modules']]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                result = scan_python_file(file_path)
                results.append(result)

    return results


def generate_patch_template(file_path: str) -> str:
    """Generate patch template for a file."""
    return f'''# Patch for {file_path}
# Add this to the end of the main block:

if __name__ == "__main__":
    import sys
    exit_code = main()
    print()  
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)
'''


def main():
    """Main scanning function."""
    print("🔍 Scanning repository for completion protocol compliance...")

    # Scan key directories
    directories_to_scan = [
        "src/services",
        "src/core/managers",
        "scripts",
        "tools",
        ".",
    ]

    all_results = []
    for directory in directories_to_scan:
        if os.path.exists(directory):
            print(f"📁 Scanning: {directory}")
            results = scan_directory(directory)
            all_results.extend(results)

    # Filter results
    files_needing_patches = [r for r in all_results if r.get("needs_patch", False)]
    files_with_markers = [r for r in all_results if r.get("has_completion_marker", False)]
    files_with_main = [r for r in all_results if r.get("has_main", False)]

    # Generate report
    print("\n📊 SCAN RESULTS:")
    print(f"   Total files scanned: {len(all_results)}")
    print(f"   Files with main blocks: {len(files_with_main)}")
    print(f"   Files with completion markers: {len(files_with_markers)}")
    print(f"   Files needing patches: {len(files_needing_patches)}")

    if files_needing_patches:
        print("\n🔧 FILES NEEDING PATCHES:")
        for result in files_needing_patches:
            print(f"   ❌ {result['file_path']} (Line {result.get('completion_marker_line', 'N/A')})")

        print("\n📝 PATCH TEMPLATES:")
        for result in files_needing_patches:
            print(f"\n{generate_patch_template(result['file_path'])}")
    else:
        print("\n✅ ALL FILES COMPLIANT - No patches needed!")

    # Save detailed report
    report = {
        "scan_summary": {
            "total_files": len(all_results),
            "files_with_main": len(files_with_main),
            "files_with_markers": len(files_with_markers),
            "files_needing_patches": len(files_needing_patches)
        },
        "files_needing_patches": files_needing_patches,
        "all_results": all_results
    }

    with open("completion_protocol_scan_report.json", "w", encoding="utf-8") as f:
        import json
        json.dump(report, f, indent=2)

    print("\n📁 Detailed report saved: completion_protocol_scan_report.json")

    return len(files_needing_patches)


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
