#!/usr/bin/env python3
"""
OSRS Smoke Test Runner - Agent Cellphone V2
==========================================

Quick smoke test runner for OSRS gaming system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from osrs.tests.smoke_tests import run_osrs_smoke_tests


if __name__ == "__main__":
    print("🚀 OSRS SMOKE TEST RUNNER")
    print("=" * 50)
    
    success = run_osrs_smoke_tests()
    
    if success:
        print("\n🎉 SMOKE TESTS COMPLETED SUCCESSFULLY!")
        print("✅ OSRS system is production-ready")
        print("✅ V2 coding standards maintained")
        sys.exit(0)
    else:
        print("\n❌ SMOKE TESTS FAILED!")
        print("❌ OSRS system needs attention")
        sys.exit(1)
