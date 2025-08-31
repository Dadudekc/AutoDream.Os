#!/usr/bin/env python3
"""Single Source of Truth compliance checks.

This script consolidates repository-wide line limit scanning with targeted
module validation. It is the authoritative utility for verifying coding
standards across the project.
"""

import os


def check_file_line_count(file_path: str) -> int | None:
    """Return the line count for ``file_path`` or ``None`` if missing."""
    try:
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return len(f.readlines())
    except Exception as e:  # pragma: no cover - defensive
        print(f"Error reading {file_path}: {e}")
        return None


def scan_repository(root: str = ".", max_lines: int = 250):
    """Scan ``root`` for Python files and collect line count violations."""
    total = compliant = 0
    violations: list[tuple[str, int]] = []
    for dirpath, dirs, files in os.walk(root):
        if any(skip in dirpath for skip in {"backups", "__pycache__", ".git"}):
            continue
        for name in files:
            if not name.endswith(".py"):
                continue
            total += 1
            path = os.path.join(dirpath, name)
            lines = check_file_line_count(path) or 0
            if lines <= max_lines:
                compliant += 1
            else:
                violations.append((path, lines))
    return total, compliant, violations


def report_repository_status(total: int, compliant: int, violations: list[tuple[str, int]]):
    """Print a summary of repository-wide compliance."""
    percent = (compliant / total * 100) if total else 0
    print("🔍 V2 COMPLIANCE STATUS CHECK")
    print("=" * 50)
    print(f"📊 Total Python Files: {total}")
    print(f"✅ Compliant Files: {compliant}")
    print(f"🚨 Violation Files: {len(violations)}")
    print(f"🎯 Overall Compliance: {percent:.1f}%")
    if violations:
        print("\n🚨 Violations Found:")
        for path, lines in violations[:10]:
            print(f"  - {path} ({lines} lines)")
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more")
    else:
        print("\n🎉 100% V2 COMPLIANCE ACHIEVED!")


def check_specific_files(refactored_files: list[str], max_lines: int = 500):
    """Verify targeted files stay under ``max_lines``."""
    print("\n🔍 Refactored Files")
    print("=" * 30)
    for file_path in refactored_files:
        current = check_file_line_count(file_path)
        if current is None:
            print(f"   ❌ {file_path} - NOT FOUND")
            continue
        status = "✅" if current <= max_lines else "❌"
        note = "COMPLIANT" if current <= max_lines else "NON-COMPLIANT"
        print(f"   {status} {file_path} - {current} lines ({note})")


def check_required_modules(extracted_modules: list[str]):
    """Ensure expected modules exist and report their line counts."""
    print("\n🔧 Extracted Modules")
    print("=" * 30)
    for module_path in extracted_modules:
        if os.path.exists(module_path):
            lines = check_file_line_count(module_path)
            print(f"   ✅ {module_path} - {lines} lines")
        else:
            print(f"   ❌ {module_path} - NOT FOUND")


def check_init_files(init_files: list[str]):
    """Confirm required ``__init__`` files are present."""
    print("\n📦 Package Init Files")
    print("=" * 25)
    for init_file in init_files:
        if os.path.exists(init_file):
            print(f"   ✅ {init_file}")
        else:
            print(f"   ❌ {init_file} - MISSING")


def main():
    total, compliant, violations = scan_repository()
    report_repository_status(total, compliant, violations)

    check_specific_files(
        [
            "src/core/v2_comprehensive_messaging_system.py",
            "src/core/autonomous_development.py",
        ]
    )

    check_required_modules(
        [
            "src/core/messaging/router.py",
            "src/core/messaging/validator.py",
            "src/core/messaging/formatter.py",
            "src/core/messaging/storage.py",
            "src/autonomous_development/workflow/engine.py",
            "src/autonomous_development/tasks/manager.py",
            "src/autonomous_development/code/generator.py",
            "src/autonomous_development/testing/orchestrator.py",
        ]
    )

    check_init_files(
        [
            "src/core/messaging/__init__.py",
            "src/autonomous_development/__init__.py",
        ]
    )

    print("\n🎯 COMPLIANCE CHECK COMPLETE")


if __name__ == "__main__":
    main()
