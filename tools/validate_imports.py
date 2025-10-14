#!/usr/bin/env python3
"""
Import Validator Tool
=====================

Automatically tests all public API imports from a module to catch import
errors before they reach production.

Created by: Agent-7 (Session Cleanup - Tool You Wished You Had)
Date: 2025-10-11
"""

import argparse
import importlib
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def validate_module_imports(module_path: str) -> tuple[bool, list[str]]:
    """Validate all public API imports from a module.

    Args:
        module_path: Python module path (e.g., "src.integrations.jarvis")

    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []

    try:
        # Import the module
        module = importlib.import_module(module_path)

        # Get __all__ if it exists
        if hasattr(module, "__all__"):
            exports = module.__all__
            print(f"✓ Module {module_path} loaded successfully")
            print(f"  Exports: {', '.join(exports)}")

            # Try to access each export
            for export in exports:
                try:
                    getattr(module, export)
                    print(f"  ✓ {export} accessible")
                except AttributeError as e:
                    error_msg = f"  ✗ {export} not accessible: {e}"
                    print(error_msg)
                    errors.append(error_msg)
        else:
            print(f"⚠ Module {module_path} has no __all__ (not a public API)")

    except ImportError as e:
        error_msg = f"✗ Failed to import {module_path}: {e}"
        print(error_msg)
        errors.append(error_msg)
    except Exception as e:
        error_msg = f"✗ Unexpected error importing {module_path}: {e}"
        print(error_msg)
        errors.append(error_msg)

    return (len(errors) == 0, errors)


def validate_directory(directory: str) -> tuple[bool, int, int]:
    """Validate all public APIs in a directory.

    Args:
        directory: Directory path (e.g., "src/integrations")

    Returns:
        Tuple of (all_success: bool, total: int, failed: int)
    """
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"✗ Directory not found: {directory}")
        return (False, 0, 0)

    # Find all __init__.py files with __all__
    init_files = list(directory_path.rglob("__init__.py"))

    total = 0
    failed = 0

    print(f"\n{'='*70}")
    print(f"Validating imports in: {directory}")
    print(f"{'='*70}\n")

    for init_file in init_files:
        # Convert path to module path
        relative = init_file.relative_to(Path.cwd())
        module_parts = list(relative.parts[:-1])  # Remove __init__.py
        module_path = ".".join(module_parts)

        print(f"\nTesting: {module_path}")
        print("-" * 70)

        success, errors = validate_module_imports(module_path)
        total += 1

        if not success:
            failed += 1
            print(f"✗ FAILED: {module_path}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"✓ PASSED: {module_path}")

    return (failed == 0, total, failed)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate public API imports to catch errors early",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single module
  python tools/validate_imports.py --module src.integrations.jarvis
  
  # Validate all modules in directory
  python tools/validate_imports.py --directory src/integrations
  
  # Validate multiple modules
  python tools/validate_imports.py --module src.integrations.jarvis --module src.integrations.osrs
""",
    )

    parser.add_argument(
        "--module", action="append", help="Module path to validate (e.g., src.integrations.jarvis)"
    )

    parser.add_argument(
        "--directory", help="Directory to scan for modules (e.g., src/integrations)"
    )

    args = parser.parse_args()

    if not args.module and not args.directory:
        parser.print_help()
        return 1

    all_success = True

    # Validate individual modules
    if args.module:
        for module_path in args.module:
            print(f"\n{'='*70}")
            print(f"Validating: {module_path}")
            print(f"{'='*70}\n")

            success, errors = validate_module_imports(module_path)
            if not success:
                all_success = False

    # Validate directory
    if args.directory:
        success, total, failed = validate_directory(args.directory)
        if not success:
            all_success = False

        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"Total modules: {total}")
        print(f"Passed: {total - failed}")
        print(f"Failed: {failed}")

        if all_success:
            print("\n✅ All imports validated successfully!")
        else:
            print(f"\n❌ {failed} module(s) failed validation")

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
