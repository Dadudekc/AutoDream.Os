#!/usr/bin/env python3
"""
Project Scanner - Wrapper
========================

Simple wrapper for the modular project scanner tool.

This file maintains backward compatibility while using the new modular structure.
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Import and run the main scanner
from projectscanner.core import ProjectScanner


def main():
    """Main entry point for backward compatibility."""
    scanner = ProjectScanner(project_root=".")
    result = scanner.scan_project()
    return result


if __name__ == "__main__":
    result = main()
    print(f"Scan result: {result}")
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
