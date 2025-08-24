#!/usr/bin/env python3
"""
Unified Test Runner Entry Point - Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - Consolidated Test System

This script replaces the previous 3 test runners:
- run_tests.py (485 lines) - DEPRECATED
- run_tdd_tests.py (456 lines) - DEPRECATED
- run_all_tests.py (311 lines) - DEPRECATED

Usage:
    python test_runner.py                    # Run all tests
    python test_runner.py --mode critical    # Run critical tests only
    python test_runner.py --mode smoke       # Run smoke tests
    python test_runner.py --mode unit        # Run unit tests
    python test_runner.py --mode files test_file.py  # Run specific files
"""

import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add tests directory to path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

# Import the unified runner
from tests.runners.unified_runner import main

if __name__ == "__main__":
    main()
