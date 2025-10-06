#!/usr/bin/env python3
"""
Import Smoke Test for Messaging System
=====================================

Tests that all messaging imports work correctly after BC shim restoration.
Validates both shim paths and canonical paths.

Usage:
    python tools/import_smoke_messaging.py

Returns:
    0 - All imports successful
    2 - Import failures detected
"""

import importlib
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Modules to test
MODULES_TO_TEST = [
    # BC Shim paths (should work via shims)
    "src.services.consolidated_messaging_service",
    
    # Canonical paths (should work directly)
    "src.services.messaging_service",
    "src.services.messaging_service_core", 
    "src.services.messaging_service_main",
    "src.services.messaging_service_utils",
    
    # Discord Commander dependencies (critical path)
    "src.services.discord_commander.bot",
    "src.services.discord_commander.commands",
]


def test_import(module_name: str) -> tuple[str, bool, str]:
    """
    Test importing a module.
    
    Returns:
        (module_name, success, error_message)
    """
    try:
        importlib.import_module(module_name)
        return (module_name, True, "")
    except Exception as e:
        return (module_name, False, str(e))


def main() -> int:
    """Run import smoke tests."""
    print("🔍 Messaging Import Smoke Test")
    print("=" * 40)
    
    failed_imports = []
    successful_imports = []
    
    for module_name in MODULES_TO_TEST:
        print(f"Testing: {module_name}...", end=" ")
        
        name, success, error = test_import(module_name)
        
        if success:
            print("✅")
            successful_imports.append(name)
        else:
            print("❌")
            failed_imports.append((name, error))
    
    print("\n" + "=" * 40)
    print("📊 Results:")
    print(f"  ✅ Successful: {len(successful_imports)}")
    print(f"  ❌ Failed: {len(failed_imports)}")
    
    if failed_imports:
        print("\n❌ Import failures:")
        for module, error in failed_imports:
            print(f"  - {module}")
            print(f"    Error: {error}")
        
        print("\n🔧 Troubleshooting:")
        print("  1. Check that all messaging service files exist")
        print("  2. Verify BC shim is properly created")
        print("  3. Check for circular import issues")
        print("  4. Ensure all dependencies are installed")
        
        return 2
    else:
        print("\n✅ All imports successful!")
        print("🎯 Discord Commander should now be able to start")
        return 0


if __name__ == "__main__":
    sys.exit(main())

