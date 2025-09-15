#!/usr/bin/env python3
"""
Test Coverage Improvement Tool - V2 Compliance Wrapper
=====================================================

V2 compliant wrapper for the modular coverage improvement system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/test_coverage_improvement.py --analyze --target messaging
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from coverage.coverage_improver import main

if __name__ == "__main__":
    main()
