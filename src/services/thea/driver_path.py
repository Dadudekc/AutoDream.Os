#!/usr/bin/env python3
"""
Thea Driver Path Helper - V2 Compliant
=======================================

Provides deterministic ChromeDriver path resolution for Thea autonomous system.
Ensures consistent driver location across different environments.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
V2 Compliance: ≤50 lines, single responsibility, type hints
"""

import platform
from pathlib import Path


def os_name() -> str:
    """Detect operating system name."""
    system = platform.system().lower()
    return "windows" if system.startswith("win") else "unix"


def chromedriver_path() -> str:
    """
    Return absolute path to ChromeDriver executable.
    
    Returns:
        str: Absolute path to tools/bin/chromedriver[.exe]
    """
    root = Path(__file__).resolve().parents[3]  # project root
    driver_name = "chromedriver.exe" if os_name() == "windows" else "chromedriver"
    driver_path = root / "tools" / "bin" / driver_name
    return str(driver_path)


if __name__ == "__main__":
    print(f"ChromeDriver path: {chromedriver_path()}")
    print(f"OS: {os_name()}")
