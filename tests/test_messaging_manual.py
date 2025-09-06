#!/usr/bin/env python3
"""
Manual Smoke Tests for Messaging System - Agent Cellphone V2
===========================================================

Simple manual tests to verify messaging features work.
Run this script directly to test messaging functionality.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_test(name, command, expected_success=True):
    """Run a test command and report results."""
    print(f"\n🧪 Testing: {name}")
    print(f"Command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if expected_success:
            if result.returncode == 0:
                print("✅ PASS")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
                return True
            else:
                print("❌ FAIL")
                if result.stderr.strip():
                    print(f"Error: {result.stderr.strip()}")
                return False
        else:
            # For tests that should fail
            if result.returncode != 0:
                print("✅ PASS (Expected failure)")
                return True
            else:
                print("❌ FAIL (Expected failure but got success)")
                return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run manual smoke tests."""
    print("🚀 MESSAGING SYSTEM SMOKE TESTS")
    print("=" * 50)

    # Set PYTHONPATH
    os.environ["PYTHONPATH"] = "src"

    # Test commands
    tests = [
        ("CLI Help", ["python", "-m", "src.services.messaging_cli", "--help"]),
        (
            "Agent Listing",
            ["python", "-m", "src.services.messaging_cli", "--list-agents"],
        ),
        (
            "Coordinates Display",
            ["python", "-m", "src.services.messaging_cli", "--coordinates"],
        ),
        (
            "Hard Onboarding Dry Run",
            [
                "python",
                "-m",
                "src.services.messaging_cli",
                "--hard-onboarding",
                "--dry-run",
                "--yes",
            ],
        ),
        (
            "Hard Onboarding Subset",
            [
                "python",
                "-m",
                "src.services.messaging_cli",
                "--hard-onboarding",
                "--agents",
                "Agent-1,Agent-2",
                "--dry-run",
                "--yes",
            ],
        ),
    ]

    passed = 0
    total = len(tests)

    for name, command in tests:
        if run_test(name, command):
            passed += 1

    print(f"\n📊 RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL SMOKE TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
