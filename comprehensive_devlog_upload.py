#!/usr/bin/env python3
"""
Comprehensive Devlog Upload Script - V2 Compliant (Refactored)
==============================================================

Refactored comprehensive devlog upload importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

from comprehensive_devlog_core import ComprehensiveDevlogCore


def main():
    """Main entry point for comprehensive devlog upload."""
    print("🚀 Starting Comprehensive Devlog Upload")
    
    # Initialize devlog core
    devlog_core = ComprehensiveDevlogCore()
    
    # Run comprehensive export
    success = devlog_core.run_comprehensive_export()
    
    if success:
        print("\n✅ Comprehensive devlog upload completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Comprehensive devlog upload failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()