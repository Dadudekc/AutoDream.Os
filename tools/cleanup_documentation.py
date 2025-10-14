#!/usr/bin/env python3
"""
Documentation Cleanup Tool - WRAPPER (V2 COMPLIANT)
===================================================

⚠️ DEPRECATED WRAPPER: This file delegates to the refactored implementation.

Original: 513 lines (V2 violation)
Refactored into 3 V2-compliant modules:
  - cleanup_documentation_reference_scanner.py (124 lines)
  - cleanup_documentation_deduplicator.py (117 lines)
  - cleanup_documentation_refactored.py (288 lines)

This wrapper maintained for backward compatibility.

Refactored: Agent-1 (2025-10-11), Agent-3 (2025-10-14)
License: MIT
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))


def main():
    """Delegate to refactored implementation."""
    try:
        from cleanup_documentation_refactored import main as refactored_main
        
        print("⚠️  Using refactored implementation (cleanup_documentation_refactored.py)")
        print("=" * 70)
        refactored_main()
    except ImportError as e:
        print(f"❌ Error: Refactored implementation not found: {e}")
        print("Please ensure cleanup_documentation_refactored.py is available")
        sys.exit(1)


if __name__ == "__main__":
    main()
