#!/usr/bin/env python3
"""
V2 Compliance Analysis CLI Tool - Wrapper
=========================================

Simple wrapper for the modular V2 compliance analysis tool.

This file maintains backward compatibility while using the new modular structure.
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Import and run the main CLI
from analysis.cli import main

if __name__ == "__main__":
    sys.exit(main())
