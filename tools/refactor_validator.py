#!/usr/bin/env python3
"""
Refactor Validator
==================

Validates that refactored modules maintain functionality.
Tests imports, backwards compatibility, and basic functionality.

Created from: Agent-2 session learning (manually tested imports after each refactor)
Author: Agent-2 (Architecture & Design Specialist)
Created: 2025-10-13
"""

import importlib
from typing import Any


def validate_imports(module_path: str, expected_exports: list[str]) -> dict[str, Any]:
    """Validate that a module exports expected items."""
    results = {"success": True, "module": module_path, "found": [], "missing": [], "errors": []}

    try:
        # Add src to path if needed
        import sys
        from pathlib import Path

        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Convert file path to module path
        if module_path.endswith(".py"):
            module_path = module_path[:-3]
        module_path = module_path.replace("/", ".").replace("\\", ".")

        # Import module
        module = importlib.import_module(module_path)

        # Check exports
        for item in expected_exports:
            if hasattr(module, item):
                results["found"].append(item)
            else:
                results["missing"].append(item)
                results["success"] = False

    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))

    return results


def validate_backwards_compatibility(
    old_module: str, new_module: str, items: list[str]
) -> dict[str, Any]:
    """Validate that new module maintains same exports as old."""
    results = {
        "success": True,
        "old_module": old_module,
        "new_module": new_module,
        "compatible": [],
        "incompatible": [],
        "errors": [],
    }

    try:
        # Import both modules
        old = importlib.import_module(old_module)
        new = importlib.import_module(new_module)

        # Check each item
        for item in items:
            old_has = hasattr(old, item)
            new_has = hasattr(new, item)

            if old_has and new_has:
                results["compatible"].append(item)
            elif not old_has and not new_has:
                results["compatible"].append(f"{item} (both missing)")
            else:
                results["incompatible"].append(f"{item} (old:{old_has}, new:{new_has})")
                results["success"] = False

    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))

    return results


def run_basic_functionality_test(module_path: str, test_code: str) -> dict[str, Any]:
    """Run basic functionality test."""
    results = {"success": True, "output": "", "errors": []}

    try:
        # Execute test code
        exec(test_code, {"__name__": "__main__"})
        results["output"] = "Test executed successfully"
    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))

    return results


def main():
    """Main entry point."""
    print("🔍 REFACTOR VALIDATOR\n")

    # Example: Validate config_ssot refactor
    print("Testing config_ssot.py refactor...")

    expected_exports = [
        "ConfigEnvironment",
        "ConfigSource",
        "ReportFormat",
        "TimeoutConfig",
        "AgentConfig",
        "BrowserConfig",
        "get_config",
        "get_unified_config",
    ]

    results = validate_imports("src.core.config_ssot", expected_exports)

    if results["success"]:
        print(f"✅ All {len(results['found'])} exports found!")
    else:
        print("❌ Validation failed!")
        if results["missing"]:
            print(f"   Missing: {', '.join(results['missing'])}")
        if results["errors"]:
            print(f"   Errors: {', '.join(results['errors'])}")

    # Test basic functionality
    print("\nTesting basic functionality...")
    test_code = """
from src.core.config_ssot import get_config, ConfigEnvironment
config = get_config('agent_count')
print(f"   Agent count: {config}")
"""

    func_results = run_basic_functionality_test("src.core.config_ssot", test_code)

    if func_results["success"]:
        print("✅ Basic functionality working!")
    else:
        print(f"❌ Functionality test failed: {func_results['errors']}")


if __name__ == "__main__":
    main()
