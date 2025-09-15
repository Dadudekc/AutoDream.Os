#!/usr/bin/env python3
"""
Auto-Remediate LOC Violations - V2 Compliance Wrapper
===================================================

V2 compliant wrapper for the modular LOC remediation system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/auto_remediate_loc.py --target src
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from loc_remediation.loc_analyzer import main

if __name__ == "__main__":
    main()
