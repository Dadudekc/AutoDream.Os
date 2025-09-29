#!/usr/bin/env python3
"""
Discord Bot Test Runner
======================

Simple script to run Discord bot tests with proper configuration.
"""

import os
import subprocess
import sys


def run_discord_tests():
    """Run Discord bot tests with proper configuration."""
    print("🧪 Running Discord Bot Tests...")
    print("=" * 50)

    # Set up environment
    os.environ["DISCORD_BOT_TOKEN"] = "test_token_12345"
    os.environ["APP_ENV"] = "test"

    # Run pytest with specific options
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_discord_bot.py",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--color=yes",
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)

        print("\n" + "=" * 50)
        if result.returncode == 0:
            print("✅ All Discord bot tests passed!")
        else:
            print("❌ Some Discord bot tests failed!")
            print(f"Exit code: {result.returncode}")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_specific_test(test_name):
    """Run a specific test."""
    print(f"🧪 Running specific test: {test_name}")
    print("=" * 50)

    # Set up environment
    os.environ["DISCORD_BOT_TOKEN"] = "test_token_12345"
    os.environ["APP_ENV"] = "test"

    # Run specific test
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        f"tests/test_discord_bot.py::{test_name}",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--color=yes",
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        success = run_discord_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
